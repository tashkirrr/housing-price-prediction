import { Hero } from './components/Hero';
import { PredictionForm } from './components/PredictionForm';
import { Features } from './components/Features';
import { Footer } from './components/Footer';

function App() {
  return (
    <div className="min-h-screen">
      <Hero />
      <PredictionForm />
      <Features />
      <Footer />
    </div>
  );
}

export default App;
