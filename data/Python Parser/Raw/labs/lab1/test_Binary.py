from hypothesis import given
from hypothesis.strategies import lists, integers
import Binary
import random

@given(lists(integers()))
def test_Binary(L:list) -> None:
    if not L:
        L = [1]
    t = random.choice(L)
    L.sort()
    t_index = L.index(t)
    assert Binary.binary_search(L, t) == t_index



if __name__ == "__main__":
    import pytest

    pytest.main(['test_Binary.py'])
