from manim import *
import numpy as np

class RecursionScene(Scene):

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
        title = Text("Understanding Recursion", font_size=48)
        title.to_edge(UP, buff=1)
        
        subtitle = Text("A mathematical perspective", font_size=32)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(1)
        
        # [00:03-00:08] Concept: Recursive Definition
        # Create background rectangle for bottom text
        bottom_text = Text("A recursive function calls itself with simpler inputs", font_size=30)
        bottom_text.to_edge(DOWN, buff=0.7)
        bottom_text_bg = SurroundingRectangle(
            bottom_text,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Factorial definition
        factorial_def = MathTex(
            r"\text{factorial}(n) = \begin{cases}"
            r"1 & \text{if } n = 0 \\"
            r"n \times \text{factorial}(n-1) & \text{if } n > 0"
            r"\end{cases}"
        )
        factorial_def.scale(0.9)
        factorial_def.move_to(ORIGIN)
        
        # Base case label
        base_case_label = Text("Base case", font_size=24, color=YELLOW)
        base_case_label.next_to(factorial_def, LEFT, buff=1)
        base_arrow = Arrow(base_case_label.get_right(), factorial_def.get_corner(UL) + np.array([0.5, -0.2, 0]), color=YELLOW)
        
        # Recursive case label
        recursive_case_label = Text("Recursive case", font_size=24, color=GREEN)
        recursive_case_label.next_to(factorial_def, RIGHT, buff=1)
        recursive_arrow = Arrow(recursive_case_label.get_left(), factorial_def.get_corner(UR) + np.array([-1, -1, 0]), color=GREEN)
        
        self.play(
            FadeIn(bottom_text_bg),
            Write(bottom_text)
        )
        self.play(Write(factorial_def))
        self.play(
            FadeIn(base_case_label),
            Create(base_arrow),
            FadeIn(recursive_case_label),
            Create(recursive_arrow)
        )
        self.wait(2)
        
        # [00:08-00:15] Visualization: Factorial Example
        self.play(
            FadeOut(bottom_text_bg),
            FadeOut(bottom_text),
            FadeOut(base_case_label),
            FadeOut(base_arrow),
            FadeOut(recursive_case_label),
            FadeOut(recursive_arrow),
            FadeOut(factorial_def)
        )
        
        new_bottom_text = Text("Example: factorial(4) = 4 × 3 × 2 × 1 = 24", font_size=30)
        new_bottom_text.to_edge(DOWN, buff=0.7)
        new_bottom_text_bg = SurroundingRectangle(
            new_bottom_text,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Recursive call visualization
        call_1 = MathTex(r"\text{factorial}(4) = 4 \times \text{factorial}(3)")
        call_2 = MathTex(r"\text{factorial}(3) = 3 \times \text{factorial}(2)")
        call_3 = MathTex(r"\text{factorial}(2) = 2 \times \text{factorial}(1)")
        call_4 = MathTex(r"\text{factorial}(1) = 1 \times \text{factorial}(0)")
        call_5 = MathTex(r"\text{factorial}(0) = 1")
        
        call_1.shift(UP * 1)
        call_2.shift(UP * 0.5)
        call_3.shift(UP * 0)
        call_4.shift(DOWN * 0.5)
        call_5.shift(DOWN * 1)
        
        # Arrows connecting levels
        arrow_1 = Arrow(call_1.get_bottom() + np.array([0, 0.1, 0]), call_2.get_top() + np.array([0, -0.1, 0]), buff=0.1)
        arrow_2 = Arrow(call_2.get_bottom() + np.array([0, 0.1, 0]), call_3.get_top() + np.array([0, -0.1, 0]), buff=0.1)
        arrow_3 = Arrow(call_3.get_bottom() + np.array([0, 0.1, 0]), call_4.get_top() + np.array([0, -0.1, 0]), buff=0.1)
        arrow_4 = Arrow(call_4.get_bottom() + np.array([0, 0.1, 0]), call_5.get_top() + np.array([0, -0.1, 0]), buff=0.1)
        
        self.play(
            FadeIn(new_bottom_text_bg),
            Write(new_bottom_text)
        )
        
        self.play(Write(call_1))
        self.play(Create(arrow_1))
        self.play(Write(call_2))
        self.play(Create(arrow_2))
        self.play(Write(call_3))
        self.play(Create(arrow_3))
        self.play(Write(call_4))
        self.play(Create(arrow_4))
        self.play(Write(call_5))
        
        self.wait(2)
        
        # [00:15-00:22] Animation: Unwinding the Recursion
        unwinding_text = Text("Recursion unwinds from the base case upward", font_size=30)
        unwinding_text.to_edge(DOWN, buff=0.7)
        unwinding_text_bg = SurroundingRectangle(
            unwinding_text,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        self.play(
            FadeOut(new_bottom_text_bg),
            FadeOut(new_bottom_text),
            FadeIn(unwinding_text_bg),
            Write(unwinding_text)
        )
        
        # Highlight base case
        self.play(call_5.animate.set_color(YELLOW))
        
        # Unwinding calculations
        result_1 = MathTex(r"\text{factorial}(1) = 1 \times 1 = 1")
        result_2 = MathTex(r"\text{factorial}(2) = 2 \times 1 = 2")
        result_3 = MathTex(r"\text{factorial}(3) = 3 \times 2 = 6")
        result_4 = MathTex(r"\text{factorial}(4) = 4 \times 6 = 24")
        
        result_1.set_x(3).set_y(call_4.get_y())
        result_2.set_x(3).set_y(call_3.get_y())
        result_3.set_x(3).set_y(call_2.get_y())
        result_4.set_x(3).set_y(call_1.get_y())
        
        self.play(Write(result_1))
        self.play(call_4.animate.set_color(YELLOW))
        
        self.play(Write(result_2))
        self.play(call_3.animate.set_color(YELLOW))
        
        self.play(Write(result_3))
        self.play(call_2.animate.set_color(YELLOW))
        
        self.play(Write(result_4))
        self.play(call_1.animate.set_color(YELLOW))
        
        # Circle final result
        final_result = MathTex("24")
        final_result.move_to(result_4.get_right() + np.array([1, 0, 0]))
        final_result.scale(1.5)
        
        result_circle = Circle(radius=0.5, color=RED)
        result_circle.move_to(final_result)
        
        result_label = Text("Result", font_size=24, color=RED)
        result_label.next_to(result_circle, RIGHT, buff=0.5)
        
        self.play(FadeIn(final_result))
        self.play(Create(result_circle))
        self.play(Write(result_label))
        
        self.wait(2)
        
        # [00:22-00:27] Conclusion: Recursion Pattern
        self.play(
            FadeOut(call_1), FadeOut(call_2), FadeOut(call_3), FadeOut(call_4), FadeOut(call_5),
            FadeOut(arrow_1), FadeOut(arrow_2), FadeOut(arrow_3), FadeOut(arrow_4),
            FadeOut(result_1), FadeOut(result_2), FadeOut(result_3), FadeOut(result_4),
            FadeOut(final_result), FadeOut(result_circle), FadeOut(result_label),
            FadeOut(unwinding_text_bg), FadeOut(unwinding_text)
        )
        
        conclusion_text = Text("Recursion: Breaking down problems into simpler versions of themselves", font_size=30)
        conclusion_text.to_edge(DOWN, buff=0.7)
        conclusion_text_bg = SurroundingRectangle(
            conclusion_text,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # General recursion pattern
        pattern = MathTex(
            r"\text{solve}(\text{problem}) = \begin{cases}"
            r"\text{solution} & \text{if problem is simple} \\"
            r"\text{combine}(\text{solve}(\text{simpler\_problem})) & \text{otherwise}"
            r"\end{cases}"
        )
        pattern.scale(0.9)
        pattern.move_to(ORIGIN)
        
        self.play(
            FadeIn(conclusion_text_bg),
            Write(conclusion_text)
        )
        self.play(Write(pattern))
        
        # Base case label
        base_case_label = Text("Base case", font_size=24, color=YELLOW)
        base_case_label.next_to(pattern, LEFT, buff=1)
        base_arrow = Arrow(base_case_label.get_right(), pattern.get_corner(UL) + np.array([0.5, -0.2, 0]), color=YELLOW)
        
        # Recursive case label
        recursive_case_label = Text("Recursive case", font_size=24, color=GREEN)
        recursive_case_label.next_to(pattern, RIGHT, buff=1)
        recursive_arrow = Arrow(recursive_case_label.get_left(), pattern.get_corner(UR) + np.array([-1, -1, 0]), color=GREEN)
        
        self.play(
            FadeIn(base_case_label),
            Create(base_arrow),
            FadeIn(recursive_case_label),
            Create(recursive_arrow)
        )
        
        self.wait(3)