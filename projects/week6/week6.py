import marimo

__generated_with = "0.19.4"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Example 1: Maxone
    """)
    return


@app.cell
async def _():
    import random, numpy as np, matplotlib.pyplot as plt
    import micropip                  # Used from Pyodide which is used in browser toinstall pure Python packages dynamically using micropip,
    await micropip.install("plotly") # This case being plotly
    import plotly.graph_objects as go
    return go, np, plt, random


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 1: Initialisation
    Implement the ```createInital(nInd,nBits)``` function that creates ```nInd``` arrays of ```nBits``` bits each one, where each bit is 1 or 0 with 50% chance.
    """)
    return


@app.cell
def _(random):
    def createInitial(nInd,nBits):
        population = [[random.choice([0,1]) for _ in range(nBits)] for _ in range(nInd)]
        return population
    return (createInitial,)


@app.cell
def _(createInitial):
    createInitial(6,5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 2: Evaluation
    Implement the ```fitness(individual)``` function that receives an array ```individual``` and it returns ```nOnes```, the number of ones that the array contains (you can assume the array only contains zeros or ones).
    """)
    return


@app.cell
def _(np):
    def fitness(individual):
        nOnes = np.sum(individual)

        return nOnes
    return (fitness,)


@app.cell
def _(fitness):
    print(fitness([0,1,1,1,0,0]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 3: Selection
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Implement the ```selectThreeWinners(population)``` function, that takes as an input the whole population. This function should do the following:
    1. Select randomly two individuals from ```population```, then compare their fitness and select the one with highest fitness. This individual is called ```firstWinner```
    2. Repeat the above step twice, in order to obtain ```secondWinner``` and ```thirdWinner```
    3. Return ```firstWinner```,```secondWinner```, and ```thirdWinner```

    You can use the ```random.sample(population,k)``` for randomly extract ```k``` elements from ```population```
    """)
    return


@app.cell
def _(fitness, random):
    def selectThreeWinners(population):
        winners=[]
        for i in range(3):
            pair = random.sample(population,2)
            fitnessOne = fitness(pair[0])
            fitnessTwo = fitness(pair[1])

            if (fitnessOne >= fitnessTwo):
                winners.append(pair[0])
            else:
                winners.append(pair[1])


        return winners[0],winners[1],winners[2]
    return (selectThreeWinners,)


@app.cell
def _(createInitial, selectThreeWinners):
    pop = createInitial(6,5)
    win = selectThreeWinners(pop)
    print(win)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 4: Crossover
    Implement the ```crossover(parent1,parent2)``` function, that takes as an input two individuals ```parent1``` and ```parent2``` and returns ```firstChild``` and ```secondChild``` which are obtained with the following procedure:
    1. Create a random crossover point x, with ```x=[1,len(parent1)-1]```
    2. Create ```firstChild```, an array containing the same elements from ```parent1``` from index 0 to x-1, and containing the same elements from ```parent2``` from index x to len(parent)-1.
    3. Create ```secondChild``` as the inverse combination from ```firstChild```
    """)
    return


@app.cell
def _(random):
    def crossover(parent1,parent2):
        x = random.randint(1,len(parent1)-1)
        firstChild = parent1[:x] + parent2[x:]
        secondChild = parent2[:x] + parent1[x:]
        return firstChild,secondChild
    return (crossover,)


@app.cell
def _(crossover):
    crossover([1,1,1,1,1,1],[0,0,0,0,0,0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 5: Mutation
    Implement the ```mutation(individual,pMut)``` function, that takes as an input an array ```individual``` and ```pMut```, the probability of mutation, and for each element of ```individual``` it changes its value (from 0 to 1 or from 1 to 0) with probability ```pMut```
    """)
    return


@app.cell
def _(random):
    def mutation(individual,pMutation):
        for i in range(len(individual)):
            r = random.random()
            if (r < pMutation):
                individual[i] = 1 - individual[i]

        return individual
    return (mutation,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ------
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Putting all together
    Now we implement our ```runGA()``` function, that will call every other function we created.
    """)
    return


@app.cell
def _(createInitial, crossover, fitness, mutation, selectThreeWinners):

    def runGA(totalIndividuals,numberBits,numberIterations,pMutation):
        fitnesses = []
        population = createInitial(totalIndividuals, numberBits)  #Store best fitness for each generation
        for k in range(0, numberIterations):
            print(k)
            winners = selectThreeWinners(population)
            next_gen = []  #Create initial random individuals
            for i in [0, 1]:
                for j in range(i + 1, 3):
                    children = crossover(winners[i], winners[j])
                    next_gen.append(children[0])
                    next_gen.append(children[1])

            # 
            next_gen = population + next_gen 
            next_gen.sort(key=fitness)  
            next_gen = next_gen[-6:]

            population.sort(key=fitness)
            population = population[6:]  #Crossover: we have winners A,B and C. 

            next_gen = population + next_gen  # We crossover the pairs AB, AC and BC. Each 

            for i in range(0, len(next_gen)):
                next_gen[i] = mutation(next_gen[i], pMutation)
            population = next_gen
            print(len(population))

            fitnesses.append(max([fitness(ind) for ind in next_gen]))
        return fitnesses  #Delete 6 less fit individuals  #Add 6 individuals from new generation  #Mutation
    return (runGA,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And we call the function with specific values for the parameters
    """)
    return


@app.cell
def _(plt, runGA):
    _fit = runGA(100,50,100,0.01)
    plt.plot(range(100), _fit)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ------
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Task 6:
    Explore modifying the selection and crossover processes to achieve a better fitness. You can also modify how the ```next_gen``` is being defined in ```runGA()```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---------
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Example 2: Maximising a real-valued function
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We want to find the values $x^{*}$ and $y^{*}$ such that $f(x,y)=-(x+y)^2$ has a maximum.

    We can start with random arrays of two elements $[x_0,y_0]$ where $x_0,y_0\in[-1,1]$ and use genetic algorithm to see if we find the optimal solution.

    Let's visualise $f(x,y)$:
    """)
    return


@app.cell(hide_code=True)
def _(np, plt):
    plt.rcParams['figure.dpi'] = 300

    from matplotlib import cm
    from matplotlib.ticker import LinearLocator
    _fig, _ax = plt.subplots(subplot_kw={'projection': '3d'})
    _X = np.arange(-5, 5, 0.25)
    _Y = np.arange(-5, 5, 0.25)
    # Make data.
    _X, _Y = np.meshgrid(_X, _Y)
    _Z = -(_X ** 2 + _Y ** 2)
    _surf = _ax.plot_surface(_X, _Y, _Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    _ax.set(xlabel='X', ylabel='Y', zlabel='Z')
    # Plot the surface.
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ------------
    Now let's create some initial points and plot them together
    """)
    return


@app.cell(hide_code=True)
def _(go, mo, np, random):
    ## This code was created with the help of GPT-5 for the rendering of the points + surface

    # Generate population
    population = []
    for i in range(100):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        population.append([x, y])

    # Compute z = -x^2 - y^2
    x_vals = [p[0] for p in population]
    y_vals = [p[1] for p in population]
    z_vals = [-x**2 - y**2 for x, y in population]

    # Scatter points
    scatter = go.Scatter3d(
        x=x_vals,
        y=y_vals,
        z=z_vals,
        mode='markers',
        marker=dict(size=5, color=z_vals, colorscale='Viridis', opacity=0.8),
        name='Points'
    )

    # Surface
    X = np.linspace(-1, 1, 50)
    Y = np.linspace(-1, 1, 50)
    X, Y = np.meshgrid(X, Y)
    Z = -X**2 - Y**2

    surface = go.Surface(
        x=X, y=Y, z=Z,
        colorscale='Viridis', opacity=0.5, showscale=False
    )

    fig = go.Figure(data=[surface, scatter])
    fig.update_layout(
        title="Interactive 3D Plot of f(x,y) = -x² - y²",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Z = -x² - y²",
        ),
        width=700,
        height=600,
    )

    mo.ui.plotly(fig)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Final Task:
    Implement the following functions to run a genetic algorithm for the probklem stated above.
    your algorithm should do the following:
    - Create an initial population of 100 points scattered randomnly in the range $x=[-1,1]$ and $y=[-1,1]$
    - Calculate the fitness of each point is given by evaluating the point in the function $f(x,y)$.
    - Selection process is similar as Example 1 (i.e. selecting three winners)
    - You can implement whatever crossover you consider adequate.
    - For each step, each individual suffers a mutation on each of its coordinates $x$ and $y$ which are modified by a random noise $\delta$, where $\delta=[-0.05,0.05]$ (uniformly distributed).
    - Implement the ```runGA_1()``` function so it runs 100 iterations of the algorithm. Check if the points converge to a solution.

    ## Extra task (not compulsory):
    - Plot the points for each iteration of the algorithm together with the surface. Visualise how the points move through the surface
    - Visualise how the points move through the surface by plotting the path or trail that they leave when they move from one iteration to the next one.
    """)
    return


@app.cell
def _(random):
    def createInitial_1(nInd=100):
        population = [[random.uniform(-1, 1), random.uniform(-1, 1)] for _ in range(nInd)]
        return population
    return (createInitial_1,)


@app.function
def fitness_1(individual):
    x, y = individual
    fitness =  - (x + y) ** 2
    return fitness


@app.cell
def _(random):
    def selectThreeWinners_1(population):
        winners = []
        for _ in range(3):
            a, b = random.sample(population, 2)
            winners.append(a if fitness_1(a) > fitness_1(b) else b)
        return winners[0], winners[1], winners[2]
    return (selectThreeWinners_1,)


@app.cell
def _(random):
    def crossover_1(parent1, parent2):
        alpha = random.random()
        firstChild = [alpha * parent1[0] + (1 - alpha) * parent2[0],
                  alpha * parent1[1] + (1 - alpha) * parent2[1]]
        secondChild = [(1 - alpha) * parent1[0] + alpha * parent2[0],
                  (1 - alpha) * parent1[1] + alpha * parent2[1]]
        return firstChild, secondChild
    return (crossover_1,)


@app.cell
def _(random):
    def mutation_1(individual, pMutation=1.0):
        if random.random() < pMutation:
            delta_x = random.uniform(-0.05, 0.05)
            delta_y = random.uniform(-0.05, 0.05)
            individual[0] += delta_x
            individual[1] += delta_y
            individual[0] = max(-1, min(1, individual[0]))
            individual[1] = max(-1, min(1, individual[1]))
        return individual
    return (mutation_1,)


@app.cell
def _(
    createInitial_1,
    crossover_1,
    mutation_1,
    plot_evolution,
    selectThreeWinners_1,
):
    def runGA_1(nInd=100, nIter=100, pMutation=1.0, visualise=False):
        population = createInitial_1(nInd)
        best_fit = []
        generations = [population.copy()]

        for _ in range(nIter):
            winners = selectThreeWinners_1(population)
            next_gen = []
            for i in [0, 1]:
                for j in range(i + 1, 3):
                    c1, c2 = crossover_1(winners[i], winners[j])
                    next_gen.append(mutation_1(c1, pMutation))
                    next_gen.append(mutation_1(c2, pMutation))

            # Combine and keep the best individuals
            population += next_gen
            population.sort(key=fitness_1, reverse=True)
            population = population[:nInd]

            generations.append(population.copy())
            best_fit.append(fitness_1(population[0]))

        best_individual = population[0]
        print(f"Best individual: {best_individual}, Fitness: {best_fit[-1]}")

        if visualise:
            plot_evolution(generations)

        return best_fit, generations
    return (runGA_1,)


@app.cell
def _(go, runGA_1):
    best_fit, _ = runGA_1(nInd=100, nIter=50, pMutation=1.0, visualise=False)

    figGA = go.Figure()
    figGA.add_trace(go.Scatter(
        y=best_fit,
        mode="lines+markers",
        name="Best Fitness"
    ))

    figGA.update_layout(
        title="Convergence of Genetic Algorithm",
        xaxis_title="Iteration",
        yaxis_title="Best Fitness",
        width=800,
        height=500
    )

    import marimo as mo
    mo.ui.plotly(figGA)  # works in online view
    return (mo,)


@app.cell
def _(runGA_1):
    fits, gens = runGA_1(nInd=100, nIter=50, pMutation=1.0, visualise=True)


    return


@app.cell
def _(go, np):
    def plot_evolution(generations):
        """
        Visualise population evolution over generations on the surface f(x, y) = -(x + y)^2,
        with trails and color variation between generations.
        """
        # Create surface grid
        X = np.linspace(-1, 1, 60)
        Y = np.linspace(-1, 1, 60)
        X, Y = np.meshgrid(X, Y)
        Z = -(X + Y)**2

        # Create 3D surface
        surface = go.Surface(
            x=X, y=Y, z=Z,
            colorscale="Viridis", opacity=0.5, showscale=False
        )

        # Choose distinct colors for generations
        colors = [
            "red", "orange", "yellow", "green", "cyan",
            "blue", "purple", "magenta", "lime", "gold"
        ]

        # Prepare frames and traces
        frames = []
        all_trails = []

        # Loop through generations
        for i, pop in enumerate(generations):
            x_vals = [p[0] for p in pop]
            y_vals = [p[1] for p in pop]
            z_vals = [-(x + y)**2 for x, y in pop]

            color = colors[i % len(colors)]

            # Scatter for current generation
            scatter = go.Scatter3d(
                x=x_vals, y=y_vals, z=z_vals,
                mode="markers",
                marker=dict(size=5, color=color, opacity=0.9),
                name=f"Gen {i+1}"
            )

            # Draw trails for each individual (if previous generation exists)
            if i > 0:
                prev_pop = generations[i-1]
                for (x0, y0), (x1, y1) in zip(prev_pop, pop):
                    trail = go.Scatter3d(
                        x=[x0, x1],
                        y=[y0, y1],
                        z=[-(x0 + y0)**2, -(x1 + y1)**2],
                        mode="lines",
                        line=dict(color=color, width=2),
                        opacity=0.6,
                        showlegend=False
                    )
                    all_trails.append(trail)

            # Add a frame for animation
            frames.append(go.Frame(data=[scatter], name=f"Frame{i}"))

        # Initial frame data
        initial_data = [surface, frames[0].data[0]] + all_trails

        # Build figure with all traces and frames
        fig = go.Figure(
            data=initial_data,
            frames=frames
        )

        # Layout and controls
        fig.update_layout(
            title="Evolution of Population with Trails — f(x, y) = -(x + y)²",
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z = -(x + y)²"
            ),
            width=900,
            height=700,
            updatemenus=[{
                "buttons": [
                    {"args": [None, {"frame": {"duration": 100, "redraw": True}, "fromcurrent": True}],
                     "label": "▶ Play", "method": "animate"},
                    {"args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                     "label": "⏸ Pause", "method": "animate"}
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 70},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }]
        )

        fig.show()
    return (plot_evolution,)


@app.cell
def _(mo):
    mo.md(r"""
    ---
    ## AI Use & Acknowledgement

    AI tools (ChatGPT, GPT-5 family) were used in a very limited and supportive capacity during the completion of the final task only of this assignment.

    AI assistance was restricted to:
    - High-level guidance on structuring a genetic algorithm loop for a continuous optimisation problem.
    - Clarification of standard implementation patterns for crossover, mutation with bounded noise, and population selection.
    - Minor suggestions related to visualisation mechanics for plotting population movement over a surface.

    All core components of the final task — including the definition of the optimisation problem, fitness function formulation, genetic operators, convergence logic, parameter choices, and interpretation of results were designed, implemented, and validated independently by me, based on course material and my own understanding.
    """)
    return


if __name__ == "__main__":
    app.run()
