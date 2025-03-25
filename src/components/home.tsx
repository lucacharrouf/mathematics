import TopicShowcase from "./landing/TopicShowcase.tsx";
import InteractiveDemo from "./landing/InteractiveDemo.tsx";
import FutureFeatures from "./landing/FutureFeatures.tsx";
import Footer from "./landing/Footer.tsx";
import EmailSignup from "./landing/EmailSignup.tsx";
import HeroSection from "./landing/HeroSection.tsx";
import Header from "./landing/Header.tsx";

function Home() {
  return (
    <div className="w-full min-h-screen bg-white">
      <Header />
      <HeroSection />
      <div id="topics" className="pt-16">
        <TopicShowcase />
      </div>
      <div id="demo" className="pt-16">
        <InteractiveDemo />
      </div>
      <div id="features" className="pt-16">
        <FutureFeatures />
      </div>
      <div id="contact" className="pt-16">
        <EmailSignup />
      </div>
      <Footer />
    </div>
  );
}

export default Home;
