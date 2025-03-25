import React from "react";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

interface TopicCardProps {
  title: string;
  description: string;
  imageUrl: string;
  isAvailable: boolean;
  onClick?: () => void;
}

const TopicCard = ({
  title = "Linear Algebra",
  description = "Visualize vectors, matrices, and transformations in interactive 3D space.",
  imageUrl = "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&q=80",
  isAvailable = true,
  onClick = () => console.log("Topic card clicked"),
}: TopicCardProps) => {
  return (
    <Card className="w-full max-w-[320px] overflow-hidden transition-all duration-300 hover:shadow-lg bg-white">
      <div className="relative h-48 overflow-hidden">
        <img
          src={imageUrl}
          alt={`${title} visualization preview`}
          className="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
        />
        <div className="absolute top-2 right-2">
          <Badge
            variant={isAvailable ? "default" : "secondary"}
            className={isAvailable ? "bg-green-500" : "bg-amber-500"}
          >
            {isAvailable ? "Available" : "Coming Soon"}
          </Badge>
        </div>
      </div>

      <CardHeader className="pb-2">
        <h3 className="text-xl font-bold">{title}</h3>
      </CardHeader>

      <CardContent>
        <p className="text-sm text-gray-600">{description}</p>
      </CardContent>

      <CardFooter>
        <Button
          onClick={
            isAvailable ? () => (window.location.href = "/topics") : onClick
          }
          variant={isAvailable ? "default" : "outline"}
          className="w-full"
          disabled={!isAvailable}
        >
          {isAvailable ? "Explore Topic" : "Get Notified"}
        </Button>
      </CardFooter>
    </Card>
  );
};

export default TopicCard;
