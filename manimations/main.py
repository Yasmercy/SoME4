from manim import *
from assets import *

class Test(Scene):
    def construct(self):
        self.wait()
        lb1 = Lightbulb(radius=1.3)
        lb2 = Lightbulb(on=True).next_to(lb1)
        self.play(Create(lb1))
        self.play(Create(lb2))
        self.wait()
