import pytest
from app.chat.services import ChatService

def test_yield_word_by_word_simple():
    text = "Hello world"
    tokens = list(ChatService.yield_word_by_word(text))
    assert tokens == ["Hello", " ", "world"]

def test_yield_word_by_word_with_newlines():
    text = "Line 1\nLine 2"
    tokens = list(ChatService.yield_word_by_word(text))
    assert tokens == ["Line", " ", "1", "\n", "Line", " ", "2"]

def test_yield_word_by_word_with_multiple_spaces():
    text = "  spaced  "
    tokens = list(ChatService.yield_word_by_word(text))
    assert tokens == ["  ", "spaced", "  "]
