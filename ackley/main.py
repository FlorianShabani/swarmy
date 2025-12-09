import numpy as np
import matplotlib.pyplot as plt

# Ackley function
def ackley(x, y, z):
    term1 = -20 * np.exp(-0.2 * np.sqrt((x**2 + y**2 + z**2) / 3))
    term2 = -np.exp((np.cos(2*np.pi*x) + np.cos(2*np.pi*y) + np.cos(2*np.pi*z)) / 3)
    return term1 + term2 + 20 + np.e

# Fitness function (maximization)
def fitness(individual):
    x, y, z = individual
    return 1 / (ackley(x, y, z) + 1)

# Initialize population
def initialize_population(pop_size, bounds):
    return np.random.uniform(bounds[0], bounds[1], (pop_size, 3))

# Tournament selection
def tournament_selection(population, fitnesses, tournament_size=3):
    idx = np.random.choice(len(population), tournament_size, replace=False)
    winner = idx[np.argmax(fitnesses[idx])]
    return population[winner].copy()

# Uniform crossover
def crossover(parent1, parent2):
    mask = np.random.rand(3) < 0.5
    child = np.where(mask, parent1, parent2)
    return child

# Gaussian mutation
def mutate(individual, mutation_rate, bounds, sigma=5.0):
    mask = np.random.rand(3) < mutation_rate
    individual[mask] += np.random.normal(0, sigma, np.sum(mask))
    individual = np.clip(individual, bounds[0], bounds[1])
    return individual

# Evolutionary algorithm
def evolutionary_algorithm(pop_size=100, generations=2000, mutation_rate=0.03, elitism=2, bounds=(-32.768, 32.768)):
    population = initialize_population(pop_size, bounds)
    best_fitness_history = []
    avg_fitness_history = []
    params = {'pop_size': pop_size, 'generations': generations, 'mutation_rate': mutation_rate, 'elitism': elitism}
    
    for gen in range(generations):
        fitnesses = np.array([fitness(ind) for ind in population])
        
        best_fitness_history.append(np.max(fitnesses))
        avg_fitness_history.append(np.mean(fitnesses))
        
        # Sort by fitness
        sorted_idx = np.argsort(fitnesses)[::-1]
        population = population[sorted_idx]
        fitnesses = fitnesses[sorted_idx]
        
        # Elitism
        new_population = [population[i].copy() for i in range(elitism)]
        
        # Adaptive sigma: decrease over three phases
        if gen < generations // 3:
            sigma = 5.0
        elif gen < 2 * generations // 3:
            sigma = 2.0
        else:
            sigma = 0.2
        
        # Generate offspring
        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate, bounds, sigma)
            new_population.append(child)
        
        population = np.array(new_population)
        
        if (gen + 1) % 20 == 0:
            best_ind = population[0]
            print(f"Gen {gen+1}: Best fitness = {fitnesses[0]:.6f}, "
                  f"Ackley value = {ackley(*best_ind):.6f}, Position = {best_ind}")
    
    return population[0], best_fitness_history, avg_fitness_history, params

# Run and plot
if __name__ == "__main__":
    best_solution, best_hist, avg_hist, params = evolutionary_algorithm()
    
    print(f"\nFinal solution: {best_solution}")
    print(f"Ackley value: {ackley(*best_solution):.8f}")
    print(f"Fitness: {fitness(best_solution):.8f}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(best_hist, label='Best Fitness', linewidth=2)
    plt.plot(avg_hist, label='Average Fitness', linewidth=2)
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    param_text = f"Pop={params['pop_size']}, Gen={params['generations']}, Mut={params['mutation_rate']}, Elite={params['elitism']}"
    plt.title(f'Evolutionary Algorithm on Ackley Problem (3D)\n{param_text}', fontsize=10)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    filename = f"ackley_p{params['pop_size']}_g{params['generations']}_m{params['mutation_rate']}.png"
    plt.savefig(filename, dpi=300)
    plt.show()
