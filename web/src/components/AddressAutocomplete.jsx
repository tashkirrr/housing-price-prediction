import { useState, useEffect, useRef } from 'react';
import { Search, MapPin, Loader2 } from 'lucide-react';
import { useAddressSearch } from '../hooks/useGeocoding';

export const AddressAutocomplete = ({ onSelect }) => {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const inputRef = useRef(null);
  const containerRef = useRef(null);

  const { data: suggestions, isLoading } = useAddressSearch(query);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (suggestion) => {
    setQuery(suggestion.fullAddress);
    setIsOpen(false);
    onSelect(suggestion);
  };

  return (
    <div ref={containerRef} className="relative">
      <div className="relative">
        <MapPin className="absolute left-4 top-1/2 transform -translate-y-1/2 text-ocean-500 w-5 h-5" />
        <input
          ref={inputRef}
          type="text"
          value={query}
          onChange={(e) => {
            setQuery(e.target.value);
            setIsOpen(true);
          }}
          onFocus={() => setIsOpen(true)}
          placeholder="Search for an address in California..."
          className="input-field pl-12 pr-12"
        />
        {isLoading ? (
          <Loader2 className="absolute right-4 top-1/2 transform -translate-y-1/2 text-ocean-500 w-5 h-5 animate-spin" />
        ) : (
          <Search className="absolute right-4 top-1/2 transform -translate-y-1/2 text-slate-400 w-5 h-5" />
        )}
      </div>

      {isOpen && suggestions && suggestions.length > 0 && (
        <div className="absolute z-50 w-full mt-2 bg-white rounded-xl shadow-xl border border-slate-200 overflow-hidden">
          {suggestions.map((suggestion) => (
            <button
              key={suggestion.id}
              onClick={() => handleSelect(suggestion)}
              className="w-full px-4 py-3 text-left hover:bg-ocean-50 transition-colors flex items-start gap-3"
            >
              <MapPin className="w-4 h-4 text-ocean-500 mt-1 flex-shrink-0" />
              <div>
                <div className="font-medium text-slate-800">{suggestion.name}</div>
                <div className="text-sm text-slate-500 truncate">{suggestion.fullAddress}</div>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
