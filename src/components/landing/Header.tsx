import React from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

interface HeaderProps {
  links?: Array<{ label: string; href: string }>;
}

const Header = ({
  links = [
    { label: "Topics", href: "#topics" },
    { label: "Demo", href: "#demo" },
    { label: "Features", href: "#features" },
    { label: "Contact", href: "#contact" },
  ],
}: HeaderProps) => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white shadow-sm py-4">
      <div className="container mx-auto px-4 flex justify-between items-center">
        <div className="flex items-center">
          <Link
            to="/"
            className="text-2xl font-bold text-slate-900 flex items-center"
          >
            <svg
              viewBox="0 0 24 24"
              width="32"
              height="32"
              className="mr-2 text-blue-600"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="12" cy="12" r="10" />
              <line x1="14.31" y1="8" x2="20.05" y2="17.94" />
              <line x1="9.69" y1="8" x2="21.17" y2="8" />
              <line x1="7.38" y1="12" x2="13.12" y2="2.06" />
              <line x1="9.69" y1="16" x2="3.95" y2="6.06" />
              <line x1="14.31" y1="16" x2="2.83" y2="16" />
              <line x1="16.62" y1="12" x2="10.88" y2="21.94" />
            </svg>
            <div className="flex items-center">
              MathViz
              <span className="ml-2 text-xs font-medium px-2 py-1 bg-blue-100 text-blue-800 rounded-full">
                BETA
              </span>
            </div>
          </Link>
        </div>

        <nav className="hidden md:flex items-center space-x-8">
          {links.map((link, index) => (
            <a
              key={index}
              href={link.href}
              className="text-slate-700 hover:text-blue-600 font-medium transition-colors"
            >
              {link.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center space-x-4">
          <Button
            variant="outline"
            className="hidden md:inline-flex border-slate-300 hover:bg-slate-100 text-slate-800"
          >
            Sign In
          </Button>
          <Button className="bg-blue-600 hover:bg-blue-700 text-white">
            Get Started
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;
