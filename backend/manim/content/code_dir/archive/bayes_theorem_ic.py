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
        # Title in TOP ZONE
        title = Text("Bayes' Theorem", font_size=48)
        title.to_edge(UP, buff=0.5)
        
        # Subtitle below title
        subtitle = Text("Updating Beliefs with New Evidence", font_size=32)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        # Initial formula in MIDDLE ZONE
        bayes_formula = MathTex(
            r"P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}",
            font_size=40
        )
        bayes_formula.move_to(ORIGIN)
        
        # Explanatory text in BOTTOM ZONE with background
        explanation = Text("Bayes' theorem relates conditional probabilities P(A|B) and P(B|A)", font_size=30)
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
        
        # Animate introduction elements
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(subtitle))
        self.wait(0.5)
        self.play(
            FadeIn(explanation_bg),
            Write(explanation)
        )
        self.play(Write(bayes_formula))
        self.wait(1)
        
        # [00:05-00:12] Medical Test Example Setup
        # Move formula up
        new_formula_position = bayes_formula.copy()
        new_formula_position.shift(UP)
        
        # New explanation for example
        new_explanation = Text("Example: Medical Test for a Rare Disease (1% prevalence)", font_size=30)
        new_explanation.to_edge(DOWN, buff=0.5)
        if new_explanation.width > 12:
            new_explanation.scale(12/new_explanation.width)
        new_explanation_bg = SurroundingRectangle(
            new_explanation,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Create 2x2 grid
        grid = VGroup()
        
        # Cell background rectangles
        cell_width, cell_height = 3, 1
        positions = [
            [-cell_width/2, cell_height/2],  # Top-left
            [cell_width/2, cell_height/2],   # Top-right
            [-cell_width/2, -cell_height/2], # Bottom-left
            [cell_width/2, -cell_height/2]   # Bottom-right
        ]
        
        for pos in positions:
            cell = Rectangle(
                width=cell_width,
                height=cell_height,
                stroke_color=WHITE,
                fill_color=BLACK,
                fill_opacity=0.1
            )
            cell.move_to([pos[0], pos[1] - 0.5, 0])  # -0.5 to center at MIDDLE ZONE
            grid.add(cell)
        
        # Grid headers
        left_header = Text("Disease (D)", font_size=28)
        left_header.move_to([-cell_width/2, cell_height/2 + 0.5, 0])
        
        right_header = Text("No Disease (~D)", font_size=28)
        right_header.move_to([cell_width/2, cell_height/2 + 0.5, 0])
        
        top_header = Text("Positive Test (T)", font_size=28)
        top_header.move_to([0, cell_height + 0.5, 0])
        
        # Population value
        population = Text("Population: N = 1000", font_size=28)
        population.move_to([0, -2, 0])
        
        # Animate transition
        self.play(
            Transform(bayes_formula, new_formula_position),
            FadeOut(explanation_bg),
            FadeOut(explanation)
        )
        self.play(
            FadeIn(new_explanation_bg),
            Write(new_explanation)
        )
        self.play(
            Create(grid),
            Write(left_header),
            Write(right_header),
            Write(top_header),
            Write(population)
        )
        self.wait(1)
        
        # [00:12-00:18] Filling in the Prior Probabilities
        # Update explanation
        prior_explanation = Text("Prior probabilities: P(D) = 0.01, P(~D) = 0.99", font_size=30)
        prior_explanation.to_edge(DOWN, buff=0.5)
        if prior_explanation.width > 12:
            prior_explanation.scale(12/prior_explanation.width)
        prior_explanation_bg = SurroundingRectangle(
            prior_explanation,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Bottom left cell content
        bl_cell_text = MathTex(r"P(D) = 0.01 \rightarrow 10 \text{ people}", font_size=32)
        bl_cell_text.move_to(grid[2].get_center())
        
        # Bottom right cell content
        br_cell_text = MathTex(r"P(\sim D) = 0.99 \rightarrow 990 \text{ people}", font_size=32)
        br_cell_text.move_to(grid[3].get_center())
        
        # Animate
        self.play(
            FadeOut(new_explanation_bg),
            FadeOut(new_explanation),
            FadeIn(prior_explanation_bg),
            Write(prior_explanation)
        )
        self.play(Write(bl_cell_text))
        self.wait(0.5)
        self.play(Write(br_cell_text))
        self.wait(1)
        
        # Highlight animation
        self.play(
            Indicate(bl_cell_text),
            Indicate(grid[2])
        )
        self.play(
            Indicate(br_cell_text),
            Indicate(grid[3])
        )
        self.wait(1)
        
        # [00:18-00:22] Test Accuracy Information
        # Update explanation
        accuracy_explanation = Text("Test sensitivity: P(T|D) = 0.95, specificity: P(~T|~D) = 0.90", font_size=28)
        accuracy_explanation.to_edge(DOWN, buff=0.5)
        if accuracy_explanation.width > 12:
            accuracy_explanation.scale(12/accuracy_explanation.width)
        accuracy_explanation_bg = SurroundingRectangle(
            accuracy_explanation,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Top left cell content
        tl_cell_text = MathTex(r"P(T|D) = 0.95 \rightarrow 9.5 \text{ people}", font_size=32)
        tl_cell_text.move_to(grid[0].get_center())
        
        # Top right cell content
        tr_cell_text = MathTex(r"P(T|\sim D) = 0.10 \rightarrow 99 \text{ people}", font_size=32)
        tr_cell_text.move_to(grid[1].get_center())
        
        # Animate
        self.play(
            FadeOut(prior_explanation_bg),
            FadeOut(prior_explanation),
            FadeIn(accuracy_explanation_bg),
            Write(accuracy_explanation)
        )
        self.play(Write(tl_cell_text))
        self.wait(0.5)
        self.play(Write(tr_cell_text))
        self.wait(1)
        
        # Animate arrows for conditional probability flow
        arrow1 = Arrow(
            start=grid[2].get_top() + UP*0.1,
            end=grid[0].get_bottom() - DOWN*0.1,
            color=YELLOW
        )
        
        arrow2 = Arrow(
            start=grid[3].get_top() + UP*0.1,
            end=grid[1].get_bottom() - DOWN*0.1,
            color=YELLOW
        )
        
        self.play(
            Create(arrow1),
            Indicate(bl_cell_text),
            Indicate(tl_cell_text)
        )
        self.wait(0.5)
        self.play(
            Create(arrow2),
            Indicate(br_cell_text),
            Indicate(tr_cell_text)
        )
        self.wait(1)
        
        # [00:22-00:28] Bayes' Calculation
        # Update explanation
        bayes_explanation = Text("What is P(D|T)? The probability of disease given positive test", font_size=28)
        bayes_explanation.to_edge(DOWN, buff=0.5)
        if bayes_explanation.width > 12:
            bayes_explanation.scale(12/bayes_explanation.width)
        bayes_explanation_bg = SurroundingRectangle(
            bayes_explanation,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Specific Bayes formula
        specific_bayes = MathTex(
            r"P(D|T) = \frac{P(T|D) \cdot P(D)}{P(T)} = \frac{0.95 \cdot 0.01}{0.95 \cdot 0.01 + 0.10 \cdot 0.99}",
            font_size=36
        )
        specific_bayes.move_to([0, 1.5, 0])
        
        # Calculation steps
        calculation = MathTex(
            r"P(D|T) = \frac{9.5}{9.5 + 99} = \frac{9.5}{108.5} \approx 0.088",
            font_size=36
        )
        calculation.move_to([0, 0.5, 0])
        
        # Animate
        self.play(
            FadeOut(accuracy_explanation_bg),
            FadeOut(accuracy_explanation),
            FadeIn(bayes_explanation_bg),
            Write(bayes_explanation),
            FadeOut(arrow1),
            FadeOut(arrow2)
        )
        self.play(ReplacementTransform(bayes_formula, specific_bayes))
        self.wait(1)
        self.play(Write(calculation))
        self.wait(1)
        
        # Highlight connections between grid and formula
        self.play(
            Indicate(tl_cell_text),
            Indicate(specific_bayes)
        )
        self.wait(0.5)
        self.play(
            Indicate(bl_cell_text),
            Indicate(specific_bayes)
        )
        self.wait(0.5)
        self.play(
            Indicate(tr_cell_text),
            Indicate(specific_bayes)
        )
        self.wait(1)
        
        # [00:28-00:30] Conclusion
        # Final explanation
        final_explanation = Text("Despite positive test, only 8.8% chance of having the disease!", font_size=30)
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
        
        # Final formula
        final_formula = MathTex(
            r"P(D|T) \approx 0.088 \ll P(T|D) = 0.95",
            font_size=40
        )
        final_formula.move_to(ORIGIN)
        
        # Fade grid slightly
        faded_grid = VGroup(grid, tl_cell_text, tr_cell_text, bl_cell_text, br_cell_text,
                           left_header, right_header, top_header, population)
        
        # Animate
        self.play(
            FadeOut(bayes_explanation_bg),
            FadeOut(bayes_explanation),
            FadeIn(final_explanation_bg),
            Write(final_explanation),
            faded_grid.animate.set_opacity(0.5)
        )
        self.play(
            FadeOut(specific_bayes),
            ReplacementTransform(calculation, final_formula)
        )
        
        # Highlight the final result
        highlight_rect = SurroundingRectangle(final_formula, color=YELLOW, buff=0.2)
        self.play(Create(highlight_rect))
        self.wait(2)