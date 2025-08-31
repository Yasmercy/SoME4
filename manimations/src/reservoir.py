import manim as m
from item import LabeledBox


class Array(m.VGroup):
    def __init__(self, cap, size, colors=None, buff=0.1, texts=None, **kwargs):
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

        if texts is None:
            texts = [""] * cap
        elif not isinstance(texts, (list, tuple)):
            texts = [texts] * cap
        else:
            assert len(texts) <= cap
            texts = texts + [""] * (cap - size)

        # Build squares
        items = m.VGroup()
        for i in range(cap):
            sq = LabeledBox(
                side_length=1.0, text=texts[i], show_text=bool(texts[i]), **kwargs
            )
            opacity = 1 if i < size else 0
            sq.square.set_fill(colors[i], opacity=opacity)
            items.add(sq)
        items.arrange(m.RIGHT, buff=buff)
        # Build bbox
        bbox = m.SurroundingRectangle(items, color=m.WHITE, stroke_width=2)

        self.squares = items
        self.add(bbox, items)
