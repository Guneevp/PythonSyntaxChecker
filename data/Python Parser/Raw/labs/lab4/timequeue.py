"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Winter 2025 ===
Department of Mathematical and Computational Sciences,
University of Toronto Mississauga

=== Module Description ===
This module runs timing experiments to determine how the time taken
to enqueue or dequeue grows as the queue size grows.
"""
from timeit import timeit

from myqueue3 import Queue

import matplotlib.pyplot as plt

###############################################################################
# Task 3: Running timing experiments
###############################################################################
# TODO: implement this function
def _setup_queue(qsize: int) -> Queue:
    """Return a queue of the given size."""
    # Experiment preparation: return a queue of size <qsize>.
    # You can "cheat" here and set your queue's _items attribute directly
    # to a list of the appropriate size by writing something like
    #
    #     queue._items = list(range(qsize))
    #
    # to save a bit of time in setting up the experiment.
    queue = Queue()
    queue._items = list(range(qsize))
    return queue



def time_queue() -> tuple[list[int], list[float], list[float]]:
    """Run timing experiments for Queue.enqueue and Queue.dequeue."""
    # The queue sizes to try.
    # queue_sizes = range(0,1000000,25000)
    queue_sizes =  [1000, 2000,]
    # The number of times to call a single enqueue or dequeue operation.
    trials = 200

    # This loop runs the timing experiment. For each queue size, 
    # its three steps are:
    #   1. Initialize the sample queue.
    #   2. Call the function "timeit", which takes three arguments:
    #        - a *string* representation of a piece of code to run
    #        - the number of times to run it (just 1 for us)
    #        - globals is a technical argument that you DON'T need to care about
    #   3. Report the total time taken to do an enqueue on the queue <trials> times.
    def short(n):
        a = 2
        for i in range(n):
            a += 1

    enqueue_times = []
    for queue_size in queue_sizes:
        queue = _setup_queue(queue_size)
        time = 0
        for _ in range(trials):
            time += timeit(f'short({queue_size})', number=1, globals=locals())
        print(f'short: Queue size {queue_size:>7}, time {time}')
        enqueue_times.append(time)

    def long(n):
        n = n ** 165
        a = 2
        for i in range(n):
            a += 1




    # TODO: using the above loop as an analogy, write a second timing
    # experiment here that runs dequeue on the given queues, and reports the
    # time taken. Note that you can reuse most of the same code.
    dequeue_times = []
    for queue_size in queue_sizes:
        time = 0
        for _ in range(trials):
            time += timeit(f'long({queue_size})', number=1, globals=locals())
        print(f'long: Queue size {queue_size:>7}, time {time}')
        dequeue_times.append(time)

    return queue_sizes, [], dequeue_times

def TWO_PLOT(x, y1, y2, xerr, y1err, y2err, title, xlabel, y1label, y2label):
    plt.figure()
    plt.errorbar(x, y1, yerr=y1err, xerr=xerr, fmt=".", capsize=2, label=y1label)
    plt.errorbar(x, y2, yerr=y2err, xerr=xerr, fmt=".", capsize=2, label=y2label)

    plt.xlabel(xlabel)
    plt.ylabel(y1label)
    plt.ylabel(y2label)
    plt.title(title)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    a, b, c = time_queue()
    plt.plot(a, b)
    plt.plot(a, c)
    # plt.axis([0, 200000, 0, 0.2])
    plt.show()
    TWO_PLOT(a, b, c, 0, 0, 0, "Manjyot wya", "q sizes", "enqueue times", "dequeue times")
