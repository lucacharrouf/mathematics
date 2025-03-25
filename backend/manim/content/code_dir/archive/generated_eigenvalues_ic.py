from manim import *

class EigenvaluesScene(Scene):
    def construct(self):
        # Part 1: Introduction
        title = MathTex(r"\text{Eigenvalues \& Eigenvectors}").scale(1.2)
        title.move_to(UP * 0.5)
        
        definition = MathTex(r"\text{When } A\vec{v} = \lambda\vec{v}").next_to(title, DOWN, buff=0.5)
        
        explanation = Text("A vector that only changes in scale, not direction", font_size=30)
        explanation.next_to(definition, DOWN, buff=0.5)
        
        # Animate Introduction
        self.play(FadeIn(title, duration=1.5))
        self.play(FadeIn(definition, duration=1.5))
        self.play(FadeIn(explanation, duration=2))
        
        # Part 2: Visual Demonstration
        self.play(FadeOut(title), FadeOut(definition), FadeOut(explanation))
        
        # Setup coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            axis_config={"include_tip": True, "color": BLUE},
        ).scale(0.8)
        
        grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        ).scale(0.8)
        
        # Display matrix
        matrix_A = MathTex(r"A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}").scale(0.9)
        matrix_A.to_corner(UL, buff=0.5)
        
        # First eigenvector
        eigenvector1 = Vector([1, 1], color=RED)
        eigenvector1_label = MathTex(r"\vec{v}_1 = \begin{bmatrix} 1 \\ 1 \end{bmatrix}", color=RED).scale(0.7)
        eigenvector1_label.next_to(eigenvector1.get_end(), UR, buff=0.2)
        
        # Transformed first eigenvector
        eigenvector1_transformed = Vector([3, 3], color=RED)
        
        # Second eigenvector
        eigenvector2 = Vector([1, -1], color=BLUE)
        eigenvector2_label = MathTex(r"\vec{v}_2 = \begin{bmatrix} 1 \\ -1 \end{bmatrix}", color=BLUE).scale(0.7)
        eigenvector2_label.next_to(eigenvector2.get_end(), DR, buff=0.2)
        
        # Transformed second eigenvector (same direction, eigenvalue = 1)
        eigenvector2_transformed = Vector([1, -1], color=BLUE)
        
        # Eigenvalue labels
        lambda1_label = MathTex(r"\lambda_1 = 3", color=RED).scale(0.9)
        lambda1_label.to_corner(UR, buff=0.5)
        
        lambda2_label = MathTex(r"\lambda_2 = 1", color=BLUE).scale(0.9)
        lambda2_label.next_to(lambda1_label, DOWN, buff=0.3)
        
        # Animation sequence
        self.play(
            Create(grid, lag_ratio=0.1, run_time=1),
            Create(axes, lag_ratio=0.1, run_time=1)
        )
        self.play(Write(matrix_A, run_time=1))
        
        # Draw first eigenvector
        self.play(GrowArrow(eigenvector1), FadeIn(eigenvector1_label), run_time=1)
        
        # Show transformation of first eigenvector
        self.play(
            Transform(eigenvector1, eigenvector1_transformed, rate_func=rate_functions.smooth, run_time=2),
            FadeIn(lambda1_label, run_time=1)
        )
        self.wait(1)
        
        # Draw second eigenvector
        self.play(GrowArrow(eigenvector2), FadeIn(eigenvector2_label), run_time=1)
        
        # Show transformation of second eigenvector (no visual change in length, just emphasize)
        self.play(
            Indicate(eigenvector2, color=YELLOW, scale_factor=1.1, run_time=2),
            FadeIn(lambda2_label, run_time=1)
        )
        
        # Final pause to observe the complete visualization
        self.wait(1)