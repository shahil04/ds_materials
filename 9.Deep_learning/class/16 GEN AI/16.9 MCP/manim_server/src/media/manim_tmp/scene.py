
from manim import *

class CalculusExplainer(Scene):
    def construct(self):
        # Title
        title = Text("Calculus in the Real World", font_size=42, color=BLUE)
        subtitle = Text("Derivatives and Integrals, Step by Step", font_size=26, color=GRAY)
        subtitle.next_to(title, DOWN)
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---------- Step 1: Set up a real world scenario ----------
        step1 = Text("Step 1: A car driving down a road", font_size=32, color=YELLOW)
        step1.to_edge(UP)
        self.play(Write(step1))

        axes1 = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=5,
            y_length=4,
            axis_config={"include_tip": True, "color": WHITE},
        ).shift(LEFT * 3 + DOWN * 0.3)

        x_label1 = Text("time", font_size=20).next_to(axes1.x_axis, DOWN)
        y_label1 = Text("position", font_size=20).next_to(axes1.y_axis, LEFT).rotate(PI / 2).shift(RIGHT * 0.3)

        def pos_func(x):
            return 0.15 * x ** 2 + 0.2

        pos_graph = axes1.plot(pos_func, x_range=[0, 5.5], color=BLUE)
        pos_label = MathTex("x(t)", color=BLUE, font_size=32).next_to(pos_graph, UP, buff=0.1).shift(LEFT * 0.5)

        self.play(Create(axes1), Write(x_label1), Write(y_label1))
        self.play(Create(pos_graph), Write(pos_label))
        self.wait(1)
        self.play(FadeOut(step1))

        # ---------- Step 2: Derivative = instantaneous rate of change ----------
        step2 = Text("Step 2: How fast is the car going RIGHT NOW?", font_size=30, color=YELLOW)
        step2.to_edge(UP)
        self.play(Write(step2))
        self.wait(0.5)

        t0 = 3.0
        dt_vals = [1.5, 0.8, 0.3]
        dot = Dot(axes1.c2p(t0, pos_func(t0)), color=RED)
        self.play(FadeIn(dot))

        secant_lines = VGroup()
        for dt in dt_vals:
            t1 = t0 + dt
            p0 = axes1.c2p(t0, pos_func(t0))
            p1 = axes1.c2p(t1, pos_func(t1))
            slope_line = Line(p0, p0 + (p1 - p0) * 3, color=ORANGE, stroke_width=3)
            secant_lines.add(slope_line)

        self.play(Create(secant_lines[0]))
        self.wait(0.3)
        self.play(Transform(secant_lines[0], secant_lines[1]))
        self.wait(0.3)
        self.play(Transform(secant_lines[0], secant_lines[2]))
        self.wait(0.3)

        zoom_text = Text("As the interval shrinks to zero...", font_size=24, color=GRAY)
        zoom_text.next_to(axes1, DOWN, buff=0.6)
        self.play(Write(zoom_text))
        self.wait(1)

        tangent_slope = 0.3 * t0
        tangent_p0 = axes1.c2p(t0 - 1, pos_func(t0) - tangent_slope * 1)
        tangent_p1 = axes1.c2p(t0 + 1, pos_func(t0) + tangent_slope * 1)
        tangent_line = Line(tangent_p0, tangent_p1, color=RED, stroke_width=4)

        self.play(Transform(secant_lines[0], tangent_line), FadeOut(zoom_text))
        self.wait(0.5)

        derivative_eq = MathTex(
            r"\text{velocity} = \frac{dx}{dt} = \text{slope of tangent line}",
            font_size=30, color=RED
        ).shift(RIGHT * 3.3 + UP * 1.2)
        self.play(Write(derivative_eq))
        self.wait(1.5)
        self.play(FadeOut(step2))

        # ---------- Step 3: Clear and move to velocity graph ----------
        step3 = Text("Step 3: This gives us the velocity curve", font_size=30, color=YELLOW)
        step3.to_edge(UP)
        self.play(
            FadeOut(axes1), FadeOut(pos_graph), FadeOut(pos_label),
            FadeOut(x_label1), FadeOut(y_label1), FadeOut(dot),
            FadeOut(secant_lines[0]), FadeOut(derivative_eq),
            Write(step3),
        )
        self.wait(0.3)

        axes2 = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 3, 1],
            x_length=5.5,
            y_length=3.5,
            axis_config={"include_tip": True, "color": WHITE},
        ).shift(DOWN * 0.5)

        x_label2 = Text("time", font_size=20).next_to(axes2.x_axis, DOWN)
        y_label2 = Text("velocity", font_size=20).next_to(axes2.y_axis, LEFT).rotate(PI / 2).shift(RIGHT * 0.3)

        def vel_func(x):
            return 0.3 * x + 0.2

        vel_graph = axes2.plot(vel_func, x_range=[0, 5.5], color=GREEN)
        vel_label = MathTex("v(t)", color=GREEN, font_size=32).next_to(vel_graph, UP, buff=0.1).shift(RIGHT * 1)

        self.play(Create(axes2), Write(x_label2), Write(y_label2))
        self.play(Create(vel_graph), Write(vel_label))
        self.wait(1)
        self.play(FadeOut(step3))

        # ---------- Step 4: Integral = area under curve = total distance ----------
        step4 = Text("Step 4: How far did the car travel in total?", font_size=30, color=YELLOW)
        step4.to_edge(UP)
        self.play(Write(step4))
        self.wait(0.5)

        rects = axes2.get_riemann_rectangles(
            vel_graph, x_range=[0, 5], dx=0.5, color=[GREEN, TEAL], fill_opacity=0.5, stroke_width=0.5
        )
        self.play(Create(rects))
        self.wait(1)

        shrink_text = Text("As the strips get thinner and thinner...", font_size=24, color=GRAY)
        shrink_text.to_edge(DOWN)
        self.play(Write(shrink_text))

        rects2 = axes2.get_riemann_rectangles(
            vel_graph, x_range=[0, 5], dx=0.1, color=[GREEN, TEAL], fill_opacity=0.5, stroke_width=0.2
        )
        self.play(Transform(rects, rects2))
        self.wait(1)

        area = axes2.get_area(vel_graph, x_range=[0, 5], color=[GREEN, TEAL], opacity=0.5)
        self.play(Transform(rects, area), FadeOut(shrink_text))
        self.wait(0.5)

        integral_eq = MathTex(
            r"\text{distance} = \int_0^T v(t)\, dt = \text{area under the curve}",
            font_size=28, color=GREEN
        ).next_to(axes2, RIGHT, buff=0.3).shift(LEFT*0.3)
        integral_eq.to_edge(RIGHT).shift(UP*1.5)
        self.wait(0.2)
        self.play(FadeOut(step4))

        step4b = Text("Total distance = the shaded area", font_size=28, color=YELLOW)
        step4b.to_edge(UP)
        self.play(Write(step4b))
        self.wait(1.5)
        self.play(FadeOut(step4b))

        # ---------- Step 5: Connect them: Fundamental Theorem ----------
        step5 = Text("Step 5: Derivatives and integrals undo each other",
                      font_size=28, color=YELLOW)
        step5.to_edge(UP)
        self.play(
            FadeOut(axes2), FadeOut(vel_graph), FadeOut(vel_label),
            FadeOut(x_label2), FadeOut(y_label2), FadeOut(rects),
            Write(step5),
        )
        self.wait(0.3)

        pos_box = RoundedRectangle(width=3, height=1.2, color=BLUE, fill_opacity=0.2).shift(LEFT * 3.3)
        pos_box_label = MathTex("x(t)", r"\text{ position}", font_size=30).move_to(pos_box.get_center())

        vel_box = RoundedRectangle(width=3, height=1.2, color=GREEN, fill_opacity=0.2).shift(RIGHT * 3.3)
        vel_box_label = MathTex("v(t)", r"\text{ velocity}", font_size=30).move_to(vel_box.get_center())

        self.play(Create(pos_box), Write(pos_box_label))
        self.play(Create(vel_box), Write(vel_box_label))

        arrow_down = CurvedArrow(
            pos_box.get_right() + UP * 0.3, vel_box.get_left() + UP * 0.3, color=RED
        )
        arrow_down_label = MathTex(r"\text{differentiate}", font_size=22, color=RED).next_to(
            arrow_down, UP, buff=0.1
        )

        arrow_up = CurvedArrow(
            vel_box.get_left() + DOWN * 0.3, pos_box.get_right() + DOWN * 0.3, color=TEAL
        )
        arrow_up_label = MathTex(r"\text{integrate}", font_size=22, color=TEAL).next_to(
            arrow_up, DOWN, buff=0.1
        )

        self.play(Create(arrow_down), Write(arrow_down_label))
        self.play(Create(arrow_up), Write(arrow_up_label))
        self.wait(2)
        self.play(FadeOut(step5))

        # ---------- Conclusion ----------
        conclusion = Text("This is the Fundamental Theorem of Calculus",
                           font_size=30, color=YELLOW)
        conclusion.to_edge(UP)
        self.play(Write(conclusion))
        self.wait(1)

        apps_title = Text("Used every day in:", font_size=26, color=WHITE).shift(UP * 1.5)
        apps = VGroup(
            Text("• Physics: velocity, acceleration, force", font_size=22),
            Text("• Economics: marginal cost, profit optimization", font_size=22),
            Text("• Medicine: drug concentration over time", font_size=22),
            Text("• Engineering: stress, flow rates, signal processing", font_size=22),
            Text("• Machine learning: gradient descent", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).shift(DOWN * 0.3)

        self.play(
            FadeOut(pos_box), FadeOut(pos_box_label), FadeOut(vel_box), FadeOut(vel_box_label),
            FadeOut(arrow_down), FadeOut(arrow_down_label), FadeOut(arrow_up), FadeOut(arrow_up_label),
            FadeOut(conclusion),
        )
        self.play(Write(apps_title))
        for line in apps:
            self.play(FadeIn(line, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(2)

        final_eq = MathTex(
            r"\frac{d}{dt}\int_0^t f(\tau)\, d\tau = f(t)",
            font_size=48, color=BLUE
        )
        self.play(FadeOut(apps_title), FadeOut(apps))
        self.play(Write(final_eq))
        self.wait(2)
