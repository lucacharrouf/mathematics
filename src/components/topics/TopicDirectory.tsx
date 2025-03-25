import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Search } from "lucide-react";

interface TopicDirectoryProps {
  title?: string;
  description?: string;
}

interface Topic {
  id: string;
  title: string;
  description: string;
  imageUrl: string;
  videoUrl?: string;
  category: string;
  hasVideo?: boolean;
}

const TopicDirectory: React.FC<TopicDirectoryProps> = ({
  title = "Mathematics Visualization Library",
  description = "Explore our collection of interactive visualizations to help you understand complex mathematical concepts.",
}) => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [topicSuggestion, setTopicSuggestion] = useState("");

  // Sample topics - these would come from your database in a real app
  const topics: Topic[] = [
    {
      id: "linear-algebra-vectors",
      title: "Vector Operations",
      description:
        "Visualize vector addition, subtraction, and scalar multiplication in 2D and 3D space.",
      imageUrl:
        "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&q=80",
      videoUrl: "/src/videos/vector_addition_animation.mp4",
      category: "Linear Algebra",
      hasVideo: true,
    },
    {
      id: "linear-algebra-orthogonality",
      title: "Orthogonality & Projections",
      description:
        "Learn about orthogonal vectors, projections, and their applications in linear algebra.",
      imageUrl:
        "https://images.unsplash.com/photo-1580894908361-967195033215?w=800&q=80",
      videoUrl: "/src/videos/orthogonality_animation.mp4",
      category: "Linear Algebra",
      hasVideo: true,
    },
  ];

  const filteredTopics = topics.filter(
    (topic) =>
      topic.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      topic.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      topic.category.toLowerCase().includes(searchQuery.toLowerCase()),
  );

  const handleSubmitSuggestion = (e: React.FormEvent) => {
    e.preventDefault();
    // In a real app, you would send this to your backend
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
          <div className="relative max-w-md mx-auto">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 h-5 w-5" />
            <Input
              type="text"
              placeholder="Search topics by name or category..."
              className="pl-10 py-6 text-base"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
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
                  {topic.hasVideo ? (
                    <video
                      src={topic.videoUrl}
                      controls
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <img
                      src={topic.imageUrl}
                      alt={topic.title}
                      className="w-full h-full object-cover"
                    />
                  )}
                </div>
                <div className="p-6">
                  <div className="text-sm font-medium text-indigo-600 mb-1">
                    {topic.category}
                  </div>
                  <h3 className="text-xl font-bold mb-2">{topic.title}</h3>
                  <p className="text-slate-600 mb-4">{topic.description}</p>
                  <Button
                    className="w-full"
                    onClick={() => {
                      if (topic.videoUrl) {
                        // Open the video in a new tab or modal
                        window.open(topic.videoUrl, "_blank");
                      } else {
                        // In a real app, this would navigate to the specific topic page
                        alert("Video content will be added later");
                      }
                    }}
                  >
                    {topic.hasVideo
                      ? "Watch Full Video"
                      : "Watch Visualization"}
                  </Button>
                </div>
              </div>
            ))
          ) : (
            <div className="col-span-full text-center py-12">
              <p className="text-lg text-slate-600 mb-4">
                No topics found matching "{searchQuery}"
              </p>
              <Button variant="outline" onClick={() => setSearchQuery("")}>
                Clear Search
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
