import React from "react";
import { Button } from "@/components/ui/button";
import { ArrowRight, Upload, Sparkles, BookOpen } from "lucide-react";

interface FutureFeaturesProps {
  title?: string;
  description?: string;
  features?: {
    title: string;
    description: string;
    icon: React.ReactNode;
    mockupImage?: string;
  }[];
}

const FutureFeatures: React.FC<FutureFeaturesProps> = ({
  title = "Coming Soon to Our Platform",
  description = "We're constantly working to make learning mathematics more intuitive and engaging. Here's what's coming next:",
  features = [
    {
      title: "Homework Upload & Analysis",
      description:
        "Upload your math homework and get step-by-step visual explanations for each problem. Our system will identify the concepts and create custom visualizations.",
      icon: <Upload className="h-6 w-6" />,
      mockupImage:
        "https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?w=800&q=80",
    },
    {
      title: "Interactive Textbook Integration",
      description:
        "Connect your digital textbooks to automatically generate visualizations for theorems and examples as you study.",
      icon: <BookOpen className="h-6 w-6" />,
      mockupImage:
        "https://images.unsplash.com/photo-1532619675605-1ede6c2ed2b0?w=800&q=80",
    },
    {
      title: "AI-Powered Concept Mapping",
      description:
        "Our AI will map connections between mathematical concepts, helping you understand how different topics relate to each other.",
      icon: <Sparkles className="h-6 w-6" />,
      mockupImage:
        "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=800&q=80",
    },
  ],
}) => {
  return (
    <section className="w-full py-20 bg-slate-50">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold tracking-tight mb-4">{title}</h2>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            {description}
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white rounded-xl shadow-md overflow-hidden flex flex-col h-full"
            >
              <div className="p-6 flex-1">
                <div className="inline-flex items-center justify-center p-2 bg-primary/10 rounded-lg mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-slate-600 mb-4">{feature.description}</p>
              </div>

              {feature.mockupImage && (
                <div className="relative h-48 w-full overflow-hidden bg-slate-100">
                  <img
                    src={feature.mockupImage}
                    alt={`${feature.title} mockup`}
                    className="w-full h-full object-cover transition-transform hover:scale-105"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent flex items-end">
                    <div className="p-4 w-full">
                      <Button variant="secondary" size="sm" className="w-full">
                        <span>Learn more</span>
                        <ArrowRight className="ml-2 h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="mt-16 text-center">
          <Button className="mr-4">Explore Current Features</Button>
          <Button variant="outline">Get Notified About Updates</Button>
        </div>
      </div>
    </section>
  );
};

export default FutureFeatures;
