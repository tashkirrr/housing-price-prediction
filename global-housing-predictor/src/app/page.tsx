import { Hero } from '@/components/sections/Hero';
import { FeaturedLocations } from '@/components/sections/FeaturedLocations';
import { HowItWorks } from '@/components/sections/HowItWorks';
import { StatsSection } from '@/components/sections/StatsSection';

export default function HomePage() {
  return (
    <>
      <Hero />
      <StatsSection />
      <FeaturedLocations />
      <HowItWorks />
    </>
  );
}
