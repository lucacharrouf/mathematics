from manim import *

class vectoradditionScene(Scene):
    def construct(self):
        # Setup
        title = Text("Vector Addition", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.5).to_edge(UP))
        
        # Create a coordinate system for our vectors
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=7,
            y_length=7,
            axis_config={"include_tip": True, "numbers_to_exclude": [0]}
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        # Create two vectors to demonstrate vector addition
        vec1 = [2, 3, 0]  # Vector A
        vec2 = [3, 1, 0]  # Vector B
        
        # Calculate the resultant vector (A + B)
        result_vec = [vec1[0] + vec2[0], vec1[1] + vec2[1], 0]
        
        # Create the arrows representing our vectors
        vector_a = Arrow(axes.coords_to_point(0, 0, 0), axes.coords_to_point(vec1[0], vec1[1], 0), 
                        buff=0, color=BLUE, stroke_width=4)
        vector_b = Arrow(axes.coords_to_point(0, 0, 0), axes.coords_to_point(vec2[0], vec2[1], 0), 
                        buff=0, color=RED, stroke_width=4)
        
        # Resultant vector C = A + B
        vector_c = Arrow(axes.coords_to_point(0, 0, 0), axes.coords_to_point(result_vec[0], result_vec[1], 0), 
                        buff=0, color=PURPLE, stroke_width=4)
        
        # Vector labels
        vec_a_label = MathTex("\\vec{a}", color=BLUE).next_to(vector_a.get_center(), UP+RIGHT, buff=0.1)
        vec_b_label = MathTex("\\vec{b}", color=RED).next_to(vector_b.get_center(), DOWN+RIGHT, buff=0.1)
        vec_c_label = MathTex("\\vec{c} = \\vec{a} + \\vec{b}", color=PURPLE).next_to(vector_c.get_center(), RIGHT, buff=0.1)
        
        # Display the coordinate system
        self.play(Create(axes), Write(axes_labels))
        self.wait(1)
        
        # Display the first vector A
        self.play(GrowArrow(vector_a), Write(vec_a_label))
        self.wait(1)
        
        # Display the second vector B
        self.play(GrowArrow(vector_b), Write(vec_b_label))
        self.wait(1)
        
        # Create vector B starting from the tip of vector A (parallelogram method)
        vector_b_shifted = Arrow(
            axes.coords_to_point(vec1[0], vec1[1], 0),
            axes.coords_to_point(result_vec[0], result_vec[1], 0),
            buff=0, color=RED, stroke_width=4
        )
        
        # Create vector A starting from the tip of vector B (completing the parallelogram)
        vector_a_shifted = Arrow(
            axes.coords_to_point(vec2[0], vec2[1], 0),
            axes.coords_to_point(result_vec[0], result_vec[1], 0),
            buff=0, color=BLUE, stroke_width=4
        )
        
        # Show parallelogram method of vector addition
        self.play(GrowArrow(vector_b_shifted))
        self.play(GrowArrow(vector_a_shifted))
        self.wait(1)
        
        # Draw dashed lines to complete the parallelogram
        dashed_line1 = DashedLine(
            axes.coords_to_point(0, 0, 0),
            axes.coords_to_point(result_vec[0], result_vec[1], 0),
            dash_length=0.2
        )
        
        # Show the resultant vector C
        self.play(Create(dashed_line1))
        self.play(GrowArrow(vector_c), Write(vec_c_label))
        self.wait(1)
        
        # Add a mathematical description of vector addition
        formula = MathTex(
            "\\vec{c} &= \\vec{a} + \\vec{b}\\\\",
            f"({result_vec[0]}, {result_vec[1]}) &= ({vec1[0]}, {vec1[1]}) + ({vec2[0]}, {vec2[1]})\\\\",
            f"({result_vec[0]}, {result_vec[1]}) &= ({vec1[0] + vec2[0]}, {vec1[1] + vec2[1]})"
        ).to_edge(DOWN)
        
        self.play(Write(formula))
        self.wait(2)
        
        # Create a note about vector addition properties
        properties = VGroup(
            Text("Vector Addition Properties:", font_size=24),
            Tex("• Commutative: $\\vec{a} + \\vec{b} = \\vec{b} + \\vec{a}$", font_size=20),
            Tex("• Associative: $(\\vec{a} + \\vec{b}) + \\vec{c} = \\vec{a} + (\\vec{b} + \\vec{c})$", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(DL)
        
        self.play(Write(properties))
        self.wait(2)
        
        # Final scene showing both ways to think about vector addition
        summary = Text("Vector addition can be visualized using the parallelogram method", 
                      font_size=24).to_edge(DOWN)
        self.play(FadeOut(formula), FadeIn(summary))
        self.wait(2)