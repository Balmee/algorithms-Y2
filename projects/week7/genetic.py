import marimo

__generated_with = "0.16.5"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""## Genetic Algorithm with colours""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout("This code is an original creation of the author. GPT-5 was used to add explanatory comments to it.")

    return


@app.cell
def _():
    import numpy as np, matplotlib.pyplot as plt
    return np, plt


@app.cell
def _():
    import random

    # Creates the initial population of individuals
    # Each individual is a list [R, G, B] of 3 integers (0–255)
    def createInitial(nInd):
        population = []
        for i in range(nInd):
            b1 = random.randint(0, 255)
            b2 = random.randint(0, 255)
            b3 = random.randint(0, 255)
            population.append([b1, b2, b3])
        return population
    return createInitial, random


@app.function
def fitness(individual):
    """
    Fitness function that measures how close an RGB colour is to one of the
    primary colours (red, green, or blue). Lower distance = higher fitness.

    Returns the *negative* of the smallest colour difference so that higher
    fitness values are better (since genetic algorithms often maximize fitness).
    """
    diffR = abs(individual[0] - 255) + abs(individual[1]) + abs(individual[2])
    diffG = abs(individual[1] - 255) + abs(individual[0]) + abs(individual[2])
    diffB = abs(individual[2] - 255) + abs(individual[1]) + abs(individual[0])
    return -min(diffR, diffB, diffG)


@app.cell
def _(np, random):
    # Selects 3 "winners" from the population using tournament selection
    def selectThreeWinners(population):
        # Each "tournament" compares 2 random individuals
        firstPair = random.sample(population, 2)
        fitnesses = [fitness(indiv) for indiv in firstPair]
        firstWinner = firstPair[np.argmax(fitnesses)]

        secondPair = random.sample(population, 2)
        fitnesses = [fitness(indiv) for indiv in secondPair]
        secondWinner = secondPair[np.argmax(fitnesses)]

        thirdPair = random.sample(population, 2)
        fitnesses = [fitness(indiv) for indiv in thirdPair]
        thirdWinner = thirdPair[np.argmax(fitnesses)]

        return firstWinner, secondWinner, thirdWinner

    # Combines two parent individuals at a random crossover point
    def crossover(parent1, parent2):
        x = random.randint(0, 3)  # crossover point between 0–3
        firstChild = parent1[:x] + parent2[x:]
        secondChild = parent2[:x] + parent1[x:]
        return firstChild, secondChild

    # Applies random small changes to an individual's genes
    def mutation(individual, pMutation):
        for i in range(len(individual)):
            if random.random() < pMutation:
                noise = random.randint(-1, 1)
                individual[i] = individual[i] + noise
        return individual
    return crossover, mutation, selectThreeWinners


@app.cell
def _(createInitial, crossover, mutation, selectThreeWinners):
    def runGAColour():
        # Parameters
        nInd = 100             # Number of individuals per generation
        pMutation = 0.001      # Mutation probability
        numberIterations = 1000

        # Tracking metrics
        xValues, yValues, fitnesses, matrix = [], [], [], []

        # Initialize population
        population = createInitial(nInd)

        # Run genetic algorithm for a number of iterations
        for k in range(numberIterations):
            winners = selectThreeWinners(population)  # Tournament selection

            next_gen = []
            # Create children from all pairs of winners (AB, AC, BC)
            for i in [0, 1]:
                for j in range(i + 1, 3):
                    children = crossover(winners[i], winners[j])
                    next_gen.append(children[0])
                    next_gen.append(children[1])

            # Sort population by fitness (lowest first)
            population.sort(key=fitness)
            population = population[6:]  # Remove 6 least fit individuals

            # Add children to form the new generation
            next_gen = population + next_gen

            # Apply mutation to each individual
            for i in range(len(next_gen)):
                next_gen[i] = mutation(next_gen[i], pMutation)

            # Update population
            population = next_gen

            # Track average R, G, and best fitness per generation
            xValues.append(sum([population[i][0] for i in range(len(population))]) / len(population))
            yValues.append(sum([population[i][1] for i in range(len(population))]) / len(population))
            fitnesses.append(max([fitness(ind) for ind in next_gen]))
            matrix.append(population)

        # Return all fitness scores and evolution matrix
        return (fitnesses, matrix)
    return (runGAColour,)


@app.cell
def _(runGAColour):
    f, m = runGAColour()
    return (m,)


@app.cell
def _(m, np):
    img = np.array(m, dtype=int)
    return


@app.cell
def _(m, np, plt):
    plt.gcf().set_dpi(300)
    n = np.transpose(m)
    img_1 = np.array(m[:100], dtype=int)  # Show first 100 generations
    plt.imshow(img_1, aspect='auto')       # Each row ~ one generation
    plt.show()
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
