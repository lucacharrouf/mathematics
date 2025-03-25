import React from "react";
import TopicCard from "./TopicCard";

interface Topic {
  id: string;
  title: string;
  description: string;
  imageUrl: string;
  isAvailable: boolean;
}

interface TopicShowcaseProps {
  topics?: Topic[];
  onTopicClick?: (topicId: string) => void;
}

const TopicShowcase = ({
  topics = [
    {
      id: "linear-algebra",
      title: "Linear Algebra",
      description:
        "Visualize vectors, matrices, and transformations in interactive 3D space.",
      imageUrl:
        "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&q=80",
      isAvailable: true,
    },
    {
      id: "calculus",
      title: "Calculus",
      description:
        "Explore derivatives, integrals, and limits through dynamic visualizations.",
      imageUrl:
        "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=800&q=80",
      isAvailable: false,
    },
    {
      id: "probability",
      title: "Probability",
      description:
        "Understand distributions, random variables, and statistical concepts visually.",
      imageUrl:
        "https://images.unsplash.com/photo-1518133910546-b6c2fb7d79e3?w=800&q=80",
      isAvailable: false,
    },
    {
      id: "machine-learning",
      title: "Machine Learning",
      description:
        "See how algorithms learn from data with interactive visualizations of key ML concepts.",
      imageUrl:
        "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=800&q=80",
      isAvailable: false,
    },
  ],
  onTopicClick = (topicId: string) => console.log(`Topic clicked: ${topicId}`),
}: TopicShowcaseProps) => {
  return (
    <section className="py-16 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">Mathematical Topics</h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Explore our growing library of interactive mathematical
            visualizations designed to make complex concepts intuitive and
            engaging.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 justify-items-center">
          {topics.map((topic) => (
            <TopicCard
              key={topic.id}
              title={topic.title}
              description={topic.description}
              imageUrl={topic.imageUrl}
              isAvailable={topic.isAvailable}
              onClick={() => onTopicClick(topic.id)}
            />
          ))}
        </div>

        <div className="mt-12 text-center">
          <p className="text-gray-500 italic">
            More topics are being added regularly. Sign up to get notified when
            new topics are available.
          </p>
        </div>
      </div>
    </section>
  );
};

export default TopicShowcase;
