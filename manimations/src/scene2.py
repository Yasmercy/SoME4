import itertools as it

import manim as m
import numpy as np
from pseudocode import Action, Pseudocode, get_color
from reservoir import Array


class Scene2a(m.Scene):
    def construct(self):
        items = list(range(1, 11))
        rng = np.random.default_rng(1234)

        # create the input data
        array = Array(
            cap=10, size=10, texts=items, colors=[get_color(i) for i in items]
        ).to_edge(m.UP)

        # create a set of samples that will use later in the animation
        sample_items = [
            list(rng.choice(items, size=5, replace=False)) for _ in range(10)
        ]
        samples = [
            Array(
                cap=5,
                size=5,
                texts=sample_item,
                colors=[get_color(i) for i in sample_item],
            ).next_to(array, m.DOWN)
            for sample_item in sample_items
        ]

        # calculate the counts of how often each element appears in the sample
        counts = np.cumsum(
            np.eye(10)[np.array([np.array(x) - 1 for x in sample_items])].sum(axis=1),
            axis=0,
        )

        # animate an array A
        self.play(m.Create(array))
        self.wait(1)

        # transform that into a sample S (right below it)
        self.play(m.TransformFromCopy(array, samples[0]))
        self.wait(1)

        # add a histogram to the right
        subcounts = counts[:]
        chart = (
            m.BarChart(
                values=subcounts[0],
                bar_names=[str(i + 1) for i in range(10)],
                y_range=[0, max(subcounts[0]) + 1, 1],
                y_axis_config={
                    "include_numbers": False,  # remove numeric labels
                    "include_ticks": False,  # remove tick marks
                },
            )
            .scale_to_fit_width(self.camera.frame_width / 2)
            .to_corner(m.DOWN + m.RIGHT)
        )

        self.play(m.Create(chart))
        self.wait(1)

        for i in range(1, len(subcounts)):
            time = 0.3 if i < 10 else 0.1
            old_chart = chart
            chart = (
                m.BarChart(
                    values=subcounts[i],
                    bar_names=["8", "9"],
                    y_range=[0, max(subcounts[i]) + 1, 1],
                    y_axis_config={
                        "include_ticks": False,  # remove tick marks
                        "include_numbers": False,  # remove numeric labels
                    },
                )
                .scale_to_fit_width(self.camera.frame_width / 2)
                .to_corner(m.DOWN + m.RIGHT)
            )

            animate = m.AnimationGroup(
                m.ReplacementTransform(old_chart, chart),
                m.Transform(samples[i - 1], samples[i]),
                lag_ratio=0.0,
            )
            self.play(animate, run_time=time)
        self.wait(1)

        tex0 = m.Tex(r"$Pr( S = S_1 ) = Pr( S = S_2 ) = \ldots$").to_edge(m.LEFT)
        self.play(m.Write(tex0))
        self.wait(1)
        tex1 = m.Tex(r"$Pr( x_i \in S ) = Pr( x_j \in S)$").next_to(tex0, m.DOWN)
        self.play(m.Write(tex1))
        self.wait(1)


class Scene2b(Pseudocode):
    def __init__(self):
        def generate_stream(n):
            rng = np.random.default_rng(1337)
            for _ in range(n):
                yield int(rng.integers(n * n))

        def sample_permute(stream, k, rng):
            # 1. Initialize reservoir
            reservoir = []
            yield (0, Action.INIT, reservoir)

            for value in stream:
                # 2. Read item from stream
                yield (1, Action.READ, value)

                # 3. Add to reservoir
                reservoir.append(value)
                yield (2, Action.UPDATE, [(0, x) for x in reservoir])

            # 4. Permute reservoir
            reservoir = rng.permutation(reservoir)
            for _ in range(len(reservoir)):
                yield (3, Action.RAND, rng.random())
            yield (3, Action.UPDATE, [(0, x) for x in reservoir])

            # 5. Truncate reservoir
            reservoir = reservoir[:k]
            yield (4, Action.UPDATE, [(0, x) for x in reservoir])

        program_permute = [
            "resevoir = init_resevoir()",
            "for item in stream:",
            "    add(resevoir, item)",
            "permute(resevoir)",
            "truncate(resevoir, k)",
        ]

        super().__init__(sample_permute, program_permute)
        self.args = generate_stream(10), 5, np.random.default_rng(1234)

    def construct(self):
        self.play(self.animate_program_init())

        trace = self.func(*self.args)
        for lines, action, state in trace:
            animations = self.step_program(lines) + self.step_animate(action, state)
            self.play(*animations)
        self.wait(1)


class Scene2c(Pseudocode):
    def __init__(self):
        def generate_stream(n):
            rng = np.random.default_rng(1337)
            for _ in range(n):
                yield int(rng.integers(n * n))

        def sample_permute(stream, k, rng):
            # 1. Initialize reservoir
            reservoir = []
            yield (0, Action.INIT, reservoir)

            for value in stream:
                # 2. Read item from stream
                yield (1, Action.READ, value)

                # 3. Add to reservoir
                reservoir.append(value)
                yield (2, Action.UPDATE, list(enumerate(reservoir)))

            # 4. Permute reservoir
            reservoir = rng.permutation(reservoir)
            for _ in range(len(reservoir)):
                yield (3, Action.RAND, rng.random())
            yield (3, Action.UPDATE, list(enumerate(reservoir)))

            # 5. Truncate reservoir
            reservoir = reservoir[:k]
            yield (4, Action.UPDATE, list(enumerate(reservoir)))

        program_permute = [
            "resevoir = init_resevoir()",
            "for item in stream:",
            "    add(resevoir, item)",
            "permute(resevoir)",
            "truncate(resevoir, k)",
        ]

        super().__init__(sample_permute, program_permute)
        self.args = generate_stream(10), 5, np.random.default_rng(1234)

    def construct(self):
        self.play(self.animate_program_init())

        trace = self.func(*self.args)
        for lines, action, state in trace:
            animations = self.step_program(lines) + self.step_animate(action, state)
            self.play(*animations)
        self.wait(1)
