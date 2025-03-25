import Generate from "@/components/generate/Generate";
import { BrowserRouter } from "react-router-dom";

export default {
  title: "Pages/Generate",
  component: Generate,
  parameters: {
    layout: "fullscreen",
  },
};

export const Default = () => (
  <BrowserRouter>
    <Generate />
  </BrowserRouter>
);
