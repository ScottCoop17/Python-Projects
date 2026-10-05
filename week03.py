
class DynamicArray:
    """A fixed-capacity array of non-negative integers that doubles its
    capacity whenever it fills up.
    """

    _DEFAULT_CAPACITY: int = 4
    _GROWTH_FACTOR: int = 2
    _EMPTY: int = -1

    def __init__(self, capacity: int = _DEFAULT_CAPACITY) -> None:
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        self._capacity: int = capacity
        self._size: int = 0
        self._underlying: list[int] = []
        for _ in range(self._capacity):
            self._underlying.append(self._EMPTY)

    def __str__(self) -> str:
        inside = ""
        for i in range(self._size):
            inside = inside + str(self._underlying[i])
            if i < self._size - 1:
                inside = inside + ", "
        return "[" + inside + "]"

    def resize(self) -> None:
        bigger_capacity = self._capacity * self._GROWTH_FACTOR
        temp: list[int] = []
        for _ in range(bigger_capacity):
            temp.append(self._EMPTY)
        for i in range(self._size):
            temp[i] = self._underlying[i]
        self._underlying = temp
        self._capacity = bigger_capacity

    def add(self, value: int) -> None:
        if value < 0:
            raise ValueError("values must be non-negative")
        if self._size >= self._capacity:
            self.resize()
        self._underlying[self._size] = value
        self._size = self._size + 1

    # ----- Problem 1: accessors -----

    def __len__(self) -> int:
        """Return the number of values stored in this array."""
        return self._size

    def get_size(self) -> int:
        """Return the number of values stored in this array."""
        return self._size

    def get_capacity(self) -> int:
        """Return the total number of slots in the underlying array."""
        return self._capacity

    def get(self, index: int) -> int:
        """Return the value stored at `index`."""
        if index < 0 or index >= self._size:
            return self._EMPTY
        return self._underlying[index]

    def index_of(self, value: int) -> int:
        """Return the position of the first occurrence of `value`."""
        for i in range(self._size):
            if self._underlying[i] == value:
                return i
        return self._EMPTY

    def contains(self, value: int) -> bool:
        """Return True if `value` is stored in this array."""
        return self.index_of(value) != self._EMPTY

    def remove(self, value: int) -> bool:
        """Remove the first occurrence of `value`."""
        index = self.index_of(value)

        if index == self._EMPTY:
            return False

        for i in range(index, self._size - 1):
            self._underlying[i] = self._underlying[i + 1]

        self._underlying[self._size - 1] = self._EMPTY
        self._size = self._size - 1
        return True

    # ----- Problem 2: magic methods -----

    @classmethod
    def from_values(cls, values: list[int]) -> "DynamicArray":
        """Build and return a new array holding `values`, in order."""
        result = cls()

        for value in values:
            result.add(value)

        return result

    def __eq__(self, other: object) -> bool:
        """Return True when `other` holds the same values in the same order."""
        if type(self) is not type(other):
            return False

        for i in range(self._size):
            if self._underlying[i] != other._underlying[i]:
                return False

        return self._size == other._size

    def __repr__(self) -> str:
        """Return a string that could rebuild this object."""
        return f"{type(self).__name__}.from_values({self._underlying[:self._size]!r})"

    def __add__(self, other: "DynamicArray") -> "DynamicArray":
        """Return a NEW array holding this array's values followed by `other`'s."""
        result = DynamicArray()

        for i in range(self._size):
            result.add(self._underlying[i])

        for i in range(other._size):
            result.add(other._underlying[i])

        return result


class Card:
    """One playing card: a rank and a suit that travel together."""

    _RANKS: tuple[str, ...] = (
        "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A",
    )

    _RED_SUITS: tuple[str, ...] = ("hearts", "diamonds")

    def __init__(self, rank: str, suit: str) -> None:
        self._rank: str = rank
        self._suit: str = suit

    def label(self) -> str:
        return f"{self._rank} of {self._suit}"

    def __eq__(self, other: object) -> bool:
        return (
            type(self) is type(other)
            and self._rank == other._rank
            and self._suit == other._suit
        )

    @staticmethod
    def is_valid_rank(rank: str) -> bool:
        """Return True if `rank` is one of the 13 legal ranks."""
        return rank in Card._RANKS

    @property
    def rank(self) -> str:
        """Return this card's rank."""
        return self._rank

    @rank.setter
    def rank(self, value: str) -> None:
        """Set this card's rank."""
        if not self.is_valid_rank(value):
            raise ValueError(f"{value!r} is not one of the 13 legal ranks")

        self._rank = value

    @property
    def color(self) -> str:
        """Return the color of this card."""
        if self._suit in self._RED_SUITS:
            return "red"
        return "black"

    def __repr__(self) -> str:
        """Return a string that rebuilds this card."""
        return f"Card({self._rank!r}, {self._suit!r})"


def announce(func):
    """Wrap `func` so that every call prints `calling <name>` before running."""
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


class BoundedArray(DynamicArray):
    """A DynamicArray that refuses to hold more than a fixed number of values."""

    _DEFAULT_LIMIT: int = 6

    def __init__(self, limit: int = _DEFAULT_LIMIT) -> None:
        super().__init__()
        self.__limit = limit

    def get_limit(self) -> int:
        """Return the greatest number of values this array will hold."""
        return self.__limit

    def add(self, value: int) -> None:
        """Store `value`, or raise IndexError if this array is full."""
        if self._size >= self.__limit:
            raise IndexError("array is full")

        super().add(value)


if __name__ == "__main__":
    # ----- Problem 1 -----
    da = DynamicArray()
    da.add(10001)
    da.add(60626)
    da.add(90210)
    print(da)
    print(len(da), da.get_size(), da.get_capacity())

    print(da.get(0), da.get(2))
    print(da.get(-1), da.get(3), da.get(100))

    print(da.index_of(10001), da.index_of(90210), da.index_of(99999))
    print(da.contains(60626), da.contains(99999))

    da.add(11111)
    da.add(22222)
    print(da)
    print(len(da), da.get_capacity())

    print(da.remove(90210))
    print(da)
    print(len(da), da.get_capacity())
    print(da.remove(90210))
    print(da.index_of(22222))

    # ----- Problem 2 -----
    a = DynamicArray.from_values([10001, 60626, 90210])
    print(a)
    print(len(a), a.get_capacity())

    print(repr(a))
    print(repr(DynamicArray()))

    b = DynamicArray.from_values([10001, 60626, 90210])
    print(a == b)
    print(a is b)

    wide = DynamicArray(64)
    wide.add(10001)
    wide.add(60626)
    wide.add(90210)
    print(a == wide, a.get_capacity(), wide.get_capacity())

    print(a == DynamicArray.from_values([10001, 60626]))
    print(a == DynamicArray.from_values([90210, 60626, 10001]))
    print(a == "not an array")
    print(a == None)

    c = a + DynamicArray.from_values([11111, 22222])
    print(c)
    print(len(c))
    print(a)
    print(len(a))

    empty = DynamicArray()
    print(empty + empty)
    print(a + empty == a)

    # ----- Problem 3 -----
    card = Card("7", "hearts")

    print(card.label())
    print(card.rank)
    print(card.color)
    print(Card("K", "spades").color)

    print(Card.is_valid_rank("Q"))
    print(Card.is_valid_rank("1"))
    print(card.is_valid_rank("10"))

    print(repr(card))
    print([card, card])

    print(Card("7", "hearts") == card)

    card.rank = "K"
    print(card.rank, card.label())

    try:
        card.rank = "1"
    except ValueError as error:
        print("ValueError:", error)

    try:
        card.color = "green"  # ty: ignore[invalid-assignment]
    except AttributeError:
        print("AttributeError as expected")


    # ----- Problem 4 -----
    bounded = BoundedArray()
    print(type(bounded).__name__, bounded.get_limit())

    for value in range(6):
        bounded.add(value)
    print(len(bounded), bounded.get_capacity())

    try:
        bounded.add(99)
    except IndexError as error:
        print("IndexError:", error)

    pair = BoundedArray.from_values([1, 2])
    print(type(pair).__name__, pair)
    print(repr(pair))

    try:
        BoundedArray.from_values([0, 1, 2, 3, 4, 5, 6])
    except IndexError as error:
        print("IndexError:", error)

    print(pair == DynamicArray.from_values([1, 2]))
    print(pair == BoundedArray.from_values([1, 2]))

    print(sorted(vars(bounded)))

    # ----- Problem 3, continued: applying the decorator -----

    @announce
    def describe(rank: str, suit: str) -> str:
        return f"{rank} of {suit}"

    print(describe("7", "hearts"))
    print(describe.__name__)
