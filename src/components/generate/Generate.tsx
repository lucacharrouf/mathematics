import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Video } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface GenerateProps {
  title?: string;
  description?: string;
}

interface RecommendedTopic {
  id: string;
  name: string;
}

const Generate: React.FC<GenerateProps> = ({
  title = "Generate Math Visualization",
  description = "Input a mathematical topic or problem, and we'll generate a video explanation with interactive visualizations.",
}) => {
  const navigate = useNavigate();
  const [topic, setTopic] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedVideo, setGeneratedVideo] = useState<string | null>(null);

  // Sample recommended topics
  const recommendedTopics: RecommendedTopic[] = [
    { id: "eigenvalues", name: "Eigenvalues" },
    { id: "fourier-transform", name: "Fourier Transform" },
    { id: "matrix-multiplication", name: "Matrix Multiplication" },
    { id: "vector-spaces", name: "Vector Spaces" },
    { id: "differential-equations", name: "Differential Equations" },
    { id: "probability-distributions", name: "Probability Distributions" },
  ];

  const handleGenerateVideo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setIsGenerating(true);

    // Simulate video generation with a timeout
    // In a real application, this would be an API call to a backend service
    setTimeout(() => {
      // For demo purposes, we'll just set a sample video
      // In a real app, this would be the URL returned from the API
      setGeneratedVideo("/src/videos/vector_addition_animation.mp4");
      setIsGenerating(false);
    }, 3000);
  };

  const handleTopicClick = (topicName: string) => {
    setTopic(topicName);
  };

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Header */}
      <div className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => navigate("/")}
              className="mr-4"
              aria-label="Back to home"
            >
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <h1 className="text-2xl font-bold">{title}</h1>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-3xl mx-auto mb-12">
          <p className="text-lg text-slate-600 mb-8 text-center">
            {description}
          </p>

          {/* Input form */}
          <form
            onSubmit={handleGenerateVideo}
            className="space-y-6 bg-white p-6 rounded-xl shadow-md"
          >
            <div>
              <label
                htmlFor="topic"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
                Mathematical Topic or Problem
              </label>
              <Input
                id="topic"
                type="text"
                placeholder="e.g., Eigenvalues, Fourier Transform, Vector Addition"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                required
                className="py-6 text-base"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Recommended Topics
              </label>
              <div className="flex flex-wrap gap-2">
                {recommendedTopics.map((recTopic) => (
                  <Badge
                    key={recTopic.id}
                    variant="outline"
                    className="cursor-pointer hover:bg-slate-100"
                    onClick={() => handleTopicClick(recTopic.name)}
                  >
                    {recTopic.name}
                  </Badge>
                ))}
              </div>
            </div>

            <Button
              type="submit"
              className="w-full py-6"
              disabled={!topic.trim() || isGenerating}
            >
              {isGenerating ? (
                <>
                  <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent"></div>
                  Generating Video...
                </>
              ) : (
                <>Generate Visualization</>
              )}
            </Button>
          </form>

          {/* Generated video section */}
          {generatedVideo && (
            <div className="mt-12 bg-white p-6 rounded-xl shadow-md">
              <h2 className="text-xl font-bold mb-4 flex items-center">
                <Video className="mr-2 h-5 w-5 text-indigo-700" />
                Generated Visualization
              </h2>
              <div className="aspect-video rounded-lg overflow-hidden bg-black">
                <video
                  src={generatedVideo}
                  controls
                  className="w-full h-full"
                  autoPlay
                />
              </div>
              <div className="mt-4">
                <h3 className="font-medium text-lg mb-2">Related Topics</h3>
                <div className="flex flex-wrap gap-2">
                  {recommendedTopics.slice(0, 4).map((recTopic) => (
                    <Badge
                      key={recTopic.id}
                      variant="outline"
                      className="cursor-pointer hover:bg-slate-100"
                      onClick={() => handleTopicClick(recTopic.name)}
                    >
                      {recTopic.name}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Generate;
