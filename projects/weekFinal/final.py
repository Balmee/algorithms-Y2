import marimo

__generated_with = "0.19.4"
app = marimo.App()


@app.cell
def _(mo):
    mo.md("""
    # S.T.A.R.S Mission Allocation System

    An **interactive tactical decision-support simulator** for allocating
    **S.T.A.R.S operatives** to missions across **Raccoon City**.

    ## Algorithms Demonstrated
    - Quicksort-based stat ranking
    - Distance-based search with penalties
    - Genetic Algorithm mission optimisation
    - Perceptron-based mission success prediction

    User acts as the dispatch officer where these members are allocated to mission areas to achieve their goals, which is determined by **Misison success rate**.

    The goal I wanted to show here was how user input can change and build up new data, and do the narative selected seemed appropriate to achieve this goal in the most creative way.

    ⚠️ As a result of this page running on Github Pages and requiring Pyodide to run Plotly, the time graphs may show some annomalies as a result of Micropip installing this library live each time.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import math
    import random
    import time
    from dataclasses import dataclass
    return dataclass, math, mo, np, plt, random, time


@app.cell
def _(dataclass):
    @dataclass
    class StarsMember:
        id: int
        name: str
        strength: int
        vigour: int
        mobility: int
        charisma: int
        intellect: int
        location: tuple  # (x, y)
    return (StarsMember,)


@app.cell
def _(StarsMember):
    members_list = [
        StarsMember(1, "Jill Valentine", 8, 7, 9, 6, 7, (2, 3)),
        StarsMember(2, "Chris Redfield", 9, 8, 6, 5, 6, (7, 1)),
        StarsMember(3, "Barry Burton", 7, 9, 5, 6, 5, (0, 4)),
        StarsMember(4, "Rebecca Chambers", 5, 6, 7, 8, 9, (4, 4)),
    ]
    return (members_list,)


@app.cell
def _():
    missions_list = [
        {"id": "Hospital", "location": (5, 5), "required": 2, "difficulty": 7},
        {"id": "Police Station", "location": (1, 1), "required": 2, "difficulty": 6},
        {"id": "Laboratory", "location": (8, 3), "required": 2, "difficulty": 9},
    ]
    return (missions_list,)


@app.cell
def _():
    """
    Persistent training history.
    Key: member name
    Value: list of training events
    """
    training_history = {}
    return (training_history,)


@app.cell
def _(mo):
    mo.md(r"""
    # Quicksort
    - Sort members by specific stats
    """)
    return


@app.function
def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


@app.function
def euclidean_distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


@app.function
def quicksort_members(arr, key):
    if len(arr) <= 1:
        return arr
    pivot = getattr(arr[len(arr) // 2], key)
    left = [x for x in arr if getattr(x, key) > pivot]
    middle = [x for x in arr if getattr(x, key) == pivot]
    right = [x for x in arr if getattr(x, key) < pivot]
    return quicksort_members(left, key) + middle + quicksort_members(right, key)


@app.cell
def _(mo):
    sort_stat_ui = mo.ui.dropdown(
        options=["strength", "vigour", "mobility", "charisma", "intellect"],
        value="strength",
        label="📊 Sort members by stat"
    )
    return (sort_stat_ui,)


@app.cell
def _(members_list, mo, plt, sort_stat_ui):
    sorted_members = quicksort_members(members_list, sort_stat_ui.value)

    names = [n.name for n in sorted_members]
    values = [getattr(n, sort_stat_ui.value) for n in sorted_members]

    plt.figure()
    plt.barh(names, values)
    plt.xlabel(sort_stat_ui.value.capitalize())
    plt.title("Quicksort Ranking")
    plt.gca().invert_yaxis()

    md_lines = [f"### Ranked by {sort_stat_ui.value.capitalize()}"]
    for n in sorted_members:
        md_lines.append(f"- **{n.name}** → {getattr(n, sort_stat_ui.value)}")

    mo.vstack([
        mo.hstack([sort_stat_ui]),

            mo.md("\n".join(md_lines)),
            mo.mpl.interactive(plt.gcf())

    ])
    return


@app.function
def search_member_with_penalty(
    member,
    mission_location,
    radius=3,
):
    """
    Compute distance and apply a penalty if the member
    is outside the effective mission radius.
    """
    dist = manhattan_distance(member.location, mission_location)
    penalty = 1 if dist > radius else 0

    adjusted_stats = {
        "strength": max(1, member.strength - penalty),
        "vigour": max(1, member.vigour - penalty),
        "mobility": max(1, member.mobility - penalty),
        "charisma": max(1, member.charisma - penalty),
        "intellect": max(1, member.intellect - penalty),
    }

    return dist, penalty, adjusted_stats


@app.cell
def _(mo):
    sort_text = """
    **Quicksort — Sorting Algorithm**

    Quicksort is used in this system to rank S.T.A.R.S members efficiently based on a chosen attribute such as strength, mobility, or intellect. Sorting is a core requirement because decision-making often depends on quickly identifying the strongest or weakest candidates for a task. Quicksort was chosen over alternatives like bubble sort or insertion sort due to its superior average-case performance of O(n log n), making it well suited for scalable systems. Its divide-and-conquer approach mirrors real-world prioritisation, where a pivot criterion is used to split candidates into higher and lower-priority groups. This makes Quicksort the most fitting for my tactical ranking.
    """

    # Display it in the blue Markdown box
    mo.md(sort_text).callout(kind="info")
    return


@app.cell
def _(mo):
    sort_crit = """
    **Quicksort — Critical Aspects and Bias Analysis**

    Although Quicksort is an efficient and widely used sorting algorithm, it can introduce indirect bias depending on how I have applied it. Bias arises from the choice of sorting key, ranking S.T.A.R.S members solely by a single attribute such as strength or intellect can disadvantage individuals who are more balanced or who excel in other relevant attributes, requiring user to check all dropdowns each time before a run. This may lead to systematic over-selection of specialists and underutilisation of versatile members, when it comes to stat improvement later in the GA section. Additionally, poor pivot selection can result in worst-case O(n²) performance, which could disproportionately impact larger datasets and reduce responsiveness in time-critical systems.

    To mitigate this, the system allows dynamic selection of sorting criteria and encourages repeated re-sorting based on different attributes. A potential improvement would be multi-criteria sorting or weighted scoring rather than single-stat ordering. This would give a better perception to the user which member has the highest stats as well as could show the mean, mode and meadian.
    """

    # Display it in the blue Markdown box
    mo.md(sort_crit).callout(kind="info")
    return


@app.cell
def _(members_list, mo):
    member_search_ui = mo.ui.dropdown(
        options=["Select member"] + [m.name for m in members_list],
        value=members_list[0].name,
        label="👤 Select S.T.A.R.S Member"
    )
    return (member_search_ui,)


@app.cell
def _(missions_list, mo):
    mission_search_ui = mo.ui.dropdown(
        options=["Select mission"] + [m["id"] for m in missions_list],
        value=missions_list[0]["id"],
        label="📍 Select Mission Location"
    )
    return (mission_search_ui,)


@app.cell
def _(mo):
    radius_ui = mo.ui.slider(
        start=0,
        stop=10,
        step=1,
        value=3,
        label="🛑 Effective Radius Before Penalty"
    )
    return (radius_ui,)


@app.cell
def _(mo):
    mo.md(r"""
    #Searching
    - Find members distance to mission areas, and use the dropdown to move each member to mission area.
    - Penalties are created later on due to the search between the mission centre and members location.
    - Encourages mission movement to better the missions success rate for next time.
    - History is recorded to show who has been used more and where that member has moved across the map.
    """)
    return


@app.cell
def _(
    member_search_ui,
    members_list,
    mission_search_ui,
    missions_list,
    mo,
    plt,
    radius_ui,
):
    # --------------------------
    # DEFAULT UI (ALWAYS RENDERED)
    # --------------------------

    # Default placeholder plot
    plt.figure()
    plt.bar([], [])  # empty plot initially
    plt.axhline(7, linestyle="--")
    plt.ylabel("Stat Value")
    plt.title("Adjusted Stats After Distance Penalty")

    chart = mo.vstack([
        mo.hstack([member_search_ui, mission_search_ui, radius_ui]),
        mo.md("🔍 Select a member and a mission, then adjust the radius to evaluate proximity."),
        mo.mpl.interactive(plt.gcf())
    ])

    # --------------------------
    # ACTIVE STATE (updates if selection is valid)
    # --------------------------

    if member_search_ui.value != "Select member" and mission_search_ui.value != "Select mission":

        # Get the selected member and mission
        member_obj = next(
            m for m in members_list
            if m.name == member_search_ui.value
        )

        mission_obj = next(
            m for m in missions_list
            if m["id"] == mission_search_ui.value
        )

        # Compute distance penalty and adjusted stats
        dist, penalty, adjusted_stats = search_member_with_penalty(
            member_obj,
            mission_obj["location"],
            radius_ui.value,
        )

        # Update the plot
        plt.figure()
        plt.bar(adjusted_stats.keys(), adjusted_stats.values())
        plt.axhline(7, linestyle="--")
        plt.ylabel("Stat Value")
        plt.title("Adjusted Stats After Distance Penalty")

        # Update chart UI (overlays on existing UI)
        chart = mo.vstack([
            mo.hstack([member_search_ui, mission_search_ui, radius_ui]),
            mo.md(f"""
            ## 🔍 Proximity Evaluation

            **Member:** {member_obj.name}  
            **Mission:** {mission_obj["id"]}    
            **Effective Radius:** `{radius_ui.value}`
            """),
            mo.mpl.interactive(plt.gcf())
        ])

    chart
    return


@app.cell
def _(member_search_ui, members_list, mission_search_ui, missions_list, mo):
    member_objective = next(m for m in members_list if m.name == member_search_ui.value)
    mission_objective = next(m for m in missions_list if m["id"] == mission_search_ui.value)

    manhattan = manhattan_distance(member_objective.location, mission_objective["location"])
    euclidean = euclidean_distance(member_objective.location, mission_objective["location"])

    mo.md(f"""
    ### 📐 Distance Metrics Comparison

    - **Manhattan Distance:** `{manhattan}`
    - **Euclidean Distance:** `{euclidean:.2f}`

    > Manhattan distance is used for penalties  
    > to simulate **grid-based urban traversal**.
    """)
    return


@app.cell
def _(missions_list):
    MISSION_POSITIONS = {
        m["id"]: m["location"]
        for m in missions_list
    }
    return (MISSION_POSITIONS,)


@app.cell
def _(mo):
    show_radius_ui = mo.ui.checkbox(
        value=True,
        label="🗺️ Show Mission Radius Overlays"
    )
    return (show_radius_ui,)


@app.cell
def _(mo):
    run_map_button = mo.ui.button(
        label="Run",
        kind="info"
    )
    return (run_map_button,)


@app.cell
def _(mo):
    get_map_run, set_map_run = mo.state(0)
    return get_map_run, set_map_run


@app.cell
def _(get_map_run, run_map_button, set_map_run):
    run_map_button
    set_map_run(get_map_run() + 1)
    return


@app.cell
def _(mo):
    get_last_map_run, set_last_map_run = mo.state(0)
    return get_last_map_run, set_last_map_run


@app.cell
def _():
    movement_history = {}
    return (movement_history,)


@app.cell
def _(math, random):
    def move_member_after_mission(
        member,
        mission_node,
        mission_positions,
        radius,
        run_id,
        movement_history,
    ):
        """
        Move a member to a random position within `radius`
        of the mission location and record the movement.
        """

        def random_point(center, radius):
            angle = random.uniform(0, 2 * math.pi)
            r = radius * math.sqrt(random.random())
            return (
                center[0] + r * math.cos(angle),
                center[1] + r * math.sin(angle),
            )

        old_pos = member.location
        mission_pos = mission_positions[mission_node]

        new_pos = random_point(mission_pos, radius)
        member.location = new_pos

        movement_history.setdefault(member.name, []).append({
            "run": run_id,
            "mission": mission_node,
            "from": old_pos,
            "to": new_pos,
        })
    return (move_member_after_mission,)


@app.cell
def _(
    get_map_run,
    members_list,
    missions_list,
    mo,
    plt,
    radius_ui,
    show_radius_ui,
):
    _ = get_map_run()  # force redraw on movement

    plt.figure(figsize=(6, 6))
    plt.title("Raccoon City — Tactical Overview")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    plt.grid(True, linestyle="--", alpha=0.5)

    for k in members_list:
        plt.scatter(*k.location, s=120)
        plt.text(
            k.location[0] + 0.15,
            k.location[1] + 0.15,
            k.name,
            fontsize=8
        )

    for missi in missions_list:
        loc = missi["location"]
        plt.scatter(*loc, marker="*", s=180)
        plt.text(
            loc[0] + 0.15,
            loc[1] + 0.15,
            missi["id"],
            fontsize=9,
            weight="bold"
        )

        if show_radius_ui.value:
            plt.gca().add_patch(
                plt.Circle(loc, radius_ui.value, alpha=0.15)
            )

    mo.vstack([
        show_radius_ui,
        mo.mpl.interactive(plt.gcf())
    ])
    return


@app.cell
def _(
    MISSION_POSITIONS,
    get_last_map_run,
    get_map_run,
    member_search_ui,
    members_list,
    mission_search_ui,
    missions_list,
    mo,
    move_member_after_mission,
    movement_history,
    radius_ui,
    run_map_button,
    set_last_map_run,
):
    # DEFAULT UI (ALWAYS rendered)
    map = mo.vstack([
        mo.hstack([member_search_ui, mission_search_ui, run_map_button]),
        mo.md("🗺️ Select a member and mission, then press **Run Map**.")
    ])

    # FORCE dependency on map run counter
    run = int(get_map_run())
    last_run = int(get_last_map_run())

    # ACTIVE STATE
    if run > last_run and member_search_ui.value != "Select member" and mission_search_ui.value != "Select mission":

        # Get selected member and mission
        member_0 = next(
            m for m in members_list
            if m.name == member_search_ui.value
        )

        mission = next(
            m for m in missions_list
            if m["id"] == mission_search_ui.value
        )

        # Move member
        move_member_after_mission(
            member=member_0,
            mission_node=mission["id"],
            mission_positions=MISSION_POSITIONS,
            radius=radius_ui.value,
            run_id=run,
            movement_history=movement_history,
        )

        # Update last run
        set_last_map_run(run)

        # Update map UI
        map = mo.vstack([
            mo.hstack([member_search_ui, mission_search_ui, run_map_button]),
            mo.md(f"""
            ## 🗺️ Mission Executed

            **Run #:** {run}  
            **Member:** {member_0.name}  
            **Mission:** {mission['id']}  
            **New Location:** `{member_0.location}`
            """)
        ])

    map
    return


@app.cell
def _(get_map_run, mo, movement_history):
    _ = get_map_run()  # force recompute

    out = mo.md("### 🗺️ No movement data yet.")

    if movement_history:
        mh = ["## 🗺️ Movement History", ""]
        for me, moves in movement_history.items():
            mh.append(f"### 👤 {me}")
            for m in moves:
                mh.append(
                    f"- Run {m['run']} → **{m['mission']}**: "
                    f"{m['from']} → {m['to']}"
                )
            mh.append("")
        out = mo.md("\n".join(mh))

    out
    return


@app.cell
def _(mo):
    search_text = """
    **Search Algorithm — Member & Mission Evaluation**

    A search algorithm is used to evaluate individual S.T.A.R.S members in relation to specific mission locations. Unlike sorting, which orders an entire dataset, search focuses on examining one entity at a time to compute proximity, distance penalties, and adjusted performance. A linear search approach is appropriate here because the data size is relatively small and unsorted, and each evaluation involves constant-time distance calculations. This makes the overall process O(n) when applied to all members match the simplicity and predictability of linear search which aligns well with real-time tactical analysis, where clarity and reliability are more important than complex indexing structures.
    """

    # Display it in the blue Markdown box
    mo.md(search_text).callout(kind="info")
    return


@app.cell
def _(mo):
    search_crit = """
    **Search Algorithm — Critical Aspects and Bias Analysis**

    The search algorithm evaluates members individually by calculating distance-based penalties relative to mission locations. While computationally simple and transparent, this approach may introduce geographical bias, favouring members who are still selected in the dropdown, casusing them to move without a realistic set of rules in a real world map. Over time, this could lead to certain members being repeatedly selected may leave them penalised as they move to mission areas, whereas those who are not do not recieve any penalties and stat decreases, reinforcing unequal participation and experience distribution.

    Populations most affected include members stationed farther from mission hubs or those recently relocated due to prior runs. The bias is structural rather than intentional, emerging from the assumption that proximity should always reduce effectiveness penalties. To counteract this, the system applies soft penalties rather than absolute exclusion, ensuring distant members remain viable candidates. Additionally, both Manhattan and Euclidean distance models are used depending on context, reducing oversimplification of movement constraints.

    Further mitigation could include incorporating transportation resources, fatigue recovery, or rotation policies to prevent repeated disadvantage. Because the algorithm is fully explainable and operates in linear time, its decisions are easy to audit. This transparency makes it suitable for tactical systems where fairness concerns can be actively monitored and adjusted by human operators.
    """

    # Display it in the blue Markdown box
    mo.md(search_crit).callout(kind="info")
    return


@app.cell
def _(mo):
    mo.md(r"""
    # Genetic
    - Using this will show how long it takes a selected member to gain points in their weakest stats. Used here as a response to fatigue which loses stat due to success rate in perceptron section.
    - Recordings are created to show data growing over time, giving a history the user can check to see who has been used more for training.
    """)
    return


@app.function
def extract_stats(member):
    return {
        "strength": member.strength,
        "vigour": member.vigour,
        "mobility": member.mobility,
        "charisma": member.charisma,
        "intellect": member.intellect,
    }


@app.function
def ga_fitness_training(chromosome, base_stats, target_stat):
    """
    Fitness = how fast (in days) the weakest stat
    improves by +1.
    Each gene represents one day of training.
    """
    value = base_stats[target_stat]
    start_value = value
    days = 0

    for gene in chromosome:
        days += 1
        if gene == target_stat:
            value += 0.1  # training gain per day

        if value >= start_value + 1:
            return 1 / days  # faster = better fitness

    return 0.0001


@app.function
def run_training_ga(
    member,
    population_size=40,
    max_days=60,
    generations=80,
    mutation_rate=0.1,
    random_module=None,
):
    stats = extract_stats(member)
    weakest_stat = min(stats, key=stats.get)
    stat_names = list(stats.keys())

    # Initial population
    population = [
        [random_module.choice(stat_names) for _ in range(max_days)]
        for _ in range(population_size)
    ]

    convergence_history = []
    best_days_overall = max_days

    for gen in range(generations):
        population.sort(
            key=lambda c: ga_fitness_training(c, stats, weakest_stat),
            reverse=True
        )

        best = population[0]
        fitness = ga_fitness_training(best, stats, weakest_stat)

        if fitness > 0:
            days_required = int(1 / fitness)
            best_days_overall = min(best_days_overall, days_required)

        convergence_history.append(best_days_overall)

        # Elitism
        new_population = population[:5]

        while len(new_population) < population_size:
            p1, p2 = random_module.sample(population[:20], 2)
            cut = random_module.randint(1, max_days - 1)
            child = p1[:cut] + p2[cut:]

            if random_module.random() < mutation_rate:
                idx = random_module.randint(0, max_days - 1)
                child[idx] = random_module.choice(stat_names)

            new_population.append(child)

        population = new_population

        # Apply improvement to stats (pure result, not mutation)
    updated_stats = stats.copy()
    updated_stats[weakest_stat] += 1

    return {
        "weakest_stat": weakest_stat,
        "days_required": best_days_overall,
        "convergence": convergence_history,
        "updated_stats": updated_stats,
    }


@app.cell
def _(members_list, mo):
    ga_training_member_ui = mo.ui.dropdown(
        options=["Select member"] + [m.name for m in members_list],
        value="Select member",
        label="🧬 Select Member for Training"
    )
    return (ga_training_member_ui,)


@app.cell
def _(mo):
    run_ga_button = mo.ui.button(
        label="🧬 Run GA Training",
        kind="success"
    )
    return (run_ga_button,)


@app.cell
def _(mo):
    get_ga_run, set_ga_run = mo.state(0)
    return get_ga_run, set_ga_run


@app.cell
def _(get_ga_run, run_ga_button, set_ga_run):
    run_ga_button
    set_ga_run(get_ga_run() + 1)
    return


@app.cell
def _(
    ga_training_member_ui,
    get_ga_run,
    members_list,
    mo,
    plt,
    random,
    run_ga_button,
    training_history,
):
    # DEFAULT UI (ALWAYS rendered)
    ga_output = mo.vstack([
        mo.hstack([ga_training_member_ui, run_ga_button]),
        mo.md("🧬 Select a member and press **Run GA Training**.")
    ])

    # FORCE dependency on GA run counter
    run_id = get_ga_run()

    # ACTIVE STATE
    if ga_training_member_ui.value != "Select member" and run_id > 0:
        member = next(
            m for m in members_list
            if m.name == ga_training_member_ui.value
        )

        # Capture original stats
        base_stats = extract_stats(member)

        result = run_training_ga(
            member=member,
            population_size=50,
            max_days=60,
            generations=100,
            mutation_rate=0.1,
            random_module=random,
        )

        weakest = result["weakest_stat"]
        days = result["days_required"]
        convergence = result["convergence"]
        updated_stats = result["updated_stats"]

        original_value = base_stats[weakest]
        updated_value = updated_stats[weakest]
        # Apply returned update to the member
        setattr(member, weakest, updated_value)

        training_history.setdefault(member.name, []).append({
            "stat": weakest,
            "from": original_value,
            "to": updated_value,
            "days": days,
        })

        # Convergence plot
        plt.figure()
        plt.plot(convergence)
        plt.xlabel("Generation")
        plt.ylabel("Days Required for +1 Improvement")
        plt.title("GA Convergence: Training Efficiency")
        plt.grid(alpha=0.3)

        ga_output = mo.vstack([
            mo.hstack([ga_training_member_ui, run_ga_button]),
            mo.md(f"""
            ## 🧬 Genetic Algorithm Training Result

            **Run #:** {run_id}  
            **Member:** {member.name}  
            **Weakest Stat:** `{weakest.capitalize()}`  
            **Stat Improvement:** `{original_value} → {updated_value}`  
            **Days of Practice Required:** `{days}`

            > Only the weakest attribute is trained and improved.
            """),
            mo.mpl.interactive(plt.gcf()),
        ])

    ga_output
    return


@app.function
def compute_average_training_days(events):
    if not events:
        return None
    total_days = sum(e["days"] for e in events)
    return total_days / len(events)


@app.cell
def _(get_ga_run, mo, training_history):
    # Force recompute when GA runs
    _ = get_ga_run()

    black = mo.md("### 📘 Training History\nNo training data available yet.")

    if training_history:
        md = ["## 📘 Training History & Growth Over Time", ""]
        for memb, events in training_history.items():
            avg_days = compute_average_training_days(events)

            md.append(f"### 👤 {memb}")
            md.append(f"- **Training Sessions:** {len(events)}")

            if avg_days is not None:
                md.append(
                    f"- **Average Days per +1 Stat:** `{avg_days:.1f}` days"
                )

            md.append("")
            md.append("| Session | Stat | From → To | Days |")
            md.append("|--------|------|-----------|------|")

            for o, e in enumerate(events, 1):
                md.append(
                    f"| {o} | {e['stat'].capitalize()} | "
                    f"{e['from']} → {e['to']} | {e['days']} |"
                )

            md.append("")
        black = mo.md("\n".join(md))

    black
    return


@app.cell
def _(mo):
    ga_text = """
    **Genetic Algorithm (GA) — Training Optimisation**

    The Genetic Algorithm is used to optimise long-term training decisions by determining how quickly a S.T.A.R.S member can improve their weakest stat through practice. This problem is not well suited to deterministic or greedy algorithms because it involves uncertainty, trade-offs, and many possible training sequences. A GA is ideal for this type of optimisation as it explores a large solution space using evolution-inspired mechanisms such as selection, crossover, and mutation. By simulating generations of training plans, the GA finds an efficient strategy that minimises the number of days required for improvement. This reflects realistic training processes, where progress emerges gradually rather than instantly.
    """

    # Display it in the blue Markdown box
    mo.md(ga_text).callout(kind="info")
    return


@app.cell
def _(mo):
    ga_crit = """
    **Genetic Algorithm — Critical Aspects and Bias Analysis**

    The Genetic Algorithm introduces several potential biases due to its stochastic and heuristic nature. Selection pressure may favour early high-performing solutions, leading to premature convergence and reduced diversity in the population. This can bias results toward specific training patterns that are not globally optimal. Additionally, because the GA focuses exclusively on improving the weakest stat, it may overlook broader skill balance, potentially over-specialising individuals at the expense of overall effectiveness.

    Members with already well-balanced stats may benefit less from the algorithm, while those with extreme weaknesses receive disproportionate attention. This creates a form of optimisation bias that prioritises numerical improvement over contextual usefulness. To mitigate this, the system uses mutation, elitism limits, and convergence tracking to preserve diversity and avoid stagnation.

    Potential improvements should include multi-objective fitness functions, adaptive mutation rates, or fairness constraints that rotate training focus over time. Importantly, the GA’s output is not applied blindly; it returns recommendations that are explicitly visible and interpretable. This human-in-the-loop design ensures that algorithmic bias does not automatically create all system-level decisions. A key aspect of my system is that there is an operator who still makes the final calls, and this system acts as a digital plan essentially.
    """

    # Display it in the blue Markdown box
    mo.md(ga_crit).callout(kind="info")
    return


@app.cell
def _(mo):
    mo.md(r"""
    #Perceptron
    - Final section which determines the success rate of the S.T.A.R.S member on the mission selected earlier in the Search section.
    - This works as the final put together of this system where all prior parts are taken in consideration to recieve a successful mission result.
    - Penalties are applied which were created back in prior sections.
    - Stats may degrade due to the mission success rate being lower than desired and will push the user back to the GA section to build back stats.
    """)
    return


@app.function
def compute_distance_penalty(member, mission, radius):
    # Determine if member is in or out of mission radius
    if manhattan_distance(member.location, mission["location"]) > radius:
        dist = manhattan_distance(member.location, mission["location"])
    else:
        dist = euclidean_distance(member.location, mission["location"])
    max_dist = 15
    penalty_pct = min(1.0, dist / max_dist)
    return penalty_pct


@app.cell
def _(np):
    class TrainableMLP:
        def __init__(self, input_size, hidden_sizes=[12,8], output_size=1, lr=0.05):
            self.lr = lr
            self.weights = []
            self.biases = []
            self.activations = []
            layer_sizes = [input_size] + hidden_sizes + [output_size]
            for i in range(len(layer_sizes)-1):
                w = np.random.randn(layer_sizes[i], layer_sizes[i+1]) * 0.1
                self.weights.append(w)
                b = np.zeros(layer_sizes[i+1])
                # small positive bias to avoid stuck at 0
                if i == len(layer_sizes)-2:
                    b[:] = 0.5
                self.biases.append(b)

        def relu(self, x): return np.maximum(0, x)
        def relu_derivative(self, x): return (x>0).astype(float)
        def sigmoid(self, x): return 1/(1+np.exp(-x))
        def sigmoid_derivative(self, x):
            s = self.sigmoid(x)
            return s*(1-s)

        def forward(self, x):
            self.activations = []
            a = x
            for i in range(len(self.weights)-1):
                z = a @ self.weights[i] + self.biases[i]
                a = self.relu(z)
                self.activations.append((a,z))
            z_out = a @ self.weights[-1] + self.biases[-1]
            out = self.sigmoid(z_out)
            self.activations.append((out,z_out))
            return out.item()

        def train(self, x, y_true):
            y_true = np.array([y_true])
            y_pred = self.forward(x)
            loss_grad = 2*(y_pred - y_true)

            # Output layer
            out_a, out_z = self.activations[-1]
            delta = loss_grad * self.sigmoid_derivative(out_z)
            a_prev = self.activations[-2][0] if len(self.activations)>1 else x
            self.weights[-1] -= self.lr * np.outer(a_prev, delta)
            self.biases[-1] -= self.lr * delta

            # Hidden layers
            delta_next = delta
            for i in reversed(range(len(self.weights)-1)):
                a, z = self.activations[i]
                a_prev = x if i==0 else self.activations[i-1][0]
                delta = (delta_next @ self.weights[i+1].T) * self.relu_derivative(z)
                self.weights[i] -= self.lr * np.outer(a_prev, delta)
                self.biases[i] -= self.lr * delta
                delta_next = delta

    # -----------------------------
    # Persistent instance
    # -----------------------------
    mlp_state = TrainableMLP(input_size=6)  # 5 stats + distance_penalty

    # -----------------------------
    # Synthetic pre-training
    # -----------------------------
    for _ in range(5000):  # more iterations for better learning
        # Random stats between 0 and 100, then normalized to 0–1
        status = np.random.randint(0,101, size=5) / 100
        # Random penalty 0–1
        penal = np.random.rand()
        x = np.append(status, penal)
        # Compute target success as weighted stats minus distance penalty
        y = (0.3*status[0] + 0.25*status[1] + 0.2*status[2] + 0.1*status[3] + 0.15*status[4])
        y *= (1 - penal)
        # Stretch to [0,1] for better gradients
        y = np.clip(y*1.5, 0, 1)
        mlp_state.train(x, y)

    mission_results = {}
    return mission_results, mlp_state


@app.cell
def _():
    mission_history = []
    return (mission_history,)


@app.cell
def _(mo):
    run_mission_btn = mo.ui.button(
        label="🎯 Execute Mission (MLP)",
        kind="danger"
    )
    return (run_mission_btn,)


@app.cell
def _(mo):
    get_mlp_run, set_mlp_run = mo.state(0)
    return get_mlp_run, set_mlp_run


@app.cell
def _(get_mlp_run, run_mission_btn, set_mlp_run):
    run_mission_btn
    set_mlp_run(get_mlp_run() + 1)
    return


@app.cell
def _(
    get_mlp_run,
    member_search_ui,
    members_list,
    mission_history,
    mission_results,
    mission_search_ui,
    missions_list,
    mlp_state,
    mo,
    np,
    radius_ui,
    random,
    run_mission_btn,
):
    # -----------------------------
    # DEFAULT UI
    # -----------------------------
    mlp_output = mo.vstack([
        mo.hstack([run_mission_btn]),
        mo.md("⚠️ Select a member and a mission, then press **Execute Mission**.")
    ])

    run_mlp = get_mlp_run()

    if (
        run_mlp > 0
        and member_search_ui.value != "Select member"
        and mission_search_ui.value != "Select mission"
    ):
        member_object = next(m for m in members_list if m.name == member_search_ui.value)
        mission_object = next(m for m in missions_list if m["id"] == mission_search_ui.value)
        radius = radius_ui.value

        # -----------------------------
        # Distance logic
        # -----------------------------
        dist_e = euclidean_distance(member_object.location, mission_object["location"])
        dist_m = manhattan_distance(member_object.location, mission_object["location"])
        if dist_e <= radius:
            dist_used = dist_e
            distance_type = "Euclidean"
        else:
            dist_used = dist_m
            distance_type = "Manhattan"
        max_dist = 15
        penalty_pct = min(1.0, dist_used / max_dist)

        # -----------------------------
        # Build normalized stat vector (original stats only)
        # -----------------------------
        stats_vector = np.array([
            member_object.strength / 10,
            member_object.vigour / 10,
            member_object.mobility / 10,
            member_object.charisma / 10,
            member_object.intellect / 10,
            penalty_pct
        ], dtype=float)

        # -----------------------------
        # MLP prediction
        # -----------------------------
        success_rate = mlp_state.forward(stats_vector)
        success_pct = int(success_rate * 100)

        # -----------------------------
        # Online training target (stretched 0–1)
        # -----------------------------
        target_success = (0.3*stats_vector[0] + 0.25*stats_vector[1] + 0.2*stats_vector[2] +
                          0.1*stats_vector[3] + 0.15*stats_vector[4])
        target_success *= (1 - stats_vector[5])
        target_success = np.clip(target_success * 1.5, 0, 1)  # stretch to improve learning
        mlp_state.train(stats_vector, target_success)

        # -----------------------------
        # Critical success & stat degradation
        # -----------------------------
        critical = random.random() < 0.10
        stat_changes = {}
        for stat in ["strength", "vigour", "mobility", "charisma", "intellect"]:
            original = getattr(member_object, stat)
            change = 0

            if critical:
                change = 1  # Critical mission boosts stats
            else:
                # Softened degradation
                gap = max(0, 70 - success_pct)  # Only penalize below 70%
                max_loss_per_stat = 2
                degradation_chance = gap / 50
                for _ in range(max_loss_per_stat):
                    if random.random() < degradation_chance:
                        change -= 1

            new_value = max(0, original + change)
            setattr(member_object, stat, new_value)
            stat_changes[stat] = (original, new_value, change)

        # -----------------------------
        # Record mission snapshot
        # -----------------------------
        mission_history.append({
            "run": run_mlp,
            "member": member_object.name,
            "mission": mission_object["id"],
            "location": mission_object["location"],
            "radius": radius,
            "distance_type": distance_type,
            "penalty_pct": penalty_pct,
            "success_pct": success_pct,
            "critical": critical,
            "stat_changes": stat_changes,
        })

        mission_results[run_mlp] = {
            "member": member_object.name,
            "mission": mission_object["id"],
            "success_pct": success_pct,
            "critical": critical,
            "distance_type": distance_type,
            "penalty_pct": penalty_pct,
            "stat_changes": stat_changes,
        }

        # -----------------------------
        # Build Markdown
        # -----------------------------
        status_emoji = "🟢" if success_pct >= 70 else "🟡" if success_pct >= 40 else "🔴"
        critical_emoji = "🔥" if critical else "—"

        mp_lines = [
            "## 🧠 MLP Mission Evaluation",
            "",
            "---",
            "",
            "### 📌 Mission Overview",
            f"- **👤 Member:** `{member_object.name}`",
            f"- **📍 Mission:** `{mission_object['id']}`",
            f"- **📐 Distance Model:** `{distance_type}`",
            f"- **🎯 Radius:** `{radius}`",
            f"- **🧮 Distance Penalty:** `{penalty_pct:.0%}`",
            "",
            "---",
            "",
            "### 📊 Outcome Prediction",
            f"- **Success Probability:** {status_emoji} **`{success_pct}%`**",
            f"- **Critical Success:** {critical_emoji} `{critical}`",
            "",
            "---",
            "",
            "### 📉 Stat Impact Report",
            "| Stat | Original | Δ Change | New |",
            "|------|----------|----------|-----|",
        ]

        for stat, (orig, new, change) in sorted(stat_changes.items(), key=lambda x: x[1][2]):
            delta = f"+{change}" if change > 0 else f"{change}"
            mp_lines.append(f"| **{stat.capitalize()}** | {orig} | `{delta}` | **{new}** |")

        mp_lines.extend([
            "",
            "---",
            f"🕒 *Mission evaluated at radius `{radius}` using {distance_type} distance modelling.*"
        ])

        mlp_output = mo.vstack([
            mo.hstack([run_mission_btn]),
            mo.md("\n".join(mp_lines)),
        ])

    mlp_output
    return (stats_vector,)


@app.cell
def _(go, mlp_state, mo, np, stats_vector):
    """
    Visualize MLP network with meaningful hover labels for inputs, hidden, and output nodes.
    Hover labels include stat names, penalty, and output node as Success Chance.
    """
    import micropip                  # Used from Pyodide which is used in browser toinstall pure Python packages dynamically using micropip,
    await micropip.install("plotly") # This case being plotly
    import plotly.graph_objects as go

    # Forward pass to get activations
    def get_activations(mlp, poi):
        acts = [poi]
        a = poi
        for indi in range(len(mlp.weights)-1):
            z = a @ mlp.weights[indi] + mlp.biases[indi]
            a = mlp.relu(z)
            acts.append(a)
        z_out = a @ mlp.weights[-1] + mlp.biases[-1]
        a_out = mlp.sigmoid(z_out)
        acts.append(a_out)
        return acts

    activations = get_activations(mlp_state, stats_vector)

    # Node positions
    layer_sizes = [len(stats_vector)] + [w.shape[1] for w in mlp_state.weights]
    positions = []
    for l_idx, size in enumerate(layer_sizes):
        poi = np.ones(size) * l_idx
        few = np.linspace(-size/2, size/2, size)
        positions.append(np.stack([poi, few], axis=1))

    # Build edges
    edge_x, edge_y = [], []
    for l in range(len(mlp_state.weights)):
        for indi in range(mlp_state.weights[l].shape[0]):
            for acca in range(mlp_state.weights[l].shape[1]):
                x0, y0 = positions[l][indi]
                x1, y1 = positions[l+1][acca]
                edge_x += [x0, x1, None]
                edge_y += [y0, y1, None]

    # Build node positions, colors, and hover labels
    node_x, node_y, node_color, hover_text = [], [], [], []
    input_names = ["Strength", "Vigor", "Mobility", "Intellect", "Perception", "Penalty"]
    for l_idx, layer_act in enumerate(activations):
        for n_idx, val in enumerate(layer_act):
            poi, few = positions[l_idx][n_idx]
            node_x.append(poi)
            node_y.append(few)
            node_color.append(val)

            # Assign names based on layer
            if l_idx == 0:
                # Input layer
                name = input_names[n_idx] if n_idx < len(input_names) else f"Input-{n_idx}"
            elif l_idx == len(activations)-1:
                # Output layer
                name = "Success Chance"
            else:
                # Hidden layers
                name = f"H{l_idx}-{n_idx}"
            hover_text.append(f"{name}: {val:.2f}")

    # Create figure
    fig = go.Figure()

    # Draw edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(color='gray', width=1),
        hoverinfo='none'
    ))

    # Draw nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        marker=dict(
            size=20,
            color=node_color,
            colorscale='Viridis',
            cmin=0,
            cmax=1
        ),
        text=hover_text,
        hoverinfo='text'
    ))

    fig.update_layout(
        showlegend=False,
        title="🧠 MLP Network Activation",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    )

    mo.ui.plotly(fig)
    return


@app.cell
def _(mo):
    mlp_text = """
    **Perceptron / MLP — Mission Success Prediction**

    The perceptron-based neural network (implemented as a multi-layer perceptron) is used to predict the probability of mission success based on multiple interacting factors. These include member statistics and distance-based penalties, which do not combine linearly in a simple or predictable way. A neural network is well suited to this task because it can learn complex, non-linear relationships from data rather than relying on fixed rules. Through training and continuous updates, the model adapts as missions are executed, improving future predictions. This makes the perceptron approach effective for simulating real-world decision-making under uncertainty, where outcomes depend on many interconnected variables.
    """

    # Display it in the blue Markdown box
    mo.md(mlp_text).callout(kind="info")
    return


@app.cell
def _(mo):
    mlp_crit = """
    **Perceptron / MLP — Critical Aspects and Bias Analysis**

    The perceptron-based neural network presents the highest risk of hidden bias due to its learned, non-linear decision-making process. Bias can be introduced through training data assumptions, such as how success probability is defined or which stats are weighted more heavily. If these assumptions reflect subjective or unbalanced priorities, the model may consistently favour certain member profiles while undervaluing others.

    Members with unconventional stat distributions or those affected by repeated penalties may be disproportionately predicted as low-success candidates, reinforcing a feedback loop where they are assigned fewer missions and thus gain less opportunity to improve. To mitigate this, the model uses normalised inputs, soft penalties, and continuous online retraining, allowing it to adapt rather than remain fixed.

    Transparency is addressed through activation visualisation, enabling inspection of how inputs influence outputs. Further mitigation could include retraining with diverse synthetic scenarios, regular bias audits, or ensemble models to reduce overconfidence. While neural networks are powerful, their use in this system is deliberately constrained and monitored to ensure predictive support enhances—rather than replaces—human judgement.
    """

    # Display it in the blue Markdown box
    mo.md(mlp_crit).callout(kind="info")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Time Complexity Analysis

    **Goal:** Demonstrate how different computational algorithms process S.T.A.R.S members, showing how execution time scales with dataset size or computational workload.


    ## Algorithm Complexity Summary

    | Algorithm | Best Case | Average Case | Worst Case | Space Complexity | Notes |
    |-----------|-----------|--------------|------------|-----------------|----------------|
    | **QuickSort** | O(n log n) | O(n log n) | O(n²) | O(log n) | Efficient general-purpose sort; average-case is fast; worst-case occurs with poor pivot selection. |
    | **Search (Linear)** | O(1) | O(n) | O(n) | O(1) | Simple search; scales linearly with dataset; ideal for unsorted data. |
    | **Genetic Algorithm (GA)** | O(G × P × D) | O(G × P × D) | O(G × P × D) | O(P) | Heuristic optimization; runtime scales with generations, population, and chromosome length. |
    | **MLP Inference** | O(n) | O(n) | O(n) | O(weights) | Linear in number of forward passes; network size determines per-pass cost. |
    | **MLP Training** | O(n) | O(n) | O(n) | O(weights) | Linear in number of training iterations; backpropagation dominates runtime. |
    """)
    return


@app.cell
def _(mo, plt, random, time):

    # Time complexity experiment
    input_sizes = [10, 20, 40, 80, 160]
    times = []

    class DummyMember:
        def __init__(self, val):
            self.strength = val

    for w in input_sizes:
        test_data = [DummyMember(random.randint(1, 100)) for _ in range(w)]

        start = time.time()
        quicksort_members(test_data, "strength")
        times.append(time.time() - start)


    # Plot time growth
    plt.figure()
    plt.plot(input_sizes, times, marker="o")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Quicksort Time Growth vs Input Size")
    plt.grid(True)

    mo.vstack([
        mo.md("""
    ### ⏱️ Quicksort Time Complexity Analysis

    This plot shows how execution time grows as the number of members increases.
    The curve demonstrates super-linear growth consistent with an **O(n log n)**
    average-case time complexity.
    """),
        mo.mpl.interactive(plt.gcf())
    ])
    return


@app.cell
def _(StarsMember, mo, plt, random, time):


    # Time complexity experiment 
    search_input_sizes = [50, 100, 200, 400, 800, 1600]
    search_times = []

    # Fixed mission location for consistency
    mission_location = (5, 5)
    search_radius = 3

    for cc in search_input_sizes:
        # Generate synthetic members
        members = [
            StarsMember(
                i,
                f"M{i}",
                random.randint(1, 10),
                random.randint(1, 10),
                random.randint(1, 10),
                random.randint(1, 10),
                random.randint(1, 10),
                (random.randint(0, 10), random.randint(0, 10))
            )
            for i in range(cc)
        ]

        # Measure searching all members
        start_search = time.time()
        for count in members:
            search_member_with_penalty(
                count,
                mission_location,
                search_radius
            )
        search_times.append(time.time() - start_search)


    # Plot time growth
    plt.figure()
    plt.plot(search_input_sizes, search_times, marker="o")
    plt.xlabel("Number of Members (n)")
    plt.ylabel("Time (seconds)")
    plt.title("Search Time Growth vs Input Size")
    plt.grid(True)

    mo.vstack([
        mo.md("""
    ### 🔍 Search Algorithm Time Complexity

    This plot illustrates how search time increases as the number of members grows.
    Each search computes distance and applies a penalty in constant time, resulting
    in overall **O(n)** complexity when applied across all members.
    """),
        mo.mpl.interactive(plt.gcf())
    ])
    return


@app.cell
def _(members_list, mo, plt, random, time):


    # GA Time Complexity Experiment
    population_sizes = [10, 20, 40, 80, 160]
    ga_times = []

    test_member = members_list[0]

    for pop_size in population_sizes:
        ga_start = time.time()
        run_training_ga(
            member=test_member,
            population_size=pop_size,
            max_days=60,        # chromosome length (D)
            generations=50,     # fixed generations (G)
            mutation_rate=0.1,
            random_module=random
        )
        ga_times.append(time.time() - ga_start)


    # Plot runtime growth
    plt.figure()
    plt.plot(population_sizes, ga_times, marker="o")
    plt.xlabel("Population Size (P)")
    plt.ylabel("Time (seconds)")
    plt.title("Genetic Algorithm Runtime vs Population Size")
    plt.grid(True)

    mo.vstack([
        mo.md("""
    ### 🧬 Genetic Algorithm Time Complexity Analysis

    This plot shows how runtime increases as population size grows while the number
    of generations and chromosome length remain fixed. The near-linear trend
    supports the expected **O(G × P × D)** time complexity of the genetic algorithm.
    """),
        mo.mpl.interactive(plt.gcf())
    ])
    return


@app.cell
def _(mlp_state, mo, np, plt, time):

    # MLP Inference Time Complexity
    forward_passes = [100, 500, 1000, 2000, 5000]
    mlp_times = []

    for cqc in forward_passes:
        mlp_start = time.time()
        for _ in range(cqc):
            mlp_state.forward(np.random.rand(6))
        mlp_times.append(time.time() - mlp_start)


    # Plot inference scaling
    plt.figure()
    plt.plot(forward_passes, mlp_times, marker="o")
    plt.xlabel("Number of Forward Passes")
    plt.ylabel("Time (seconds)")
    plt.title("MLP Inference Time Complexity")
    plt.grid(True)

    mo.vstack([
        mo.md("""
    ### 🧠 MLP Inference Time Complexity

    This plot shows how inference time grows with the number of forward passes
    through the neural network. Since network size is fixed, runtime increases
    linearly, confirming **O(n)** inference complexity.
    """),
        mo.mpl.interactive(plt.gcf())
    ])
    return


@app.cell
def _(mlp_state, mo, np, plt, time):

    # MLP Training Time Complexity
    training_steps = [50, 100, 200, 400, 800]
    train_times = []

    for steps in training_steps:
        train_start = time.time()
        for _ in range(steps):
            tr_x = np.random.rand(6)
            tr_y = np.random.rand()
            mlp_state.train(tr_x, tr_y)
        train_times.append(time.time() - train_start)


    # Plot training scaling
    plt.figure()
    plt.plot(training_steps, train_times, marker="o")
    plt.xlabel("Number of Training Steps")
    plt.ylabel("Time (seconds)")
    plt.title("MLP Training Time Complexity")
    plt.grid(True)

    mo.vstack([
        mo.md("""
    ### 🧠 MLP Training Time Complexity

    This plot demonstrates how training time increases with the number of
    backpropagation steps. With a fixed network architecture, training exhibits
    linear time complexity **O(n)** with respect to training iterations.
    """),
        mo.mpl.interactive(plt.gcf())
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## AI Use & Acknowledgement

    This project was developed with the assistance of an AI-based large language model (ChatGPT5, by OpenAI) as a support tool throughout the design and implementation process. The AI was used to assist with code structuring, debugging, refactoring, and the explanation of algorithmic concepts.

    All core ideas, system design decisions, parameter choices, and final implementations were reviewed, adapted, and integrated by myself. The AI functioned as an interactive programming assistant and writing aid.

    I maintained full control over how algorithms such as Quicksort, linear search, Genetic Algorithms, and perceptron-based neural networks were applied within the S.T.A.R.S Mission Allocation System.

    For the **Quicksort** component, AI assistance was used so sorting had selected attributes handled correctly. I integrated my own logic into the interactive visualisation and ensured it aligned with the system’s tactical ranking goals.

    In the **Search and distance evaluation** component, AI support helped refine the logic for applying distance-based penalties and clarifying the use of Manhattan versus Euclidean distance models. I validated these decisions and adjusted penalty behaviour to avoid hard exclusions.

    For the **Genetic Algorithm**, AI assistance supported the design of the fitness function, convergence tracking, and mutation strategy. I refined the algorithm to focus exclusively on improving the weakest stat and ensured that the final output was interpretable and safely applied to member attributes.

    In the **Perceptron-based neural network**, AI support helped with structuring the forward pass, training logic, and input normalisation. I retained full control over the model design, training assumptions, and evaluation criteria, and critically monitored its predictions for bias and stability.


    Where AI-generated suggestions were used, they were critically evaluated, modified where necessary as they didnt achieve what I wanted to do when used, instead needing to be used for small specific sections in a cell at a time. This approach ensured that the final work represents my understanding and intent, while responsibly leveraging AI as a productivity and learning enhancement tool in accordance with Ual's AI usage guidelines.
    """)
    return


if __name__ == "__main__":
    app.run()
