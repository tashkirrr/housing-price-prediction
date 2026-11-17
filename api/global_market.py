"""Global market data endpoints backed by Numbeo and REST Countries."""

import os
import re
import time
from typing import Any, Literal

import httpx
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/global", tags=["Global housing markets"])

NUMBEO_BASE_URL = "https://www.numbeo.com"
REST_COUNTRIES_URL = "https://restcountries.com/v3.1/all"
REQUEST_TIMEOUT_SECONDS = 12.0
COUNTRIES_CACHE_TTL_SECONDS = 24 * 60 * 60
CITIES_CACHE_TTL_SECONDS = 6 * 60 * 60
PRICES_CACHE_TTL_SECONDS = 60 * 60
SQUARE_FEET_PER_SQUARE_METER = 10.7639

_cache: dict[str, tuple[float, Any]] = {}


class GlobalEstimateRequest(BaseModel):
    city_id: int = Field(gt=0)
    area_sqm: float = Field(gt=0, le=10000)
    position: Literal["center", "outside"] = "center"
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")


def _numbeo_api_key() -> str:
    key = os.getenv("NUMBEO_API_KEY", "").strip()
    if not key:
        raise HTTPException(
            status_code=503,
            detail="Live market estimates are not configured. Set NUMBEO_API_KEY on the API service.",
        )
    return key


def _cached(key: str, ttl_seconds: int) -> Any | None:
    cached_value = _cache.get(key)
    if cached_value is None:
        return None
    expires_at, value = cached_value
    if expires_at <= time.monotonic():
        _cache.pop(key, None)
        return None
    return value


def _store_cache(key: str, value: Any, ttl_seconds: int) -> None:
    _cache[key] = (time.monotonic() + ttl_seconds, value)


async def _request_json(
    url: str,
    *,
    params: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
) -> Any:
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="The upstream data provider could not complete the request.",
        ) from exc


async def _get_countries() -> list[dict[str, Any]]:
    cache_key = "rest-countries"
    cached_value = _cached(cache_key, COUNTRIES_CACHE_TTL_SECONDS)
    if cached_value is not None:
        return cached_value

    payload = await _request_json(
        REST_COUNTRIES_URL,
        params={"fields": "name,cca2,region,currencies"},
    )
    if not isinstance(payload, list):
        raise HTTPException(status_code=502, detail="The country catalog returned an invalid response.")

    countries = []
    for entry in payload:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        code = entry.get("cca2")
        common_name = name.get("common") if isinstance(name, dict) else None
        if not isinstance(common_name, str) or not isinstance(code, str):
            continue
        currencies = entry.get("currencies")
        currency = next(iter(currencies), None) if isinstance(currencies, dict) else None
        countries.append({
            "code": code,
            "name": common_name,
            "region": entry.get("region") or "Other",
            "currency": currency,
        })

    countries.sort(key=lambda country: country["name"].casefold())
    _store_cache(cache_key, countries, COUNTRIES_CACHE_TTL_SECONDS)
    return countries


async def _get_cities() -> list[dict[str, Any]]:
    cache_key = "numbeo-cities"
    cached_value = _cached(cache_key, CITIES_CACHE_TTL_SECONDS)
    if cached_value is not None:
        return cached_value

    payload = await _request_json(
        f"{NUMBEO_BASE_URL}/api/cities",
        headers={"X-Api-Key": _numbeo_api_key()},
    )
    entries = payload.get("cities") if isinstance(payload, dict) else None
    if not isinstance(entries, list):
        raise HTTPException(status_code=502, detail="Numbeo returned an invalid city catalog.")

    cities = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        city_id = entry.get("city_id")
        city_name = entry.get("city")
        country_name = entry.get("country")
        if not isinstance(city_id, int) or not isinstance(city_name, str) or not isinstance(country_name, str):
            continue
        cities.append({
            "city_id": city_id,
            "city": city_name,
            "country": country_name,
            "latitude": entry.get("latitude"),
            "longitude": entry.get("longitude"),
        })

    _store_cache(cache_key, cities, CITIES_CACHE_TTL_SECONDS)
    return cities


@router.get("/countries")
async def list_countries() -> dict[str, Any]:
    """Return a worldwide country catalog; this does not imply housing-price coverage."""
    countries = await _get_countries()
    return {"countries": countries, "count": len(countries)}


@router.get("/cities")
async def list_cities(
    q: str = Query(default="", max_length=100),
    country: str = Query(default="", max_length=100),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=100),
) -> dict[str, Any]:
    """Search Numbeo-supported cities and return a bounded page of results."""
    cities = await _get_cities()
    search_term = q.casefold().strip()
    country_term = country.casefold().strip()
    matches = [
        city for city in cities
        if (not country_term or country_term in city["country"].casefold())
        and (
            not search_term
            or search_term in city["city"].casefold()
            or search_term in city["country"].casefold()
        )
    ]
    start = (page - 1) * page_size
    return {
        "cities": matches[start:start + page_size],
        "count": len(matches),
        "page": page,
        "page_size": page_size,
        "pages": (len(matches) + page_size - 1) // page_size,
        "provider": "Numbeo",
    }


def _price_item(prices: list[Any], position: Literal["center", "outside"]) -> dict[str, Any]:
    location = "city centre" if position == "center" else "outside of centre"
    for item in prices:
        if not isinstance(item, dict):
            continue
        name = item.get("item_name")
        if not isinstance(name, str):
            continue
        normalized_name = re.sub(r"\s+", " ", name.casefold())
        if (
            "price per square meter to buy apartment" in normalized_name
            or "price per square feet to buy apartment" in normalized_name
            or "price per square foot to buy apartment" in normalized_name
        ) and location in normalized_name:
            return item
    raise HTTPException(
        status_code=404,
        detail=f"Numbeo has no apartment purchase price for this city and location type ({position}).",
    )


def _number(item: dict[str, Any], key: str) -> float:
    value = item.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        raise HTTPException(status_code=502, detail="Numbeo returned an invalid property price.")
    return float(value)


@router.post("/estimate")
async def estimate_property(request: GlobalEstimateRequest) -> dict[str, Any]:
    """Estimate a market-average apartment value from Numbeo's per-area prices."""
    api_key = _numbeo_api_key()
    cache_key = f"numbeo-prices:{request.city_id}:{request.currency}"
    payload = _cached(cache_key, PRICES_CACHE_TTL_SECONDS)
    if payload is None:
        payload = await _request_json(
            f"{NUMBEO_BASE_URL}/api/city_prices",
            params={
                "city_id": str(request.city_id),
                "currency": request.currency,
                "use_estimated": "false",
            },
            headers={"X-Api-Key": api_key},
        )
        _store_cache(cache_key, payload, PRICES_CACHE_TTL_SECONDS)

    prices = payload.get("prices") if isinstance(payload, dict) else None
    if not isinstance(prices, list):
        raise HTTPException(status_code=502, detail="Numbeo returned an invalid city price response.")
    item = _price_item(prices, request.position)

    item_name = item.get("item_name", "").casefold()
    area = request.area_sqm
    if "square feet" in item_name or "square foot" in item_name:
        area *= SQUARE_FEET_PER_SQUARE_METER

    average_per_area = _number(item, "average_price")
    lowest_per_area = _number(item, "lowest_price")
    highest_per_area = _number(item, "highest_price")
    return {
        "provider": "Numbeo",
        "name": payload.get("name"),
        "city_id": request.city_id,
        "currency": payload.get("currency") or request.currency,
        "position": request.position,
        "area_sqm": request.area_sqm,
        "average_price_per_area": average_per_area,
        "estimated_value": round(average_per_area * area, 2),
        "low_estimate": round(lowest_per_area * area, 2),
        "high_estimate": round(highest_per_area * area, 2),
        "data_points": item.get("data_points"),
        "year_last_update": payload.get("yearLastUpdate"),
        "month_last_update": payload.get("monthLastUpdate"),
        "disclaimer": "Market-average estimate, not an appraisal or property-specific valuation.",
    }
