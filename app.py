from flask import Flask, render_template, request, jsonify
import random
import numpy as np

app = Flask(__name__)

class GeneticAlgorithm:
    def __init__(self, population_size=100, genes_length=10):
        self.population_size = population_size
        self.genes_length = genes_length
        self.population = self.create_initial_population()
        self.best_individual = None
        self.best_fitness = float('-inf')
        self.generation = 0

    def create_initial_population(self):
        return [[random.randint(0, 1) for _ in range(self.genes_length)] 
                for _ in range(self.population_size)]

    def fitness(self, individual):
        # Exemple simple : compter le nombre de 1
        return sum(individual)

    def select_parents(self):
        # Sélection par tournoi
        fitness_scores = [self.fitness(ind) for ind in self.population]
        tournament_size = 3
        parents = []
        
        for _ in range(2):
            tournament = random.sample(list(enumerate(fitness_scores)), tournament_size)
            winner_idx = max(tournament, key=lambda x: x[1])[0]
            parents.append(self.population[winner_idx])
        
        return parents

    def crossover(self, parent1, parent2):
        # Croisement en un point
        crossover_point = random.randint(1, len(parent1)-1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2

    def mutate(self, individual, mutation_rate=0.01):
        # Mutation par inversion de bit
        return [bit if random.random() > mutation_rate else 1 - bit 
                for bit in individual]

    def evolve(self):
        new_population = []
        
        # Élitisme : garder le meilleur individu
        if self.best_individual:
            new_population.append(self.best_individual)
        
        # Créer nouvelle génération
        while len(new_population) < self.population_size:
            parents = self.select_parents()
            child1, child2 = self.crossover(parents[0], parents[1])
            child1 = self.mutate(child1)
            child2 = self.mutate(child2)
            new_population.extend([child1, child2])
        
        self.population = new_population[:self.population_size]
        self.generation += 1
        
        # Mettre à jour le meilleur individu
        for individual in self.population:
            fitness = self.fitness(individual)
            if fitness > self.best_fitness:
                self.best_fitness = fitness
                self.best_individual = individual

    def get_stats(self):
        fitness_scores = [self.fitness(ind) for ind in self.population]
        return {
            'generation': self.generation,
            'best_fitness': self.best_fitness,
            'avg_fitness': np.mean(fitness_scores),
            'best_individual': ''.join(map(str, self.best_individual)) if self.best_individual else None
        }

# Instance globale de l'algorithme génétique
ga = GeneticAlgorithm()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/evolve', methods=['POST'])
def evolve():
    generations = int(request.json.get('generations', 1))
    for _ in range(generations):
        ga.evolve()
    return jsonify(ga.get_stats())

@app.route('/reset', methods=['POST'])
def reset():
    global ga
    population_size = int(request.json.get('population_size', 100))
    genes_length = int(request.json.get('genes_length', 10))
    ga = GeneticAlgorithm(population_size, genes_length)
    return jsonify(ga.get_stats())

if __name__ == '__main__':
    app.run(debug=True)