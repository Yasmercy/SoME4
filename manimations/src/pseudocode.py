import itertools as it

import manim as m
from resevoir import Array
from sample import Action


class Pseudocode(m.Scene):
    """
    TODO:

    1. Add two layouts, one with hidden code and one showing the code
        - if hidden code, then move the resevoir to the middle
        - if showing code, then move the resevoir to the bottom
    2. Flesh out the graphics more
        - rng can transform between a set of numbvers
        - colors can have a pattern (instead of solid)
    """

    def __init__(self, func, code, *args):
        super().__init__()
        self.func = func
        self.args = args
        self.code = code

        # mobject for the pseudocode
        self.program = m.Code(
            code_string="\n".join(self.code),
            language="python",
            background="window",
        ).to_corner(m.UP + m.RIGHT)

        lines = self.program.code_lines.submobjects
        width = self.program.get_width()
        height = lines[0].get_height()
        sep = lines[1].get_center()[1] - lines[0].get_center()[1]
        top = lines[0].get_center()[1]
        self.highlights = m.VGroup(
            [
                m.SurroundingRectangle(line, buff=0.05)
                .set_fill(m.YELLOW, opacity=0)
                .set_stroke(m.YELLOW, width=0)
                .stretch_to_fit_width(width)
                .stretch_to_fit_height(height)
                .align_to(self.program, m.LEFT)
                .set_y(top + i * sep)
                for i, line in enumerate(lines)
            ]
        )
        self.highlight = None

        # mobjects for the sampling
        self.resevoir = Array(5, 0).to_edge(m.DOWN)
        self.cursor = m.Square(side_length=1.0).to_corner(m.DOWN + m.RIGHT)
        self.rng_box = m.Square(side_length=1.0).next_to(self.cursor, m.LEFT, buff=0.05)
        self.rng_text = m.Text(".57").move_to(self.rng_box.get_center())

    def get_color(self, i):
        colors = [
            "blue",
            "teal",
            "green",
            "yellow",
            "gold",
            "red",
            "maroon",
            "purple",
        ]
        modifiers = ["a", "c", "e"]
        colors = ["_".join(x) for x in it.product(colors, modifiers)]
        return colors[i % len(colors)]

    def step_program(self, line):
        """
        Returns an animation that highlight the lines in the program
        """

        animations = []
        if self.highlight is not None:
            animations.append(self.highlights[self.highlight].animate.set_opacity(0))
        self.highlight = line
        animations.append(self.highlights[self.highlight].animate.set_opacity(0.3))
        return animations

    def step_animate(self, action, state):
        def animate_init(state):
            """
            Create an array for a resevoir, and two boxes:
                1. Generation of random number
                2. The item under the cursor

            The state is the initial resevoir.
            """

            # TODO: add an initial state to resevoir
            return [
                m.Create(self.resevoir),
                m.Create(self.cursor),
                m.Create(self.rng_box),
                m.Create(self.rng_text),
            ]

        def animate_read(state):
            """New integer flows into the lens. The state is the new item."""

            color = self.get_color(state)
            return [
                self.cursor.animate.set_fill(color, opacity=0.5),
            ]

        def animate_update(state):
            """Match transform the resevoir. The state is the new resevoir."""
            colors = [self.get_color(i) for i in state]
            old_resevoir = self.resevoir
            self.resevoir = Array(
                cap=max(5, len(state)), size=len(state), colors=colors
            ).to_edge(m.DOWN)
            return [
                m.ReplacementTransform(old_resevoir, self.resevoir),
            ]

        def animate_rand(state):
            """Add a new random number into the box. The state is the new number."""
            old_text = self.rng_text
            self.rng_text = m.Text(f"{state:.2f}").move_to(self.rng_box.get_center())
            return [
                m.ReplacementTransform(old_text, self.rng_text),
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
        animations = [
            m.Create(self.program),
            m.Create(self.highlights),
        ]
        return animations

    def construct(self):
        self.play(self.init_construction())

        trace = self.func(*self.args)
        for lines, action, state in trace:
            animations = self.step_program(lines) + self.step_animate(action, state)
            self.play(*animations)
