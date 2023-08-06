from typing import Union, List

from django_actionable_messages.adaptive_card.mixins import ElementMixin
from django_actionable_messages.adaptive_card.types import BackgroundImage
from django_actionable_messages.adaptive_card.utils import (
    FallbackOption, Style, VerticalAlignment, SpacingStyle, ImageSize, Width
)
from django_actionable_messages.exceptions import CardException
from django_actionable_messages.mixins import CardElement


class ActionSet(ElementMixin):
    def __init__(self, actions: list, **kwargs):
        self._data = {
            "type": "ActionSet"
        }
        super().__init__(**kwargs)
        self._set_base_actions(actions)

    def _set_base_actions(self, actions: list):
        self._data["actions"] = self._get_items_list(actions)

    def add_actions(self, actions):
        if isinstance(actions, (list, set, tuple)):
            self._data["actions"].extend(self._get_items_list(actions))
        else:
            self._data["actions"].append(actions.as_data())


class Container(ElementMixin):
    def __init__(self, items: list, select_action=None, style: Style = None,
                 vertical_content_alignment: VerticalAlignment = None, bleed: bool = None,
                 background_image: Union[str, BackgroundImage] = None, min_height: str = None, **kwargs):
        self._data = {
            "type": "Container"
        }
        super().__init__(**kwargs)
        self._set_base_items(items)
        if select_action:
            self.set_select_action(select_action)
        if style is not None:
            self.set_style(style)
        if vertical_content_alignment:
            self.set_vertical_content_alignment(vertical_content_alignment)
        if bleed is not None:
            self.set_bleed(bleed)
        if background_image is not None:
            self.set_background_image(background_image)
        if min_height is not None:
            self.set_min_height(min_height)

    def _set_base_items(self, items: list):
        self._data["items"] = self._get_items_list(items)

    def add_items(self, items):
        if isinstance(items, (list, set, tuple)):
            self._data["items"].extend(self._get_items_list(items))
        else:
            self._data["items"].append(items.as_data())

    def set_select_action(self, action):
        self._data["selectAction"] = action.as_data()

    def set_style(self, style: Style):
        self._data["style"] = style

    def set_vertical_content_alignment(self, alignment: VerticalAlignment):
        self._data["verticalContentAlignment"] = alignment

    def set_bleed(self, value=True):
        self._data["bleed"] = value

    def set_background_image(self, image: Union[str, BackgroundImage]):
        if isinstance(image, str):
            self._data["backgroundImage"] = image
        elif isinstance(image, BackgroundImage):
            self._data["backgroundImage"] = image.as_data()
        else:
            raise CardException("Invalid image type")

    def set_min_height(self, height: str):
        self._data["minHeight"] = height


class Column(CardElement):
    def __init__(self, items: list = None, background_image: Union[str, BackgroundImage] = None, bleed: bool = None,
                 fallback=None, min_height: str = None, separator: bool = None, spacing: SpacingStyle = None,
                 select_action=None, style: Style = None, vertical_content_alignment: VerticalAlignment = None,
                 width: Union[str, int, Width] = None, item_id: str = None, is_visible: bool = None,
                 requires: dict = None, **kwargs):
        self._data = {
            "type": "Column"
        }
        super().__init__(**kwargs)
        if items:
            self.add_items(items)
        if background_image is not None:
            self.set_background_image(background_image)
        if bleed is not None:
            self.set_bleed(bleed)
        if fallback is not None:
            self.set_fallback(fallback)
        if min_height is not None:
            self.set_min_height(min_height)
        if separator is not None:
            self.set_separator(separator)
        if spacing is not None:
            self.set_spacing(spacing)
        if select_action is not None:
            self.set_select_action(select_action)
        if style is not None:
            self.set_style(style)
        if vertical_content_alignment:
            self.set_vertical_content_alignment(vertical_content_alignment)
        if width is not None:
            self.set_width(width)
        if item_id is not None:
            self.set_id(item_id)
        if is_visible is not None:
            self.set_is_visible(is_visible)
        if requires is not None:
            self.set_requires(requires)

    def add_items(self, items):
        self._data.setdefault("items", [])
        if isinstance(items, (list, set, tuple)):
            self._data["items"].extend(self._get_items_list(items))
        else:
            self._data["items"].append(items.as_data())

    def set_background_image(self, image: Union[str, BackgroundImage]):
        if isinstance(image, str):
            self._data["backgroundImage"] = image
        elif isinstance(image, BackgroundImage):
            self._data["backgroundImage"] = image.as_data()
        else:
            raise CardException("Invalid image type")

    def set_bleed(self, value=True):
        self._data["bleed"] = value

    def set_fallback(self, fallback):
        if isinstance(fallback, FallbackOption):
            self._data["fallback"] = fallback
        elif isinstance(fallback, Column):
            self._data["fallback"] = fallback.as_data()
        else:
            raise CardException("Invalid fallback type")

    def set_min_height(self, height: str):
        self._data["minHeight"] = height

    def set_separator(self, value=True):
        self._data["separator"] = value

    def set_spacing(self, spacing: SpacingStyle):
        self._data["spacing"] = spacing

    def set_select_action(self, action):
        self._data["selectAction"] = action.as_data()

    def set_style(self, style: Style):
        self._data["style"] = style

    def set_vertical_content_alignment(self, alignment: VerticalAlignment):
        self._data["verticalContentAlignment"] = alignment

    def set_width(self, width: Union[str, int, Width]):
        if isinstance(width, Width):
            self._data["width"] = width
        elif isinstance(width, (str, int)):
            self._data["width"] = width
        else:
            raise CardException("Invalid width type")

    def set_id(self, item_id: str):
        self._data["id"] = item_id

    def set_is_visible(self, value=True):
        self._data["isVisible"] = value

    def set_requires(self, requires: dict):
        self._data["requires"] = requires


class ColumnSet(ElementMixin):
    def __init__(self, columns: list = None, select_action=None, style: Style = None, bleed: bool = None,
                 min_height: str = None, **kwargs):
        self._data = {
            "type": "ColumnSet"
        }
        super().__init__(**kwargs)
        if columns:
            self.add_columns(columns)
        if select_action is not None:
            self.set_select_action(select_action)
        if style is not None:
            self.set_style(style)
        if bleed is not None:
            self.set_bleed(bleed)
        if min_height is not None:
            self.set_min_height(min_height)

    def add_columns(self, columns):
        self._data.setdefault("columns", [])
        if isinstance(columns, (list, set, tuple)):
            self._data["columns"].extend(self._get_items_list(columns))
        else:
            self._data["columns"].append(columns.as_data())

    def set_select_action(self, action):
        self._data["selectAction"] = action.as_data()

    def set_style(self, style: Style):
        self._data["style"] = style

    def set_bleed(self, value=True):
        self._data["bleed"] = value

    def set_min_height(self, value: str):
        self._data["minHeight"] = value


class Fact(CardElement):
    def __init__(self, title, value, **kwargs):
        self._data = {}
        super().__init__(**kwargs)
        self._data = {
            "title": title,
            "value": value
        }


class FactSet(ElementMixin):
    def __init__(self, facts: List[Fact], **kwargs):
        self._data = {
            "type": "FactSet"
        }
        super().__init__(**kwargs)
        self._set_base_facts(facts)

    def _set_base_facts(self, facts: List[Fact]):
        self._data["facts"] = self._get_items_list(facts)

    def add_facts(self, facts):
        if isinstance(facts, (list, set, tuple)):
            self._data["facts"].extend(self._get_items_list(facts))
        else:
            self._data["facts"].append(facts.as_data())


class ImageSet(ElementMixin):
    def __init__(self, images: list, image_size: ImageSize = None, **kwargs):
        self._data = {
            "type": "ImageSet"
        }
        super().__init__(**kwargs)
        self._set_base_images(images)
        if image_size is not None:
            self.set_image_size(image_size)

    def _set_base_images(self, images: list):
        self._data["images"] = self._get_items_list(images)

    def add_images(self, images):
        if isinstance(images, (list, set, tuple)):
            self._data["images"].extend(self._get_items_list(images))
        else:
            self._data["images"].append(images.as_data())

    def set_image_size(self, size: ImageSize):
        self._data["imageSize"] = size
