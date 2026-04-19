import marimo

__generated_with = "0.16.5"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Graphs""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout("Disclaimer: no AI tools were used to create this notebook.")
    return


@app.cell
def _():
    import networkx as nx, matplotlib.pyplot as plt, numpy as np
    return np, nx, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 1
    Modify ```edge_list.txt```,```adjacency_list.txt``` to obtain the given graph
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### 1. Adjacency list:""")
    return


@app.cell
def _(nx):
    fh = open('adjacency_list.txt', 'rb')
    G = nx.read_adjlist(fh)
    return (G,)


@app.cell
def _(G):
    G.edges()
    return


@app.cell
def _(G, nx, plt):
    nx.draw(G,with_labels = True)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### 2. Edge list:""")
    return


@app.cell
def _(nx):
    _fh = open('edge_list.txt', 'rb')
    H = nx.read_edgelist(_fh)
    _fh.close()
    return (H,)


@app.cell
def _(H, nx, plt):
    nx.draw(H,with_labels = True)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""#### 3. Adjacency Matrix""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""Now create a 2D numpy.array that defines the adjacency matrix""")
    return


@app.cell
def _(np):
    # your code here:
    A = np.array([
    [0, 1, 0, 1, 0],
    [1, 0, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1],
    [0, 0, 1, 1, 0]])
    return (A,)


@app.cell
def _(A, nx, plt):
    G_1 = nx.from_numpy_array(A)
    nx.draw(G_1, with_labels=True)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 2
    Implement the Depth-first search algorithm. You only need to complete the recursive part ```DSF_rec()```
    """
    )
    return


@app.cell
def _():
    def DFS(source_node,adj_list,target):
        visited = [False]*len(adj_list)
        DFS_rec(source_node,visited,adj_list,target)


    def DFS_rec(n,visited,adj_list,target):
        visited[n] = True
        print(n)

        if n == target:
            return True

        for neighbour in adj_list[n]:
            if not visited[neighbour]:
                found = DFS_rec(neighbour, visited, adj_list, target)
                if found:
                    return True   

        return False  
    return (DFS,)


@app.cell
def _(DFS):
    adj = [
        [1, 3],            # node 0
        [0, 2, 3],         # node 1
        [1, 3, 4],         # node 2
        [0, 1, 2, 4],      # node 3
        [3, 2]             # node 4
    ]


    DFS(3,adj,0)
    return (adj,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Task 3
    Implement the Breadth-first search algorithm.
    """
    )
    return


@app.function
def BFS(source_node, adjacency_list,target):
    queue = []
    visited = [False]*len(adjacency_list)

    queue.insert(0,source_node)
    visited[source_node] = True

    while (len(queue) > 0):
        current_node = queue.pop(0)
        print(current_node)
        if current_node == target:
            return current_node 

        for neighbour in adjacency_list[current_node]:
            if not visited[neighbour]:
                queue.append(neighbour)
                visited[neighbour] = True

    return None


@app.cell
def _(adj):
    BFS(3,adj,0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Task 4""")
    return


@app.cell
def _():
    graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
               [4, 0, 8, 0, 0, 0, 0, 11, 0],
               [0, 8, 0, 7, 0, 4, 0, 0, 2],
               [0, 0, 7, 0, 9, 14, 0, 0, 0],
               [0, 0, 0, 9, 0, 10, 0, 0, 0],
               [0, 0, 4, 14, 10, 0, 2, 0, 0],
               [0, 0, 0, 0, 0, 2, 0, 1, 6],
               [8, 11, 0, 0, 0, 0, 1, 0, 7],
               [0, 0, 2, 0, 0, 0, 6, 7, 0]
               ]
    return (graph,)


@app.function
def dijkstra(g,source):


    #Helper function that finds the closest node that is not still visited 
    def minDistance(dist, visited,g):

        minDist = 10000

        for v in range(len(g)):
            if dist[v] < minDist and visited[v] == False:
                minDist = dist[v]
                min_index = v

        return min_index


@app.cell
def _(graph):
    dijkstra(graph,0)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## Final Task:
    Re-use the code from previous weeks (in particular, where we visualised trees like Binary Search or Merge Sort) to visualise the traversal of a graph. Your code should allow the user to show in a dropdown menu between BFS and DFS. then, the code would iterate every time the user presses a ```Next``` button. The visualisation should show nodes that have been visited in a different colour than the not visited. 

    ### Extra task (not compulsory):
    - Add a third colour to the node that is currently being visited.
    - Use the ```mo.refresh()``` function to create an automated animation, instead of the user pressing each time for the next iteration.
    """
    )
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def _(mo, nx, plt):
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

        node_colors = []
        for i, node in enumerate(G.nodes):
            data = G.nodes[node]
            if data.get("is_path", False):
                node_colors.append("deepskyblue")   # visited
            elif i == max(G.nodes):  # last added = current node
                node_colors.append("orange")        # current node
            else:
                node_colors.append("lightgray")     # unvisited


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
    return


@app.cell
def _(mo):
    start_node_input = mo.ui.text(label="Start Node", value="0")
    return (start_node_input,)


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


@app.cell
def _(mo):
    algorithm_choice = mo.ui.dropdown(
        options={
            "Breadth-first Search": "bfs",
            "Depth-first Search": "dfs"
        },
        value="Breadth-first Search",  # Set default value explicitly to avoid blank 
        label="Algorithm"
    )
    return (algorithm_choice,)


@app.cell
def _(
    adj,
    algorithm_choice,
    get_count,
    mo,
    next_btn,
    reset_btn,
    start_node_input,
):
    # Access the dropdown value to force marimo to track it as a dependency
    algo = algorithm_choice.value

    # --------------------------
    # BFS (actual graph layout)
    # --------------------------
    if algo == "bfs":
        start = int(start_node_input.value)

        steps = record_bfs(adj, start)
        step = min(get_count(), len(steps))

        graph_fig = draw_actual_graph(adj, steps, step)

        output = mo.vstack([
            mo.hstack([algorithm_choice, start_node_input, next_btn, reset_btn]),
            mo.md(f"### BFS — Step {step}/{len(steps)}"),
            mo.mpl.interactive(graph_fig),
        ])

    # --------------------------
    # DFS (actual graph layout)
    # --------------------------
    else:  # dfs
        start = int(start_node_input.value)

        steps = record_dfs(adj, start)
        step = min(get_count(), len(steps))

        graph_fig = draw_actual_graph(adj, steps, step)

        output = mo.vstack([
            mo.hstack([algorithm_choice, start_node_input, next_btn, reset_btn]),
            mo.md(f"### DFS — Step {step}/{len(steps)}"),
            mo.mpl.interactive(graph_fig),
        ])

    output
    return


@app.function
def record_bfs(adj_list, start):

    queue = [start]
    discovered = set([start])   # queued
    visited = set()             # actually visited
    steps = []

    while queue:
        current = queue.pop(0)

        visited.add(current)    # only NOW mark as visited

        # Record the moment we VISIT the node
        steps.append(("visit", current, visited.copy()))

        for n in adj_list[current]:
            if n not in discovered:
                discovered.add(n)
                queue.append(n)

    return steps


@app.function
def record_dfs(adj_list, start):
    visited = set()
    steps = []

    def dfs(node):
        visited.add(node)

        # Record only visit events
        steps.append(("visit", node, visited.copy()))

        for n in adj_list[node]:
            if n not in visited:
                dfs(n)

    dfs(start)
    return steps


@app.function
def draw_actual_graph(adj_list, steps, step_index):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()
    for node, neighs in enumerate(adj_list):
        for n in neighs:
            G.add_edge(node, n)

    # Extract visited + current node
    action, current, visited = steps[step_index - 1]

    # Colors
    node_colors = []
    for node in G.nodes:
        if node == current:
            node_colors.append("orange")       # current
        elif node in visited:
            node_colors.append("deepskyblue")  # visited
        else:
            node_colors.append("lightgray")    # not visited

    # FIXED positions
    pos = {
        0: (0.5, 1.0),
        1: (0.2, 0.7),
        2: (0.3, 0.4),
        3: (0.7, 0.7),
        4: (0.8, 0.4),
    }

    plt.figure(figsize=(6, 5))
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        node_size=900,
        font_size=10,
        edgecolors="black"
    )
    plt.title(f"Step {step_index}: visiting node {current}")
    return plt.gcf()


@app.function
def traversal_tree(steps):
    """
    Converts BFS/DFS steps into the same format used by binary-search trees:
    (id, parent, label, is_path)
    """
    tree = []
    parent = None

    for i, (action, node, visited) in enumerate(steps):
        label = f"Node: {node}\nVisited: {list(visited)}"
        is_path = (action == "visit")

        tree.append((i, parent, label, is_path))
        parent = i

    return tree


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""To do: Add in automatic play to run through all steps for extra task, use next_btn""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    ---
    ## AI Use & Acknowledgement

    AI tools (ChatGPT, GPT-5 family) were used only during the Final Task of this notebook, and solely in a limited, supportive capacity.

    AI assistance was restricted to:
    - High-level guidance on structuring an interactive, step-by-step visualisation of graph traversal within a Marimo notebook.
    - Suggestions on connecting UI components (dropdown selection between BFS and DFS, “Next” and “Reset” buttons, and state counters) to traversal progression logic.
    - Clarification on how to record traversal steps incrementally (e.g. storing visited nodes per step) to enable controlled iteration through BFS and DFS.
    - Advice on visually differentiating node states using colour (unvisited, visited, currently active node) in NetworkX/Matplotlib plots.
    - Minor guidance on maintaining consistent node positioning to prevent layout changes between steps.
    - General suggestions for separating traversal logic (recording BFS/DFS steps) from visualisation logic to improve clarity and maintainability.

    All algorithmic content including the implementations of Breadth-First Search (BFS), Depth-First Search (DFS), traversal correctness, adjacency representations, was designed, implemented, and tested independently by me, based on lecture material and my own understanding.
    """
    )
    return


if __name__ == "__main__":
    app.run()
