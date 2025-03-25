from manim import *
import numpy as np

class SupportVectorMachinesScene(Scene):

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
        title = Text("Support Vector Machines", font_size=48)
        title.to_edge(UP, buff=0.5)
        
        subtitle = Text("Finding the Optimal Decision Boundary", font_size=34)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        explanation = Text("SVMs find the hyperplane that maximizes the margin between classes", 
                           font_size=28)
        explanation.to_edge(DOWN, buff=0.5)
        
        explanation_bg = SurroundingRectangle(
            explanation, 
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Play introduction elements
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.play(FadeIn(explanation_bg), Write(explanation))
        self.wait(1)
        
        # [00:05-00:10] Data Points Introduction
        # Define the two classes of points
        class_plus_points = [
            [1.5, 0.8], [2.2, 1.2], [2.5, 0.7], [1.8, 1.5],
            [2.8, 1.7], [1.2, 0.4], [2.1, 0.9], [1.7, 1.3]
        ]
        
        class_minus_points = [
            [-1.5, -0.8], [-2.2, -1.2], [-2.5, -0.7], [-1.8, -1.5],
            [-2.8, -1.7], [-1.2, -0.4], [-2.1, -0.9], [-1.7, -1.3]
        ]
        
        # Create Dot objects
        plus_dots = VGroup(*[Dot(point=np.array([p[0], p[1], 0]), color=BLUE, radius=0.1) 
                             for p in class_plus_points])
        minus_dots = VGroup(*[Dot(point=np.array([p[0], p[1], 0]), color=RED, radius=0.1) 
                              for p in class_minus_points])
        
        # Update text explanation
        new_explanation = Text("SVM classifies data into two distinct classes", font_size=28)
        new_explanation.to_edge(DOWN, buff=0.5)
        
        # Play animations to introduce data points
        self.play(
            FadeOut(explanation),
            FadeIn(new_explanation),
            run_time=1
        )
        
        for dot in plus_dots:
            self.play(GrowFromCenter(dot), run_time=0.2)
        for dot in minus_dots:
            self.play(GrowFromCenter(dot), run_time=0.2)
        
        self.wait(1)
        
        # [00:10-00:15] Possible Decision Boundaries
        # Create different decision boundaries
        axes = Axes(
            x_range=[-5, 5],
            y_range=[-3, 3],
            axis_config={"include_tip": False, "include_numbers": False},
        ).scale(0.8)
        
        line1 = axes.get_graph(lambda x: 0.3 * x, x_range=[-5, 5], color=YELLOW)
        line2 = axes.get_graph(lambda x: -0.5 * x, x_range=[-5, 5], color=YELLOW)
        line3 = axes.get_graph(lambda x: -1 * x, x_range=[-5, 5], color=GREEN)
        
        line1_label = Text("Poor separation", font_size=24, color=YELLOW)
        line1_label.next_to(line1.point_from_proportion(0.7), UP, buff=0.5)
        
        line2_label = Text("Medium separation", font_size=24, color=YELLOW)
        line2_label.next_to(line2.point_from_proportion(0.7), UP, buff=0.5)
        
        line3_label = Text("Better separation", font_size=24, color=GREEN)
        line3_label.next_to(line3.point_from_proportion(0.7), UP, buff=0.5)
        
        # Update explanation
        explanation_3 = Text("Many possible lines can separate the data", font_size=28)
        explanation_3.to_edge(DOWN, buff=0.5)
        
        # Play animations for decision boundaries
        self.play(
            FadeOut(new_explanation),
            FadeIn(explanation_3)
        )
        
        # Show each line sequentially
        self.play(Create(line1), FadeIn(line1_label))
        self.wait(1)
        self.play(FadeOut(line1), FadeOut(line1_label))
        
        self.play(Create(line2), FadeIn(line2_label))
        self.wait(1)
        self.play(FadeOut(line2), FadeOut(line2_label))
        
        self.play(Create(line3), FadeIn(line3_label))
        self.wait(1)
        
        # [00:15-00:20] Margin Concept
        # Define margin lines
        upper_margin = axes.get_graph(lambda x: -1 * x + 2, x_range=[-5, 5], color=BLUE_C)
        lower_margin = axes.get_graph(lambda x: -1 * x - 2, x_range=[-5, 5], color=BLUE_C)
        
        # Create shaded margin region
        margin_region = Polygon(
            upper_margin.point_from_proportion(0),
            upper_margin.point_from_proportion(1),
            lower_margin.point_from_proportion(1),
            lower_margin.point_from_proportion(0),
            fill_color=BLUE,
            fill_opacity=0.2,
            stroke_width=0
        )
        
        # Mark support vectors
        support_vectors = [
            Dot(point=np.array([1.2, 0.4, 0]), color=YELLOW, radius=0.15),
            Dot(point=np.array([1.5, 0.8, 0]), color=YELLOW, radius=0.15),
            Dot(point=np.array([-1.2, -0.4, 0]), color=YELLOW, radius=0.15),
            Dot(point=np.array([-1.5, -0.8, 0]), color=YELLOW, radius=0.15)
        ]
        
        sv_labels = [
            Text("SV", font_size=20).next_to(sv, UR, buff=0.1)
            # for sv in support_vectors
        ]
        
        # Add labels for margin lines
        upper_margin_label = MathTex(r"\vec{w} \cdot \vec{x} + b = 1", font_size=24)
        upper_margin_label.next_to(upper_margin.point_from_proportion(0.3), UR, buff=0.2)
        
        lower_margin_label = MathTex(r"\vec{w} \cdot \vec{x} + b = -1", font_size=24)
        lower_margin_label.next_to(lower_margin.point_from_proportion(0.3), DR, buff=0.2)
        
        margin_width_label = MathTex(r"\text{Margin} = \frac{2}{||\vec{w}||}", font_size=30)
        margin_width_label.move_to(np.array([4, 0, 0]))
        
        optimal_line_label = Text("Optimal Hyperplane", font_size=24, color=GREEN)
        optimal_line_label.next_to(line3.point_from_proportion(0.3), UP, buff=0.3)
        
        # Update explanation
        explanation_4 = Text("SVM finds the line with maximum margin between classes", font_size=28)
        explanation_4.to_edge(DOWN, buff=0.5)
        
        # Play animations for margin concept
        self.play(
            FadeOut(explanation_3),
            FadeIn(explanation_4),
            FadeOut(line3_label)
        )
        
        self.play(
            Create(upper_margin),
            Create(lower_margin),
            FadeIn(margin_region),
            FadeIn(upper_margin_label),
            FadeIn(lower_margin_label),
            FadeIn(optimal_line_label)
        )
        
        self.play(FadeIn(margin_width_label))
        
        # Highlight support vectors
        for sv, label in zip(support_vectors, sv_labels):
            self.play(
                GrowFromCenter(sv),
                FadeIn(label),
                run_time=0.5
            )
        
        self.wait(1)
        
        # [00:20-00:25] Mathematical Formulation
        # Create mathematical formulation
        math_title = Text("Mathematical Formulation:", font_size=30)
        math_title.to_edge(UP, buff=0.5).to_edge(RIGHT, buff=1.0)
        
        primal_form = MathTex(
            r"\min \frac{1}{2}||\vec{w}||^2 \\",
            r"\text{subject to } y_i(\vec{w}\cdot\vec{x}_i + b) \geq 1",
            font_size=28
        )
        primal_form.next_to(math_title, DOWN, buff=0.3)
        
        math_bg = SurroundingRectangle(
            VGroup(math_title, primal_form),
            fill_color=BLACK,
            fill_opacity=0.7,
            buff=0.3,
            color=WHITE
        )
        
        # Update explanation
        explanation_5 = Text("Mathematically, we minimize ||w|| with constraints on classification", font_size=28)
        explanation_5.to_edge(DOWN, buff=0.5)
        
        # Play animations for mathematical formulation
        self.play(
            FadeOut(explanation_4),
            FadeIn(explanation_5)
        )
        
        self.play(
            FadeIn(math_bg),
            Write(math_title),
            Write(primal_form)
        )
        
        self.wait(2)
        
        # [00:25-00:30] Conclusion
        # Prepare for zoom out effect
        all_objects = VGroup(
            plus_dots, minus_dots, line3, margin_region,
            upper_margin, lower_margin, 
            VGroup(*support_vectors), VGroup(*sv_labels),
            upper_margin_label, lower_margin_label,
            margin_width_label, optimal_line_label
        )
        
        # Update explanation for conclusion
        explanation_6 = Text("SVMs are powerful for linear and non-linear classification", font_size=28)
        next_topic = Text("Next: Kernel Methods for Non-linear SVMs", font_size=34)
        
        explanation_6.to_edge(DOWN, buff=0.8)
        next_topic.to_edge(DOWN, buff=0.3)
        
        # Play final animations
        self.play(
            FadeOut(explanation_5),
            FadeIn(explanation_6),
            all_objects.animate.scale(0.9)
        )
        
        self.play(FadeIn(next_topic))
        
        # Final wait
        self.wait(2)