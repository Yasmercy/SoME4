import manim as m


class Pseudocode(m.Scene):
    def __init__(self, func, code, *args):
        super().__init__()
        self.func = func
        self.args = args
        self.code = code

    def init_program(self):
        code = [m.Text(t).set_color(m.WHITE) for t in self.code]
        return m.VGroup(code).arrange(direction=m.DOWN, aligned_edge=m.LEFT)

    def step_program(self, lines):
        """
        Highlight the lines in the program
        """

        def style_emph(line: m.Text):
            return line.set_color(m.YELLOW)

        def style_unemph(line: m.Text):
            return line.set_color(m.WHITE).set_opacity(0.5)

        code = [
            style_emph(m.Text(t)) if i in lines else style_unemph(m.Text(t))
            for i, t in enumerate(self.code)
        ]
        return m.VGroup(code).arrange(direction=m.DOWN, aligned_edge=m.LEFT)

    def construct(self):
        program = self.init_program()
        self.play(m.Write(program))

        lines = [line for line, action, state in self.func(*self.args)]
        for line in lines:
            old_program = program
            new_program = self.step_program(line)
            self.play(m.Transform(old_program, new_program))
