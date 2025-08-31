import manim as m


class LabeledBox(m.VGroup):
    def __init__(self, side_length: int = 1, text: str = "", show_text: bool = False):
        super().__init__()

        self.square = m.Square(side_length=side_length)
        self.text = m.Text(str(text))
        self.set_text_visible(show_text)
        self.add(self.square, self.text)

    def set_text_visible(self, visible: bool):
        opacity = 1 if visible else 0
        self.text.set_opacity(opacity)
        return self
