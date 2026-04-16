import { motion } from 'framer-motion';
import { Brain, MapPin, Database, TrendingUp, Shield, Zap } from 'lucide-react';

const features = [
  {
    icon: Brain,
    title: 'Machine Learning Model',
    description: 'Our trained model analyzes 20,640+ properties with 85% accuracy to predict home values.',
    color: 'from-purple-500 to-indigo-600',
  },
  {
    icon: MapPin,
    title: 'Real-Time Geocoding',
    description: 'Simply type an address and we automatically convert it to precise GPS coordinates using OpenStreetMap.',
    color: 'from-ocean-500 to-teal-600',
  },
  {
    icon: Database,
    title: 'Census Bureau Data',
    description: 'We fetch real demographic data including median income, home values, and population statistics.',
    color: 'from-green-500 to-emerald-600',
  },
  {
    icon: TrendingUp,
    title: 'Market Insights',
    description: 'Understand how ocean proximity, location, and local demographics affect property values.',
    color: 'from-orange-500 to-red-600',
  },
  {
    icon: Shield,
    title: 'Privacy First',
    description: 'All predictions happen in your browser. We don\'t store your search history or personal data.',
    color: 'from-blue-500 to-cyan-600',
  },
  {
    icon: Zap,
    title: 'Instant Results',
    description: 'Get predictions in milliseconds with our optimized client-side machine learning model.',
    color: 'from-yellow-500 to-amber-600',
  },
];

export const Features = () => {
  return (
    <section id="how-it-works" className="section-padding py-20 bg-white/50">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold font-display gradient-text mb-4">
            Why Choose Our Predictor?
          </h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            We combine cutting-edge machine learning with real-world data to give you 
            the most accurate property valuations possible.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.1 }}
              className="group"
            >
              <div className="glass-card p-6 h-full hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}>
                  <feature.icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-slate-800 mb-2">
                  {feature.title}
                </h3>
                <p className="text-slate-600 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};
