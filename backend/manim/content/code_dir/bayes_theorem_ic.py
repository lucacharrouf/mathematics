from manim import *

class BayesTheoremScene(Scene):

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
        # Title
        title = Text("Bayes Theorem: Updating Beliefs with Evidence", font_size=36)
        title.to_edge(UP, buff=0.5)
        if title.width > 12:
            title.scale(12/title.width)
        
        # Bayes formula
        bayes_formula = MathTex(
            r"P(A|B) = \frac{P(B|A) \times P(A)}{P(B)}",
            font_size=40
        )
        bayes_formula.move_to(ORIGIN)
        
        # Explanatory text with background
        explanation = Text("Bayes Theorem helps us update probabilities when new evidence arrives", 
                          font_size=28)
        explanation.to_edge(DOWN, buff=0.5)
        if explanation.width > 12:
            explanation.scale(12/explanation.width)
        explanation_bg = SurroundingRectangle(
            explanation, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(Write(title))
        self.wait(0.5)
        self.play(Write(bayes_formula))
        self.play(FadeIn(explanation_bg), Write(explanation))
        self.wait(1)
        
        # [00:05-00:12] Setting up the Problem
        # Move formula up to make room for rectangle
        bayes_formula_target = bayes_formula.copy()
        bayes_formula_target.shift(UP)
        
        # New explanation text
        problem_setup = Text("Medical Test Example: 1% of population has disease, Test is 90% accurate", 
                           font_size=28)
        problem_setup.to_edge(DOWN, buff=0.5)
        if problem_setup.width > 12:
            problem_setup.scale(12/problem_setup.width)
        problem_setup_bg = SurroundingRectangle(
            problem_setup, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Rectangle visualization
        rectangle = Rectangle(width=8, height=3, color=WHITE)
        rectangle.move_to(DOWN * 0.5)
        
        # Division line at 1% from left
        division_line = Line(
            rectangle.get_corner(UL) + DOWN * rectangle.height * 0.01 + RIGHT * rectangle.width * 0.01,
            rectangle.get_corner(DL) + UP * rectangle.height * 0.01 + RIGHT * rectangle.width * 0.01,
            color=WHITE
        )
        
        # Labels and sections
        disease_section = Rectangle(
            width=rectangle.width * 0.01,
            height=rectangle.height,
            fill_color=RED,
            fill_opacity=0.5,
            color=RED
        )
        disease_section.align_to(rectangle, LEFT)
        disease_section.align_to(rectangle, UP)
        disease_section.align_to(rectangle, DOWN)
        
        no_disease_section = Rectangle(
            width=rectangle.width * 0.99,
            height=rectangle.height,
            fill_color=GREEN,
            fill_opacity=0.5,
            color=GREEN
        )
        no_disease_section.next_to(disease_section, RIGHT, buff=0)
        
        disease_label = Text("Disease", font_size=24, color=WHITE)
        disease_label.move_to(disease_section)
        if disease_label.width > disease_section.width * 0.9:
            disease_label.rotate(PI/2)
            
        no_disease_label = Text("No Disease", font_size=28, color=WHITE)
        no_disease_label.move_to(no_disease_section)
        
        self.play(
            Transform(bayes_formula, bayes_formula_target),
            FadeOut(explanation_bg), 
            FadeOut(explanation)
        )
        self.play(
            FadeIn(problem_setup_bg),
            Write(problem_setup)
        )
        self.play(Create(rectangle))
        self.play(
            FadeIn(disease_section),
            FadeIn(no_disease_section),
            Write(disease_label),
            Write(no_disease_label)
        )
        self.wait(1)
        
        # [00:12-00:20] Test Accuracy Visualization
        # Subdivide disease section
        true_positive = Rectangle(
            width=disease_section.width,
            height=disease_section.height * 0.9,
            fill_color=RED_E,
            fill_opacity=0.7,
            color=RED_E
        )
        true_positive.align_to(disease_section, UP)
        true_positive.align_to(disease_section, LEFT)
        
        false_negative = Rectangle(
            width=disease_section.width,
            height=disease_section.height * 0.1,
            fill_color=RED_A,
            fill_opacity=0.7,
            color=RED_A
        )
        false_negative.align_to(disease_section, DOWN)
        false_negative.align_to(disease_section, LEFT)
        
        # Subdivide no-disease section
        false_positive = Rectangle(
            width=no_disease_section.width,
            height=no_disease_section.height * 0.1,
            fill_color=GREEN_A,
            fill_opacity=0.7,
            color=GREEN_A
        )
        false_positive.align_to(no_disease_section, UP)
        false_positive.align_to(no_disease_section, RIGHT)
        
        true_negative = Rectangle(
            width=no_disease_section.width,
            height=no_disease_section.height * 0.9,
            fill_color=GREEN_E,
            fill_opacity=0.7,
            color=GREEN_E
        )
        true_negative.align_to(no_disease_section, DOWN)
        true_negative.align_to(no_disease_section, RIGHT)
        
        # Labels for subdivisions (smaller font size)
        tp_label = Text("True Positive", font_size=16, color=WHITE)
        tp_label.move_to(true_positive)
        if tp_label.width > true_positive.width * 0.9:
            tp_label.rotate(PI/2)
            
        fn_label = Text("False Negative", font_size=16, color=WHITE)
        fn_label.move_to(false_negative)
        if fn_label.width > false_negative.width * 0.9:
            fn_label.rotate(PI/2)
            
        fp_label = Text("False Positive", font_size=20, color=WHITE)
        fp_label.move_to(false_positive)
        
        tn_label = Text("True Negative", font_size=24, color=WHITE)
        tn_label.move_to(true_negative)
        
        # New explanatory text
        test_explanation = Text("Given a positive test, what's the probability of having the disease?", 
                               font_size=28)
        test_explanation.to_edge(DOWN, buff=0.5)
        if test_explanation.width > 12:
            test_explanation.scale(12/test_explanation.width)
        test_explanation_bg = SurroundingRectangle(
            test_explanation, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(
            FadeOut(disease_label),
            FadeOut(no_disease_label),
            FadeIn(true_positive),
            FadeIn(false_negative),
            FadeIn(false_positive),
            FadeIn(true_negative)
        )
        self.play(
            Write(tp_label),
            Write(fn_label),
            Write(fp_label),
            Write(tn_label)
        )
        self.play(
            FadeOut(problem_setup_bg),
            FadeOut(problem_setup),
            FadeIn(test_explanation_bg),
            Write(test_explanation)
        )
        self.wait(1)
        
        # [00:20-00:25] Bayes Calculation
        # Highlight positive test results
        highlight_tp = SurroundingRectangle(true_positive, color=YELLOW, buff=0.05)
        highlight_fp = SurroundingRectangle(false_positive, color=YELLOW, buff=0.05)
        
        # Arrow pointing to ratio
        arrow = Arrow(
            start=LEFT * 3 + UP * 1,
            end=RIGHT * 1 + UP * 1,
            color=YELLOW
        )
        
        # Mathematical calculation
        calculation = MathTex(
            r"P(Disease|Positive) &= \frac{P(Positive|Disease) \times P(Disease)}{P(Positive)} \\",
            r"&= \frac{0.90 \times 0.01}{0.90 \times 0.01 + 0.10 \times 0.99} \\",
            r"&\approx 0.083",
            font_size=32
        )
        calculation.move_to(LEFT * 3 + UP * 1)
        
        # New explanation
        conclusion_explanation = Text("Only about 8.3% of positive tests indicate disease", 
                                    font_size=28)
        conclusion_explanation.to_edge(DOWN, buff=0.5)
        if conclusion_explanation.width > 12:
            conclusion_explanation.scale(12/conclusion_explanation.width)
        conclusion_explanation_bg = SurroundingRectangle(
            conclusion_explanation, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(
            Create(highlight_tp),
            Create(highlight_fp)
        )
        self.play(Create(arrow))
        self.play(Write(calculation[0]))
        self.wait(0.5)
        self.play(Write(calculation[1]))
        self.wait(0.5)
        self.play(Write(calculation[2]))
        self.play(
            FadeOut(test_explanation_bg),
            FadeOut(test_explanation),
            FadeIn(conclusion_explanation_bg),
            Write(conclusion_explanation)
        )
        self.wait(1)
        
        # [00:25-00:30] Conclusion
        # Fade rectangle visualization
        all_rect_objects = VGroup(
            rectangle, disease_section, no_disease_section,
            true_positive, false_negative, false_positive, true_negative,
            tp_label, fn_label, fp_label, tn_label,
            highlight_tp, highlight_fp, arrow
        )
        
        # Final message
        final_message = Text("Bayes Theorem prevents us from confusing P(A|B) with P(B|A)", 
                           font_size=32)
        final_message.move_to(ORIGIN)
        final_message_bg = SurroundingRectangle(
            final_message, 
            fill_color=BLACK,
            fill_opacity=0.6,
            buff=0.3,
            color=WHITE
        )
        
        # Final explanation
        final_explanation = Text("P(Disease|Positive) ≠ P(Positive|Disease)", 
                               font_size=28)
        final_explanation.to_edge(DOWN, buff=0.5)
        if final_explanation.width > 12:
            final_explanation.scale(12/final_explanation.width)
        final_explanation_bg = SurroundingRectangle(
            final_explanation, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(all_rect_objects.animate.set_opacity(0.5))
        self.play(FadeOut(calculation))
        self.play(
            FadeIn(final_message_bg),
            Write(final_message)
        )
        self.play(
            FadeOut(conclusion_explanation_bg),
            FadeOut(conclusion_explanation),
            FadeIn(final_explanation_bg),
            Write(final_explanation)
        )
        self.wait(2)