import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { createClient } from "@supabase/supabase-js";
import { Mail, CheckCircle, AlertCircle } from "lucide-react";

interface EmailSignupFormProps {
  variant?: "hero" | "footer";
  buttonText?: string;
  placeholder?: string;
}

const EmailSignupForm = ({
  variant = "hero",
  buttonText = "Join Waitlist",
  placeholder = "Enter your email",
}: EmailSignupFormProps) => {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<
    "idle" | "loading" | "success" | "error"
  >("idle");
  const [message, setMessage] = useState("");

  const supabase = createClient(
    import.meta.env.VITE_SUPABASE_URL as string,
    import.meta.env.VITE_SUPABASE_ANON_KEY as string,
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setStatus("error");
      setMessage("Please enter a valid email address");
      return;
    }

    setStatus("loading");

    try {
      const { error } = await supabase
        .from("waitlist")
        .insert([{ email, created_at: new Date().toISOString() }]);

      if (error) {
        if (error.code === "23505") {
          // Unique violation
          setStatus("success");
          setMessage("You're already on our waitlist!");
        } else {
          throw error;
        }
      } else {
        setStatus("success");
        setMessage("Thanks for joining our waitlist!");
        setEmail("");
      }
    } catch (error) {
      console.error("Error adding to waitlist:", error);
      setStatus("error");
      setMessage("Something went wrong. Please try again.");
    }
  };

  const isHero = variant === "hero";
  const isFooter = variant === "footer";

  return (
    <div
      className={`w-full ${isHero ? "max-w-md" : ""} bg-white rounded-lg ${isHero ? "shadow-md" : ""}`}
    >
      <form
        onSubmit={handleSubmit}
        className={`flex flex-col ${isFooter ? "gap-2" : "gap-3"}`}
      >
        <div
          className={`flex ${isFooter ? "flex-col sm:flex-row" : "flex-col"} gap-2`}
        >
          <div className="relative flex-grow">
            <Input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={placeholder}
              className={`${isHero ? "h-12 pl-10" : ""} w-full`}
              disabled={status === "loading"}
            />
            {isHero && (
              <Mail
                className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
                size={18}
              />
            )}
          </div>
          <Button
            type="submit"
            className={`${isHero ? "h-12" : ""} whitespace-nowrap`}
            disabled={status === "loading"}
          >
            {status === "loading" ? "Processing..." : buttonText}
          </Button>
        </div>

        {status !== "idle" && (
          <div
            className={`flex items-center gap-2 text-sm ${status === "success" ? "text-green-600" : "text-red-600"}`}
          >
            {status === "success" ? (
              <CheckCircle size={16} />
            ) : status === "error" ? (
              <AlertCircle size={16} />
            ) : null}
            <span>{message}</span>
          </div>
        )}
      </form>
    </div>
  );
};

export default EmailSignupForm;
