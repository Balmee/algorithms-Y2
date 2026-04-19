import marimo

__generated_with = "0.19.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import micropip                  # Used from Pyodide which is used in browser toinstall pure Python packages dynamically using micropip,
    await micropip.install("plotly") # This case being plotly
    import plotly.graph_objects as go
    return (mo, np, go)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 1:
    Implement the Binary Search Algorithm for a sorted input array.
    """)
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


@app.cell
def _():
    binSearch([3,6,78,86,238,489,623],3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 2:
    Implement the Recursive Binary Search Algorithm for a sorted input array.
    """)
    return


@app.function
def binSearchRec(arr, target, left, right):
    if (left <= right):  
        mid = (left + right) // 2
        if (target == arr[mid]):
            return mid

        elif (target <arr[mid]):
            right = mid - 1
            return binSearchRec(arr, target, left, right)
        else:...

    return -1


@app.cell
def _():
    binSearchRec([3,6,78,86,238,489,623],86, 0, 6)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 3:
    Implement Merge Sort algorithm
    """)
    return


@app.cell
def _():
    def merge_sort(array):

        if len(array) <= 1:
            return array

        mid = len(array) // 2
        left_half = array[:mid]
        right_half = array[mid:]
        left_sorted = merge_sort(left_half)
        right_sorted = merge_sort(right_half)
        return merge(left_sorted, right_sorted)

    def merge(left, right):
        merged = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged


    # Testing:
    array = [38, 27, 43, 3, 9, 82, 10]
    sorted_array = merge_sort(array)
    print("Original array:", array)
    print("Sorted array:", sorted_array)
    return (merge_sort,)


@app.cell
def _(merge_sort):
    merge_sort([38, 27, 43, 3, 9, 82, 10])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 4:
    Implement Quicksort (last element as a pivot)
    """)
    return


@app.cell
def _():
    def quicksort(Q):

        if len(Q) <= 1:
            return Q

        pivot = Q[-1]
        left = [x for x in Q[:-1] if x < pivot]    ## loop through each element (x)
        equal = [x for x in Q if x == pivot]
        right = [x for x in Q[:-1] if x > pivot]
        return quicksort(left) + equal + quicksort(right)


    # Example usage:
    Q = [10, 7, 8, 9, 1, 5]
    sorted_Q = quicksort(Q)
    print("Original Q:", Q)
    print("Sorted Q:", sorted_Q)
    return (quicksort,)


@app.cell
def _(quicksort):
    quicksort([38, 27, 43, 3, 9, 82, 10])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Final Task
    Below you will find a series of cells that help you to plot a tree structure. A tree structure here is something like the following:
    """)
    return


@app.cell
def _():
    exampleTree = [(0, None, [8, 3, 5, 4, 7, 6, 1, 2]), (1, 0, [8, 3, 5, 4]),(2,0,[7,6,1,2]) ,(3,1,[8,3]),(4,1,[5,4]),(5, 2, [7,6])]
    return (exampleTree,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can use the helper functions to plot this tree structure for different iterations
    """)
    return


@app.cell
def _(build_graph, draw_tree, exampleTree):
    F = build_graph(exampleTree,3)
    draw_tree(F)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
            r"""
        ---------------------
        The following code was generated initially with GPT-5 plus iterations. The code generated all the helper functions defined in the first cell. The author modified it to be displayed and plotted as a tree structure using networkx library.  

        ----------
        """
        ).callout()
    return


@app.cell(hide_code=True)
def _(mo):
    import networkx as nx
    import matplotlib.pyplot as plt


    def build_graph(tree, step):
        G = nx.DiGraph()
        for entry in tree[:step]:
            if len(entry) == 4:
                node, parent, arr, is_path = entry
            else:
                node, parent, arr = entry
                is_path = False

            G.add_node(node, label=str(arr), is_path=is_path)
            if parent is not None:
                G.add_edge(parent, node)
        return G





    def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):

        if not nx.is_tree(G):
            raise TypeError("hierarchy_pos only works for trees.")

        if root is None:
            root = next(n for n,d in G.in_degree() if d==0)  # find node with in-degree 0

        def _hierarchy_pos(G, node, left, right, vert_loc, pos):
            children = list(G.successors(node))
            pos[node] = ((left + right) / 2, vert_loc)
            if len(children) != 0:
                dx = (right - left) / len(children)
                nextx = left
                for child in children:
                    _hierarchy_pos(G, child, nextx, nextx + dx, vert_loc - vert_gap, pos)
                    nextx += dx
            return pos

        return _hierarchy_pos(G, root, 0, width, vert_loc, {})


    def draw_tree(G):
        pos = hierarchy_pos(G)
        labels = nx.get_node_attributes(G, "label")

        # Default color: lightgray, path color: skyblue
        node_colors = []
        for node in G.nodes:
            if G.nodes[node].get("is_path", False):
                node_colors.append("deepskyblue")
            else:
                node_colors.append("lightgray")

        plt.figure(figsize=(6, 4))
        nx.draw(
            G,
            pos,
            with_labels=True,
            labels=labels,
            font_size=6,
            node_size=600,
            node_color=node_colors,
            edgecolors="black",
        )
        plt.axis("off")

        drawM = mo.mpl.interactive(plt.gcf())
        return drawM
    return build_graph, draw_tree


@app.cell(hide_code=True)
def _(mo):
    arr_input = mo.ui.text(label="Enter array (comma-separated)", value="8,3,5,4,7,6,1,2")
    return (arr_input,)


@app.cell
def _(mo):
    search_value_input = mo.ui.text(label="Value to search", value="5")
    return (search_value_input,)


@app.cell(hide_code=True)
def _(mo):
    next_btn = mo.ui.button(label="Next Step ▶️")
    return (next_btn,)


@app.cell(hide_code=True)
def _(mo):
    reset_btn = mo.ui.button(label="🔄 Reset")
    return (reset_btn,)


@app.cell(hide_code=True)
def _(mo):
    get_count, set_count = mo.state(1)
    return get_count, set_count


@app.cell(hide_code=True)
def _(get_count, next_btn, set_count):
    next_btn
    set_count(get_count()+1)
    print(get_count())
    return


@app.cell(hide_code=True)
def _(reset_btn, set_count):
    reset_btn
    set_count(0)
    return


@app.cell(hide_code=True)
def _(arr_input):
    arr_text = arr_input.value
    arr = [int(x.strip()) for x in arr_text.split(",") if x.strip().isdigit()]
    return (arr,)


@app.function
def tree_bin_search(arr, val, tree=None, id=0, parent=None):
    if tree is None:
        tree = []

    # To determine if this node contains the search value
    is_path = val in arr

    # Add this node to the tree
    tree.append((id, parent, arr, is_path))

    # Base case
    if len(arr) <= 1:
        return tree

    mid = len(arr) // 2
    mid_val = arr[mid]
    left = arr[:mid]
    right = arr[mid + 1:]

    # Recursively build both branches
    if left:
        tree_bin_search(left, val, tree, id + 1, id)
    if right:
        # Use offset for unique IDs
        offset = id + 1 + len(left)
        tree_bin_search(right, val, tree, offset, id)

    return tree


@app.function
def tree_merge_sort(arr, tree= [], id=[0], parent=None):
    current_id = id[0]
    tree.append((current_id, parent, arr.copy()))
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        id[0] += 1
        tree_merge_sort(L, tree, id, current_id)
        id[0] += 1
        tree_merge_sort(R, tree, id, current_id)

        i=j=k=0
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

    return tree


@app.function
def tree_quicksort(arr, tree=[], id=[0], parent=None):
    current_id = id[0]

    if len(arr) > 1:
        # Use the last element as pivot (deterministic, no randomness)
        pivot = arr[-1]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        # Create a visual representation showing partitions with pivot highlighted
        # Format: "[left] | pivot | [right]"
        partition_display = str(left) + " | " + str(pivot) + " | " + str(right)
        tree.append((current_id, parent, partition_display))

        # Recurse on left
        if len(left) > 0:
            id[0] += 1
            if len(left) == 1:
                tree.append((id[0], current_id, str(left)))
            else:
                tree_quicksort(left, tree, id, current_id)

        # Recurse on right
        if len(right) > 0:
            id[0] += 1
            if len(right) == 1:
                tree.append((id[0], current_id, str(right)))
            else:
                tree_quicksort(right, tree, id, current_id)
    else:
        # Base case: single element or empty
        tree.append((current_id, parent, str(arr)))

    return tree


@app.cell
def _(mo):
    algorithm_choice = mo.ui.dropdown(
    options={
        "Binary Search": "binary",
        "Merge Sort": "merge",
        "Quicksort": "quicksort"
    },
    value="Binary Search",
    label="Algorithm"
    )
    return (algorithm_choice,)


@app.cell
def _(
    algorithm_choice,
    arr,
    arr_input,
    build_graph,
    draw_tree,
    get_count,
    mo,
    next_btn,
    reset_btn,
    search_value_input,
):
    # Access the dropdown value to force marimo to track it as a dependency
    algo = algorithm_choice.value

    # --------------------------
    # BINARY SEARCH (tree view)
    # --------------------------
    if algo == "binary":
        val = int(search_value_input.value) if search_value_input.value.isdigit() else None
        tree_data = tree_bin_search(arr, val, tree=[])
        step = min(get_count(), len(tree_data))
        G_show = build_graph(tree_data, step)

        output = mo.vstack([
            mo.hstack([arr_input, algorithm_choice, search_value_input, next_btn, reset_btn]),
            mo.md(f"### Binary Search — Step {step}/{len(tree_data)}"),
            draw_tree(G_show),
        ])

    # --------------------------
    # MERGE SORT (tree view)
    # --------------------------
    elif algo == "merge":
        tree_data = tree_merge_sort(arr.copy(), tree=[], id=[0])
        step = min(get_count(), len(tree_data))
        G_show = build_graph(tree_data, step)

        output = mo.vstack([
            mo.hstack([arr_input, algorithm_choice, next_btn, reset_btn]),
            mo.md(f"### Merge Sort — Step {step}/{len(tree_data)}"),
            draw_tree(G_show),
        ])

    # --------------------------
    # QUICKSORT (tree view)
    # --------------------------
    elif algo == "quicksort":
        tree_data = tree_quicksort(arr.copy(), tree=[], id=[0])
        step = min(get_count(), len(tree_data))
        G_show = build_graph(tree_data, step)

        output = mo.vstack([
            mo.hstack([arr_input, algorithm_choice, next_btn, reset_btn]),
            mo.md(f"### Quicksort — Step {step}/{len(tree_data)}"),
            draw_tree(G_show),
        ])

    output
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Tasks:
    - Modify the previous cell so it allows the user to input the value to search for (now it is fixed to 5)
    - Create a new function ```tree_merge_sort()```. This function is similar to ```tree_bin_search()``` but it created the tree for a Merge Sort algorithm (i.e. instead of only opening one branch like binary search, now it always open two branches). Use the same helper functions to plor the merge sort tree for each iteration.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Extra Tasks (not compulsory, just if you want to learn more):
    - Add a dropdown menu that allows you to choose between Binary Search and Mergesort and then it shows the corresponding tree.
    - Add as a third option the Quicksort algorithm with its corresponding tree
    - Modify the helper functions so for the Binary search algorithm it displays the whole tree (not only the chosen left or right child node), and it also show the chosen path (i.e. chosen nodes) with a different colour. You might have to add an extra attribute to the nodes of the tree that accounts whether they belong to the path or not. Then, in the ```draw_tree()``` helper function (particularly, in the ```nx.draw()``` part) you can give a ```color``` option to nodes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Completed all tasks!
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## AI Use & Acknowledgement

    AI tools (ChatGPT, GPT-5 family) were used in a limited and supportive capacity during the development of this notebook.

    AI assistance was restricted to:
    - General debugging guidance for Python syntax, recursion structure, and logical errors.
    - Clarifying usage of standard Python libraries and common visualisation patterns.
    - Suggesting minor improvements to code readability and structure.
    """)
    return


if __name__ == "__main__":
    app.run()
