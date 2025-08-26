import manim as m


class Array(m.VGroup):
    def __init__(self, cap, size, colors=None, buff=0.1, **kwargs):
        """
        Create a horizontal array of squares.

        Args:
            n (int): Number of squares.
            size (float): Side length of each square.
            colors (list or single color):
                If a list, it must have length n.
                If a single color, it’s applied to all squares.
            buff (float): Spacing between squares.
            **kwargs: Passed to Square (e.g. stroke_color).
        """
        super().__init__(**kwargs)

        if colors is None:
            colors = [m.WHITE] * cap
        elif not isinstance(colors, (list, tuple)):
            colors = [colors] * cap
        else:
            assert len(colors) <= cap
            colors = colors + [m.WHITE] * (cap - size)

        # Build squares
        squares = m.VGroup()
        for i in range(size):
            sq = m.Square(side_length=1.0, **kwargs)
            sq.set_fill(colors[i], opacity=1.0)
            squares.add(sq)
        for i in range(size, cap):
            sq = m.Square(side_length=1.0, **kwargs)
            sq.set_fill(colors[i], opacity=0.0)
            squares.add(sq)
        squares.arrange(m.RIGHT, buff=buff)
        # Build bbox
        bbox = m.SurroundingRectangle(squares, color=m.WHITE, stroke_width=2)

        self.add(bbox, squares)
