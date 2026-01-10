def binary_search(comparable, target):
    left = 0
    right = len(comparable) - 1
    while left <= right:
        middle = (left + right) // 2
        # print("Left:", left, "middle item:", comparable[middle], "right:", right)
        if comparable[middle] == target:
            return middle
        elif comparable[middle] < target:
            left = middle
        else: right = middle
    return -1
