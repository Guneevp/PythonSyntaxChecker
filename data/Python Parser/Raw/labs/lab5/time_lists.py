"""CSC148 Lab 5: Linked Lists

=== CSC148 Winter 2025 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module description ===

This module runs timing experiments to determine how the time taken
to call `len` on a Python list vs. a LinkedList grows as the list size grows.
"""
from timeit import timeit

from labs.lab5.linked_list import AidenLinkedList
from linked_list import LinkedList

NUM_TRIALS = 3000                        # The number of trials to run.
SIZES = [1000, 2000, 4000, 8000, 16000]  # The list sizes to try.


def profile_len(list_class: type, size: int) -> float:
    """Return the time taken to call len on a list of the given class and size.

    Precondition: list_class is either list or LinkedList.
    """
    my_list = list_class([0] * size)
    # for i in range(size):
    #     my_list.append(0)
    # if isinstance(list_class, LinkedList):
    #     my_list = LinkedList(my_list)
    return timeit("len(my_list)", number=1, globals=locals())


if __name__ == '__main__':
    # Try both Python's list and our LinkedList
    for list_class in [list, LinkedList, AidenLinkedList]:
        # Try each list size
        for s in range(0, 25000, 1000):
            time = profile_len(list_class, s)
            print(f'[{list_class.__name__}] Size {s:>6}: {time}')
