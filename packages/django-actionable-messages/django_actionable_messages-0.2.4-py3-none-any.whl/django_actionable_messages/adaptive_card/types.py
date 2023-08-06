from django_actionable_messages.adaptive_card.utils import HorizontalAlignment, VerticalAlignment, FillMode
from django_actionable_messages.mixins import CardElement


class BackgroundImage(CardElement):
    def __init__(self, url: str, fill_mode: FillMode = None, horizontal_alignment: HorizontalAlignment = None,
                 vertical_alignment: VerticalAlignment = None, **kwargs):
        self._data = {
            "url": url
        }
        super().__init__(**kwargs)
        if fill_mode is not None:
            self.set_fill_mode(fill_mode)
        if horizontal_alignment is not None:
            self.set_horizontal_alignment(horizontal_alignment)
        if vertical_alignment is not None:
            self.set_vertical_alignment(vertical_alignment)

    def set_url(self, url: str):
        self._data["url"] = url

    def set_fill_mode(self, fill_mode: FillMode):
        self._data["fillMode"] = fill_mode

    def set_horizontal_alignment(self, alignment: HorizontalAlignment):
        self._data["horizontalAlignment"] = alignment

    def set_vertical_alignment(self, alignment: VerticalAlignment):
        self._data["verticalAlignment"] = alignment
