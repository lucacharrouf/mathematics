from manim import *

class EigendecompositionScene(Scene):

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
        title = Text("Eigendecomposition", font_size=48)
        title.to_edge(UP, buff=0.5)
        
        subtitle = Text("Decomposing a matrix into eigenvalues and eigenvectors", font_size=30)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Check width and scale if needed
        if subtitle.width > 12:
            subtitle.scale(12/subtitle.width)
        
        formula = MathTex(r"A = PDP^{-1}", font_size=48)
        formula.move_to(ORIGIN)
        
        explanation_text = Text("A matrix can be decomposed using its eigenvectors and eigenvalues", 
                               font_size=30)
        explanation_text.to_edge(DOWN, buff=0.5)
        if explanation_text.width > 12:
            explanation_text.scale(12/explanation_text.width)
            
        explanation_bg = SurroundingRectangle(
            explanation_text, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(Write(subtitle))
        self.wait(0.5)
        self.play(FadeIn(formula))
        self.play(FadeIn(explanation_bg), Write(explanation_text))
        self.wait(1)
        
        # [00:05-00:10] Matrix Example
        matrix_A = MathTex(r"A = \begin{bmatrix} 4 & 2 \\ 1 & 3 \end{bmatrix}", font_size=44)
        matrix_A.move_to([-2, 0, 0])
        
        explanation_text2 = Text("Let's decompose this 2×2 matrix A", font_size=30)
        explanation_text2.to_edge(DOWN, buff=0.5)
        if explanation_text2.width > 12:
            explanation_text2.scale(12/explanation_text2.width)
            
        explanation_bg2 = SurroundingRectangle(
            explanation_text2, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        eigenvalues = MathTex(r"\lambda_1 = 5, \lambda_2 = 2", font_size=44)
        eigenvalues.move_to([2, 1, 0])
        
        eigenvectors = MathTex(
            r"v_1 = \begin{bmatrix} 2 \\ 1 \end{bmatrix}, v_2 = \begin{bmatrix} 1 \\ -1 \end{bmatrix}", 
            font_size=44
        )
        eigenvectors.move_to([2, -1, 0])
        
        self.play(FadeOut(formula))
        self.play(FadeIn(matrix_A))
        self.play(
            FadeOut(explanation_bg),
            FadeOut(explanation_text),
            FadeIn(explanation_bg2),
            FadeIn(explanation_text2)
        )
        self.wait(2)
        
        self.play(FadeIn(eigenvalues))
        self.play(FadeIn(eigenvectors))
        self.wait(1)
        
        # [00:10-00:20] Decomposition Visualization
        small_matrix_A_group = VGroup(
            Text("Matrix A:", font_size=30),
            MathTex(r"\begin{bmatrix} 4 & 2 \\ 1 & 3 \end{bmatrix}", font_size=38)
        ).arrange(RIGHT, buff=0.2)
        small_matrix_A_group.move_to([0, 1.5, 0])
        
        matrix_P = MathTex(r"P = \begin{bmatrix} 2 & 1 \\ 1 & -1 \end{bmatrix}", font_size=40)
        matrix_P.move_to([-3, 0, 0])
        
        label_P = Text("P: Eigenvector Matrix", font_size=24)
        label_P.next_to(matrix_P, DOWN, buff=0.2)
        if label_P.width > matrix_P.width + 1:
            label_P.scale((matrix_P.width + 1)/label_P.width)
        
        matrix_D = MathTex(r"D = \begin{bmatrix} 5 & 0 \\ 0 & 2 \end{bmatrix}", font_size=40)
        matrix_D.move_to([0, 0, 0])
        
        label_D = Text("D: Diagonal Eigenvalue Matrix", font_size=24)
        label_D.next_to(matrix_D, DOWN, buff=0.2)
        if label_D.width > matrix_D.width + 1:
            label_D.scale((matrix_D.width + 1)/label_D.width)
        
        matrix_P_inv = MathTex(r"P^{-1} = \begin{bmatrix} 1/3 & 1/3 \\ 1/3 & -2/3 \end{bmatrix}", font_size=40)
        matrix_P_inv.move_to([3, 0, 0])
        
        label_P_inv = Text("P⁻¹: Inverse of P", font_size=24)
        label_P_inv.next_to(matrix_P_inv, DOWN, buff=0.2)
        
        explanation_text3 = Text("P contains eigenvectors as columns, D contains eigenvalues on diagonal", 
                                font_size=28)
        explanation_text3.to_edge(DOWN, buff=0.5)
        if explanation_text3.width > 12:
            explanation_text3.scale(12/explanation_text3.width)
            
        explanation_bg3 = SurroundingRectangle(
            explanation_text3, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(
            FadeOut(eigenvalues),
            FadeOut(eigenvectors),
            Transform(matrix_A, small_matrix_A_group)
        )
        self.wait(0.5)
        
        self.play(FadeIn(matrix_P), FadeIn(label_P))
        self.play(FadeIn(matrix_D), FadeIn(label_D))
        self.play(FadeIn(matrix_P_inv), FadeIn(label_P_inv))
        
        self.play(
            FadeOut(explanation_bg2),
            FadeOut(explanation_text2),
            FadeIn(explanation_bg3),
            FadeIn(explanation_text3)
        )
        self.wait(2)
        
        # [00:20-00:25] Verification
        small_P = MathTex(r"P", font_size=44)
        small_D = MathTex(r"D", font_size=44)
        small_P_inv = MathTex(r"P^{-1}", font_size=44)
        
        multiplication1 = MathTex(r"\times", font_size=36)
        multiplication2 = MathTex(r"\times", font_size=36)
        
        verification_group = VGroup(
            small_P, multiplication1, small_D, multiplication2, small_P_inv
        ).arrange(RIGHT, buff=0.3)
        verification_group.move_to([0, 1, 0])
        
        equals_sign = MathTex(r"=", font_size=44)
        result_matrix = MathTex(r"\begin{bmatrix} 4 & 2 \\ 1 & 3 \end{bmatrix}", font_size=44)
        equals_A = MathTex(r"= A", font_size=44)
        
        result_group = VGroup(
            equals_sign, result_matrix, equals_A
        ).arrange(RIGHT, buff=0.3)
        result_group.move_to([0, 0, 0])
        
        explanation_text4 = Text("The product PDP⁻¹ equals our original matrix A, verifying the decomposition", 
                               font_size=28)
        explanation_text4.to_edge(DOWN, buff=0.5)
        if explanation_text4.width > 12:
            explanation_text4.scale(12/explanation_text4.width)
            
        explanation_bg4 = SurroundingRectangle(
            explanation_text4, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(
            FadeOut(label_P),
            FadeOut(label_D),
            FadeOut(label_P_inv),
            FadeOut(matrix_A),
            Transform(matrix_P, small_P),
            Transform(matrix_D, small_D),
            Transform(matrix_P_inv, small_P_inv),
            FadeIn(multiplication1),
            FadeIn(multiplication2)
        )
        self.wait(0.5)
        
        self.play(FadeIn(result_group))
        
        self.play(
            FadeOut(explanation_bg3),
            FadeOut(explanation_text3),
            FadeIn(explanation_bg4),
            FadeIn(explanation_text4)
        )
        self.wait(2)
        
        # [00:25-00:30] Conclusion
        final_formula = MathTex(r"A = PDP^{-1}", font_size=52)
        final_formula.move_to(ORIGIN)
        
        explanation_text5 = Text("Eigendecomposition expresses a matrix in terms of its fundamental components", 
                               font_size=28)
        explanation_text5.to_edge(DOWN, buff=1.0)
        if explanation_text5.width > 12:
            explanation_text5.scale(12/explanation_text5.width)
            
        explanation_bg5 = SurroundingRectangle(
            explanation_text5, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        final_message = Text("Used for diagonalization, computing matrix powers, and solving systems", 
                           font_size=28)
        final_message.next_to(explanation_text5, DOWN, buff=0.3)
        if final_message.width > 12:
            final_message.scale(12/final_message.width)
            
        final_message_bg = SurroundingRectangle(
            final_message, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(
            FadeOut(verification_group),
            FadeOut(result_group),
            FadeOut(matrix_P),
            FadeOut(matrix_D),
            FadeOut(matrix_P_inv),
            FadeOut(multiplication1),
            FadeOut(multiplication2),
            FadeIn(final_formula)
        )
        
        self.play(
            FadeOut(explanation_bg4),
            FadeOut(explanation_text4),
            FadeIn(explanation_bg5),
            FadeIn(explanation_text5)
        )
        
        self.play(
            FadeIn(final_message_bg),
            FadeIn(final_message)
        )
        
        self.wait(2)