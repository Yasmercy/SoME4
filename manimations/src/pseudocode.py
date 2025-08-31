import itertools as it
from enum import Enum, auto

import manim as m
from item import LabeledBox
from reservoir import Array


def get_color(value):
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

    return colors[value % len(colors)]


class Action(Enum):
    # initializing the reservoir
    INIT = auto()
    # reading an element from the stream
    READ = auto()
    # updating the reservoir in some way
    UPDATE = auto()
    # generating a random number
    RAND = auto()
    # control flow
    BRANCH = auto()


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
        # sep = lines[1].get_center()[1] - lines[0].get_center()[1]
        # top = lines[0].get_center()[1]
        self.highlights = m.VGroup(
            [
                m.SurroundingRectangle(line, buff=0.05)
                .set_fill(m.YELLOW, opacity=0)
                .set_stroke(m.YELLOW, width=0)
                .stretch_to_fit_width(width)
                .stretch_to_fit_height(height)
                .align_to(self.program, m.LEFT)
                .align_to(line, m.DOWN)
                for i, line in enumerate(lines)
            ]
        )
        self.highlight = None

        # mobjects for the sampling
        self.resevoir = Array(5, 0).to_edge(m.LEFT)
        self.cursor = LabeledBox(side_length=1.0).to_corner(m.DOWN + m.RIGHT)
        self.rng = LabeledBox(text=".00", show_text=True).next_to(
            self.cursor, m.LEFT, buff=0.05
        )

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

            return [
                m.Create(self.resevoir),
                m.Create(self.cursor),
                m.Create(self.rng),
            ]

        def animate_read(state):
            """New integer flows into the lens. The state is the new item."""

            color = get_color(state)
            old_cursor = self.cursor
            self.cursor = LabeledBox(
                side_length=1.0, text=state, show_text=False
            ).to_corner(m.DOWN + m.RIGHT)
            self.cursor.square.set_fill(color, opacity=1)
            return [
                m.ReplacementTransform(old_cursor, self.cursor),
            ]

        def animate_update(state):
            """Match transform the resevoir. The state is the new resevoir."""
            colors = [get_color(i) for _, i in state]
            old_resevoir = self.resevoir
            texts = [f"{-key:.2f}"[1:] if key != 0 else "" for key, val in state]
            self.resevoir = Array(
                cap=max(5, len(state)), size=len(state), colors=colors, texts=texts
            ).to_edge(m.LEFT)
            return [
                m.ReplacementTransform(old_resevoir, self.resevoir),
            ]

        def animate_rand(state):
            """Add a new random number into the box. The state is the new number."""
            old_rng = self.rng
            self.rng = LabeledBox(text=f"{state:.2f}"[1:], show_text=True).next_to(
                self.cursor, m.LEFT, buff=0.05
            )
            return [
                m.ReplacementTransform(old_rng, self.rng),
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

    def animate_program_init(self):
        animations = [
            m.Create(self.program),
            m.Create(self.highlights),
        ]
        return animations

    def construct(self):
        # TODO: add an option to toggle visibility of the program/highlights
        self.play(self.init_construction())

        trace = self.func(*self.args)
        for lines, action, state in trace:
            animations = self.step_program(lines) + self.step_animate(action, state)
            self.play(*animations)
