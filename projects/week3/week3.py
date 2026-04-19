import marimo

__generated_with = "0.16.5"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import numpy as np
    return mo, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 1:
    Implement the Linear Search Algorithm for an arbitrary input array
    """
    )
    return


@app.function
def linSearch(arr,val):
    for i in range(0, len(arr)):
        if arr[i] == val:
            return i
    return -1


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 2
    Create an array of 500 elements, where the array is not sorted and has elements from 0 to 499 with no repetitions (Hint: use ```np.arange()``` and then ```np.random.shuffle()```).
    Then, call the ```search()``` function to find number 10 in the array. Calculate the time it takes to find the number.
    """
    )
    return


@app.cell
def _(np):
    import time 
    array_size = 500
    np_array = np.arange(array_size)
    np.random.shuffle(np_array)

    start_time = time.time()
    result = linSearch(np_array, 1)
    elapsed_time = time.time() - start_time

    print("Element found at index: ", result)
    print("elapsed time: ", elapsed_time, "seconds")
    return (time,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 3
    Repeat the process in Task 2 for 1000 different arrays (all of them of size 500), and store the elapsed time for each one of these runs. Then plot a frequency histogram for the time values.
    """
    )
    return


@app.cell
def _(np, time):
    def _():
        import matplotlib.pyplot as plt

        elapsed_times = np.empty(1000, dtype=float)

        for i in range(1000):
            array_size = 500
            np_array = np.arange(array_size)
            np.random.shuffle(np_array)

            start_time = time.time()
            result = linSearch(np_array, 1)
            elapsed_time = time.time() - start_time

            np.put(elapsed_times, i, elapsed_time)


        sorted_data = np.sort(elapsed_times)
        cleaned_data = sorted_data[20:-20]

        plt.hist(cleaned_data, bins=50)
        plt.xlabel("Elapsed Time (seconds)")
        plt.ylabel("Frequency")
        plt.title("Histogram of Elapsed Times for 1000 Runs")
        plt.show()

    _()



    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 4:
    Implement the Binary Search Algorithm for a sorted input array.
    """
    )
    return


@app.function
def binSearch(arr, val):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = low + (high - low) // 2  
        if arr[mid] == val:
            return mid
        elif arr[mid] < val:
            low = mid + 1
        else:
            high = mid - 1

    return -1


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 5:
    Implement the Recursive Binary Search Algorithm for a sorted input array.
    """
    )
    return


@app.function
def binSearchRec(arr, left, right, val):
    if left > right:  # Base case: not found
        return -1

    mid = (left + right) // 2

    if arr[mid] == val:
        return mid
    elif arr[mid] > val:
        return binSearchRec(arr, left, mid - 1, val)
    else:
        return binSearchRec(arr, mid + 1, right, val)


@app.cell
def _():
    arr = [2, 4, 6, 8, 10, 12, 14]
    print(binSearch(arr, 10))  # Output: 4
    print(binSearch(arr, 5))   # Output: -1 (not found)

    arr = [2, 4, 6, 8, 10, 12, 14]
    print(binSearchRec(arr, 0, len(arr)-1, 10))  # Output: 4
    print(binSearchRec(arr, 0, len(arr)-1, 5))   # Output: -1

    """
    Binary search is used to efficiently find a target value in a sorted array by repeatedly dividing the search space in half. 
    The iterative version (binSearch) uses a while loop to adjust the low and high indices until the target is found or the search space is empty. 

    The recursive version (binSearchRec) achieves the same by calling itself on the left or right subarray based on comparisons, with a base case that stops the recursion when the target is not found. 

    Both functions return the index of the target if it exists, or -1 if the target is not present. 

    Example:
    arr = [2, 4, 6, 8, 10, 12, 14]

    binSearch(arr, 10) or binSearchRec(arr, 0, len(arr)-1, 10) 
      → returns 4 because 10 is at index 4

    binSearch(arr, 5) or binSearchRec(arr, 0, len(arr)-1, 5) 
      → returns -1 because 5 is not in the array
    """

    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ---
    ## AI Use & Acknowledgement

    AI tools (ChatGPT, GPT-5 family) were used as a supportive development aid during the creation of this notebook, rather than to generate complete solutions.

    AI assistance was used to:
    - Help verify the correctness of search algorithm logic (linear search, iterative binary search, and recursive binary search).
    - Debug indexing, boundary conditions, and base cases in both iterative and recursive implementations.
    - Improve code structure, naming clarity, and readability while preserving the intended algorithmic behaviour.
    - Assist with data analysis tasks, including repeated timing measurements and the construction of a histogram to visualise execution-time distribution.

    All algorithms were implemented and tested manually by me, based on lecture material and personal understanding of search algorithms. The experimental setup (array sizes, number of runs, timing methodology, and data cleaning choices) was designed and executed independently.
    """
    )
    return


if __name__ == "__main__":
    app.run()
