import Link from 'next/link';
import { Github, Twitter, Mail, Globe } from 'lucide-react';

const footerLinks = {
  product: [
    { label: 'Explore', href: '/explore' },
    { label: 'Predict', href: '/predict' },
    { label: 'Countries', href: '/explore' },
  ],
  resources: [
    { label: 'API Documentation', href: '/about' },
    { label: 'Data Sources', href: '/about' },
    { label: 'Methodology', href: '/about' },
  ],
  legal: [
    { label: 'Privacy Policy', href: '#' },
    { label: 'Terms of Service', href: '#' },
    { label: 'Cookie Policy', href: '#' },
  ],
};

export function Footer() {
  return (
    <footer className="border-t bg-slate-50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-2 md:col-span-1">
            <Link href="/" className="flex items-center gap-2 mb-4">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-ocean-600 to-teal-500">
                <Globe className="h-6 w-6 text-white" />
              </div>
              <span className="text-xl font-bold font-display">Global Housing</span>
            </Link>
            <p className="text-sm text-slate-600 mb-4">
              Property valuation using machine learning and real-time data from around the world.
            </p>
            <div className="flex gap-4">
              <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-slate-600">
                <Github className="h-5 w-5" />
              </a>
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="text-slate-400 hover:text-slate-600">
                <Twitter className="h-5 w-5" />
              </a>
              <a href="mailto:contact@example.com" className="text-slate-400 hover:text-slate-600">
                <Mail className="h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Links */}
          <div>
            <h3 className="font-semibold text-slate-900 mb-4">Product</h3>
            <ul className="space-y-2">
              {footerLinks.product.map((link) => (
                <li key={link.label}>
                  <Link href={link.href} className="text-sm text-slate-600 hover:text-slate-900">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-slate-900 mb-4">Resources</h3>
            <ul className="space-y-2">
              {footerLinks.resources.map((link) => (
                <li key={link.label}>
                  <Link href={link.href} className="text-sm text-slate-600 hover:text-slate-900">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-slate-900 mb-4">Legal</h3>
            <ul className="space-y-2">
              {footerLinks.legal.map((link) => (
                <li key={link.label}>
                  <Link href={link.href} className="text-sm text-slate-600 hover:text-slate-900">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t text-center text-sm text-slate-500">
          <p>&copy; {new Date().getFullYear()} Global Housing Predictor. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
