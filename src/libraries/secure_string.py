from __future__ import annotations


class TaggedString(str):
    def __new__(cls, value: str):
        return str.__new__(cls, value)

    @classmethod
    def concat_all(cls, *args: str | TaggedString) -> TaggedString:
        """
        Concatenate multiple TaggedString or str instances in order.
        All TaggedString args must be of the same subclass.
        """
        result = ""
        for arg in args:
            if isinstance(arg, TaggedString):
                if type(arg) is not cls:
                    raise TypeError(
                        f"Cannot concat {
                            type(arg).__name__} with {
                            cls.__name__}")
                result += str(arg)
            elif isinstance(arg, str):
                result += arg
            else:
                raise TypeError(f"Argument must be str or {cls.__name__}")
        return cls(result)


class SafeString(TaggedString):
    pass


class EscapedString(TaggedString):
    pass


class EncodedString(TaggedString):
    pass
