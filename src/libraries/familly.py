from typing import Generic, TypeVar

T = TypeVar('T')

class Parents(Generic[T]):
    def __init__(self, parents: list[T]):
        assert len(parents) != 0, "Parents list cannot be empty"
        assert all(isinstance(p, type(parents[0])) for p in parents), "All parents must be of the same type"
        self.parents = parents

    @staticmethod
    def from_couple(a: T, b: T) -> 'Parents[T]':
        return Parents([a, b])

    def is_couple(self) -> bool:
        return len(self.parents) == 2

    def couple(self) -> tuple[T, T]:
        assert len(self.parents) == 2, "Is not a couple"
        return (self.parents[0], self.parents[1])

    def father(self) -> T:
        assert len(self.parents) >= 1
        return self.parents[0]

    def mother(self) -> T:
        assert len(self.parents) >= 2
        return self.parents[1]

    def __getitem__(self, index: int) -> T:
        assert 0 <= index < len(self.parents), "Index out of range"
        return self.parents[index]
