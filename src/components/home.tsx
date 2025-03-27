import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Video, BookOpen, Send } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import Footer from "./landing/Footer.tsx";

interface RecommendedTopic {
  id: string;
  name: string;
}

// Video mapping based on available videos
const videoMapping: { [key: string]: string } = {
  "eigenvalues": "/videos/eigenvalue_and_eigenvectors_animation_ic.mp4",
  "eigenvectors": "/videos/eigenvalue_and_eigenvectors_animation_ic.mp4",
  "eigendecomposition": "/videos/eigendecomposition_animation_ic.mp4",
  "complex numbers": "/videos/complex_numbers_animation_ic.mp4",
  "bayes theorem": "/videos/bayes_theorem_animation_ic.mp4",
  "bayesian": "/videos/bayes_theorem_animation_ic.mp4",
  "support vector machines": "/videos/support_vector_machines_animation_1.mp4",
  "svm": "/videos/support_vector_machines_animation_1.mp4",
  "gradient descent": "/videos/gradient_descent_animation.mp4",
  "derivatives": "/videos/calculus_derivatives_animation.mp4",
  "fourier transform": "/videos/fourier_transform_animation.mp4",
  "financial mathematics": "/videos/financial_mathematics_animation_ic.mp4",
  "pythagorean theorem": "/videos/pythagorean_theorem_animation_ic.mp4",
  "vector addition": "/videos/vector_addition_animation.mp4",
  "orthogonality": "/videos/orthogonality_animation.mp4",
  "singular value decomposition": "/videos/singular_value_decomposition_animation.mp4",
  "svd": "/videos/singular_value_decomposition_animation.mp4"
};

function Home() {
  const navigate = useNavigate();
  const [topic, setTopic] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedVideo, setGeneratedVideo] = useState<string | null>(null);
  const [showSuggestionForm, setShowSuggestionForm] = useState(false);
  const [suggestion, setSuggestion] = useState("");
  const [suggestionSubmitted, setSuggestionSubmitted] = useState(false);

  // Sample recommended topics
  const recommendedTopics: RecommendedTopic[] = [
    { id: "eigenvalues", name: "Eigenvalues" },
    { id: "fourier-transform", name: "Fourier Transform" },
    { id: "svm", name: "Support Vector Machines" },
    { id: "gradient-descent", name: "Gradient Descent" },
    { id: "derivatives", name: "Derivatives" },
    { id: "complex-numbers", name: "Complex Numbers" },
    { id: "bayes-theorem", name: "Bayes Theorem" },
    { id: "pythagorean-theorem", name: "Pythagorean Theorem" },
    { id: "vector-addition", name: "Vector Addition" },
    { id: "orthogonality", name: "Orthogonality" },
    { id: "svd", name: "Singular Value Decomposition" },
    { id: "financial-mathematics", name: "Financial Mathematics" }
  ];

  const findSimilarTopic = (inputTopic: string): string | null => {
    const normalizedInput = inputTopic.toLowerCase().trim();
    
    // Direct match
    if (videoMapping[normalizedInput]) {
      return normalizedInput;
    }

    // Check for partial matches
    for (const topic of Object.keys(videoMapping)) {
      if (normalizedInput.includes(topic) || topic.includes(normalizedInput)) {
        return topic;
      }
    }

    return null;
  };

  const handleGenerateVideo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setIsGenerating(true);
    setShowSuggestionForm(false);
    setSuggestionSubmitted(false);

    // Check if we have a similar topic
    const similarTopic = findSimilarTopic(topic);
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 5000));

    if (similarTopic) {
      setGeneratedVideo(videoMapping[similarTopic]);
    } else {
      setShowSuggestionForm(true);
    }

    setIsGenerating(false);
  };

  const handleTopicClick = (topicName: string) => {
    setTopic(topicName);
  };

  const handleSuggestionSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!suggestion.trim()) return;
    
    // Here you would typically send the suggestion to your backend
    setSuggestionSubmitted(true);
    setSuggestion("");
  };

  return (
    <div className="min-h-screen bg-slate-50 relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-100 to-slate-200">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-slate-200/50 via-transparent to-transparent animate-pulse"></div>
      </div>

      {/* Header */}
      <div className="relative bg-white/80 backdrop-blur-sm shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold">Math Visualizer</h1>
              <Badge variant="secondary" className="bg-blue-100 text-blue-800 hover:bg-blue-100">
                Beta
              </Badge>
            </div>
            <Button
              variant="outline"
              onClick={() => navigate("/topics")}
              className="flex items-center gap-2"
            >
              <BookOpen className="h-4 w-4" />
              Browse Library
            </Button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="relative min-h-[calc(100vh-4rem)] flex items-center justify-center">
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-3xl mx-auto text-center">
            <h2 className="text-4xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-slate-900 to-slate-600">
              Generate Math Visualization
            </h2>
            <p className="text-lg text-slate-600 mb-8">
              Input a mathematical topic or problem, and we'll generate a video explanation with interactive visualizations.
            </p>

            {/* Topic input form */}
            <form onSubmit={handleGenerateVideo} className="space-y-4 bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-lg">
              <Input
                type="text"
                placeholder="Enter a mathematical topic (e.g., 'Eigenvalues and Eigenvectors')"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                required
                className="py-6 text-base"
              />
              <Button
                type="submit"
                className="w-full py-6"
                disabled={!topic.trim() || isGenerating}
              >
                {isGenerating ? (
                  <span className="flex items-center gap-2">
                    <Video className="h-5 w-5 animate-pulse" />
                    Generating Video...
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    <Video className="h-5 w-5" />
                    Generate Video
                  </span>
                )}
              </Button>
            </form>

            {/* Recommended topics */}
            <div className="mt-12">
              <h3 className="text-lg font-semibold mb-4">Recommended Topics</h3>
              <div className="flex flex-wrap justify-center gap-2">
                {recommendedTopics.map((topic) => (
                  <Badge
                    key={topic.id}
                    variant="outline"
                    className="cursor-pointer hover:bg-primary hover:text-white transition-colors"
                    onClick={() => handleTopicClick(topic.name)}
                  >
                    {topic.name}
                  </Badge>
                ))}
              </div>
            </div>
          </div>

          {/* Generated video section */}
          {generatedVideo && (
            <div className="max-w-3xl mx-auto mt-12">
              <h3 className="text-xl font-bold mb-4">Generated Video</h3>
              <div className="bg-white/80 backdrop-blur-sm rounded-xl shadow-lg overflow-hidden">
                <video
                  src={generatedVideo}
                  controls
                  className="w-full aspect-video"
                />
              </div>
            </div>
          )}

          {/* Suggestion form */}
          {showSuggestionForm && (
            <div className="max-w-3xl mx-auto mt-12 bg-white/80 backdrop-blur-sm p-8 rounded-2xl shadow-lg">
              <h3 className="text-xl font-bold mb-4">Topic Not Available</h3>
              <p className="text-slate-600 mb-6">
                We don't have a visualization for this topic yet. Suggest it to us, and we'll consider adding it to our library.
              </p>
              {!suggestionSubmitted ? (
                <form onSubmit={handleSuggestionSubmit} className="space-y-4">
                  <Input
                    type="text"
                    placeholder="Enter your topic suggestion"
                    value={suggestion}
                    onChange={(e) => setSuggestion(e.target.value)}
                    required
                    className="py-6 text-base"
                  />
                  <Button
                    type="submit"
                    className="w-full py-6"
                    disabled={!suggestion.trim()}
                  >
                    <span className="flex items-center gap-2">
                      <Send className="h-5 w-5" />
                      Submit Suggestion
                    </span>
                  </Button>
                </form>
              ) : (
                <div className="text-center">
                  <p className="text-green-600 font-medium">Thank you for your suggestion! We'll consider adding this topic to our library.</p>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setShowSuggestionForm(false);
                      setSuggestionSubmitted(false);
                    }}
                    className="mt-4"
                  >
                    Try Another Topic
                  </Button>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Footer - Only visible on scroll */}
      <div className="relative mt-auto">
        <Footer />
      </div>
    </div>
  );
}

export default Home;
