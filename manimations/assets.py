from manim import *

class Lightbulb(VGroup):
    def __init__(self, radius=0.5, color=WHITE, fill_color=YELLOW, on=False):
        VGroup.__init__(self)

        bulb = Circle(radius=radius)

        filament = Text('~', color=color, width=radius/2)
        filament.next_to(filament, DOWN, buff=radius/8)

        base = Ellipse(width=radius/1.5, height=radius/6)
        base.next_to(bulb, DOWN, buff=radius/2)

        points = [bulb.point_at_angle(theta) for theta in [-PI/3, -2*PI/3]]
        points += [base.get_critical_point(dir) for dir in [LEFT, RIGHT]]

        base = Union(base, Polygon(*points), color=color, fill_color=GRAY, fill_opacity=1)
        bulb = Difference(bulb, base, color=color, fill_color=fill_color if on else color, fill_opacity=0.7 if on else 0.2)

        self.add(bulb)
        self.add(filament)
        self.add(base)
