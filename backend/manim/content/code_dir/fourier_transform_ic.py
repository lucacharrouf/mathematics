from manim import *
import numpy as np

class FourierTransformScene(Scene):

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
        # Title at TOP ZONE
        title = Text("Fourier Transform: Time to Frequency Domain", font_size=40)
        title.to_edge(UP, buff=0.5)
        if title.width > 12:
            title.scale(12/title.width)
        
        # Subtitle below title
        subtitle = Text("Decomposing signals into frequency components", font_size=30)
        subtitle.next_to(title, DOWN, buff=0.3)
        if subtitle.width > 12:
            subtitle.scale(12/subtitle.width)
        
        # Explanatory text in BOTTOM ZONE with background
        explanation = Text("The Fourier Transform converts a time-domain signal into its frequency representation", 
                          font_size=28)
        if explanation.width > 12:
            explanation.scale(12/explanation.width)
        explanation.to_edge(DOWN, buff=0.8)
        
        explanation_bg = SurroundingRectangle(
            explanation,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Play introduction animations
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeIn(subtitle))
        self.wait(0.5)
        self.play(FadeIn(explanation_bg), Write(explanation))
        self.wait(1)
        
        # [00:05-00:12] Time Domain Signal
        # Create time domain axes
        time_axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=8,
            y_length=4,
            axis_config={"include_tip": False, "numbers_to_include": [-4, -2, 0, 2, 4]}
        ).move_to(ORIGIN)
        
        # Add labels to axes
        time_x_label = Text("Time (s)", font_size=24).next_to(time_axes.x_axis, DOWN, buff=0.3)
        time_y_label = Text("Amplitude", font_size=24).next_to(time_axes.y_axis, LEFT, buff=0.3)
        time_domain = VGroup(time_axes, time_x_label, time_y_label)
        
        # Define the composite signal function: f(t) = sin(2πt) + 0.5sin(6πt)
        def signal_func(t):
            return np.sin(2*np.pi*t) + 0.5*np.sin(6*np.pi*t)
        
        # Create the signal graph
        signal_graph = time_axes.plot(signal_func, color=WHITE)
        
        # Create formula for the signal
        formula = MathTex(r"f(t) = \sin(2\pi t) + 0.5\sin(6\pi t)", font_size=36)
        formula.next_to(explanation_bg, UP, buff=0.2)
        formula_bg = SurroundingRectangle(
            formula,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Play time domain animations
        self.play(Create(time_domain))
        self.wait(0.5)
        self.play(Create(signal_graph), run_time=1.5)
        self.play(FadeIn(formula_bg), Write(formula))
        self.wait(1)
        
        # [00:12-00:20] Transform Process
        # Update explanatory text
        new_explanation = Text("The Fourier Transform identifies frequency components present in the signal", 
                              font_size=28)
        if new_explanation.width > 12:
            new_explanation.scale(12/new_explanation.width)
        new_explanation.move_to(explanation)
        
        # Fourier Transform equation
        transform_eq = MathTex(r"F(\omega) = \int f(t)e^{-i\omega t}dt", font_size=36)
        transform_eq.move_to(formula)
        transform_eq_bg = SurroundingRectangle(
            transform_eq,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Define component functions
        def component1(t):
            return np.sin(2*np.pi*t)
        
        def component2(t):
            return 0.5*np.sin(6*np.pi*t)
        
        # Create component graphs
        component1_graph = time_axes.plot(component1, color=RED)
        component2_graph = time_axes.plot(component2, color=BLUE)
        
        # Labels for components
        comp1_label = MathTex(r"\sin(2\pi t)", color=RED, font_size=28)
        comp1_label.next_to(time_axes.c2p(4, 1), RIGHT, buff=0.2)
        
        comp2_label = MathTex(r"0.5\sin(6\pi t)", color=BLUE, font_size=28)
        comp2_label.next_to(time_axes.c2p(4, -1), RIGHT, buff=0.2)
        
        # Play transform animations
        self.play(
            FadeOut(explanation),
            FadeIn(new_explanation),
            run_time=0.8
        )
        self.play(
            FadeOut(formula_bg),
            FadeOut(formula),
            FadeIn(transform_eq_bg),
            FadeIn(transform_eq),
            run_time=1
        )
        self.wait(0.5)
        
        # Clone original signal for animation
        comp1_copy = component1_graph.copy()
        comp2_copy = component2_graph.copy()
        
        # Animate components separating
        self.play(
            Transform(signal_graph, comp1_copy),
            signal_graph.animate.shift(UP),
            run_time=1.5
        )
        self.play(
            FadeIn(component2_graph),
            component2_graph.animate.shift(DOWN*2),
            run_time=1.5
        )
        
        # Add labels to components
        self.play(
            FadeIn(comp1_label), 
            FadeIn(comp2_label)
        )
        self.wait(1)
        
        # [00:20-00:30] Frequency Domain Result
        # Fade out time domain elements
        self.play(
            FadeOut(signal_graph),
            FadeOut(comp1_label),
            FadeOut(component2_graph),
            FadeOut(comp2_label),
            FadeOut(time_domain),
            run_time=1
        )
        
        # Create frequency domain axes
        freq_axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 1.5, 0.5],
            x_length=8,
            y_length=4,
            axis_config={"include_tip": False}
        ).move_to(ORIGIN)
        
        # Add labels to frequency axes
        freq_x_label = Text("Frequency (Hz)", font_size=24).next_to(freq_axes.x_axis, DOWN, buff=0.3)
        freq_y_label = Text("Magnitude", font_size=24).next_to(freq_axes.y_axis, LEFT, buff=0.3)
        freq_domain = VGroup(freq_axes, freq_x_label, freq_y_label)
        
        # Create frequency spikes
        spike1 = Line(
            freq_axes.c2p(1, 0),
            freq_axes.c2p(1, 1),
            color=RED,
            stroke_width=4
        )
        spike1_dot = Dot(freq_axes.c2p(1, 1), color=RED)
        
        spike3 = Line(
            freq_axes.c2p(3, 0),
            freq_axes.c2p(3, 0.5),
            color=BLUE,
            stroke_width=4
        )
        spike3_dot = Dot(freq_axes.c2p(3, 0.5), color=BLUE)
        
        # Labels for frequency spikes
        spike1_label = Text("1 Hz", font_size=20, color=RED)
        spike1_label.next_to(spike1_dot, UP, buff=0.1)
        
        spike3_label = Text("3 Hz", font_size=20, color=BLUE)
        spike3_label.next_to(spike3_dot, UP, buff=0.1)
        
        # Final explanatory text
        final_explanation = Text("The Fourier Transform reveals two frequency components: 1 Hz and 3 Hz with magnitudes 1.0 and 0.5", 
                                font_size=24)
        if final_explanation.width > 12:
            final_explanation.scale(12/final_explanation.width)
        final_explanation.move_to(new_explanation)
        final_explanation_bg = SurroundingRectangle(
            final_explanation,
            fill_color=BLACK,
            fill_opacity=0.8,
            buff=0.2,
            color=WHITE
        )
        
        # Play frequency domain animations
        self.play(Create(freq_domain))
        self.wait(0.5)
        
        self.play(
            Create(spike1),
            FadeIn(spike1_dot),
            Create(spike1_label),
            run_time=1
        )
        
        self.play(
            Create(spike3),
            FadeIn(spike3_dot),
            Create(spike3_label),
            run_time=1
        )
        
        self.play(
            FadeOut(new_explanation),
            FadeOut(transform_eq_bg),
            FadeOut(transform_eq),
            FadeIn(final_explanation_bg),
            Write(final_explanation),
            run_time=1.5
        )
        
        self.wait(2)