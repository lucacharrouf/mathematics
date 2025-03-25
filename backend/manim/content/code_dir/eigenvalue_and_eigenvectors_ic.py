from manim import *

class EigenvalueAndEigenvectorsScene(Scene):

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

        # [00:00-00:05] Introduction
        title = Text("Eigenvalues and Eigenvectors", font_size=44)
        title.to_edge(UP, buff=0.5)
        
        subtitle = Text("Linear transformations that preserve direction", font_size=32)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Create coordinate system
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            axis_config={"include_tip": True, "numbers_to_include": range(-3, 4)}
        )
        axes.move_to(ORIGIN)
        
        # Create grid
        grid = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            background_line_style={
                "stroke_color": BLUE_E,
                "stroke_width": 1,
                "stroke_opacity": 0.5
            }
        )
        grid.move_to(ORIGIN)
        
        x_label = Text("x", font_size=24).next_to(axes.x_axis.get_end(), RIGHT, buff=0.2)
        y_label = Text("y", font_size=24).next_to(axes.y_axis.get_end(), UP, buff=0.2)
        
        # Play animations for introduction
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(0.5)
        self.play(
            Create(grid),
            Create(axes),
            Write(x_label),
            Write(y_label)
        )
        self.wait(1)
        
        # [00:05-00:10] Eigenvector Concept Introduction
        explanation_box = Text(
            "An eigenvector maintains its direction when transformed by a matrix", 
            font_size=30
        )
        explanation_box.to_edge(DOWN, buff=0.7)
        explanation_bg = SurroundingRectangle(
            explanation_box, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Define the matrix A
        matrix_A = Matrix([
            [2, 1],
            [1, 2]
        ], h_buff=1.8)
        matrix_A.scale(0.8)
        matrix_A.move_to([-5, 1, 0])
        
        matrix_A_label = MathTex("A = ", font_size=36)
        matrix_A_label.next_to(matrix_A, LEFT, buff=0.3)
        
        # Define the first eigenvector
        vector_v1 = Arrow(
            start=ORIGIN, 
            end=[1, 1, 0], 
            buff=0, 
            color=RED,
            stroke_width=4
        )
        
        vector_v1_label = MathTex(r"v_1 = \begin{bmatrix} 1 \\ 1 \end{bmatrix}", font_size=30)
        vector_v1_label.next_to(vector_v1.get_end(), UP+RIGHT, buff=0.3)
        
        # Play animations for first eigenvector
        self.play(
            FadeIn(explanation_bg),
            Write(explanation_box)
        )
        self.wait(1)
        
        self.play(
            Write(matrix_A_label),
            Write(matrix_A)
        )
        self.wait(1)
        
        self.play(
            Create(vector_v1),
            Write(vector_v1_label)
        )
        self.wait(1)
        
        # [00:10-00:15] Transformation Visualization
        # Transform the vector
        transformed_v1 = Arrow(
            start=ORIGIN, 
            end=[3, 3, 0], 
            buff=0, 
            color=RED,
            stroke_width=4
        )
        
        transformed_v1_label = MathTex(r"A v_1", font_size=30)
        transformed_v1_label.next_to(transformed_v1.get_end(), UP+RIGHT, buff=0.3)
        
        vector_v1_copy = vector_v1.copy()
        vector_v1_label_copy = vector_v1_label.copy()
        
        # Update explanation
        new_explanation = Text(
            "Av₁ = 3v₁, where λ = 3 is the eigenvalue", 
            font_size=30
        )
        new_explanation.to_edge(DOWN, buff=0.7)
        new_explanation_bg = SurroundingRectangle(
            new_explanation, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Equation
        eigenvalue_eq = MathTex(r"A \cdot v_1 = \lambda \cdot v_1", font_size=36)
        eigenvalue_eq.move_to([4, 1, 0])
        
        # Animation for transformation
        self.play(
            Transform(vector_v1_copy, transformed_v1),
            Transform(vector_v1_label_copy, transformed_v1_label)
        )
        self.wait(0.5)
        
        self.play(
            FadeOut(explanation_bg),
            FadeOut(explanation_box),
            FadeIn(new_explanation_bg),
            Write(new_explanation),
            Write(eigenvalue_eq)
        )
        self.wait(1)
        
        # [00:15-00:20] Second Eigenvector Example
        vector_v2 = Arrow(
            start=ORIGIN, 
            end=[1, -1, 0], 
            buff=0, 
            color=BLUE,
            stroke_width=4
        )
        
        vector_v2_label = MathTex(r"v_2 = \begin{bmatrix} 1 \\ -1 \end{bmatrix}", font_size=30)
        vector_v2_label.next_to(vector_v2.get_end(), DOWN+RIGHT, buff=0.3)
        
        self.play(
            Create(vector_v2),
            Write(vector_v2_label)
        )
        self.wait(1)
        
        # Transform the second vector
        transformed_v2 = Arrow(
            start=ORIGIN, 
            end=[1, -1, 0], 
            buff=0, 
            color=BLUE,
            stroke_width=4,
            max_stroke_width_to_length_ratio=10,
            max_tip_length_to_length_ratio=0.5
        )
        
        transformed_v2_label = MathTex(r"A v_2", font_size=30)
        transformed_v2_label.next_to(transformed_v2.get_end(), DOWN+RIGHT, buff=0.3)
        
        vector_v2_copy = vector_v2.copy()
        vector_v2_label_copy = vector_v2_label.copy()
        
        # Update explanation for second eigenvector
        final_explanation = Text(
            "Av₂ = 1v₂, where λ = 1 is the eigenvalue", 
            font_size=30
        )
        final_explanation.to_edge(DOWN, buff=0.7)
        final_explanation_bg = SurroundingRectangle(
            final_explanation, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(
            Transform(vector_v2_copy, transformed_v2),
            Transform(vector_v2_label_copy, transformed_v2_label)
        )
        self.wait(0.5)
        
        self.play(
            FadeOut(new_explanation_bg),
            FadeOut(new_explanation),
            FadeIn(final_explanation_bg),
            Write(final_explanation)
        )
        self.wait(1)
        
        # [00:20-00:25] Visual Summary
        # Create a non-eigenvector that changes direction
        non_eigen_vector = Arrow(
            start=ORIGIN, 
            end=[2, 0, 0], 
            buff=0, 
            color=GREEN,
            stroke_width=4
        )
        
        non_eigen_vector_label = MathTex(r"u = \begin{bmatrix} 2 \\ 0 \end{bmatrix}", font_size=30)
        non_eigen_vector_label.next_to(non_eigen_vector.get_end(), DOWN, buff=0.3)
        
        # Transform the non-eigenvector (changes direction)
        transformed_non_eigen = Arrow(
            start=ORIGIN, 
            end=[4, 2, 0], 
            buff=0, 
            color=GREEN,
            stroke_width=4
        )
        
        transformed_non_eigen_label = MathTex(r"Au", font_size=30)
        transformed_non_eigen_label.next_to(transformed_non_eigen.get_end(), UP, buff=0.3)
        
        summary_1 = Text(
            "Eigenvectors maintain their direction under transformation", 
            font_size=30
        )
        summary_1.to_edge(DOWN, buff=1.2)
        
        summary_2 = Text(
            "Each eigenvector has an associated eigenvalue (λ) that determines scaling", 
            font_size=28
        )
        summary_2.next_to(summary_1, DOWN, buff=0.4)
        
        summary_bg = SurroundingRectangle(
            VGroup(summary_1, summary_2), 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(
            FadeOut(final_explanation_bg),
            FadeOut(final_explanation),
            FadeIn(summary_bg),
            Write(summary_1),
            Write(summary_2)
        )
        self.wait(0.5)
        
        # Add a non-eigenvector that changes direction
        self.play(
            Create(non_eigen_vector),
            Write(non_eigen_vector_label)
        )
        self.wait(0.5)
        
        non_eigen_copy = non_eigen_vector.copy()
        non_eigen_label_copy = non_eigen_vector_label.copy()
        
        self.play(
            Transform(non_eigen_copy, transformed_non_eigen),
            Transform(non_eigen_label_copy, transformed_non_eigen_label)
        )
        self.wait(1)
        
        # Highlight eigenvectors one more time
        self.play(
            Indicate(vector_v1, scale_factor=1.2),
            Indicate(vector_v1_copy, scale_factor=1.2),
            Indicate(vector_v2, scale_factor=1.2),
            Indicate(vector_v2_copy, scale_factor=1.2),
        )
        self.wait(1)
        
        # [00:25-00:30] Conclusion
        conclusion_title = Text("Key Takeaway", font_size=44)
        conclusion_title.to_edge(UP, buff=0.5)
        
        conclusion_text = Text(
            "For an n×n matrix, we solve det(A-λI) = 0 to find eigenvalues", 
            font_size=32
        )
        conclusion_text.to_edge(DOWN, buff=1.0)
        conclusion_bg = SurroundingRectangle(
            conclusion_text, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        final_equation = MathTex(r"A \cdot v = \lambda \cdot v", font_size=48)
        final_equation.move_to(ORIGIN)
        
        self.play(
            FadeOut(summary_bg),
            FadeOut(summary_1),
            FadeOut(summary_2),
            FadeOut(vector_v1),
            FadeOut(vector_v1_copy),
            FadeOut(vector_v1_label),
            FadeOut(vector_v1_label_copy),
            FadeOut(vector_v2),
            FadeOut(vector_v2_copy),
            FadeOut(vector_v2_label),
            FadeOut(vector_v2_label_copy),
            FadeOut(non_eigen_vector),
            FadeOut(non_eigen_copy),
            FadeOut(non_eigen_vector_label),
            FadeOut(non_eigen_label_copy),
            FadeOut(matrix_A),
            FadeOut(matrix_A_label),
            FadeOut(eigenvalue_eq),
            FadeTransform(title, conclusion_title)
        )
        self.wait(0.5)
        
        self.play(
            Write(final_equation),
            FadeIn(conclusion_bg),
            Write(conclusion_text)
        )
        self.wait(2)
        
        # Final fade out
        self.play(
            FadeOut(conclusion_title),
            FadeOut(final_equation),
            FadeOut(conclusion_bg),
            FadeOut(conclusion_text),
            FadeOut(grid),
            FadeOut(axes),
            FadeOut(x_label),
            FadeOut(y_label)
        )
        self.wait(1)