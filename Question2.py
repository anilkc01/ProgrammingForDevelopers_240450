def maxPathSum(arr):

    if not arr:
        return 0

    max_sum = float('-inf')

    def dfs(i):
        nonlocal max_sum

        # Out of bounds or non-existing plant
        if i >= len(arr) or arr[i] is None:
            return 0

        # Downstream contributions
        left_gain = max(dfs(2 * i + 1), 0)
        right_gain = max(dfs(2 * i + 2), 0)

        # Power produced by cascade passing through this plant
        current_total = arr[i] + left_gain + right_gain

        # Update global maximum
        max_sum = max(max_sum, current_total)

        # Return max single-direction contribution
        return arr[i] + max(left_gain, right_gain)

    dfs(0)
    return max_sum



# Example 1
arr1 = [1, 2, 3]
print("Input:", arr1)
print("Maximum Cascade Power:", maxPathSum(arr1))
print()

# Example 2
arr2 = [10, -90, 20, 6, None, 15, 7]
print("Input:", arr2)
print("Maximum Cascade Power:", maxPathSum(arr2))
