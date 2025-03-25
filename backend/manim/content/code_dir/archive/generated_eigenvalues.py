from manim import *

class eigenvaluesScene(Scene):
    def construct(self):
        # Setup - title for the scene
        title = Text("Eigenvalues and Eigenvectors", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.5).to_edge(UP))
        
        # Main visualization code about eigenvalues
        # Define a 2x2 matrix
        matrix = [[3, 1], [1, 2]]
        matrix_mob = Matrix(matrix)
        matrix_tex = MathTex("A = ")
        matrix_group = VGroup(matrix_tex, matrix_mob).arrange(RIGHT).scale(0.8).to_edge(LEFT)
        
        # Display the matrix
        self.play(Write(matrix_group))
        self.wait(1)
        
        # Explanation of eigenvalue equation
        eigen_eq = MathTex("A\\vec{v} = \\lambda\\vec{v}")
        eigen_eq_expanded = MathTex("A\\vec{v} - \\lambda\\vec{v} = \\vec{0}")
        eigen_eq_factored = MathTex("(A - \\lambda I)\\vec{v} = \\vec{0}")
        
        for eq in [eigen_eq, eigen_eq_expanded, eigen_eq_factored]:
            eq.next_to(matrix_group, DOWN, buff=0.8)
            
        # Animate the eigenvalue equations
        self.play(Write(eigen_eq))
        self.wait(1)
        self.play(TransformMatchingTex(eigen_eq, eigen_eq_expanded))
        self.wait(1)
        self.play(TransformMatchingTex(eigen_eq_expanded, eigen_eq_factored))
        self.wait(1)
        
        # Show that for non-trivial solutions, determinant must be zero
        det_eq = MathTex("\\det(A - \\lambda I) = 0")
        det_eq.next_to(eigen_eq_factored, DOWN, buff=0.5)
        self.play(Write(det_eq))
        self.wait(1)
        
        # Calculate the characteristic polynomial
        char_poly = MathTex("\\det\\begin{pmatrix} 3-\\lambda & 1 \\\\ 1 & 2-\\lambda \\end{pmatrix} = 0")
        char_poly.next_to(det_eq, DOWN, buff=0.5)
        self.play(Write(char_poly))
        self.wait(1)
        
        # Expand the determinant
        det_expanded = MathTex("(3-\\lambda)(2-\\lambda) - 1 = 0")
        det_expanded.next_to(char_poly, DOWN, buff=0.5)
        self.play(Write(det_expanded))
        self.wait(1)
        
        # Simplify the polynomial
        poly_simplified = MathTex("\\lambda^2 - 5\\lambda + 5 = 0")
        poly_simplified.next_to(det_expanded, DOWN, buff=0.5)
        self.play(Write(poly_simplified))
        self.wait(1)
        
        # Show the eigenvalues
        eigenvalues = MathTex("\\lambda_1 = 3.618..., \\lambda_2 = 1.382...")
        eigenvalues.next_to(poly_simplified, DOWN, buff=0.5)
        self.play(Write(eigenvalues))
        self.wait(1)
        
        # Clear previous calculations
        self.play(
            *[FadeOut(mob) for mob in [eigen_eq_factored, det_eq, char_poly, det_expanded, poly_simplified, eigenvalues]]
        )
        self.wait(0.5)
        
        # Create a coordinate system for visualizing eigenvectors
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"include_tip": False, "include_numbers": True},
        ).scale(0.8)
        
        axes.add_coordinates()
        axes.to_edge(RIGHT)
        
        self.play(Create(axes))
        self.wait(1)
        
        # Define our vectors - original vector and its transformation
        vector = np.array([1, 0.5])
        vector_mob = Vector(vector, color=BLUE).shift(axes.get_origin())
        vector_label = MathTex("\\vec{v}", color=BLUE).next_to(vector_mob.get_end(), RIGHT, buff=0.1)
        
        # Calculate Av (the transformed vector)
        transformed_vector = np.array([matrix[0][0]*vector[0] + matrix[0][1]*vector[1], 
                                       matrix[1][0]*vector[0] + matrix[1][1]*vector[1]])
        transformed_mob = Vector(transformed_vector, color=RED).shift(axes.get_origin())
        transformed_label = MathTex("A\\vec{v}", color=RED).next_to(transformed_mob.get_end(), RIGHT, buff=0.1)
        
        # Show the vectors
        self.play(Create(vector_mob), Write(vector_label))
        self.wait(1)
        self.play(Create(transformed_mob), Write(transformed_label))
        self.wait(1)
        
        # Now show an eigenvector
        # Eigenvector for λ₁ ≈ 3.618 is approximately [1, 0.618]
        eigenvector = np.array([1, 0.618])
        # Normalize it
        eigenvector = eigenvector / np.linalg.norm(eigenvector) * 2
        
        # Create vector and its transformation
        eigen_mob = Vector(eigenvector, color=GREEN).shift(axes.get_origin())
        eigen_label = MathTex("\\vec{v}_1", color=GREEN).next_to(eigen_mob.get_end(), UP, buff=0.1)
        
        eigenvalue = 3.618
        scaled_eigen = eigenvalue * eigenvector
        scaled_mob = Vector(scaled_eigen, color=YELLOW).shift(axes.get_origin())
        scaled_label = MathTex("\\lambda_1 \\vec{v}_1", color=YELLOW).next_to(scaled_mob.get_end(), UP, buff=0.1)
        
        # Clear previous vectors
        self.play(
            *[FadeOut(mob) for mob in [vector_mob, vector_label, transformed_mob, transformed_label]]
        )
        
        # Add a text explanation
        eigen_text = Text("Eigenvector", color=GREEN, font_size=24).next_to(axes, UP, buff=0.2)
        self.play(Write(eigen_text))
        
        # Show the eigenvector
        self.play(Create(eigen_mob), Write(eigen_label))
        self.wait(1)
        
        # Show what happens when we multiply by A - it scales by λ
        A_eigen_text = Text("A·Eigenvector = λ·Eigenvector", font_size=24).next_to(eigen_text, DOWN, buff=0.2)
        self.play(Write(A_eigen_text))
        self.play(Create(scaled_mob), Write(scaled_label))
        self.wait(2)
        
        # Final message
        conclusion = Text("Eigenvectors are only scaled (not rotated) by the matrix", font_size=24)
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)