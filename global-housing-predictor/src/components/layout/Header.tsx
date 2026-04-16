'use client';

import Link from 'next/link';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X, Globe, Search, Home, Map, Calculator, Info } from 'lucide-react';

const navItems = [
  { href: '/', label: 'Home', icon: Home },
  { href: '/explore', label: 'Explore', icon: Map },
  { href: '/predict', label: 'Predict', icon: Calculator },
  { href: '/about', label: 'About', icon: Info },
];

export function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-white/80 backdrop-blur-xl">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-ocean-600 to-teal-500">
              <Globe className="h-6 w-6 text-white" />
            </div>
            <span className="hidden text-xl font-bold sm:inline-block font-display">
              Global Housing
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-100 hover:text-slate-900"
              >
                <item.icon className="h-4 w-4" />
                {item.label}
              </Link>
            ))}
          </nav>

          {/* Search & Mobile Menu */}
          <div className="flex items-center gap-2">
            <Link
              href="/explore"
              className="hidden sm:flex items-center gap-2 rounded-lg bg-slate-100 px-4 py-2 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-200"
            >
              <Search className="h-4 w-4" />
              <span>Search</span>
            </Link>

            <button
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-100 md:hidden"
            >
              {isMenuOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      <AnimatePresence>
        {isMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="border-t bg-white md:hidden"
          >
            <nav className="container mx-auto px-4 py-4 space-y-1">
              {navItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => setIsMenuOpen(false)}
                  className="flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-100"
                >
                  <item.icon className="h-5 w-5" />
                  {item.label}
                </Link>
              ))}
            </nav>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
