import logging
from typing import NamedTuple, Any

logger = logging.getLogger(__name__)


class BoxBounds(NamedTuple):
    x: int
    y: int
    width: int
    height: int


def get_checkbox_html(form_name: str, checkbox_name: str, checked: bool) -> str:
    checked_str = 'checked' if checked else ''
    return f'<input type="checkbox" name="{form_name}" value="{checkbox_name}" {checked_str}/>'


def safe_form_get(form_dict: dict[str, Any], key: str, default: str = '') -> Any:
    if key not in form_dict:
        logger.warning(f'Expected key ({key}) not found in dict: {form_dict}')
        return default
    else:
        return form_dict[key]
