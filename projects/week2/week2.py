import marimo

__generated_with = "0.19.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import numpy as np
    import marimo as mo 
    import micropip                  # Used from Pyodide which is used in browser toinstall pure Python packages dynamically using micropip,
    await micropip.install("plotly") # This case being plotly
    import plotly.graph_objects as go
    return go, mo, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 1: Insertion sort
    From the discussion in class, implement insertion sort.
    """)
    return


@app.function
def insertionSort(arr):
    for i in range(1, len(arr)):
        k = arr[i]
        j = i - 1

        while j >= 0 and k < arr[j]:
            arr[j + 1] = arr[j]
            j = j - 1

        arr[j + 1] = k

    return arr


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 2:
    Calculate the time that Insertion Sort takes to sort an array of 1000 random elements.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("Hint: Use the *time* library and *time.time()* method to get the instant time of execution").callout() 
    return


@app.cell
def _():
    import time
    import random

    arr_1000 = [random.randint(1, 1000) for _ in range(1000)]

    start_time = time.time()
    insertionSort(arr_1000)
    end_time = time.time()

    print(f"Time taken to sort 1000 elements: {end_time - start_time:.4f} seconds")
    return random, time


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 3: Bubble sort
    Now implement Bubble Sort
    """)
    return


@app.function
def bubbleSort(arr):
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break

    return arr


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Comparing both Sorting algorithms next to each other with the same task - Result: Insertion Sort is faster
    """)
    return


@app.cell
def _(mo, random, time):
    # Generate random data
    sample_data = [random.randint(1, 100) for _ in range(20)]
    arr_for_timing = [random.randint(1, 10000) for _ in range(1000)]

    # ---- Sorting samples ----
    sorted_insertion = insertionSort(sample_data.copy())
    sorted_bubble = bubbleSort(sample_data.copy())

    # ---- Timing ----
    start_times = time.time()
    insertionSort(arr_for_timing.copy())
    insertion_time = time.time() - start_times

    start_times = time.time()
    bubbleSort(arr_for_timing.copy())
    bubble_time = time.time() - start_times

    # ---- Markdown output ----
    mo.md(f"""
    ### 🧪 Sorting Comparison

    **Random sample (unsorted):**  
    `{sample_data}`

    **Sorted with Insertion Sort:**  
    `{sorted_insertion}`

    **Sorted with Bubble Sort:**  
    `{sorted_bubble}`

    ---

    ### ⏱️ Timing on 1000 Random Elements

    | Algorithm | Time (seconds) |
    |------------|----------------|
    | Insertion Sort | `{insertion_time:.6f}` |
    | Bubble Sort | `{bubble_time:.6f}` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    -----------------------------------------------------------
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Final Task (for next week)
    Use the code below to build your own interactive visualiser of sorting algorithms.
    Your visualiser should have the following functions:
    - It should allow the user choosing between three algorithms to use: Insertion sort, Bubble sort, and a third one of your choice (you can create your own crazy algorithm if you want).
    - Once that the user chooses their algorithm, they press "restart" to initiate. Then, the user can press "Increment" to run the next step of the sorting algorithm. This means that the user can run the algoithm step by step, every time the button is pressed.
    - The interface should colour the part of the array that has been sorted in a different colour than the unsorted part. This has been already implemented for the bubble sort case, but you will have to implement it for the other algorithms
    - Add interactive messages. For example, when choosing an algorithms, a pop-up message could appear explaining the basics of the chosen sorting algorithm.

    #### If you want to go beyond...
    - For bubble sort, add a different colour to the pairs that have had a swap in the last step, so the user can lnow which values have recently changed.
    - Add a monitor that shows the average time that the last step took (or you can average the last couple of steps to get a more accurate value)
    - Add the capability so the user can input custom arrays, of variable size and with particular structures (not only random arrays, for example reversed arrays, arrays with patterns, etcetera).

    Push your changes to your git.arts account by the beginning of the class next week.
    """)
    return


@app.cell
def _(mo):
    reset_button = mo.ui.button(label="Reset")
    reset_button
    return (reset_button,)


@app.cell
def _(mo):
    dropdown = mo.ui.dropdown(
        options=["bubble", "insertion", "merge"],
        value="bubble",
        label="Sorting algorithm:"
    )
    dropdown
    return (dropdown,)


@app.cell
def _(mo, np, reset_button):

    n = 100  # size of the array
    state = {
        "arr": np.random.randint(0,100,n),  # random array
        "i": 0  # current bubble sort pass
    }
    reset_button
    # Button to perform one pass
    next_button = mo.ui.button(value=0, on_click=lambda value: value + 1, label="Increment")
    next_button
    return n, next_button, state


@app.cell
def _(dropdown, go, mo, n, next_button, np, reset_button, state):
    import time as ti

    # --- Ensure each algorithm has its own state ---
    if "bubble" not in state:
        state["bubble"] = {"arr": np.random.randint(0, 100, n), "i": 0, "last_next": 0}
    if "insertion" not in state:
        state["insertion"] = {"arr": np.random.randint(0, 100, n), "i": 0, "last_next": 0}
    if "merge" not in state:
        state["merge"] = {"arr": np.random.randint(0, 100, n), "i": 0, "last_next": 0}

    # timing storage (persistent)
    if "timings" not in state:
        state["timings"] = []

    algo_state = state[dropdown.value]
    arr = algo_state["arr"]
    i = algo_state.get("i", 0)

    # Safely read current button values (may be None initially)
    current_next = next_button.value if (next_button is not None and next_button.value is not None) else 0
    current_reset = reset_button.value if (reset_button is not None and reset_button.value is not None) else 0

    # --- Handle Reset ---
    # Only act if reset button count increased relative to a stored sentinel (we'll use a global reset_count stored in state)
    if "reset_count" not in state:
        state["reset_count"] = 0

    if current_reset > state["reset_count"]:
        for key in ("bubble", "insertion", "merge"):
            state[key]["arr"] = np.random.randint(0, 100, n)
            state[key]["i"] = 0         # <- reset step to 0
            state[key]["last_next"] = current_next




        state["reset_count"] = current_reset
        state["timings"].clear()

        # refresh local references
        algo_state = state[dropdown.value]
        arr = algo_state["arr"]
        i = algo_state.get("i", 0)

    colors = ["skyblue"] * n

    # --- Only perform a step when the Increment button has advanced for THIS algorithm ---
    last_next = algo_state.get("last_next", 0)
    if current_next > last_next:
        # mark we handled this press for this algorithm
        algo_state["last_next"] = current_next

        start = ti.perf_counter()

        match dropdown.value:
            case "bubble":
                # perform one outer pass
                if i < n - 1:
                    for j in range(n - i - 1):
                        if arr[j] > arr[j + 1]:
                            arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    algo_state["i"] = i + 1  # update stored i
                    i = algo_state["i"]
                # colour sorted tail
                for k in range(n - i, n):
                    colors[k] = "lightgreen"

            case "insertion":
                # perform one insertion of element at i+1
                if i < n - 1:
                    key = arr[i + 1]
                    j = i
                    while j >= 0 and arr[j] > key:
                        arr[j + 1] = arr[j]
                        j -= 1
                    arr[j + 1] = key
                    algo_state["i"] = i + 1
                    i = algo_state["i"]
                # colour sorted prefix
                for k in range(i + 1):
                    colors[k] = "lightgreen"

            case "merge":
                # bottom-up merge sort: one full merge pass per step i
                i = algo_state["i"]  # read step
                size = 1 << i         # compute size dynamically

                if size < n:
                    for left in range(0, n, 2 * size):
                        mid = min(left + size, n)
                        right = min(left + 2 * size, n)

                        i1, i2 = left, mid
                        merged = []

                        while i1 < mid and i2 < right:
                            if arr[i1] <= arr[i2]:
                                merged.append(arr[i1])
                                i1 += 1
                            else:
                                merged.append(arr[i2])
                                i2 += 1

                        if i1 < mid:
                            merged.extend(arr[i1:mid])
                        if i2 < right:
                            merged.extend(arr[i2:right])

                        arr[left:right] = merged

                    # increment step
                    algo_state["i"] += 1
                    i = algo_state["i"]

                # colour guaranteed sorted prefix
                for k in range(min(2 * size, n)):
                    colors[k] = "lightgreen"

        elapsed = ti.perf_counter() - start  # end timing
        state["timings"].append(elapsed)     # store value

    else:
        # Only colour previously-sorted part if step > 0
        if algo_state["i"] > 0:
            if dropdown.value == "bubble":
                for k in range(n - algo_state["i"], n):
                    colors[k] = "lightgreen"
            elif dropdown.value == "insertion":
                for k in range(algo_state["i"] + 1):
                    colors[k] = "lightgreen"
            elif dropdown.value == "merge":
                size = 1 << algo_state["i"]
                for k in range(min(2 * size, n)):
                    colors[k] = "lightgreen"




    # --- Plot (fixed y-scale) ---
    fig = go.Figure(data=[go.Bar(x=np.arange(n), y=arr, marker_color=colors)])
    fig.update_layout(
        title=f"{dropdown.value.title()} Sort – Step {algo_state['i']}",
        xaxis_title="Index",
        yaxis_title="Value",
        template="plotly_white",
        width=600,
        height=350
    )
    fig.update_yaxes(range=[0, 100])  # keep y-scale fixed

    mo.hstack([mo.ui.plotly(fig)])
    return


@app.cell
def _(mo, next_button, state):
    _ = next_button.value  # trigger re-run when button pressed

    timings = state.get("timings", [])
    N = 2  # Number of steps to average

    msg = (
        f"Average time for last {min(len(timings), N)} step(s): "
        f"{sum(timings[-N:]) / min(len(timings), N):.6f} seconds"
        if timings
        else "No timing data yet."
    )

    mo.md(msg)
    return


@app.cell
def _(dropdown, mo):
    explanations = {
        "bubble": """
    **Bubble Sort:**  
    Bubble sort is a simple comparison-based sorting algorithm that repeatedly goes through a list, compares adjacent elements, and swaps them if they are in the wrong order. This process continues until the list is fully sorted. With each pass, the largest unsorted elements move toward the end of the list, which is why the algorithm is described as “bubbling” elements to the top. While bubble sort is easy to understand and implement, it is inefficient for large datasets and is mainly used for educational purposes rather than practical applications.
    """,
        "insertion": """
    **Insertion Sort:**  
    Insertion sort works by building a sorted section of the list one element at a time. It starts by assuming the first element is already sorted, then takes the next element and inserts it into its correct position among the previously sorted elements by shifting larger values to the right. This process is repeated until all elements are placed correctly. Insertion sort is simple and performs well on small datasets or lists that are already nearly sorted, making it useful in certain practical scenarios despite its poor performance on large, unsorted datasets.
    """,
        "merge": """
    **Merge Sort:**  
    Merge sort is a more advanced sorting algorithm based on the divide-and-conquer approach. It works by repeatedly dividing the list into smaller sublists until each sublist contains only one element, which is inherently sorted. These sublists are then merged back together in sorted order to produce larger sorted lists, eventually resulting in a fully sorted list. Merge sort is highly efficient and consistent in performance, making it suitable for large datasets, although it requires additional memory to store the temporary sublists during the merging process.
    """
    }
    mo.md(explanations[dropdown.value]).callout(kind="info")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## AI Use & Acknowledgement

    AI tools (ChatGPT, GPT-5 family) were used as a development assistant during the creation of this notebook, rather than as a source of final answers or complete solutions.

    Specifically, AI assistance supported:
    - Debugging logic and state-handling issues in the Marimo interactive environment (buttons, dropdowns, and step-based execution).
    - Refining algorithm visualisation behaviour, including step-by-step execution, colouring of sorted/unsorted regions, and reset logic.
    - Improving code clarity, structure, and readability without altering the underlying algorithms.
    - Suggesting safe and idiomatic Python patterns for timing, plotting, and UI updates.

    All sorting algorithms (Insertion Sort, Bubble Sort, and Merge Sort), performance comparisons, explanations, and data values were implemented and verified manually by me, based on material covered in lectures and independent understanding of the algorithms.
    """)
    return


if __name__ == "__main__":
    app.run()
