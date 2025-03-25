import React, { useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

interface InteractiveDemoProps {
  title?: string;
  description?: string;
  concepts?: {
    id: string;
    name: string;
    description: string;
    visualizationUrl: string;
    videoUrl?: string;
  }[];
}

const InteractiveDemo = ({
  title = "Try Our Interactive Visualizations",
  description = "Select a mathematical concept below to see how our platform transforms abstract ideas into intuitive visual representations.",
  concepts = [
    {
      id: "vectors",
      name: "Vector Addition",
      description:
        "Visualize how vectors add together in 2D space with interactive controls.",
      visualizationUrl:
        "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&q=80",
      videoUrl: "/src/videos/vector_addition_animation.mp4",
    },
    {
      id: "linearSystems",
      name: "Orthogonality",
      description: "Visualize how orthogonality works.",
      visualizationUrl:
        "https://images.unsplash.com/photo-1580894908361-967195033215?w=800&q=80",
      videoUrl: "/src/videos/orthogonality_animation.mp4",
    },
  ],
}: InteractiveDemoProps) => {
  const [selectedConcept, setSelectedConcept] = useState<string | null>(null);
  const [isInteracting, setIsInteracting] = useState(false);

  const selectedConceptData = concepts.find((c) => c.id === selectedConcept);

  return (
    <section className="py-20 px-4 md:px-8 bg-slate-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <motion.h2
            className="text-3xl md:text-4xl font-bold mb-4 text-slate-900"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            {title}
          </motion.h2>
          <motion.p
            className="text-lg text-slate-600 max-w-3xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
          >
            {description}
          </motion.p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          <motion.div
            className="flex flex-col space-y-6"
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Card>
              <CardHeader>
                <CardTitle>Select a Concept</CardTitle>
                <CardDescription>
                  Choose a mathematical concept to explore its visualization
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Select onValueChange={(value) => setSelectedConcept(value)}>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Select a mathematical concept" />
                  </SelectTrigger>
                  <SelectContent>
                    {concepts.map((concept) => (
                      <SelectItem key={concept.id} value={concept.id}>
                        {concept.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>

                {selectedConceptData && (
                  <div className="mt-6">
                    <h3 className="text-xl font-semibold mb-2">
                      {selectedConceptData.name}
                    </h3>
                    <p className="text-slate-600 mb-4">
                      {selectedConceptData.description}
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            className="rounded-xl overflow-hidden shadow-lg bg-white"
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            {selectedConceptData ? (
              <div className="relative">
                {selectedConceptData.videoUrl ? (
                  <video
                    src={selectedConceptData.videoUrl}
                    autoPlay
                    loop
                    muted
                    className="w-full h-[400px] object-cover"
                  />
                ) : (
                  <img
                    src={selectedConceptData.visualizationUrl}
                    alt={`${selectedConceptData.name} visualization`}
                    className="w-full h-[400px] object-cover"
                  />
                )}
              </div>
            ) : (
              <div className="flex items-center justify-center h-[400px] bg-slate-100">
                <div className="text-center p-8">
                  <h3 className="text-xl font-semibold mb-2">
                    Select a concept to see visualization
                  </h3>
                  <p className="text-slate-500">
                    Choose from the dropdown menu to explore interactive
                    visualizations
                  </p>
                </div>
              </div>
            )}
          </motion.div>
        </div>

        <motion.div
          className="mt-12 text-center"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Button size="lg" className="bg-indigo-600 hover:bg-indigo-700">
            Explore All Visualizations
          </Button>
        </motion.div>
      </div>
    </section>
  );
};

export default InteractiveDemo;
