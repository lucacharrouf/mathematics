from manim import *

class ComplexNumbersScene(Scene):

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
        title = Text("Complex Numbers", font_size=48)
        title.to_edge(UP, buff=0.5)
        
        subtitle = Text("Geometric Interpretation", font_size=36)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Create grid
        grid = NumberPlane(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            x_length=10,
            y_length=6,
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 2,
                "stroke_opacity": 0.6
            }
        )
        
        # Add axis labels
        x_label = Text("Real", font_size=30).next_to(grid.c2p(5, 0), RIGHT, buff=0.2)
        y_label = Text("Imaginary", font_size=30).next_to(grid.c2p(0, 3), UP, buff=0.2)
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(subtitle))
        self.wait(0.5)
        self.play(Create(grid), FadeIn(x_label), FadeIn(y_label))
        self.wait(1)
        
        # [00:05-00:10] Complex Number Representation
        explanation1 = Text("A complex number z = a + bi has two components", font_size=28)
        explanation1.to_edge(DOWN, buff=0.5)
        explanation1_bg = SurroundingRectangle(
            explanation1, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Point at (3,2)
        point_coords = [3, 2, 0]
        point = Dot(grid.c2p(*point_coords), color=YELLOW)
        point_label = MathTex("z = 3 + 2i", font_size=32).next_to(point, UR, buff=0.2)
        
        # Arrow from origin to point
        arrow = Arrow(grid.c2p(0, 0, 0), grid.c2p(*point_coords), buff=0, color="#3498db")
        
        # Component lines
        horizontal_line = DashedLine(
            grid.c2p(0, 0, 0), grid.c2p(3, 0, 0), 
            color=RED, stroke_width=3
        )
        vertical_line = DashedLine(
            grid.c2p(3, 0, 0), grid.c2p(3, 2, 0), 
            color=GREEN, stroke_width=3
        )
        
        # Component labels
        horizontal_label = MathTex("a = 3", font_size=28, color=RED).next_to(horizontal_line, DOWN, buff=0.2)
        vertical_label = MathTex("b = 2", font_size=28, color=GREEN).next_to(vertical_line, RIGHT, buff=0.2)
        
        self.play(
            FadeIn(explanation1_bg),
            Write(explanation1)
        )
        self.wait(0.5)
        self.play(FadeIn(point), Write(point_label))
        self.wait(0.5)
        self.play(GrowArrow(arrow))
        self.wait(0.5)
        self.play(Create(horizontal_line), Create(vertical_line))
        self.wait(0.5)
        self.play(Write(horizontal_label), Write(vertical_label))
        self.wait(1)
        
        # [00:10-00:20] Polar Form Introduction
        explanation2 = Text("Complex numbers can also be represented in polar form: z = re^(iθ)", font_size=28)
        explanation2.to_edge(DOWN, buff=0.5)
        explanation2_bg = SurroundingRectangle(
            explanation2, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Calculate angle and magnitude
        angle_value = np.arctan2(2, 3)
        angle_deg = angle_value * 180 / np.pi
        magnitude = np.sqrt(3**2 + 2**2)
        
        # Angle arc
        angle_arc = Arc(
            radius=0.7,
            angle=angle_value,
            start_angle=0,
            arc_center=grid.c2p(0, 0, 0),
            color=YELLOW
        )
        
        # Angle label
        angle_label = MathTex(
            r"\theta = \arctan\left(\frac{2}{3}\right) \approx 0.59 \text{ rad}",
            font_size=28
        ).next_to(angle_arc, UR, buff=0.3)
        angle_label.shift(LEFT * 0.5)
        
        # Radius label
        radius_label = MathTex(
            r"r = \sqrt{3^2 + 2^2} = \sqrt{13} \approx 3.61",
            font_size=28
        )
        radius_label.next_to(arrow.get_center(), UL, buff=0.3)
        
        # Polar form equation
        polar_eq = MathTex(
            r"z = 3 + 2i = 3.61e^{0.59i}",
            font_size=32
        )
        polar_eq.next_to(explanation2, UP, buff=0.3)
        polar_eq_bg = SurroundingRectangle(
            polar_eq, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.1,
            color=WHITE
        )
        
        self.play(
            FadeOut(explanation1_bg),
            FadeOut(explanation1),
            FadeOut(horizontal_label),
            FadeOut(vertical_label),
            FadeOut(horizontal_line),
            FadeOut(vertical_line),
        )
        self.play(
            FadeIn(explanation2_bg),
            Write(explanation2)
        )
        self.wait(0.5)
        
        self.play(Create(angle_arc))
        self.play(Write(angle_label))
        self.wait(0.5)
        
        self.play(Write(radius_label))
        self.wait(0.5)
        
        self.play(
            FadeIn(polar_eq_bg),
            Write(polar_eq)
        )
        self.wait(1)
        
        # [00:20-00:30] Complex Multiplication Visualization
        explanation3 = Text("Multiplying by i rotates a complex number by 90°", font_size=28)
        explanation3.to_edge(DOWN, buff=0.5)
        explanation3_bg = SurroundingRectangle(
            explanation3, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # New rotated point
        rotated_coords = [-2, 3, 0]  # i·(3+2i) = -2+3i
        rotated_point = Dot(grid.c2p(*rotated_coords), color=PURPLE)
        rotated_label = MathTex(r"i \cdot z = -2 + 3i", font_size=32).next_to(rotated_point, UP, buff=0.2)
        
        # Arrow for the rotated point
        rotated_arrow = Arrow(
            grid.c2p(0, 0, 0), 
            grid.c2p(*rotated_coords), 
            buff=0, 
            color="#9b59b6"
        )
        
        # Rotation animation
        rotating_arrow = Arrow(
            grid.c2p(0, 0, 0), 
            grid.c2p(*point_coords), 
            buff=0, 
            color="#3498db"
        )
        
        # Formula for multiplication by i
        mult_formula = MathTex(
            r"i(3 + 2i) = 3i + 2i^2 = 3i - 2 = -2 + 3i",
            font_size=32
        )
        mult_formula.next_to(explanation3, UP, buff=0.3)
        mult_formula_bg = SurroundingRectangle(
            mult_formula, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.1,
            color=WHITE
        )
        
        self.play(
            FadeOut(explanation2_bg),
            FadeOut(explanation2),
            FadeOut(angle_arc),
            FadeOut(angle_label),
            FadeOut(radius_label),
            FadeOut(polar_eq_bg),
            FadeOut(polar_eq)
        )
        self.play(
            FadeIn(explanation3_bg),
            Write(explanation3)
        )
        self.wait(0.5)
        
        # Animation of rotation
        self.add(rotating_arrow)
        self.play(
            Rotating(
                rotating_arrow,
                about_point=grid.c2p(0, 0, 0),
                angle=PI/2,
                run_time=2
            )
        )
        self.remove(rotating_arrow)
        
        self.play(
            GrowArrow(rotated_arrow),
            FadeIn(rotated_point),
            Write(rotated_label)
        )
        self.wait(0.5)
        
        self.play(
            FadeIn(mult_formula_bg),
            Write(mult_formula)
        )
        self.wait(2)
        
        # Final fade out
        self.play(FadeOut(*self.mobjects))
        self.wait(0.5)