import { Github, Heart, Mail, Twitter } from 'lucide-react';

export const Footer = () => {
  return (
    <footer className="bg-slate-900 text-white py-12">
      <div className="section-padding max-w-7xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="text-2xl font-bold font-display mb-4">
              California Dream Homes
            </h3>
            <p className="text-slate-400 leading-relaxed">
              Property valuation using machine learning and real-time Census data.
              Helping Californians understand their home's worth since 2024.
            </p>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Data Sources</h4>
            <ul className="space-y-2 text-slate-400">
              <li>
                <a href="https://www.census.gov/data/developers/data-sets/acs-5year.html" 
                   target="_blank" 
                   rel="noopener noreferrer"
                   className="hover:text-white transition-colors">
                  US Census Bureau
                </a>
              </li>
              <li>
                <a href="https://nominatim.org/" 
                   target="_blank" 
                   rel="noopener noreferrer"
                   className="hover:text-white transition-colors">
                  OpenStreetMap Nominatim
                </a>
              </li>
              <li>
                <a href="https://www.kaggle.com/datasets/camnugent/california-housing-prices" 
                   target="_blank" 
                   rel="noopener noreferrer"
                   className="hover:text-white transition-colors">
                  California Housing Dataset
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Connect</h4>
            <div className="flex gap-4">
              <a href="https://github.com/tashkirrr/housing-price-prediction" 
                 target="_blank" 
                 rel="noopener noreferrer"
                 className="w-10 h-10 bg-slate-800 rounded-lg flex items-center justify-center hover:bg-slate-700 transition-colors">
                <Github className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>

        <div className="pt-8 border-t border-slate-800 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-slate-400 text-sm">
            Made with <Heart className="w-4 h-4 inline text-red-500" /> by{' '}
            <a href="https://github.com/tashkirrr" className="text-ocean-400 hover:text-ocean-300">
              @tashkirrr
            </a>
          </p>
          <p className="text-slate-500 text-sm">
            Data based on 1990 Census. Not financial advice.
          </p>
        </div>
      </div>
    </footer>
  );
};
