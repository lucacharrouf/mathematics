import React from "react";
import { ExternalLink, Github, Mail, Twitter } from "lucide-react";
import EmailSignupForm from "./EmailSignupForm";

interface FooterProps {
  companyName?: string;
  year?: number;
  links?: Array<{
    label: string;
    href: string;
    external?: boolean;
  }>;
  socialLinks?: Array<{
    icon: React.ReactNode;
    href: string;
    label: string;
  }>;
}

const Footer = ({
  companyName = "Math Visualization Platform",
  year = new Date().getFullYear(),
  links = [
    { label: "About", href: "/" },
    { label: "Video Directory", href: "/topics" },
    { label: "Contact", href: "mailto:lucacharrouf@berkeley.edu", external: true },
  ],
  socialLinks = [
    {
      icon: <Twitter size={18} />,
      href: "https://twitter.com",
      label: "Twitter",
    },
    { icon: <Github size={18} />, href: "https://github.com", label: "GitHub" },
    {
      icon: <Mail size={18} />,
      href: "mailto:info@mathviz.com",
      label: "Email",
    },
  ],
}: FooterProps) => {
  return (
    <footer className="w-full bg-slate-900 text-white py-8">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center mb-8">
          <div className="mb-6 md:mb-0">
            <h3 className="text-xl font-bold">{companyName}</h3>
            <p className="text-slate-400 mt-2">
              Transforming abstract math into visual understanding
            </p>
          </div>

          <div className="flex flex-col gap-4 w-full md:w-auto">
            <div className="bg-slate-800 p-4 rounded-lg">
              <h3 className="text-b font-medium mb-2 text-sm text-white">
                Get updates on new topics
              </h3>
              <EmailSignupForm
                variant="footer"
                buttonText="Subscribe"
                placeholder="Your email"
              />
            </div>
          </div>
        </div>

        <div className="border-t border-slate-700 pt-6 pb-4">
          <div className="flex flex-wrap gap-x-8 gap-y-2 justify-center mb-6">
            {links.map((link, index) => (
              <a
                key={index}
                href={link.href}
                className="text-slate-300 hover:text-white transition-colors"
                {...(link.external
                  ? { target: "_blank", rel: "noopener noreferrer" }
                  : {})}
              >
                {link.label}
                {link.external && (
                  <ExternalLink size={14} className="inline ml-1" />
                )}
              </a>
            ))}
          </div>

          <div className="flex justify-center gap-6 mb-6">
            {socialLinks.map((link, index) => (
              <a
                key={index}
                href={link.href}
                aria-label={link.label}
                className="text-slate-400 hover:text-white transition-colors"
                target="_blank"
                rel="noopener noreferrer"
              >
                {link.icon}
              </a>
            ))}
          </div>

          <p className="text-center text-slate-400 text-sm">
            © {year} {companyName}. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
