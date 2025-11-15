"""
For the tester,
In this function we define all scoring function,
The default one looks at Config.xxx as ints,
And also ignores the different chars and only looks at the choice.

A char can be None if one of the sequences is empty.
"""

from Consts import Choice

def default_score_function(char_1: str | None, char_2: str | None, choice: Choice) -> int:
    gap_score: int = -3
    substitution_score: int = -2
    equal_score: int = 2

    if Choice.GAP_RIGHT == choice:
        return gap_score

    if Choice.GAP_DOWN == choice:
        return gap_score
    
    if char_1 == char_2:
        return equal_score
    
    if Choice.SUBSTITUTION == choice:
        return substitution_score