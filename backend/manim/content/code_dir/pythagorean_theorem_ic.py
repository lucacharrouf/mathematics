from manim import *
import numpy as np

class PythagoreanTheoremScene(Scene):

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
        title = Text("The Pythagorean Theorem", font_size=48)
        title.to_edge(UP, buff=0.5)
        
        subtitle = MathTex(r"a^2 + b^2 = c^2", font_size=40)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(1)
        
        # [00:03-00:07] Right Triangle Setup
        self.play(FadeOut(subtitle))
        
        # Create right triangle
        triangle_points = [
            np.array([0, 0, 0]),
            np.array([3, 0, 0]),
            np.array([0, 4, 0]),
        ]
        triangle = Polygon(*triangle_points, color=WHITE)
        
        # Create right angle square
        right_angle = Square(side_length=0.4, color=WHITE)
        right_angle.move_to(triangle_points[0])
        right_angle.align_to(triangle_points[0], DL)
        
        # Labels for sides
        a_label = MathTex("a = 3", font_size=28)
        a_label.move_to(np.array([1.5, -0.3, 0]))
        
        b_label = MathTex("b = 4", font_size=28)
        b_label.move_to(np.array([-0.4, 2, 0]))
        
        c_label = MathTex("c = 5", font_size=28)
        c_label.move_to(np.array([1.7, 2.2, 0]))
        
        explanation1 = Text("Consider a right triangle with sides a = 3 and b = 4", font_size=28)
        explanation1.to_edge(DOWN, buff=0.5)
        explanation_bg1 = SurroundingRectangle(
            explanation1, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(
            Create(triangle),
            Create(right_angle)
        )
        self.play(
            Write(a_label),
            Write(b_label),
            Write(c_label)
        )
        self.play(
            FadeIn(explanation_bg1),
            Write(explanation1)
        )
        self.wait(1)
        
        # [00:08-00:12] Square Construction
        self.play(
            FadeOut(explanation_bg1),
            FadeOut(explanation1)
        )
        
        # Create squares on sides
        a_square = Square(side_length=3, color=BLUE, fill_opacity=0.5)
        a_square.align_to(triangle_points[0], UL)
        a_square.shift(RIGHT * 3)
        
        b_square = Square(side_length=4, color=RED, fill_opacity=0.5)
        b_square.align_to(triangle_points[0], DR)
        b_square.shift(UP * 4)
        
        # For the hypotenuse square, we need to rotate it to align with the hypotenuse
        c_square = Square(side_length=5, color=GREEN, fill_opacity=0.5)
        angle = np.arctan2(4, 3)
        c_square.rotate(angle)
        c_square.move_to(triangle_points[2])
        shift_vector = (triangle_points[1] - triangle_points[2]) / 2
        c_square.shift(shift_vector)
        
        explanation2 = Text("We can draw squares on each side of the triangle", font_size=28)
        explanation2.to_edge(DOWN, buff=0.5)
        explanation_bg2 = SurroundingRectangle(
            explanation2, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(
            Create(a_square),
            Create(b_square),
            Create(c_square)
        )
        self.play(
            FadeIn(explanation_bg2),
            Write(explanation2)
        )
        self.wait(1)
        
        # [00:13-00:17] Area Calculation
        self.play(
            FadeOut(explanation_bg2),
            FadeOut(explanation2)
        )
        
        # Area labels
        a_area = MathTex(r"\text{Area} = a^2 = 9", font_size=28, color=BLUE)
        a_area.move_to(np.array([1.5, -1.5, 0]))
        
        b_area = MathTex(r"\text{Area} = b^2 = 16", font_size=28, color=RED)
        b_area.move_to(np.array([-2, 2, 0]))
        
        c_area = MathTex(r"\text{Area} = c^2 = 25", font_size=28, color=GREEN)
        c_area.move_to(np.array([2.5, 2.5, 0]))
        
        explanation3 = Text("The areas of these squares are a², b², and c²", font_size=28)
        explanation3.to_edge(DOWN, buff=0.5)
        explanation_bg3 = SurroundingRectangle(
            explanation3, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(
            Write(a_area),
            Write(b_area),
            Write(c_area)
        )
        self.play(
            FadeIn(explanation_bg3),
            Write(explanation3)
        )
        self.wait(1)
        
        # [00:18-00:22] Theorem Demonstration
        self.play(
            FadeOut(explanation_bg3),
            FadeOut(explanation3),
            FadeOut(a_area),
            FadeOut(b_area),
            FadeOut(c_area)
        )
        
        # Animation of equation
        eq1 = MathTex(r"a^2 + b^2 = ?", font_size=38)
        eq1.move_to(np.array([0, 0.5, 0]))
        
        eq2 = MathTex(r"9 + 16 = 25", font_size=38)
        eq2.move_to(np.array([0, 0.5, 0]))
        
        eq3 = MathTex(r"a^2 + b^2 = c^2", font_size=38)
        eq3.move_to(np.array([0, 0.5, 0]))
        
        explanation4 = Text("The Pythagorean theorem states that a² + b² = c²", font_size=28)
        explanation4.to_edge(DOWN, buff=0.5)
        explanation_bg4 = SurroundingRectangle(
            explanation4, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(Write(eq1))
        self.wait(0.5)
        self.play(Transform(eq1, eq2))
        self.wait(0.5)
        self.play(Transform(eq1, eq3))
        
        # Pulsate the c square
        self.play(
            c_square.animate.scale(1.1),
            rate_func=there_and_back,
            run_time=1
        )
        
        self.play(
            FadeIn(explanation_bg4),
            Write(explanation4)
        )
        self.wait(1)
        
        # [00:23-00:26] Visual Proof Hint
        self.play(
            FadeOut(eq1),
            FadeOut(explanation_bg4),
            FadeOut(explanation4)
        )
        
        # Create copies of squares for rearrangement
        a_square_copy = a_square.copy()
        b_square_copy = b_square.copy()
        
        explanation5 = Text("The sum of the areas equals the area of the square on the hypotenuse", font_size=26)
        explanation5.to_edge(DOWN, buff=0.5)
        explanation_bg5 = SurroundingRectangle(
            explanation5, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Animate squares shifting towards c_square
        self.play(
            a_square_copy.animate.scale(0.9).move_to(c_square.get_center() + LEFT * 0.5 + DOWN * 0.5),
            b_square_copy.animate.scale(0.9).move_to(c_square.get_center() + RIGHT * 0.5 + UP * 0.5),
            run_time=2
        )
        
        self.play(
            FadeIn(explanation_bg5),
            Write(explanation5)
        )
        self.wait(1)
        
        # [00:27-00:30] Conclusion
        self.play(
            FadeOut(a_square_copy),
            FadeOut(b_square_copy),
            FadeOut(explanation_bg5),
            FadeOut(explanation5)
        )
        
        final_equation = MathTex(r"a^2 + b^2 = c^2", font_size=48)
        final_equation.move_to(np.array([0, 0.5, 0]))
        
        explanation6 = Text("This relationship works for all right triangles", font_size=28)
        explanation6.to_edge(DOWN, buff=0.5)
        explanation_bg6 = SurroundingRectangle(
            explanation6, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(Write(final_equation))
        self.play(
            FadeIn(explanation_bg6),
            Write(explanation6)
        )
        
        # Highlight the triangle one more time
        self.play(
            triangle.animate.set_color(YELLOW),
            rate_func=there_and_back,
            run_time=1.5
        )
        
        self.wait(1)