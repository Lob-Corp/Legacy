import pytest

from secure_string import *

# SafeString tests
def test_safe_concat_multiple_safestrings():
    a = SafeString("hello")
    b = SafeString(" world")
    c = SafeString("!!!")
    result = SafeString.concat_all(a, b, c)
    assert result == "hello world!!!"
    assert isinstance(result, SafeString)

def test_safe_concat_with_str():
    a = SafeString("hello")
    result = SafeString.concat_all(a, " world", "!!!")
    assert result == "hello world!!!"
    assert isinstance(result, SafeString)

def test_safe_concat_mixed_subclasses_raises():
    a = SafeString("hello")
    b = EscapedString(" world")
    with pytest.raises(TypeError):
        SafeString.concat_all(a, b)

def test_safe_concat_invalid_type_raises():
    a = SafeString("hello")
    with pytest.raises(TypeError):
        SafeString.concat_all(a, 123)

def test_safe_concat_empty_args():
    result = SafeString.concat_all()
    assert result == ""
    assert isinstance(result, SafeString)

# EscapedString tests
def test_escaped_concat_multiple():
    a = EscapedString("foo")
    b = EscapedString("bar")
    result = EscapedString.concat_all(a, b, "baz")
    assert result == "foobarbaz"
    assert isinstance(result, EscapedString)

def test_escaped_concat_mixed_with_safestring_raises():
    a = EscapedString("foo")
    b = SafeString("bar")
    with pytest.raises(TypeError):
        EscapedString.concat_all(a, b)

# EncodedString tests
def test_encoded_concat_preserves_type():
    a = EncodedString("x")
    b = EncodedString("y")
    result = EncodedString.concat_all(a, b)
    assert result == "xy"
    assert isinstance(result, EncodedString)
