from manim import *

class EigenvaluesScene(Scene):

    def safe_position(self, mobject, zone="MIDDLE", buff=0.5):
        """Ensure mobject stays within screen boundaries."""
        # Get frame boundaries (adjust if camera.frame_width was changed)
        frame_width = getattr(self.camera, "frame_width", 14)
        frame_height = getattr(self.camera, "frame_height", 8)
        max_x = frame_width/2 - buff
        max_y = frame_height/2 - buff
        
        # Set position based on zone
        if zone == "TOP":
            mobject.to_edge(UP, buff=buff)
            # Limit y position
            if mobject.get_top()[1] > max_y:
                mobject.shift(DOWN * (mobject.get_top()[1] - max_y))
        elif zone == "BOTTOM":
            mobject.to_edge(DOWN, buff=buff)
            # Limit y position
            if mobject.get_bottom()[1] < -max_y:
                mobject.shift(UP * (-max_y - mobject.get_bottom()[1]))
        else:  # MIDDLE zone or anything else
            # Only adjust if outside boundaries
            if mobject.get_center()[1] > max_y - mobject.height/2:
                mobject.align_to(UP * (max_y - mobject.height/2), UP)
            if mobject.get_center()[1] < -max_y + mobject.height/2:
                mobject.align_to(DOWN * (max_y - mobject.height/2), DOWN)
        
        # Check width and scale down if needed
        if mobject.width > frame_width - 2*buff:
            scale_factor = (frame_width - 2*buff) / mobject.width
            mobject.scale(scale_factor)
        
        # Check horizontal boundaries
        if mobject.get_right()[0] > max_x:
            mobject.shift(LEFT * (mobject.get_right()[0] - max_x))
        if mobject.get_left()[0] < -max_x:
            mobject.shift(RIGHT * (-max_x - mobject.get_left()[0]))
        
        return mobject
    def construct(self):
        # Set frame dimensions for consistent boundaries
        self.camera.frame_width = 14
        self.camera.frame_height = 8

        # [00:00-00:03] Introduction
        title = MathTex(r"\text{Eigenvalues and Eigenvectors}", font_size=48)
        title.to_edge(UP, buff=0.5)
        
        subtitle = MathTex(r"\text{When } A\vec{v} = \lambda\vec{v}", font_size=36)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(subtitle))
        self.wait(1)
        
        # [00:04-00:10] Setup and Definition
        explanation = Text("An eigenvector v is a non-zero vector whose direction\nis preserved under a linear transformation", 
                          font_size=28, line_spacing=0.5)
        explanation.to_edge(DOWN, buff=0.5)
        explanation_bg = SurroundingRectangle(
            explanation,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Create coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=4,
            axis_config={"include_tip": False, "numbers_to_exclude": [0]},
        )
        axes.move_to(ORIGIN)
        
        # Define basis vectors
        e1 = Arrow(axes.c2p(0, 0), axes.c2p(1, 0), buff=0, color=RED)
        e2 = Arrow(axes.c2p(0, 0), axes.c2p(0, 1), buff=0, color=BLUE)
        
        e1_label = MathTex(r"\vec{e}_1", font_size=24, color=RED)
        e1_label.next_to(e1, DOWN, buff=0.1)
        
        e2_label = MathTex(r"\vec{e}_2", font_size=24, color=BLUE)
        e2_label.next_to(e2, RIGHT, buff=0.1)
        
        # Play animations
        self.play(
            FadeIn(explanation_bg),
            Write(explanation)
        )
        self.wait(1)
        self.play(Create(axes))
        self.play(
            Create(e1),
            Create(e2),
            Write(e1_label),
            Write(e2_label)
        )
        self.wait(2)
        
        # [00:11-00:15] Matrix Transformation
        matrix_A = MathTex(r"A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}", font_size=36)
        matrix_A.to_corner(UL, buff=1)
        
        new_explanation = Text("For matrix A, we seek vectors v where Av = λv", font_size=28)
        new_explanation.move_to(explanation.get_center())
        
        self.play(
            FadeIn(matrix_A),
            FadeOut(explanation),
            FadeIn(new_explanation)
        )
        self.wait(1)
        
        # Grid for visualization
        grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-2, 2, 1],
            x_length=8,
            y_length=4,
            background_line_style={
                "stroke_color": WHITE,
                "stroke_width": 1,
                "stroke_opacity": 0.3
            }
        )
        grid.move_to(ORIGIN)
        
        # Transform the basis vectors according to the matrix A
        e1_transformed = Arrow(
            axes.c2p(0, 0), 
            axes.c2p(2, 1), 
            buff=0, 
            color=RED_E
        )
        e2_transformed = Arrow(
            axes.c2p(0, 0), 
            axes.c2p(1, 2), 
            buff=0, 
            color=BLUE_E
        )
        
        e1_transformed_label = MathTex(r"A\vec{e}_1", font_size=24, color=RED_E)
        e1_transformed_label.next_to(e1_transformed, RIGHT, buff=0.1)
        
        e2_transformed_label = MathTex(r"A\vec{e}_2", font_size=24, color=BLUE_E)
        e2_transformed_label.next_to(e2_transformed, RIGHT, buff=0.1)
        
        self.play(
            FadeIn(grid, rate_func=lambda t: t**2),
            run_time=1.5
        )
        
        # Transformed grid based on matrix A
        matrix = [[2, 1], [1, 2]]
        transformed_grid = grid.copy()
        transformed_grid.apply_matrix(matrix)
        
        self.play(
            Transform(grid, transformed_grid),
            Transform(e1, e1_transformed),
            Transform(e2, e2_transformed),
            Transform(e1_label, e1_transformed_label),
            Transform(e2_label, e2_transformed_label),
            run_time=2
        )
        self.wait(1)
        
        # [00:16-00:20] Eigenvector Visualization
        v1 = Arrow(
            axes.c2p(0, 0), 
            axes.c2p(1, 1), 
            buff=0, 
            color=GREEN
        )
        
        v1_label = MathTex(r"\vec{v}_1 = \begin{bmatrix} 1 \\ 1 \end{bmatrix}", font_size=24, color=GREEN)
        v1_label.next_to(v1, RIGHT, buff=0.1)
        
        v1_transformed = Arrow(
            axes.c2p(0, 0), 
            axes.c2p(3, 3), 
            buff=0, 
            color=GREEN_E
        )
        
        v1_transformed_label = MathTex(r"A\vec{v}_1 = 3\vec{v}_1", font_size=24, color=GREEN_E)
        v1_transformed_label.next_to(v1_transformed, UP, buff=0.1)
        
        eigenvector_explanation = Text("v₁ = [1,1] is an eigenvector with eigenvalue λ₁ = 3", font_size=28)
        eigenvector_explanation.move_to(new_explanation.get_center())
        
        self.play(
            Create(v1),
            Write(v1_label)
        )
        self.wait(1)
        
        self.play(
            FadeOut(new_explanation),
            FadeIn(eigenvector_explanation)
        )
        
        self.play(
            Create(v1_transformed),
            Write(v1_transformed_label)
        )
        
        # Highlight the eigenvector
        highlight = DashedLine(
            axes.c2p(0, 0),
            axes.c2p(3, 3),
            color=YELLOW,
            stroke_width=5,
            dash_length=0.1,
            stroke_opacity=0.7
        )
        
        self.play(
            Create(highlight),
            run_time=1
        )
        self.wait(1)
        self.play(FadeOut(highlight))
        
        # [00:21-00:25] Second Eigenvector
        v2 = Arrow(
            axes.c2p(0, 0), 
            axes.c2p(1, -1), 
            buff=0, 
            color=PURPLE
        )
        
        v2_label = MathTex(r"\vec{v}_2 = \begin{bmatrix} 1 \\ -1 \end{bmatrix}", font_size=24, color=PURPLE)
        v2_label.next_to(v2, RIGHT, buff=0.1)
        
        v2_transformed = Arrow(
            axes.c2p(0, 0), 
            axes.c2p(1, -1), 
            buff=0, 
            color=PURPLE_E
        )
        
        v2_transformed_label = MathTex(r"A\vec{v}_2 = 1\vec{v}_2", font_size=24, color=PURPLE_E)
        v2_transformed_label.next_to(v2_transformed, DOWN, buff=0.1)
        
        eigenvector2_explanation = Text("v₂ = [1,-1] is an eigenvector with eigenvalue λ₂ = 1", font_size=28)
        eigenvector2_explanation.move_to(eigenvector_explanation.get_center())
        
        self.play(
            Create(v2),
            Write(v2_label)
        )
        self.wait(1)
        
        self.play(
            FadeOut(eigenvector_explanation),
            FadeIn(eigenvector2_explanation)
        )
        
        self.play(
            Create(v2_transformed),
            Write(v2_transformed_label)
        )
        
        highlight2 = DashedLine(
            axes.c2p(0, 0),
            axes.c2p(1, -1),
            color=YELLOW,
            stroke_width=5,
            dash_length=0.1,
            stroke_opacity=0.7
        )
        
        self.play(
            Create(highlight2),
            run_time=1
        )
        self.wait(1)
        self.play(FadeOut(highlight2))
        
        # [00:26-00:30] Conclusion
        self.play(
            FadeOut(grid),
            FadeOut(matrix_A),
            FadeOut(e1),
            FadeOut(e2),
            FadeOut(e1_label),
            FadeOut(e2_label),
            FadeOut(v1_label),
            FadeOut(v2_label),
            FadeOut(v1_transformed_label),
            FadeOut(v2_transformed_label),
            FadeOut(eigenvector2_explanation),
        )
        
        eigenvalue_equation = MathTex(r"\det(A-\lambda I) = 0", font_size=36)
        eigenvalue_equation.move_to(axes.c2p(0, 1))
        
        final_explanation = Text("Eigenvalues tell us how eigenvectors are scaled by the transformation", 
                               font_size=28)
        final_explanation.move_to(eigenvector2_explanation.get_center())
        
        self.play(
            Write(eigenvalue_equation),
            FadeIn(final_explanation)
        )
        
        # Show characteristic equation
        char_equation = MathTex(
            r"\det\begin{bmatrix} 2-\lambda & 1 \\ 1 & 2-\lambda \end{bmatrix} = (2-\lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = 0", 
            font_size=30
        )
        char_equation.next_to(eigenvalue_equation, DOWN, buff=0.5)
        
        self.play(Write(char_equation))
        
        # Show solutions
        solutions = MathTex(r"\lambda_1 = 3, \lambda_2 = 1", font_size=32)
        solutions.next_to(char_equation, DOWN, buff=0.3)
        
        self.play(Write(solutions))
        self.wait(2)
        
        # Final fade out
        self.play(
            FadeOut(eigenvalue_equation),
            FadeOut(char_equation),
            FadeOut(solutions),
            FadeOut(final_explanation),
            FadeOut(v1),
            FadeOut(v1_transformed),
            FadeOut(v2),
            FadeOut(v2_transformed),
            FadeOut(axes),
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(explanation_bg)
        )
        self.wait(1)