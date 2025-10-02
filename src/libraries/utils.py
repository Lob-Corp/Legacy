from typing import Callable, Iterable, List, TypeVar


class Util:
    T = TypeVar("T")
    U = TypeVar("U")

    @staticmethod
    def list_rev_map_append(
        f: Callable[[T], U], l1: Iterable[T], l2: Iterable[U]
    ) -> List[U]:
        """Map f over l1, reverse the mapped results, then append l2."""
        mapped = [f(x) for x in l1]
        return list(reversed(mapped)) + list(l2)
