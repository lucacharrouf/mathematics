from manim import *
import numpy as np

class EigenvaluesScene(Scene):
    def construct(self):
        # [00:00-00:03] Introduction
        title = Text("Understanding Eigenvalues", font_size=48)
        title.to_edge(UP, buff=0.5)
        
        subtitle = Text("Visualizing Linear Transformations", font_size=36)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(1)
        
        # [00:04-00:10] Setup and Initial Grid
        # Fade the title and subtitle slightly
        self.play(
            title.animate.set_opacity(0.7),
            subtitle.animate.set_opacity(0.7)
        )
        
        # Create a coordinate grid
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 2,
                "stroke_opacity": 0.6
            }
        )
        grid.move_to(ORIGIN)
        
        x_label = Text("x", font_size=24).next_to(grid.c2p(5.2, 0), RIGHT)
        y_label = Text("y", font_size=24).next_to(grid.c2p(0, 5.2), UP)
        
        initial_text = Text("When a matrix transforms a vector space...", font_size=32)
        initial_text.to_edge(DOWN, buff=0.5)
        initial_text_bg = SurroundingRectangle(
            initial_text,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(
            Create(grid),
            FadeIn(x_label),
            FadeIn(y_label)
        )
        self.play(FadeIn(initial_text_bg), Write(initial_text))
        self.wait(1)
        
        # [00:11-00:15] Introducing Example Matrix and Eigenvectors
        matrix_text = Text("Matrix A = [[3, 1], [1, 3]] has eigenvectors v₁ and v₂", font_size=32)
        matrix_text.to_edge(DOWN, buff=0.5)
        matrix_text_bg = SurroundingRectangle(
            matrix_text,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Create eigenvectors
        v1 = Arrow(
            start=grid.c2p(0, 0),
            end=grid.c2p(1, 1),
            buff=0,
            color=RED
        )
        v1_label = MathTex(r"v_1", color=RED, font_size=36)
        v1_label.next_to(grid.c2p(1.2, 1.2), direction=UR, buff=0.1)
        
        v2 = Arrow(
            start=grid.c2p(0, 0),
            end=grid.c2p(1, -1),
            buff=0,
            color=BLUE
        )
        v2_label = MathTex(r"v_2", color=BLUE, font_size=36)
        v2_label.next_to(grid.c2p(1.2, -1.2), direction=DR, buff=0.1)
        
        self.play(
            FadeOut(initial_text_bg),
            FadeOut(initial_text)
        )
        self.play(
            FadeIn(matrix_text_bg),
            Write(matrix_text)
        )
        self.play(
            Create(v1),
            Create(v2)
        )
        self.play(
            FadeIn(v1_label),
            FadeIn(v2_label)
        )
        self.wait(1)
        
        # [00:16-00:20] Demonstrating Transformation with first eigenvector
        transform_text1 = Text("When A transforms v₁, it scales it by λ₁ = 4", font_size=32)
        transform_text1.to_edge(DOWN, buff=0.5)
        transform_text1_bg = SurroundingRectangle(
            transform_text1,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Define the transformation matrix
        matrix = [[3, 1], [1, 3]]
        
        # Create the transformed v1
        v1_transformed = Arrow(
            start=grid.c2p(0, 0),
            end=grid.c2p(4, 4),  # Scaled by eigenvalue λ₁ = 4
            buff=0,
            color=RED
        )
        
        eq1 = MathTex(r"A\vec{v}_1 = 4\vec{v}_1", font_size=32, color=RED)
        eq1.move_to(grid.c2p(2, 2))
        eq1_bg = SurroundingRectangle(
            eq1,
            fill_color=BLACK,
            fill_opacity=0.7,
            buff=0.1,
            color=RED_A
        )
        
        # Apply the transformation to the grid
        matrix_mob = np.array(matrix)
        self.play(
            FadeOut(matrix_text_bg),
            FadeOut(matrix_text)
        )
        self.play(
            FadeIn(transform_text1_bg),
            Write(transform_text1)
        )
        
        # Transform the grid and v1
        self.play(
            grid.animate.apply_matrix(matrix_mob),
            Transform(v1, v1_transformed)
        )
        self.play(FadeIn(eq1_bg), Write(eq1))
        self.wait(1)
        
        # [00:21-00:25] Second Eigenvalue Demonstration
        transform_text2 = Text("When A transforms v₂, it scales it by λ₂ = 2", font_size=32)
        transform_text2.to_edge(DOWN, buff=0.5)
        transform_text2_bg = SurroundingRectangle(
            transform_text2,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Create the transformed v2
        v2_transformed = Arrow(
            start=grid.c2p(0, 0),
            end=grid.c2p(2, -2),  # Scaled by eigenvalue λ₂ = 2
            buff=0,
            color=BLUE
        )
        
        eq2 = MathTex(r"A\vec{v}_2 = 2\vec{v}_2", font_size=32, color=BLUE)
        eq2.move_to(grid.c2p(2, -2))
        eq2_bg = SurroundingRectangle(
            eq2,
            fill_color=BLACK,
            fill_opacity=0.7,
            buff=0.1,
            color=BLUE_A
        )
        
        self.play(
            FadeOut(transform_text1_bg),
            FadeOut(transform_text1)
        )
        self.play(
            FadeIn(transform_text2_bg),
            Write(transform_text2)
        )
        
        # Transform v2
        self.play(Transform(v2, v2_transformed))
        self.play(FadeIn(eq2_bg), Write(eq2))
        self.wait(1)
        
        # [00:26-00:30] Conclusion
        conclusion_text = Text("Eigenvalues (λ) tell us the scaling factor along eigenvectors", font_size=32)
        conclusion_text.to_edge(DOWN, buff=0.5)
        conclusion_text_bg = SurroundingRectangle(
            conclusion_text,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        final_formula = MathTex(r"A\vec{v} = \lambda\vec{v} \text{ where } \vec{v} \text{ is an eigenvector}", font_size=40)
        final_formula.move_to(ORIGIN)
        final_formula_bg = SurroundingRectangle(
            final_formula,
            fill_color=BLACK,
            fill_opacity=0.7,
            buff=0.2,
            color=YELLOW
        )
        
        # Fade grid and vectors slightly
        self.play(
            grid.animate.set_opacity(0.5),
            v1.animate.set_opacity(0.5),
            v2.animate.set_opacity(0.5),
            v1_label.animate.set_opacity(0.5),
            v2_label.animate.set_opacity(0.5),
            eq1.animate.set_opacity(0.5),
            eq2.animate.set_opacity(0.5),
            eq1_bg.animate.set_opacity(0.5),
            eq2_bg.animate.set_opacity(0.5)
        )
        
        self.play(
            FadeOut(transform_text2_bg),
            FadeOut(transform_text2)
        )
        self.play(
            FadeIn(conclusion_text_bg),
            Write(conclusion_text)
        )
        self.play(FadeIn(final_formula_bg), Write(final_formula))
        self.wait(2)