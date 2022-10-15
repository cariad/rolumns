from typing import Any, Callable

from rolumns.translation_state import TranslationState

Translator = Callable[[TranslationState], Any]
