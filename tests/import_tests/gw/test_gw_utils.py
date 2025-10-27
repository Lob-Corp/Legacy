"""Tests for utility functions and stream functionality.

Focus on improving coverage for utils.py and stream.py modules.
"""

from collections.abc import Iterator
import pytest
from script.gw_parser.utils import fields, copy_decode, get_field, cut_space
from script.gw_parser.stream import LineStream


class TestFieldsTokenization:
    """Test fields() tokenization function."""

    def test_simple_tokens(self):
        """Test simple space-separated tokens."""
        result = fields("token1 token2 token3")
        assert result == ["token1", "token2", "token3"]

    def test_tab_separated_tokens(self):
        """Test tab-separated tokens."""
        result = fields("token1\ttoken2\ttoken3")
        assert result == ["token1", "token2", "token3"]

    def test_mixed_whitespace(self):
        """Test mixed spaces and tabs."""
        result = fields("token1 \t  token2\t\ttoken3")
        assert result == ["token1", "token2", "token3"]

    def test_leading_whitespace(self):
        """Test tokens with leading whitespace."""
        result = fields("   token1 token2")
        assert result == ["token1", "token2"]

    def test_trailing_whitespace(self):
        """Test tokens with trailing whitespace."""
        result = fields("token1 token2   ")
        assert result == ["token1", "token2"]

    def test_empty_string(self):
        """Test empty string."""
        result = fields("")
        assert result == []

    def test_only_whitespace(self):
        """Test string with only whitespace."""
        result = fields("   \t  ")
        assert result == []

    def test_single_token(self):
        """Test single token."""
        result = fields("token")
        assert result == ["token"]


class TestCopyDecode:
    """Test copy_decode() function."""

    def test_underscore_to_space(self):
        """Test underscore converted to space."""
        result = copy_decode("first_name", 0, 10)
        assert result == "first name"

    def test_backslash_escape(self):
        """Test backslash escape sequences."""
        result = copy_decode("test\\nvalue", 0, 11)
        assert result == "testnvalue"

    def test_backslash_escape_underscore(self):
        """Test escaped underscore remains underscore."""
        result = copy_decode("keep\\_underscore", 0, 16)
        assert result == "keep_underscore"

    def test_backslash_escape_backslash(self):
        """Test escaped backslash."""
        result = copy_decode("test\\\\value", 0, 11)
        assert result == "test\\value"

    def test_multiple_underscores(self):
        """Test multiple underscores."""
        result = copy_decode("first_middle_last", 0, 17)
        assert result == "first middle last"

    def test_no_special_chars(self):
        """Test string without special characters."""
        result = copy_decode("normaltext", 0, 10)
        assert result == "normaltext"

    def test_empty_string(self):
        """Test empty string."""
        result = copy_decode("", 0, 0)
        assert result == ""

    def test_partial_string(self):
        """Test decoding partial string."""
        result = copy_decode("start_middle_end", 6, 12)
        assert result == "middle"

    def test_backslash_at_end(self):
        """Test backslash at end without following character."""
        result = copy_decode("test\\", 0, 5)
        assert result == "test\\"

    def test_mixed_escapes_and_underscores(self):
        """Test mixed escape sequences and underscores."""
        result = copy_decode("test_\\nvalue_here", 0, 17)
        assert result == "test nvalue here"


class TestGetField:
    """Test get_field() function."""

    def test_field_present(self):
        """Test extracting field when present."""
        value, remaining = get_field("#tag", ["#tag", "value", "other"])
        assert value == "value"
        assert remaining == ["other"]

    def test_field_not_present(self):
        """Test when field tag not present."""
        value, remaining = get_field("#tag", ["other", "tokens"])
        assert value == ""
        assert remaining == ["other", "tokens"]

    def test_field_at_end(self):
        """Test field at end of token list."""
        value, remaining = get_field("#tag", ["before", "#tag", "value"])
        assert value == ""
        assert remaining == ["before", "#tag", "value"]

    def test_field_with_no_value(self):
        """Test field tag without value."""
        value, remaining = get_field("#tag", ["#tag"])
        assert value == ""
        assert remaining == ["#tag"]

    def test_empty_token_list(self):
        """Test with empty token list."""
        value, remaining = get_field("#tag", [])
        assert value == ""
        assert remaining == []

    def test_field_first_position(self):
        """Test field in first position with value."""
        value, remaining = get_field("#tag", ["#tag", "value", "more"])
        assert value == "value"
        assert remaining == ["more"]

    def test_different_tag(self):
        """Test with different tag name."""
        value, remaining = get_field("#bp", ["#bp", "London", "next"])
        assert value == "London"
        assert remaining == ["next"]


class TestCutSpace:
    """Test cut_space() function (strips whitespace)."""

    def test_basic_strip(self):
        """Test basic whitespace stripping."""
        result = cut_space("  text  ")
        assert result == "text"

    def test_leading_whitespace(self):
        """Test stripping leading whitespace."""
        result = cut_space("   text")
        assert result == "text"

    def test_trailing_whitespace(self):
        """Test stripping trailing whitespace."""
        result = cut_space("text   ")
        assert result == "text"

    def test_no_whitespace(self):
        """Test string without whitespace."""
        result = cut_space("text")
        assert result == "text"

    def test_empty_string(self):
        """Test empty string."""
        result = cut_space("")
        assert result == ""

    def test_only_whitespace(self):
        """Test string with only whitespace."""
        result = cut_space("   ")
        assert result == ""

    def test_tabs(self):
        """Test stripping tabs."""
        result = cut_space("\ttext\t")
        assert result == "text"

    def test_mixed_whitespace(self):
        """Test stripping mixed whitespace."""
        result = cut_space(" \t text \t ")
        assert result == "text"


class TestLineStream:
    """Test LineStream class."""

    def test_stream_creation(self):
        """Test creating a stream."""
        lines = iter(["line1", "line2", "line3"])
        stream = LineStream(lines)
        assert stream is not None

    def test_pop_lines(self):
        """Test popping lines from stream."""
        lines = iter(["line1", "line2", "line3"])
        stream = LineStream(lines)
        assert stream.pop() == "line1"
        assert stream.pop() == "line2"
        assert stream.pop() == "line3"

    def test_pop_until_empty(self):
        """Test popping until stream is empty."""
        lines = iter(["line1", "line2"])
        stream = LineStream(lines)
        stream.pop()
        stream.pop()
        assert stream.pop() is None

    def test_peek_line(self):
        """Test peeking at next line."""
        lines = iter(["line1", "line2"])
        stream = LineStream(lines)
        assert stream.peek() == "line1"
        assert stream.peek() == "line1"  # Peek doesn't consume
        assert stream.pop() == "line1"

    def test_peek_on_empty_stream(self):
        """Test peeking when stream is empty."""
        lines: Iterator[str] = iter([])
        stream = LineStream(lines)
        assert stream.peek() is None
        assert stream.peek() is None

    def test_peek_after_exhaustion(self):
        """Test peeking after stream exhausted."""
        lines = iter(["line1"])
        stream = LineStream(lines)
        stream.pop()
        assert stream.peek() is None

    def test_push_back_line(self):
        """Test pushing line back to stream."""
        lines = iter(["line1", "line2"])
        stream = LineStream(lines)
        line = stream.pop()
        if line is None:
            pytest.fail("Unexpected None from pop()")
        stream.push_back(line)
        assert stream.pop() == "line1"
        assert stream.pop() == "line2"

    def test_push_back_multiple(self):
        """Test pushing back multiple lines."""
        lines = iter(["line1", "line2", "line3"])
        stream = LineStream(lines)
        l1 = stream.pop()
        l2 = stream.pop()
        if l1 is None or l2 is None:
            pytest.fail("Unexpected None from pop()")
        stream.push_back(l2)
        stream.push_back(l1)
        assert stream.pop() == "line1"
        assert stream.pop() == "line2"
        assert stream.pop() == "line3"

    def test_push_back_without_pop(self):
        """Test pushing back without first popping."""
        lines = iter(["line1", "line2"])
        stream = LineStream(lines)
        stream.push_back("new_line")
        assert stream.pop() == "new_line"
        assert stream.pop() == "line1"

    def test_peek_after_push_back(self):
        """Test peeking after push back."""
        lines = iter(["line1"])
        stream = LineStream(lines)
        stream.push_back("pushed")
        assert stream.peek() == "pushed"
        assert stream.pop() == "pushed"

    def test_complex_push_pop_sequence(self):
        """Test complex sequence of push/pop operations."""
        lines = iter(["l1", "l2", "l3"])
        stream = LineStream(lines)
        assert stream.pop() == "l1"
        stream.push_back("l1")
        assert stream.peek() == "l1"
        assert stream.pop() == "l1"
        assert stream.pop() == "l2"
        stream.push_back("l2")
        stream.push_back("inserted")
        assert stream.pop() == "inserted"
        assert stream.pop() == "l2"
        assert stream.pop() == "l3"
        assert stream.pop() is None

    def test_empty_stream_operations(self):
        """Test operations on empty stream."""
        lines: Iterator[str] = iter([])
        stream = LineStream(lines)
        assert stream.peek() is None
        assert stream.pop() is None
        stream.push_back("line")
        assert stream.pop() == "line"
        assert stream.peek() is None


class TestFieldsWithSpecialCharacters:
    """Test fields() with special characters."""

    def test_fields_with_underscores(self):
        """Test tokenization of fields with underscores."""
        result = fields("first_name last_name")
        assert result == ["first name", "last name"]

    def test_fields_with_backslashes(self):
        """Test tokenization of fields with backslashes."""
        result = fields("test\\nvalue other\\tthing")
        assert result == ["testnvalue", "othertthing"]

    def test_fields_with_mixed_escapes(self):
        """Test tokenization with mixed escape sequences."""
        result = fields("test\\_name other_value")
        assert result == ["test_name", "other value"]

    def test_fields_preserves_non_whitespace(self):
        """Test that non-whitespace chars are preserved."""
        result = fields("!@#$% ^&*()")
        assert result == ["!@#$%", "^&*()"]
