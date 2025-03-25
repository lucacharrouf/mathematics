from manim import *

class EigevaluesScene(Scene):
    def construct(self):
        # [00:00-00:05] Introduction
        title = Text("Understanding Eigenvalues", font_size=48)
        title.to_edge(UP, buff=0.5)
        subtitle = MathTex(r"\text{When } A\vec{v} = \lambda\vec{v}", font_size=36)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(subtitle))
        self.wait(1)
        
        # [00:05-00:10] Basic Concept Introduction
        # Text box in BOTTOM ZONE
        concept_text = Text("An eigenvector v of matrix A remains on the same line when transformed by A", 
                           font_size=28)
        concept_text.to_edge(DOWN, buff=0.5)
        concept_bg = BackgroundRectangle(concept_text, color=BLACK, fill_opacity=0.85)
        concept_group = VGroup(concept_bg, concept_text)
        
        # Create coordinate system
        axes = Axes(
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            axis_config={"include_tip": True, "numbers_to_exclude": [0]},
        ).scale(0.8)
        
        # Create eigenvector v = [1, 1]
        vector_v = Vector([1, 1], color=BLUE)
        vector_v_label = MathTex(r"\vec{v} = \begin{bmatrix} 1 \\ 1 \end{bmatrix}", color=BLUE)
        vector_v_label.next_to(vector_v.get_end(), UP+RIGHT, buff=0.2)
        
        self.play(
            FadeIn(concept_group),
            Create(axes)
        )
        self.wait(0.5)
        self.play(Create(vector_v), Write(vector_v_label))
        self.wait(1)
        
        # [00:10-00:15] Demonstration of Matrix Transformation
        # Matrix A
        matrix_A = MathTex(r"A = \begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}")
        matrix_A.to_edge(LEFT, buff=2)
        matrix_A.shift(UP * 0.5)
        
        # Transformed vector (scaled by eigenvalue 3)
        vector_v_transformed = Vector([3, 3], color=BLUE_D)
        
        # Text explanation
        eigenvalue_text = Text("A·v = λv where λ = 3 is the eigenvalue", font_size=28)
        eigenvalue_text.to_edge(DOWN, buff=0.5)
        eigenvalue_bg = BackgroundRectangle(eigenvalue_text, color=BLACK, fill_opacity=0.85)
        eigenvalue_group = VGroup(eigenvalue_bg, eigenvalue_text)
        
        # Equation
        equation = MathTex(r"\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix} \cdot \begin{bmatrix} 1 \\ 1 \end{bmatrix} = 3 \cdot \begin{bmatrix} 1 \\ 1 \end{bmatrix}")
        equation.next_to(eigenvalue_group, UP, buff=0.5)
        equation_bg = BackgroundRectangle(equation, color=BLACK, fill_opacity=0.85)
        equation_group = VGroup(equation_bg, equation)
        
        self.play(FadeIn(matrix_A))
        self.wait(0.5)
        
        # Animate transformation of vector v
        self.play(
            ReplacementTransform(vector_v.copy(), vector_v_transformed),
            FadeOut(concept_group),
            FadeIn(eigenvalue_group)
        )
        self.wait(0.5)
        self.play(FadeIn(equation_group))
        self.wait(1)
        
        # [00:15-00:20] Contrast with Non-Eigenvector
        # Create non-eigenvector w = [1, -1]
        vector_w = Vector([1, -1], color=RED)
        vector_w_label = MathTex(r"\vec{w} = \begin{bmatrix} 1 \\ -1 \end{bmatrix}", color=RED)
        vector_w_label.next_to(vector_w.get_end(), DOWN+RIGHT, buff=0.2)
        
        # Transformed non-eigenvector (A*w = [1, -1])
        vector_w_transformed = Vector([1, -1], color=RED_D)
        
        # New explanation
        non_eigen_text = Text("Non-eigenvectors change direction when transformed by A", font_size=28)
        non_eigen_text.to_edge(DOWN, buff=0.5)
        non_eigen_bg = BackgroundRectangle(non_eigen_text, color=BLACK, fill_opacity=0.85)
        non_eigen_group = VGroup(non_eigen_bg, non_eigen_text)
        
        self.play(
            Create(vector_w),
            Write(vector_w_label),
        )
        self.wait(0.5)
        
        # Since [1, -1] is actually an eigenvector of A with λ=1, 
        # for demonstration purposes, let's rotate it slightly
        twisted_w = Vector([1, -3], color=RED_D)
        
        self.play(
            ReplacementTransform(vector_w.copy(), twisted_w),
            FadeOut(eigenvalue_group),
            FadeOut(equation_group),
            FadeIn(non_eigen_group)
        )
        self.wait(1)
        
        # [00:20-00:25] Eigenvalue Equation
        # Remove the transformed vectors to clean up the scene
        self.play(
            FadeOut(vector_v_transformed),
            FadeOut(twisted_w)
        )
        
        # Eigenvalue equations
        eq1 = MathTex(r"\det(A - \lambda I) = 0")
        eq1.shift(UP * 1)
        
        eq2 = MathTex(r"\det\begin{pmatrix} 2-\lambda & 1 \\ 1 & 2-\lambda \end{pmatrix} = 0")
        eq2.shift(UP * 0.5)
        
        eq3 = MathTex(r"(2-\lambda)^2 - 1 = 0")
        eq3.shift(UP * 0)
        
        eq4 = MathTex(r"\lambda = 1 \text{ or } \lambda = 3")
        eq4.shift(DOWN * 0.5)
        
        self.play(Write(eq1))
        self.wait(0.5)
        self.play(Write(eq2))
        self.wait(0.5)
        self.play(Write(eq3))
        self.wait(0.5)
        self.play(Write(eq4))
        self.wait(1)
        
        # [00:25-00:30] Conclusion
        # Clear everything except axes and eigenvector
        to_remove = [matrix_A, vector_w, vector_w_label, eq1, eq2, eq3, eq4, non_eigen_group]
        self.play(*[FadeOut(obj) for obj in to_remove])
        
        # Highlight eigenvector
        self.play(Indicate(vector_v), Indicate(vector_v_label))
        
        # Final text
        conclusion_text1 = Text("Eigenvalues (λ) tell us how much eigenvectors stretch or shrink", font_size=28)
        conclusion_text1.to_edge(DOWN, buff=0.7)
        conclusion_bg1 = BackgroundRectangle(conclusion_text1, color=BLACK, fill_opacity=0.85)
        conclusion_group1 = VGroup(conclusion_bg1, conclusion_text1)
        
        conclusion_text2 = Text("For matrix A = [[2, 1], [1, 2]], λ = 3 for eigenvector [1, 1]", font_size=26)
        conclusion_text2.next_to(conclusion_text1, DOWN, buff=0.3)
        conclusion_bg2 = BackgroundRectangle(conclusion_text2, color=BLACK, fill_opacity=0.85)
        conclusion_group2 = VGroup(conclusion_bg2, conclusion_text2)
        
        self.play(FadeIn(conclusion_group1))
        self.wait(0.5)
        self.play(FadeIn(conclusion_group2))
        self.wait(2)
        
        # Final fade out
        self.play(FadeOut(*self.mobjects))
        self.wait(0.5)