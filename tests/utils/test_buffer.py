import pytest
from utils.buffer import Buffer

@pytest.fixture
def buf():
    return Buffer(4)

def test_store_single_char(buf):
    pos = buf.store(0, 'A')
    assert pos == 1
    assert buf.get() == "A"


def test_store_overwrites_position(buf):
    buf.store(0, 'A')
    buf.store(0, 'B')
    assert buf.get() == "B"


def test_store_grows_capacity(buf):
    pos = 0
    for c in "ABCDE":
        pos = buf.store(pos, c)
    assert buf.get() == "ABCDE"
    assert len(buf.buff) >= 5


def test_mstore_whole_string(buf):
    pos = buf.mstore(0, "Hello")
    assert pos == 5
    assert buf.get() == "Hello"
    pos = buf.mstore(pos, " World")
    assert pos == 11
    assert buf.get() == "Hello World"


def test_gstore_substring(buf):
    pos = buf.gstore(0, "World", 1, 3)  # "orl"
    assert pos == 3
    assert buf.get() == "orl"

def test_get_empty_buffer(buf):
    assert buf.get() == ""


def test_append_multiple_strings(buf):
    pos = buf.gstore(0, "Hello", 0, 5)
    pos = buf.gstore(pos, "World", 0, 5)
    assert buf.get() == "HelloWorld"


def test_buffer_growth_multiple_times(buf):
    pos = 0
    for _ in range(10):  # force multiple resizes
        pos = buf.gstore(pos, "12345", 0, 5)
    result = buf.get()
    assert result == "12345" * 10
    assert len(buf.buff) >= len(result)
