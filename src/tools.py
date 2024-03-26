"""
# RSOXS Manim Tools
---
Manim tools for visualizing the in chamber sample and detector geometry for
the RSOXS insturment at 11.0.1.2. This is a collection of manim scenes and
animations that can be used to visualize the geometry of the RSOXS instrument.
"""

import numpy as np
import scipy
from manim import *


class Sample(Rectangle):
    def __init__(self, **kwargs):
        super().__init__(height=0.1, width=1, color=BLUE, **kwargs)
        self.shift(DOWN * 1.91)
        self.rotate(PI / 100)
        self.set_fill(BLUE, opacity=0.25)


class Stage(Rectangle):
    def __init__(self, **kwargs):
        super().__init__(height=1, width=4, color=BLUE_E, **kwargs)
        self.shift(DOWN * 2.5)
        self.rotate(PI / 100)
        self.set_fill(BLUE_E, opacity=1)


class Detector(Rectangle):
    def __init__(self, **kwargs):
        super().__init__(height=3, width=0.1, color=GREEN, **kwargs)
        self.shift(RIGHT * 5)
        self.set_fill(GREEN, opacity=1)


class Beam(TipableVMobject):
    def __init__(self, end, start=20 * LEFT, **kwargs) -> None:
        super().__init__(**kwargs)
        beams = []
        shift = 1
        opacity = 1 / 10

        for i in range(20):
            if i < 10:
                opacity += 0.1
            else:
                opacity -= 0.1

            beam_l = Line(
                start=start,
                end=end.get_center() * RIGHT,
                stroke_width=1.5,
                color=RED,
            )
            beam_l.set_opacity(opacity)
            beam_l.set_z_index(-2)
            beam_l.shift(DOWN * shift)
            shift -= 0.1

            beams.append(beam_l)
        self.beams = beams


class Geometry(Scene):
    def construct(self):
        sample = Sample()
        stage = Stage()
        detector = Detector()
        detector.set_z_index(1)
        sample_label = Text("Sample", font_size=20).next_to(sample, UP)
        stage_label = Text("Stage", font_size=20).move_to(stage.get_center())
        detector_label = Text("Photo Diode", font_size=20).next_to(detector, UP)

        self.play(
            DrawBorderThenFill(stage),
            Write(stage_label),
        )
        self.play(
            DrawBorderThenFill(sample),
            Write(sample_label),
        )
        self.play(
            DrawBorderThenFill(detector),
            Write(detector_label),
        )

        # constant velocity streamlines to the left
        func = lambda pos: np.array([2, 0, 0])
        stream_lines = StreamLines(
            func,
            stroke_width=1.5,
            max_anchors_per_line=30,
            x_range=[-10, detector.get_center()[0] - 3],
            y_range=[-0.5, 0.5],
        )

        stream_lines.set_z_index(-2)
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=False, flow_speed=1.5)

        beam = Beam(end=detector)
        beam_label = Text("X-rays")
        self.wait(1)
        self.play(*[Create(b) for b in beam.beams])
        self.play(Write(beam_label))
        self.wait(1)
        self.play(FadeOut(stream_lines))
        self.play(FadeOut(beam_label, sample_label, stage_label, detector_label))


class SampleZAlign(MovingCameraScene):
    def construct(self):
        sample = Sample()
        stage = Stage()
        detector = Detector()
        detector.set_z_index(1)
        beam_s = Beam(end=sample)
        beam_s.set_z_index(-2)
        beam_d = Beam(end=detector, start=ORIGIN)

        # Plot couts per size / beam profile.
        sigma = 0.25
        intensity = lambda z: (1 / 4 / np.sqrt(2 * np.pi) / sigma) * np.exp(
            -(z**2) / 2 / sigma**2
        )

        ax1 = Axes(
            y_range=[0, 2],
            x_range=[-1.5, 1.5],
            axis_config={"include_tip": False, "include_ticks": False},
            x_length=3,
            y_length=0,
            y_axis_config={"stroke_width": 0},
            x_axis_config={"stroke_width": 0},
        )
        ax1.rotate(-PI / 2)
        ax1.shift(6.1 * RIGHT)

        graph = ax1.plot(intensity, color=BLUE)

        label_bp = Text("Beam Profile", font_size=20).shift(6.2 * RIGHT).rotate(-PI / 2)

        # Add intensity vs Z to the scene to the right of the prior axes
        erf = lambda z: 1 - scipy.special.erf(z)
        z = ValueTracker(-2.5)
        ax = Axes(
            y_range=[0, 2],
            x_range=[-2.5, 2.5],
            axis_config={"include_tip": False, "include_ticks": False},
            x_length=8,
            y_length=1,
            y_axis_config={"stroke_width": 0},
        )

        ax.shift(2 * UP)
        graph1 = ax.plot(erf)

        label_i = Text("Intensity", font_size=20).shift(3 * UP)
        label_z = Text("Sample Z", font_size=20).shift(1.25 * UP)

        # Move sample and stage up to the valye of z

        sample.set_updater(lambda m: m.move_to(z.get_value(), 0))
        stage.set_updater(lambda m: m.move_to(z.get_value(), 0))

        geometry_group = VGroup(sample, stage, detector, *beam_s.beams, *beam_d.beams)

        self.add(geometry_group)
        self.wait(1)
        self.play(Create(ax1), Create(graph), Write(label_bp))
        self.play(Create(ax), Create(graph1), Write(label_i), Write(label_z))
        # self.add(dot)
        self.play(z.animate.set_value(1), run_time=3.5)  # upt to 1
        self.play(z.animate.set_value(-0.5), run_time=1.5)  # down to -.5
        self.play(z.animate.set_value(0.25), run_time=1)  # up to .25
        self.play(z.animate.set_value(-0.1), run_time=1)  # doen to -.1
        self.play(z.animate.set_value(0), run_time=1)  # up to 0


if __name__ == "__main__":
    module = SampleZAlign()
    module.render()
