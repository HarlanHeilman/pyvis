"""
# RSOXS Manim Tools
---
Manim tools for visualizing the in chamber sample and detector geometry for
the RSOXS insturment at 11.0.1.2. This is a collection of manim scenes and
animations that can be used to visualize the geometry of the RSOXS instrument.
"""

from manim import *
from numpy import short


class Sample(Rectangle):
    def __init__(self, **kwargs):
        super().__init__(height=0.1, width=1, color=BLUE, **kwargs)
        self.shift(DOWN * 1.7)
        self.rotate(PI / 100)
        self.set_fill(BLUE, opacity=0.25)


class Stage(Rectangle):
    def __init__(self, **kwargs):
        super().__init__(height=0.5, width=1.5, color=BLUE_E, **kwargs)
        self.shift(DOWN * 2)
        self.rotate(PI / 100)
        self.set_fill(BLUE_E, opacity=1)


class Detector(Rectangle):
    def __init__(self, **kwargs):
        super().__init__(height=3, width=0.1, color=GREEN, **kwargs)
        self.shift(RIGHT * 5)
        self.set_fill(GREEN, opacity=1)


class PrimalBeam(VGroup):
    def __init__(self, right, left = LEFT*10,**kwargs):
        super().__init__(**kwargs)
        self.beam = Line(
            start=left,
            end=right,
            color=YELLOW,
        )
        self.beam_halo_0 = self.beam.copy().set_stroke(width=10, opacity=0.5)
        self.beam_halo_1 = self.beam.copy().set_stroke(width=5, opacity=0.5)

        self.add(self.beam, self.beam_halo_0, self.beam_halo_1)

    def get_end(self):
        return self.beam.get_right()

    def set_end(self, end):
        self.beam.put_start_and_end_on(LEFT * 10, end)
        self.beam_halo_0.put_start_and_end_on(LEFT * 10, end)
        self.beam_halo_1.put_start_and_end_on(LEFT * 10, end)

class Beam(VGroup):
    def __init__(self, sample, detector,*vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)

        self.sample_beam = PrimalBeam(sample.get_center()[0])
        self.detector_beam = PrimalBeam(detector.get_center()[0], left=sample.get_center()[0])

        self.add(self.sample_beam, self.detector_beam)
    
    def 

class SampleDetectorGeometry(Scene):
    def construct(self):
        sample = Sample()
        stage = Stage()
        detector = Detector()

        self.play(Create(stage), Create(detector))
        self.play(Create(sample))


class VertAlign(Scene):
    def construct(self):
        sample = Sample()
        stage = Stage()
        detector = Detector()

        beam = Beam(detector.get_left())

        self.add(sample, stage, detector)
        self.play(Create(beam))

        def in_the_way(struc, beam):
            return struc.get_left()[0] < beam.get_end()[0]

        def update_beam(beam):
            if in_the_way(stage, beam):
                beam.set_end(stage.get_left()[0])
            if in_the_way(sample, beam):
                beam.set_end(sample.get_left()[0])
            else:
                beam.set_end(detector.get_left()[0])


if __name__ == "__main__":
    module = VertAlign()
    module.render()
