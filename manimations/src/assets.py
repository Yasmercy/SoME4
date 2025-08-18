from manim import *

class Lightbulb(VGroup):
    def __init__(self, radius=0.5, color=WHITE, fill_color=YELLOW, on=False):
        VGroup.__init__(self)

        bulb = Circle(radius=radius)

        filament = Text('~', color=color, width=radius/2)
        filament.next_to(filament, DOWN, buff=radius/2)

        base = Ellipse(width=radius*0.75, height=radius/6)
        base.next_to(bulb, DOWN, buff=radius/4)

        points = [bulb.point_at_angle(theta) for theta in [-PI/3, -2*PI/3]]
        points += [base.get_critical_point(dir) for dir in [LEFT, RIGHT]]

        base = Union(base, Polygon(*points))
        bulb = Union(bulb, base, color=color, fill_color=fill_color if on else color, fill_opacity=0.7 if on else 0.2)

        base.next_to(base, DOWN, buff=-radius/4)
        base = Union(base, base.copy().next_to(base, DOWN, buff=-radius/8)) #color=color, fill_color=GRAY, fill_opacity=1)

        self.add(bulb)
        self.add(filament)
        base = Union(base, Ellipse(width=radius/2,height=radius/3).move_to(base.get_critical_point(DOWN)), color=color, fill_color=GRAY, fill_opacity=1)
        self.add(base)
