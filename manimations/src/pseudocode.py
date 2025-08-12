import manim as m


class Pseudocode(m.Scene):
    def __init__(self, func, code):
        super().__init__()

        self.preamble: m.TexTemplate = m.TexTemplate()
        self.preamble.add_to_preamble(r"\usepackage{algorithm}")
        self.preamble.add_to_preamble(r"\usepackage{algpseudocode}")
        self.preamble.add_to_preamble(r"\usepackage[dvipsnames]{xcolor}")
        self.preamble.add_to_preamble(
            r"""
            \makeatletter
            \newcommand{\algcolor}[2]{%
              {\hskip-\ALG@thistlm}
              \colorbox{#1}{\parbox{10em}
              {\hskip\ALG@thistlm\relax #2}}%
            }
            \newcommand{\algemph}[1]{\algcolor{GreenYellow}{#1}}
            \makeatother
            """
        )

        self.environ = "algorithmic"
        self.func = func
        self.code = code

    def step_program(self, lines):
        """
        Highlight the lines in the program
        """

        def emph(code):
            # only modify the code starting the second word
            state = code.strip().split(" ")[0]
            line = f"\\algemph{{{' '.join(code.strip().split(' ')[1:])}}}"
            return f"{state} {line}\n"

        code = [
            code if line not in lines else emph(code)
            for line, code in enumerate(self.code)
        ]
        program = "\n".join(code)

        return m.Tex(program, tex_template=self.preamble, tex_environment=self.environ)

    def construct(self):
        program = self.step_program([])
        self.play(m.Write(program))
        self.wait()

        # TODO: generate the lines based on the trace of self.func()

        lines = [[1], [2], [3], [4]]
        for line in lines:
            old_program = program
            new_program = self.step_program(line)
            self.play(m.Transform(old_program, new_program))
            self.wait()
