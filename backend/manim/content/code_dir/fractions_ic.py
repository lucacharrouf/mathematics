from manim import *

class FractionsScene(Scene):

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
        title = Text("Understanding Fractions", font_size=48)
        title.to_edge(UP, buff=0.5)
        if title.width > 12:
            title.scale(12/title.width)
        
        explanation = Text("A fraction represents parts of a whole", font_size=36)
        explanation.to_edge(DOWN, buff=0.7)
        if explanation.width > 12:
            explanation.scale(12/explanation.width)
        
        explanation_bg = SurroundingRectangle(
            explanation,
            fill_color=BLACK,
            fill_opacity=0.7,
            buff=0.2,
            color=WHITE
        )
        
        self.play(Write(title))
        self.play(FadeIn(explanation_bg), Write(explanation))
        self.wait(2)
        
        # [00:05-00:12] First Concept: Fraction as Division
        circle = Circle(radius=1.5, color=WHITE)
        circle.move_to(ORIGIN)
        
        # Create division lines for the circle
        horizontal_line = Line(LEFT * 1.5, RIGHT * 1.5, color=WHITE)
        vertical_line = Line(UP * 1.5, DOWN * 1.5, color=WHITE)
        
        # Create the highlighted quarter
        quarter = Sector(
            radius=1.5,
            angle=PI/2,
            start_angle=PI/2,
            color=YELLOW,
            fill_opacity=0.8
        )
        
        # Fraction 1/4 notation
        fraction_1_4 = MathTex(r"\frac{1}{4}", font_size=48)
        fraction_1_4.move_to([-2, 0.5, 0])
        
        # Update bottom text
        new_explanation = Text("The fraction 1/4 means 1 part out of 4 equal parts", font_size=32)
        new_explanation.to_edge(DOWN, buff=0.7)
        if new_explanation.width > 12:
            new_explanation.scale(12/new_explanation.width)
        
        new_explanation_bg = SurroundingRectangle(
            new_explanation,
            fill_color=BLACK,
            fill_opacity=0.7,
            buff=0.2,
            color=WHITE
        )
        
        self.play(Create(circle))
        self.play(Create(horizontal_line), Create(vertical_line))
        self.play(FadeIn(quarter))
        self.play(
            FadeOut(explanation_bg),
            FadeOut(explanation),
            FadeIn(new_explanation_bg),
            Write(new_explanation)
        )
        self.play(Write(fraction_1_4))
        self.wait(2)
        
        # [00:12-00:20] Second Concept: Different Representations
        # Rectangle creation
        rectangle = Rectangle(height=1, width=4, color=WHITE)
        rectangle.move_to(ORIGIN)
        
        # Division lines for rectangle
        division_lines = VGroup()
        for i in range(1, 4):
            line = Line(
                UP * 0.5 + LEFT * 2 + RIGHT * i,
                DOWN * 0.5 + LEFT * 2 + RIGHT * i,
                color=WHITE
            )
            division_lines.add(line)
        
        # Highlighted section
        highlighted_section = Rectangle(
            height=1,
            width=1,
            color=YELLOW,
            fill_opacity=0.8
        )
        highlighted_section.move_to(LEFT * 1.5)
        
        # Decimal and percentage representations
        decimal = MathTex(r"0.25", font_size=48)
        decimal.move_to([2, 0.5, 0])
        
        percentage = MathTex(r"25\%", font_size=48)
        percentage.move_to([4, 0.5, 0])
        
        # Update explanation
        rep_explanation = Text("Fractions can be written as decimals or percentages", font_size=32)
        rep_explanation.to_edge(DOWN, buff=0.7)
        if rep_explanation.width > 12:
            rep_explanation.scale(12/rep_explanation.width)
        
        rep_explanation_bg = SurroundingRectangle(
            rep_explanation,
            fill_color=BLACK,
            fill_opacity=0.7,
            buff=0.2,
            color=WHITE
        )
        
        # Transform circle to rectangle
        self.play(
            FadeOut(quarter),
            FadeOut(horizontal_line),
            FadeOut(vertical_line),
            Transform(circle, rectangle)
        )
        self.play(Create(division_lines))
        self.play(FadeIn(highlighted_section))
        
        fraction_1_4_copy = fraction_1_4.copy()
        self.play(
            Transform(fraction_1_4, fraction_1_4_copy)
        )
        
        self.play(Write(decimal))
        self.play(Write(percentage))
        
        self.play(
            FadeOut(new_explanation_bg),
            FadeOut(new_explanation),
            FadeIn(rep_explanation_bg),
            Write(rep_explanation)
        )
        self.wait(2)
        
        # [00:20-00:30] Third Concept: Equivalent Fractions
        # Clear middle animations but keep the rectangle
        self.play(
            FadeOut(division_lines),
            FadeOut(highlighted_section),
            FadeOut(decimal),
            FadeOut(percentage)
        )
        
        # New rectangle with 8 divisions
        new_rectangle = Rectangle(height=1, width=4, color=WHITE)
        new_rectangle.move_to(ORIGIN)
        
        # 8 Division lines
        new_division_lines = VGroup()
        for i in range(1, 8):
            line = Line(
                UP * 0.5 + LEFT * 2 + RIGHT * i * 0.5,
                DOWN * 0.5 + LEFT * 2 + RIGHT * i * 0.5,
                color=WHITE
            )
            new_division_lines.add(line)
        
        # 2 Highlighted sections
        highlighted_section1 = Rectangle(
            height=1,
            width=0.5,
            color=YELLOW,
            fill_opacity=0.8
        )
        highlighted_section1.move_to(LEFT * 1.75)
        
        highlighted_section2 = Rectangle(
            height=1,
            width=0.5,
            color=YELLOW,
            fill_opacity=0.8
        )
        highlighted_section2.move_to(LEFT * 1.25)
        
        # Equivalent fractions
        fraction_2_8 = MathTex(r"\frac{2}{8}", font_size=48)
        fraction_2_8.move_to([-2, 0.5, 0])
        
        equals_sign = MathTex(r"=", font_size=48)
        equals_sign.move_to([0, 0.5, 0])
        
        fraction_1_4_new = MathTex(r"\frac{1}{4}", font_size=48)
        fraction_1_4_new.move_to([2, 0.5, 0])
        
        # Arrow and "Same value" text
        arrow = CurvedArrow(
            start_point=[-1.5, 1, 0],
            end_point=[1.5, 1, 0],
            color=RED
        )
        
        same_value_text = Text("Same value!", font_size=32, color=RED)
        same_value_text.move_to([0, 1.5, 0])
        
        # Update explanation
        equiv_explanation = Text("Equivalent fractions represent the same amount", font_size=32)
        equiv_explanation.to_edge(DOWN, buff=0.7)
        if equiv_explanation.width > 12:
            equiv_explanation.scale(12/equiv_explanation.width)
        
        equiv_explanation_bg = SurroundingRectangle(
            equiv_explanation,
            fill_color=BLACK,
            fill_opacity=0.7,
            buff=0.2,
            color=WHITE
        )
        
        # Transformations
        self.play(Transform(circle, new_rectangle))
        self.play(Create(new_division_lines))
        self.play(
            FadeIn(highlighted_section1),
            FadeIn(highlighted_section2)
        )
        
        self.play(
            Transform(fraction_1_4, fraction_2_8)
        )
        self.play(Write(equals_sign))
        self.play(Write(fraction_1_4_new))
        
        self.play(
            Create(arrow),
            Write(same_value_text)
        )
        
        self.play(
            FadeOut(rep_explanation_bg),
            FadeOut(rep_explanation),
            FadeIn(equiv_explanation_bg),
            Write(equiv_explanation)
        )
        
        self.wait(2)
        
        # Fade out everything
        self.play(FadeOut(*self.mobjects))
        self.wait(0.5)