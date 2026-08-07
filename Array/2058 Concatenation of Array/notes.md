# Notes

## Intuition
This is the simplest problem in the collection. The result array is just the input array appended to itself. Python's list concatenation with the `+` operator does exactly this in one line.

## Approach
1. Simply return `nums + nums` — Python's `+` operator concatenates two lists, creating a new list with elements from both.

## Time Complexity
**O(n)** — We create a new list of length 2n by copying all elements.

## Space Complexity
**O(n)** — The output array is of size 2n (n extra space beyond the input).

## Mistakes
- None — this is a straightforward problem. Just ensure the return type is correct.

## Revision Date
July 11, 2026
