from typing import Union

from django_actionable_messages.adaptive_card.mixins import ActionMixin
from django_actionable_messages.mixins import CardElement


class OpenUrl(ActionMixin):
    action_type = "Action.OpenUrl"

    def __init__(self, url: str, **kwargs):
        super().__init__(**kwargs)
        self.set_url(url)

    def set_url(self, url: str):
        self._data["url"] = url


class Submit(ActionMixin):
    action_type = "Action.Submit"

    def __init__(self, data: Union[str, dict] = None, **kwargs):
        super().__init__(**kwargs)
        if data is not None:
            self.set_data(data)

    def set_data(self, data: Union[str, dict]):
        self._data["data"] = data


class ShowCard(ActionMixin):
    action_type = "Action.ShowCard"

    def __init__(self, card=None, **kwargs):
        super().__init__(**kwargs)
        if card is not None:
            self.set_card(card)

    def set_card(self, card):
        self._data["card"] = card.payload


class TargetElement(CardElement):
    def __init__(self, element_id: str, is_visible: bool = None, **kwargs):
        self._data = {
            "elementId": element_id
        }
        super().__init__(**kwargs)
        if is_visible is not None:
            self.set_is_visible(is_visible)

    def set_element_id(self, element_id: str):
        self._data["elementId"] = element_id

    def set_is_visible(self, value=True):
        self._data["isVisible"] = value


class ToggleVisibility(ActionMixin):
    action_type = "Action.ToggleVisibility"

    def __init__(self, target_elements: list = None, **kwargs):
        super().__init__(**kwargs)
        if target_elements:
            self.set_target_elements(target_elements)

    def set_target_elements(self, elements: list):
        self._data["targetElements"] = []
        for element in elements:
            if isinstance(element, TargetElement):
                self._data["targetElements"].append(element.as_data())
            else:
                self._data["targetElements"].append(element)
