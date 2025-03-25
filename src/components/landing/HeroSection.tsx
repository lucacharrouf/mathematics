import React from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import EmailSignupForm from "./EmailSignupForm";

interface HeroSectionProps {
  title?: string;
  subtitle?: string;
  primaryCta?: string;
  secondaryCta?: string;
  onPrimaryClick?: () => void;
  onSecondaryClick?: () => void;
}

const HeroSection = ({
  title = "Visualize Mathematics Like Never Before",
  subtitle = "Transform abstract mathematical concepts into interactive visualizations to enhance understanding and intuition.",
  primaryCta = "Explore Visualizations",
  secondaryCta = "Watch Demo",
  onPrimaryClick = () => {},
  onSecondaryClick = () => {},
}: HeroSectionProps) => {
  return (
    <section
      id="hero"
      className="relative w-full min-h-[700px] bg-white pt-24 pb-16 overflow-hidden"
    >
      {/* Subtle background pattern */}
      <div className="absolute inset-0 bg-[radial-gradient(#e5e7eb_1px,transparent_1px)] [background-size:20px_20px] opacity-30"></div>

      {/* Main content container */}
      <div className="relative z-10 container mx-auto px-4 h-full flex flex-col lg:flex-row items-center">
        {/* Left content - Text */}
        <div className="w-full lg:w-1/2 lg:pr-12 mb-12 lg:mb-0">
          {/* Heading */}
          <motion.h1
            className="text-5xl md:text-6xl font-bold mb-6 text-slate-900 leading-tight"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.8 }}
          >
            {title}
          </motion.h1>

          {/* Subheading */}
          <motion.p
            className="text-xl md:text-2xl text-slate-600 mb-10 max-w-2xl"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.8 }}
          >
            {subtitle}
          </motion.p>

          {/* Call to action buttons */}
          <motion.div
            className="flex flex-col gap-6 mt-2"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
          >
            <Button
              size="lg"
              onClick={() => (window.location.href = "/topics")}
              className="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-8 py-6 h-auto text-lg w-full sm:w-auto"
            >
              {primaryCta} <ArrowRight className="ml-2 h-5 w-5" />
            </Button>

            <div className="bg-white/80 backdrop-blur-sm p-5 rounded-xl shadow-lg border border-slate-200">
              <h3 className="text-lg font-semibold mb-3 text-slate-800">
                Join our waitlist
              </h3>
              <p className="text-sm text-slate-600 mb-4">
                Be the first to know when we add new math topics and features.
              </p>
              <div className="w-full">
                <EmailSignupForm variant="hero" buttonText="Join Waitlist" />
              </div>
            </div>
          </motion.div>
        </div>

        {/* Right content - Image */}
        <div className="w-full lg:w-1/2 relative">
          <motion.div
            className="relative"
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.4, duration: 0.8 }}
          >
            {/* Full abstract mathematical visualization */}
            <div className="relative overflow-hidden rounded-3xl shadow-2xl">
              <div className="w-full h-[500px] bg-gradient-to-br from-blue-50 via-indigo-100 to-purple-100 rounded-3xl">
                {/* Mathematical animation */}
                <svg
                  className="absolute top-0 left-0 w-full h-full"
                  viewBox="0 0 800 500"
                  preserveAspectRatio="xMidYMid slice"
                >
                  {/* Grid pattern */}
                  <pattern
                    id="grid"
                    width="40"
                    height="40"
                    patternUnits="userSpaceOnUse"
                  >
                    <path
                      d="M 40 0 L 0 0 0 40"
                      fill="none"
                      stroke="rgba(79, 70, 229, 0.1)"
                      strokeWidth="1"
                    />
                  </pattern>
                  <rect width="100%" height="100%" fill="url(#grid)" />

                  {/* Vector field visualization */}
                  <g>
                    {Array.from({ length: 15 }).map((_, i) =>
                      Array.from({ length: 10 }).map((_, j) => (
                        <motion.path
                          key={`vector-${i}-${j}`}
                          d={`M ${50 + i * 50} ${50 + j * 50} q ${Math.sin((i + j) * 0.5) * 20} ${Math.cos((i + j) * 0.5) * 20} ${Math.sin((i + j) * 0.3) * 40} ${Math.cos((i + j) * 0.3) * 40}`}
                          stroke={
                            j % 2 === 0
                              ? "rgba(56, 189, 248, 0.6)"
                              : "rgba(168, 85, 247, 0.6)"
                          }
                          strokeWidth="2"
                          fill="none"
                          animate={{
                            d: [
                              `M ${50 + i * 50} ${50 + j * 50} q ${Math.sin((i + j) * 0.5) * 20} ${Math.cos((i + j) * 0.5) * 20} ${Math.sin((i + j) * 0.3) * 40} ${Math.cos((i + j) * 0.3) * 40}`,
                              `M ${50 + i * 50} ${50 + j * 50} q ${Math.cos((i + j) * 0.5) * 20} ${Math.sin((i + j) * 0.5) * 20} ${Math.cos((i + j) * 0.3) * 40} ${Math.sin((i + j) * 0.3) * 40}`,
                              `M ${50 + i * 50} ${50 + j * 50} q ${Math.sin((i + j) * 0.5) * 20} ${Math.cos((i + j) * 0.5) * 20} ${Math.sin((i + j) * 0.3) * 40} ${Math.cos((i + j) * 0.3) * 40}`,
                            ],
                          }}
                          transition={{
                            duration: 8 + ((i + j) % 4),
                            repeat: Infinity,
                            ease: "easeInOut",
                          }}
                        />
                      )),
                    )}
                  </g>

                  {/* Animated circles */}
                  <motion.g
                    animate={{
                      rotate: [0, 360],
                    }}
                    transition={{
                      duration: 40,
                      repeat: Infinity,
                      ease: "linear",
                    }}
                    style={{ transformOrigin: "center" }}
                  >
                    <motion.circle
                      cx="400"
                      cy="250"
                      r="120"
                      fill="none"
                      stroke="rgba(79, 70, 229, 0.2)"
                      strokeWidth="1"
                      animate={{ r: [120, 140, 120] }}
                      transition={{
                        duration: 8,
                        repeat: Infinity,
                        ease: "easeInOut",
                      }}
                    />
                    <motion.circle
                      cx="400"
                      cy="250"
                      r="80"
                      fill="none"
                      stroke="rgba(79, 70, 229, 0.3)"
                      strokeWidth="1"
                      animate={{ r: [80, 100, 80] }}
                      transition={{
                        duration: 8,
                        repeat: Infinity,
                        ease: "easeInOut",
                        delay: 0.5,
                      }}
                    />
                    <motion.circle
                      cx="400"
                      cy="250"
                      r="40"
                      fill="none"
                      stroke="rgba(79, 70, 229, 0.4)"
                      strokeWidth="1"
                      animate={{ r: [40, 60, 40] }}
                      transition={{
                        duration: 8,
                        repeat: Infinity,
                        ease: "easeInOut",
                        delay: 1,
                      }}
                    />
                  </motion.g>

                  {/* Function plot */}
                  <motion.path
                    d="M 0,250 C 100,150 200,350 300,250 C 400,150 500,350 600,250 C 700,150 800,350 900,250"
                    fill="none"
                    stroke="rgba(56, 189, 248, 0.8)"
                    strokeWidth="3"
                    animate={{
                      d: [
                        "M 0,250 C 100,150 200,350 300,250 C 400,150 500,350 600,250 C 700,150 800,350 900,250",
                        "M 0,250 C 100,350 200,150 300,250 C 400,350 500,150 600,250 C 700,350 800,150 900,250",
                        "M 0,250 C 100,150 200,350 300,250 C 400,150 500,350 600,250 C 700,150 800,350 900,250",
                      ],
                    }}
                    transition={{
                      duration: 15,
                      repeat: Infinity,
                      ease: "easeInOut",
                    }}
                  />

                  {/* Vector transformation visualization */}
                  <motion.g
                    style={{ transformOrigin: "400px 250px" }}
                    animate={{
                      rotate: [0, 360],
                    }}
                    transition={{
                      duration: 60,
                      repeat: Infinity,
                      ease: "linear",
                    }}
                  >
                    <motion.line
                      x1="400"
                      y1="250"
                      x2="550"
                      y2="250"
                      stroke="#38bdf8"
                      strokeWidth="3"
                      animate={{
                        x2: [550, 500, 400, 500, 550],
                        y2: [250, 350, 400, 350, 250],
                      }}
                      transition={{
                        duration: 12,
                        repeat: Infinity,
                        ease: "easeInOut",
                      }}
                    />
                    <motion.line
                      x1="400"
                      y1="250"
                      x2="400"
                      y2="100"
                      stroke="#a855f7"
                      strokeWidth="3"
                      animate={{
                        x2: [400, 300, 250, 300, 400],
                        y2: [100, 150, 250, 350, 400],
                      }}
                      transition={{
                        duration: 12,
                        repeat: Infinity,
                        ease: "easeInOut",
                      }}
                    />
                    <motion.circle cx="400" cy="250" r="8" fill="#1e293b" />
                    <motion.circle
                      cx="550"
                      cy="250"
                      r="8"
                      fill="#38bdf8"
                      animate={{
                        cx: [550, 500, 400, 500, 550],
                        cy: [250, 350, 400, 350, 250],
                      }}
                      transition={{
                        duration: 12,
                        repeat: Infinity,
                        ease: "easeInOut",
                      }}
                    />
                    <motion.circle
                      cx="400"
                      cy="100"
                      r="8"
                      fill="#a855f7"
                      animate={{
                        cx: [400, 300, 250, 300, 400],
                        cy: [100, 150, 250, 350, 400],
                      }}
                      transition={{
                        duration: 12,
                        repeat: Infinity,
                        ease: "easeInOut",
                      }}
                    />
                  </motion.g>
                </svg>

                {/* Decorative elements */}
                <div className="absolute top-1/4 left-1/4 w-32 h-32 rounded-full bg-blue-500/10 blur-xl"></div>
                <div className="absolute bottom-1/3 right-1/3 w-40 h-40 rounded-full bg-purple-500/10 blur-xl"></div>
                <div className="absolute top-1/3 right-1/4 w-36 h-36 rounded-full bg-indigo-500/10 blur-xl"></div>
              </div>
            </div>

            {/* Floating formula card */}
            <motion.div
              className="absolute -bottom-6 -left-6 bg-white p-4 rounded-lg shadow-xl border border-slate-100"
              animate={{
                y: [0, -10, 0],
              }}
              transition={{
                duration: 4,
                repeat: Infinity,
                ease: "easeInOut",
              }}
            >
              <div className="text-slate-800 font-mono text-sm">
                <div>
                  f(x) = ∫<sub>a</sub>
                  <sup>b</sup> e<sup>-x²</sup> dx
                </div>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </div>

      {/* Wave divider */}
      <div className="absolute bottom-0 left-0 right-0">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 1440 120"
          fill="none"
        >
          <path
            fillRule="evenodd"
            clipRule="evenodd"
            d="M0 0L60 10C120 20 240 40 360 50C480 60 600 60 720 50C840 40 960 20 1080 15C1200 10 1320 20 1380 25L1440 30V120H1380C1320 120 1200 120 1080 120C960 120 840 120 720 120C600 120 480 120 360 120C240 120 120 120 60 120H0V0Z"
            fill="#f8fafc"
          />
        </svg>
      </div>
    </section>
  );
};

export default HeroSection;
