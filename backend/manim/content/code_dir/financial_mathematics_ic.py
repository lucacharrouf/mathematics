from manim import *

class FinancialMathematicsScene(Scene):

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
        title = Text("Compound Interest", font_size=48)
        title.to_edge(UP, buff=1)
        
        subtitle = Text("The Power of Exponential Growth", font_size=36)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        formula = MathTex(r"P(t) = P_0(1+r)^t", font_size=40)
        formula.to_edge(DOWN, buff=1)
        
        formula_bg = SurroundingRectangle(
            formula, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(subtitle))
        self.wait(0.5)
        self.play(FadeIn(formula_bg), Write(formula))
        self.wait(1)
        
        # [00:06-00:12] Initial Investment Visualization
        self.play(FadeOut(formula_bg), FadeOut(formula))
        
        initial_text = Text("Initial Investment: $1,000", font_size=36)
        initial_text.to_edge(DOWN, buff=1)
        initial_text_bg = SurroundingRectangle(
            initial_text, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Create axes
        axes = Axes(
            x_range=[-0.5, 10.5, 1],
            y_range=[-0.5, 3, 0.5],
            axis_config={"include_tip": False},
            x_length=10,
            y_length=5,
        ).move_to(ORIGIN)
        
        # Add axes labels
        x_label = Text("Time (years)", font_size=24).next_to(axes.x_axis, DOWN, buff=0.5)
        y_label = Text("Amount ($)", font_size=24).next_to(axes.y_axis, LEFT, buff=0.5).rotate(PI/2)
        
        # Add tick labels
        x_labels = VGroup()
        for i in range(1, 6):
            label = Text(str(i), font_size=20)
            label.next_to(axes.c2p(i, 0), DOWN, buff=0.2)
            x_labels.add(label)
        
        y_values = [1, 1.5, 2, 2.5]
        y_labels = VGroup()
        for i, val in enumerate(y_values):
            label = Text(f"${int(val * 1000)}", font_size=20)
            label.next_to(axes.c2p(0, val), LEFT, buff=0.2)
            y_labels.add(label)
        
        # Initial investment dot
        initial_dot = Dot(axes.c2p(0, 1), color=BLUE)
        initial_dot_label = Text("$1,000", font_size=24, color=BLUE)
        initial_dot_label.next_to(initial_dot, UP + RIGHT, buff=0.2)
        
        self.play(FadeIn(initial_text_bg), Write(initial_text))
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.play(FadeIn(x_labels), FadeIn(y_labels))
        self.play(FadeIn(initial_dot), Write(initial_dot_label))
        self.wait(1)
        
        # [00:13-00:19] Single Compounding Period
        year1_text = Text("After 1 year at 10% interest: $1,000 × 1.10 = $1,100", font_size=32)
        year1_text.to_edge(DOWN, buff=1)
        year1_text_bg = SurroundingRectangle(
            year1_text, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        year1_dot = Dot(axes.c2p(1, 1.1), color=GREEN)
        year1_label = Text("$1,100", font_size=24, color=GREEN)
        year1_label.next_to(year1_dot, UP + RIGHT, buff=0.2)
        
        dotted_line = DashedLine(
            axes.c2p(0, 1), 
            axes.c2p(1, 1.1),
            dash_length=0.1,
            dashed_ratio=0.5,
        )
        
        self.play(
            FadeOut(initial_text_bg),
            FadeOut(initial_text),
            FadeIn(year1_text_bg),
            Write(year1_text)
        )
        self.play(Create(dotted_line))
        self.play(FadeIn(year1_dot), Write(year1_label))
        self.wait(1)
        
        # [00:20-00:26] Multiple Compounding Periods
        multiple_text = Text("Compounding over multiple years", font_size=36)
        multiple_text.to_edge(DOWN, buff=1)
        multiple_text_bg = SurroundingRectangle(
            multiple_text, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Create data points for years 2-5
        data_points = [
            (2, 1.21, "$1,210"),
            (3, 1.331, "$1,331"),
            (4, 1.464, "$1,464"),
            (5, 1.61, "$1,610")
        ]
        
        dots = VGroup()
        labels = VGroup()
        dotted_lines = VGroup()
        
        for year, value, label_text in data_points:
            dot = Dot(axes.c2p(year, value), color=GREEN)
            label = Text(label_text, font_size=24, color=GREEN)
            label.next_to(dot, UP + RIGHT, buff=0.2)
            
            prev_year = year - 1
            prev_value = 1.1 * (1.1 ** (prev_year - 1)) if prev_year > 0 else 1
            
            dotted_line = DashedLine(
                axes.c2p(prev_year, prev_value), 
                axes.c2p(year, value),
                dash_length=0.1,
                dashed_ratio=0.5,
            )
            
            dots.add(dot)
            labels.add(label)
            dotted_lines.add(dotted_line)
        
        self.play(
            FadeOut(year1_text_bg),
            FadeOut(year1_text),
            FadeIn(multiple_text_bg),
            Write(multiple_text)
        )
        
        for i in range(len(data_points)):
            self.play(
                Create(dotted_lines[i]),
                FadeIn(dots[i]),
                Write(labels[i]),
                run_time=0.75
            )
        
        # Create exponential curve
        def exp_func(x):
            return 1 * (1.1 ** x)
        
        curve = axes.plot(exp_func, x_range=[0, 5], color=YELLOW)
        
        self.play(Create(curve))
        self.wait(1)
        
        # [00:27-00:30] Conclusion
        conclusion_text = Text("Compound interest grows exponentially: $1,000 becomes $2,594 after 10 years", font_size=28)
        conclusion_text.to_edge(DOWN, buff=1)
        conclusion_text_bg = SurroundingRectangle(
            conclusion_text, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Fade existing elements
        self.play(
            *[mob.animate.set_opacity(0.3) for mob in [dots, labels, dotted_lines, dotted_line]],
            FadeOut(multiple_text_bg),
            FadeOut(multiple_text)
        )
        
        # Extend curve to 10 years
        extended_curve = axes.plot(exp_func, x_range=[0, 10], color=YELLOW)
        
        year10_dot = Dot(axes.c2p(10, 2.594), color=RED)
        year10_label = Text("$2,594", font_size=24, color=RED)
        year10_label.next_to(year10_dot, UP + RIGHT, buff=0.2)
        
        final_formula = MathTex(
            r"P(t) = P_0(1+r)^t = \$1,000(1+0.10)^{10} = \$2,594", 
            font_size=36
        )
        final_formula.next_to(conclusion_text_bg, UP, buff=0.5)
        final_formula_bg = SurroundingRectangle(
            final_formula, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(
            ReplacementTransform(curve, extended_curve),
            FadeIn(conclusion_text_bg),
            Write(conclusion_text)
        )
        self.play(FadeIn(year10_dot), Write(year10_label))
        self.play(FadeIn(final_formula_bg), Write(final_formula))
        
        self.wait(2)