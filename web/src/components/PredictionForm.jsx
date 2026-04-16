import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Building2, Users, Bed, Home, Wallet, MapPin, Compass } from 'lucide-react';
import { AddressAutocomplete } from './AddressAutocomplete';
import { PriceDisplay } from './PriceDisplay';
import { CensusDataCard } from './CensusDataCard';
import { usePrediction } from '../hooks/usePrediction';

const OCEAN_PROXIMITY_OPTIONS = [
  { value: '<1H OCEAN', label: 'Less than 1 Hour from Ocean', multiplier: 1.16 },
  { value: 'INLAND', label: 'Inland', multiplier: 0.60 },
  { value: 'ISLAND', label: 'Island (Premium)', multiplier: 1.84 },
  { value: 'NEAR BAY', label: 'Near Bay', multiplier: 1.25 },
  { value: 'NEAR OCEAN', label: 'Near Ocean', multiplier: 1.20 },
];

export const PredictionForm = () => {
  const [formData, setFormData] = useState({
    longitude: -122.23,
    latitude: 37.88,
    housing_median_age: 41,
    total_rooms: 880,
    total_bedrooms: 129,
    population: 322,
    households: 126,
    median_income: 8.3,
    ocean_proximity: 'NEAR BAY',
  });

  const { result, isCalculating, calculatePrice } = usePrediction();

  useEffect(() => {
    calculatePrice(formData);
  }, []);

  const handleAddressSelect = (suggestion) => {
    setFormData(prev => ({
      ...prev,
      latitude: suggestion.lat,
      longitude: suggestion.lon,
    }));
    calculatePrice({
      ...formData,
      latitude: suggestion.lat,
      longitude: suggestion.lon,
    });
  };

  const handleInputChange = (field, value) => {
    const newData = { ...formData, [field]: value };
    setFormData(newData);
    calculatePrice(newData);
  };

  const InputField = ({ icon: Icon, label, field, type = 'number', min, max, step = 1, helpText }) => (
    <div className="space-y-2">
      <label className="flex items-center gap-2 text-sm font-medium text-slate-700">
        <Icon className="w-4 h-4 text-ocean-500" />
        {label}
      </label>
      <input
        type={type}
        value={formData[field]}
        onChange={(e) => handleInputChange(field, type === 'number' ? parseFloat(e.target.value) : e.target.value)}
        min={min}
        max={max}
        step={step}
        className="input-field"
      />
      {helpText && <p className="text-xs text-slate-400">{helpText}</p>}
    </div>
  );

  const RangeField = ({ icon: Icon, label, field, min, max, step = 1, formatValue }) => (
    <div className="space-y-2">
      <label className="flex items-center gap-2 text-sm font-medium text-slate-700">
        <Icon className="w-4 h-4 text-ocean-500" />
        {label}
      </label>
      <div className="flex items-center gap-4">
        <input
          type="range"
          value={formData[field]}
          onChange={(e) => handleInputChange(field, parseFloat(e.target.value))}
          min={min}
          max={max}
          step={step}
          className="flex-1 h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-ocean-600"
        />
        <span className="px-3 py-1 bg-ocean-100 text-ocean-700 rounded-lg text-sm font-medium min-w-[80px] text-center">
          {formatValue ? formatValue(formData[field]) : formData[field]}
        </span>
      </div>
    </div>
  );

  return (
    <section id="predictor" className="section-padding py-20">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold font-display gradient-text mb-4">
            Price Predictor
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Enter property details and discover its estimated value using our prediction model 
            combined with real-time Census data.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Form Column */}
          <div className="lg:col-span-2 space-y-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="glass-card p-6"
            >
              <h3 className="text-xl font-semibold text-slate-800 mb-6 flex items-center gap-2">
                <MapPin className="w-5 h-5 text-ocean-600" />
                Location
              </h3>

              <div className="space-y-4">
                <AddressAutocomplete onSelect={handleAddressSelect} />

                <div className="grid grid-cols-2 gap-4">
                  <InputField
                    icon={Compass}
                    label="Latitude"
                    field="latitude"
                    min={32}
                    max={42}
                    step={0.01}
                    helpText="32°N to 42°N"
                  />
                  <InputField
                    icon={Compass}
                    label="Longitude"
                    field="longitude"
                    min={-125}
                    max={-114}
                    step={0.01}
                    helpText="-125°W to -114°W"
                  />
                </div>

                <div className="space-y-2">
                  <label className="flex items-center gap-2 text-sm font-medium text-slate-700">
                    <Compass className="w-4 h-4 text-ocean-500" />
                    Ocean Proximity
                  </label>
                  <select
                    value={formData.ocean_proximity}
                    onChange={(e) => handleInputChange('ocean_proximity', e.target.value)}
                    className="input-field"
                  >
                    {OCEAN_PROXIMITY_OPTIONS.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label} ({(option.multiplier * 100 - 100).toFixed(0)}%)
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.1 }}
              className="glass-card p-6"
            >
              <h3 className="text-xl font-semibold text-slate-800 mb-6 flex items-center gap-2">
                <Building2 className="w-5 h-5 text-ocean-600" />
                Property Details
              </h3>

              <div className="space-y-6">
                <RangeField
                  icon={Home}
                  label="Housing Median Age"
                  field="housing_median_age"
                  min={1}
                  max={52}
                  formatValue={(v) => `${v} years`}
                />

                <div className="grid grid-cols-2 gap-4">
                  <InputField
                    icon={Building2}
                    label="Total Rooms"
                    field="total_rooms"
                    min={2}
                    max={40000}
                  />
                  <InputField
                    icon={Bed}
                    label="Total Bedrooms"
                    field="total_bedrooms"
                    min={1}
                    max={6500}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <InputField
                    icon={Users}
                    label="Population"
                    field="population"
                    min={3}
                    max={36000}
                  />
                  <InputField
                    icon={Home}
                    label="Households"
                    field="households"
                    min={1}
                    max={6100}
                  />
                </div>

                <RangeField
                  icon={Wallet}
                  label="Median Income (in $10,000s)"
                  field="median_income"
                  min={0.5}
                  max={15}
                  step={0.1}
                  formatValue={(v) => `$${(v * 10000).toLocaleString()}`}
                />
              </div>
            </motion.div>
          </div>

          {/* Results Column */}
          <div className="space-y-6">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <PriceDisplay
                price={result?.price || 0}
                range={result?.range || { low: 0, high: 0 }}
                confidence={result?.confidence || 0.85}
                isLoading={isCalculating}
              />
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ delay: 0.2 }}
            >
              <CensusDataCard
                lat={formData.latitude}
                lon={formData.longitude}
              />
            </motion.div>
          </div>
        </div>
      </div>
    </section>
  );
};
