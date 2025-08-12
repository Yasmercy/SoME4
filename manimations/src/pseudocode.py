import manim as m


class Pseudocode(m.Scene):
    def __init__(self):
        super().__init__()
        self.preamble: m.TexTemplate = m.TexTemplate()
        self.preamble.add_to_preamble(r"\usepackage{algorithm}")
        self.preamble.add_to_preamble(r"\usepackage{algpseudocode}")
        self.preamble.add_to_preamble(r"\usepackage[dvipsnames]{xcolor}")
        self.preamble.add_to_preamble(
            r"""
            \makeatletter
            \newcommand{\algcolor}[2]{%
              \hskip-\ALG@thistlm\colorbox{#1}{\parbox{\dimexpr\linewidth-2\fboxsep}{\hskip\ALG@thistlm\relax #2}}%
            }
            \newcommand{\algemph}[1]{\algcolor{GreenYellow}{#1}}
            \makeatother
            """
        )

    def construct(self):
        code1 = r"""
        \begin{algorithmic}[1]
        	\Function{GenerateSample}{$D$, $k$} %1
                \State Initialize a resevoir with the first $k$ keys %2
                \For{each $i > k$ in increasing order} %3
                    \State $y_i \gets \mathop{uniform}()$ %4
                    \If{$y_i$ is in the lowest $k$ keys explored so far} %5
                        \State Update the resevoir to include $x_i$ (and remove the largest) %6
                    \EndIf %7
                \EndFor %8
        	\EndFunction %9
        \end{algorithmic}
        """

        alg1 = m.Tex(code1, tex_template=self.preamble)
        self.play(m.Write(alg1))
        self.wait()

        code2 = r"""
        \begin{algorithmic}[1]
        	\Function{GenerateSample}{$D$, $k$}
                \State Initialize a resevoir with the first $k$ keys
                \For{each $i > k$ in increasing order}
                    \State \algemph{$y_i \gets \mathop{uniform}()$}
                    \If{$y_i$ is in the lowest $k$ keys explored so far}
                        \State Update the resevoir to include $x_i$ (and remove the largest)
                    \EndIf
                \EndFor
        	\EndFunction
        \end{algorithmic}
        """

        alg2 = m.Tex(code2, tex_template=self.preamble)
        self.play(m.Transform(alg1, alg2))
        self.wait()

        # idea for API:
        # add a decorator for a python function
        # connect each line in the python with a line in the pseudocode
