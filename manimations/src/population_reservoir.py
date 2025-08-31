import itertools as it

import manim as m
from sample import Action

POP_SIZE = 20
RES_SIZE = 3

class Array(m.VGroup):
    def __init__(self, cap, size, values=None, colors=None, buff=0.1, **kwargs):
        """
        Create a horizontal array of squares with number labels.

        Args:
            cap (int): Maximum capacity (total squares).
            size (int): Number of active elements (≤ cap).
            values (list[int] or None): Values to show inside squares.
                                        If None, squares are empty.
            buff (float): Spacing between squares.
            **kwargs: Passed to Square (e.g. stroke_color).
        """
        super().__init__(**kwargs)

        if values is None:
            values = [""] * cap
        else:
            values = list(values) + [""] * (max(0, cap - len(values)))

        squares = m.VGroup()
        labels = m.VGroup()

        for i in range(cap):
            sq = m.Square(side_length=0.5, **kwargs)
            if i < size:
                sq.set_fill(colors[i] if colors is not None else m.GRAY, opacity=1)
                lbl = m.Text("{:.2f}".format(-values[i])[1:], font_size=14).move_to(sq.get_center())
            else:
                sq.set_fill(m.WHITE, opacity=0.0)
                lbl = m.Text("_", font_size=14).move_to(sq.get_center())

            squares.add(sq)
            labels.add(lbl)

        squares.arrange(m.RIGHT, buff=buff)

        # align labels with squares
        for sq, lbl in zip(squares, labels):
            lbl.move_to(sq.get_center())

        bbox = m.SurroundingRectangle(squares, color=m.WHITE, stroke_width=2)

        self.add(bbox, squares, labels)
        self.squares = squares
        self.values = values
        self.labels = labels


class PopulationReservoir(m.Scene):
    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args

        # mobjects for the sampling
        self.reservoir = Array(RES_SIZE, 0).to_edge(m.DOWN)
        self.cursor = m.Square(side_length=1.0).to_corner(m.DOWN + m.RIGHT)

        # display a record of the stream, highlighting
        self.history = Array(POP_SIZE, 0).center()
        self.keys = []
        self.colors = []
 
    def step_animate(self, action, state):
        def animate_init(state):
            """
            Create an array for a reservoir, and two boxes:
                1. Generation of random number
                2. The item under the cursor

            The state is the initial reservoir.
            """

            return [
                m.Create(self.reservoir),
            ]

        def animate_read(state):
            """New integer flows into the lens. The state is the new item."""
            return []


        def animate_update(state):
            
            """Match transform the reservoir. The state is the new reservoir."""
            
            old_reservoir = self.reservoir
            self.reservoir = Array(
                cap=max(RES_SIZE, len(state)), size=len(state),
                values = state,
                colors = [m.RED] * len(state)
            ).to_edge(m.DOWN)
            return [
                #m.FadeIn(self.reservoir),
                #m.FadeOut(old_reservoir)
                m.ReplacementTransform(old_reservoir, self.reservoir)
            ]

        def animate_rand(state):
            
            """Add a new random number into the box. The state is the new number."""
            self.keys += [-state]
            if -state in sorted(self.keys, reverse=True)[0:RES_SIZE]:
                self.colors += [m.RED]
            else:
                self.colors += [m.GRAY]

            old_history = self.history
            self.history = Array(
                    cap = POP_SIZE, size = len(self.keys),
                    values = self.keys,
                    colors = self.colors
            )
            return [
                #m.FadeIn(self.history),
                #m.FadeOut(old_history),
                m.ReplacementTransform(old_history, self.history)
            ]

        def animate_branch(state):
            
            """Do nothing"""
            return []

        animations = {
            Action.INIT: animate_init,
            Action.READ: animate_read,
            Action.UPDATE: animate_update,
            Action.RAND: animate_rand,
            Action.BRANCH: animate_branch,
        }
        return animations[action](state)

    def init_construction(self):
        animations = [m.Create(self.history)]
        return animations

    def construct(self):
        self.play(self.init_construction())

        trace = self.func(*self.args)
        for lines, action, state in trace:
            animations = self.step_animate(action, state)
            if (animations != []):
                self.play(*animations)
        self.wait()
        # highlight the intervals
        interval_start = self.history.squares[0].get_edge_center(m.DOWN)
        prev_idx = 0
        for i,color in enumerate(self.colors[1:]):
            if color == m.RED:
                curr_idx = i+1
                interval_end = self.history.squares[curr_idx].get_edge_center(m.DOWN)
                # draw thing
                interval = m.BraceBetweenPoints(interval_start, interval_end).scale(0.75)
                label = m.Text(str(curr_idx - prev_idx)).next_to(interval, m.DOWN, aligned_edge=m.UP)
                self.play(m.Create(interval), m.Create(label))
                interval_start = interval_end
                prev_idx = i+1
