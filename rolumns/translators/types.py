from typing import Any, Callable

from rolumns.translators.translation_state import TranslationState

Translator = Callable[[TranslationState], Any]
