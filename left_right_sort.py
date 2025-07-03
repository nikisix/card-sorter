"""Left Right Sorter
A special cased quick sort algorithm to control mechanical hardware.
The machine manages three stacks of cards: center, left and right.
The capacity of the center stack is the capacity of the machine.

Pseudocode:
    iterate through the center stack and create an index for each card.
    sort the indicies and create a mapping of current position to sorted rank
    choose the optimal pivot for the group of cards
    iterate through the center stack:
        compare the current card to the pivot
        move the card to the left or right stack depending on the card's value compared to the pivot
    the left and right stacks define new subgroups in the quicksort algorithm
    choose optimal pivots for the left and right stacks
    the datastructure is a list of tuples (index, sorted-rank, subgroup-pivot)
    rescan every 20 iterations or so to limit machine error based divergence

Visual Representation:

        | left | center | right |
ix 0    |      |        |       |
...     |      |        |       |
ix inf  |      |        |       |
"""

import random
import numpy as np
import pandas as pd


class Machine:
    def __init__(self, center):
        self.capacity = len(center)
        self.left = list()
        self.right = list()
        self.center = center
        self.d_value_group = dict(zip(self.center, [1] * self.capacity))

    def scan(self):
        for i, _ in enumerate(self.center):
            c = self.center.pop(0)
            if i % 2 == 0:
                self.left.append(c)
            else:
                self.right.append(c)

    def combine(self):
        self.center += self.left + self.right
        self.left.clear()
        self.right.clear()

    def calc_group_pivots(self):
        self.d_group_pivot = dict()
        df_value_group = pd.DataFrame(
            self.d_value_group.items(), columns=["value", "group"]
        )
        for g in df_value_group["group"].unique():
            # calculate the pivot for the i-th group
            group = df_value_group[df_value_group["group"] == g]["value"]
            if len(group) == 1:
                self.d_group_pivot[g] = group
            self.d_group_pivot[g] = np.median(group)

    def sort_iteration(self):
        """Runs a single iteration of the left-right sort algorithm.

        TODO break this into singular actions for machine control.

        Pseudocode:
        calc group pivots
        iterate through center stack
        compare to group pivot
        increment max group
        combine"""
        self.calc_group_pivots()

        # initilize sub group
        subgroup = int(list(self.d_value_group.values())[0])
        for _ in range(len(self.center)):
            c = self.center.pop(0)
            new_subgroup = self.d_value_group[c]
            if subgroup != new_subgroup:
                # subgroup changed: recombine and move to next subgroup
                self.combine()
                subgroup = new_subgroup
            assert subgroup == self.d_value_group[c], "subgroup mismatch"
            if c <= self.d_group_pivot[subgroup]:
                # motor left
                self.left.append(c)
                self.d_value_group[c] = 10 * subgroup
            else:
                # motor right
                self.right.append(c)
                self.d_value_group[c] = 10 * subgroup + 1
        self.combine()

    def is_sorted(self):
        """Check if the center stack is sorted."""
        return all(
            self.center[i] <= self.center[i + 1] for i in range(len(self.center) - 1)
        )


# machine = Machine(random.sample(range(100), 10))
machine = Machine(random.sample(range(10), 10))
print(machine.center)
print(machine.d_value_group)
machine.sort_iteration()
print(machine.center)
print(machine.d_value_group)

machine.sort_iteration()
print(machine.center)
print(machine.d_value_group)

machine.sort_iteration()
print(machine.center)
print(machine.d_value_group)
print(machine.is_sorted())

machine.sort_iteration()
print(machine.center)
print(machine.d_value_group)
print(machine.is_sorted())
