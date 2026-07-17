# Notes

## Intuition
Instead of sorting the entire array (O(n log n)), I can use a min-heap of size k to track the k largest elements. As I iterate through the array, I push each element into the heap. Whenever the heap size exceeds k, I pop the smallest element. At the end, the root of the heap (smallest in the heap) is the kth largest element overall.

## Approach
1. Initialize an empty list `min_heap`.
2. Iterate over each `num` in `nums`:
   - Push `num` into the heap using `heapq.heappush(min_heap, num)`.
   - If the heap size exceeds `k`, pop the smallest using `heapq.heappop(min_heap)`.
3. After processing all elements, `min_heap[0]` is the kth largest element.

## Time Complexity
**O(n log k)** — Each heap operation (push/pop) is O(log k), and we do this for all n elements.

## Space Complexity
**O(k)** — The heap stores at most k elements at any time.

## Mistakes
- Initially thought of using a max-heap (negating values), but a min-heap of size k is more intuitive here.
- Almost sorted the array first — that's O(n log n) and misses the point of the exercise.
- Had to remember to `import heapq` at the top.

## Revision Date
July 11, 2026
