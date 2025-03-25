import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Search, X } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface TopicDirectoryProps {
  title?: string;
  description?: string;
}

interface Topic {
  id: string;
  title: string;
  description: string;
  videoUrl: string;
  category: string;
  hasVideo: boolean;
}

const TopicDirectory: React.FC<TopicDirectoryProps> = ({
  title = "Mathematics Visualization Library",
  description = "Explore our collection of interactive visualizations to help you understand complex mathematical concepts.",
}) => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [topicSuggestion, setTopicSuggestion] = useState("");
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);

  const topics: Topic[] = [
    // Linear Algebra
    {
      id: "vector-addition",
      title: "Vector Addition",
      description: "Visualize vector addition in 2D and 3D space with step-by-step animation.",
      videoUrl: "/src/videos/vector_addition_animation.mp4",
      category: "Linear Algebra",
      hasVideo: true,
    },
    {
      id: "orthogonality",
      title: "Orthogonality",
      description: "Learn about orthogonal vectors and their geometric properties.",
      videoUrl: "/src/videos/orthogonality_animation.mp4",
      category: "Linear Algebra",
      hasVideo: true,
    },
    {
      id: "eigenvalues",
      title: "Eigenvalues and Eigenvectors",
      description: "Understanding eigenvalues and eigenvectors through geometric transformations.",
      videoUrl: "/src/videos/eigenvalue_and_eigenvectors_animation_ic.mp4",
      category: "Linear Algebra",
      hasVideo: true,
    },
    {
      id: "eigendecomposition",
      title: "Eigendecomposition",
      description: "Visualize matrix decomposition into eigenvalues and eigenvectors.",
      videoUrl: "/src/videos/eigendecomposition_animation_ic.mp4",
      category: "Linear Algebra",
      hasVideo: true,
    },
    {
      id: "svd",
      title: "Singular Value Decomposition",
      description: "Understanding SVD through geometric transformations and applications.",
      videoUrl: "/src/videos/singular_value_decomposition_animation.mp4",
      category: "Linear Algebra",
      hasVideo: true,
    },
    // Complex Analysis
    {
      id: "complex-numbers",
      title: "Complex Numbers",
      description: "Visualization of complex numbers and their operations in the complex plane.",
      videoUrl: "/src/videos/complex_numbers_animation_ic.mp4",
      category: "Complex Analysis",
      hasVideo: true,
    },
    // Probability and Statistics
    {
      id: "bayes-theorem",
      title: "Bayes' Theorem",
      description: "Understanding conditional probability and Bayes' Theorem through visualization.",
      videoUrl: "/src/videos/bayes_theorem_animation_ic.mp4",
      category: "Probability and Statistics",
      hasVideo: true,
    },
    // Machine Learning
    {
      id: "svm",
      title: "Support Vector Machines",
      description: "Visualization of SVM classification and margin maximization.",
      videoUrl: "/src/videos/support_vector_machines_animation_1.mp4",
      category: "Machine Learning",
      hasVideo: true,
    },
    {
      id: "gradient-descent",
      title: "Gradient Descent",
      description: "Understanding optimization through gradient descent visualization.",
      videoUrl: "/src/videos/gradient_descent_animation.mp4",
      category: "Machine Learning",
      hasVideo: true,
    },
    // Calculus
    {
      id: "derivatives",
      title: "Calculus Derivatives",
      description: "Visual understanding of derivatives and their geometric interpretation.",
      videoUrl: "/src/videos/calculus_derivatives_animation.mp4",
      category: "Calculus",
      hasVideo: true,
    },
    // Signal Processing
    {
      id: "fourier-transform",
      title: "Fourier Transform",
      description: "Understanding signal decomposition through Fourier Transform visualization.",
      videoUrl: "/src/videos/fourier_transform_animation.mp4",
      category: "Signal Processing",
      hasVideo: true,
    },
    // Financial Mathematics
    {
      id: "financial-math",
      title: "Financial Mathematics",
      description: "Visualization of financial concepts and mathematical models.",
      videoUrl: "/src/videos/financial_mathematics_animation_ic.mp4",
      category: "Financial Mathematics",
      hasVideo: true,
    },
    // Geometry
    {
      id: "pythagorean",
      title: "Pythagorean Theorem",
      description: "Geometric proof and visualization of the Pythagorean Theorem.",
      videoUrl: "/src/videos/pythagorean_theorem_animation_ic.mp4",
      category: "Geometry",
      hasVideo: true,
    },
  ];

  // Get unique categories from topics
  const categories = Array.from(new Set(topics.map(topic => topic.category)));

  const filteredTopics = topics.filter((topic) => {
    const matchesSearch = 
      topic.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      topic.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      topic.category.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesCategory = selectedCategories.length === 0 || selectedCategories.includes(topic.category);
    
    return matchesSearch && matchesCategory;
  });

  const toggleCategory = (category: string) => {
    setSelectedCategories(prev => 
      prev.includes(category) 
        ? prev.filter(c => c !== category)
        : [...prev, category]
    );
  };

  const handleSubmitSuggestion = (e: React.FormEvent) => {
    e.preventDefault();
    alert(
      `Thank you for suggesting "${topicSuggestion}"! We'll consider adding this topic soon.`,
    );
    setTopicSuggestion("");
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
        <div className="max-w-3xl mx-auto mb-12 text-center">
          <p className="text-lg text-slate-600 mb-8">{description}</p>

          {/* Search bar */}
          <div className="relative max-w-md mx-auto mb-6">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-5 w-5" />
            <Input
              type="text"
              placeholder="Search topics by name or category..."
              className="pl-10 py-6 text-base"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          {/* Category tags */}
          <div className="flex flex-wrap justify-center gap-2 mb-8">
            {categories.map((category) => {
              const isSelected = selectedCategories.includes(category);
              return (
                <Badge
                  key={category}
                  variant={isSelected ? "default" : "outline"}
                  className={`cursor-pointer px-4 py-1 text-sm ${
                    isSelected ? "bg-primary hover:bg-primary" : "hover:bg-primary/10"
                  }`}
                  onClick={() => toggleCategory(category)}
                >
                  {category}
                  {isSelected && (
                    <X className="ml-1 h-3 w-3 inline-block" />
                  )}
                </Badge>
              );
            })}
          </div>
        </div>

        {/* Topics grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-16">
          {filteredTopics.length > 0 ? (
            filteredTopics.map((topic) => (
              <div
                key={topic.id}
                className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300"
              >
                <div className="h-48 overflow-hidden">
                  <video
                    src={topic.videoUrl}
                    controls
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-6">
                  <div className="text-sm font-medium text-primary mb-1">
                    {topic.category}
                  </div>
                  <h3 className="text-xl font-bold mb-2">{topic.title}</h3>
                  <p className="text-slate-600 mb-4">{topic.description}</p>
                  <Button
                    className="w-full"
                    onClick={() => window.open(topic.videoUrl, "_blank")}
                  >
                    Watch Full Video
                  </Button>
                </div>
              </div>
            ))
          ) : (
            <div className="col-span-full text-center py-12">
              <p className="text-lg text-slate-600 mb-4">
                No topics found matching "{searchQuery}"
                {selectedCategories.length > 0 && ` in selected categories`}
              </p>
              <Button 
                variant="outline" 
                onClick={() => {
                  setSearchQuery("");
                  setSelectedCategories([]);
                }}
              >
                Clear Filters
              </Button>
            </div>
          )}
        </div>

        {/* Topic suggestion section */}
        <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-md p-8 mb-12">
          <h2 className="text-2xl font-bold mb-4 text-center">
            Can't find what you're looking for?
          </h2>
          <p className="text-slate-600 mb-6 text-center">
            Suggest a mathematical topic or concept you'd like to see
            visualized, and we'll consider adding it to our library.
          </p>
          <form onSubmit={handleSubmitSuggestion} className="space-y-4">
            <Input
              type="text"
              placeholder="Suggest a topic (e.g., 'Fourier Transforms')"
              value={topicSuggestion}
              onChange={(e) => setTopicSuggestion(e.target.value)}
              required
              className="py-6 text-base"
            />
            <Button
              type="submit"
              className="w-full py-6"
              disabled={!topicSuggestion.trim()}
            >
              Submit Suggestion
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default TopicDirectory;
