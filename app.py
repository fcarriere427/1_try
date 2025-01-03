from flask import Flask, render_template, request, jsonify
import random
import os
import numpy as np

app = Flask(__name__)
app_prefix = os.getenv('APP_PREFIX', '')  # '' est la valeur par défaut si la variable n'existe pas


class GeneticAlgorithm:
    def __init__(self, target="target init", population_size=100, mutation_rate=0.05):
        self.population_size = population_size
        self.target = target
        self.genes_length = len(target)
        self.chars = " abcdefghijklmnopqrstuvwxyz"  # espace + lettres minuscules
        self.mutation_rate = mutation_rate
        self.population = self.create_initial_population()
        self.best_individual = None
        self.best_fitness = float('-inf')  # Sera mis à jour avec un pourcentage
        self.generation = 0
        self.generation_history = []

        # Ajouter la génération initiale à l'historique avec le fitness en pourcentage
        fitness_scores = [self.fitness(ind) for ind in self.population]
        best_index = fitness_scores.index(max(fitness_scores))
        first_fitness = fitness_scores[best_index]
        self.best_fitness = first_fitness
        self.best_individual = self.population[best_index]
        
        self.generation_history.append({
            'id': best_index + 1,
            'genes': ''.join(self.decode_individual(self.population[best_index])),
            'fitness': round(first_fitness, 1)
        })
        
    def create_initial_population(self):
        return [[random.randint(0, len(self.chars)-1) for _ in range(self.genes_length)] 
                for _ in range(self.population_size)]
    
    def decode_individual(self, individual):
        return [self.chars[idx] for idx in individual]

    def fitness(self, individual):
        # Nombre de caractères corrects à la bonne position
        decoded = self.decode_individual(individual)
        matches = sum(1 for a, b in zip(decoded, self.target) if a == b)
        return (matches / len(self.target)) * 100  # Convertit en pourcentage
        
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

    def mutate(self, individual, mutation_rate=0.05):
        # Mutation par changement aléatoire de caractère
        return [gene if random.random() > mutation_rate 
                else random.randint(0, len(self.chars)-1) 
                for gene in individual]

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
        
        # Mettre à jour le meilleur individu global
        current_fitness_scores = [self.fitness(ind) for ind in self.population]
        current_best_index = current_fitness_scores.index(max(current_fitness_scores))
        current_best_fitness = current_fitness_scores[current_best_index]
        
        if current_best_fitness > self.best_fitness:
            self.best_fitness = current_best_fitness
            self.best_individual = self.population[current_best_index]
        
        # Ajouter à l'historique avec le fitness en pourcentage
        self.generation_history.append({
            'id': current_best_index + 1,
            'genes': ''.join(self.decode_individual(self.population[current_best_index])),
            'fitness': round(current_best_fitness, 1)  # Arrondi à 1 décimale
        })

    def get_stats(self):
        fitness_scores = [self.fitness(ind) for ind in self.population]
        best_individual = ''.join(self.decode_individual(self.best_individual)) if self.best_individual else None
        
        return {
            'generation': self.generation,
            'best_fitness': self.best_fitness,
            'avg_fitness': np.mean(fitness_scores),
            'best_individual': best_individual,
            'generation_history': self.generation_history
        }

# Instance globale de l'algorithme génétique
DEFAULT_TARGET = "nouvelle cible"
ga = GeneticAlgorithm(target=DEFAULT_TARGET)

@app.route(f'{app_prefix}/')
def home():
    return render_template('index.html', default_target=DEFAULT_TARGET)

@app.route(f'{app_prefix}/evolve', methods=['POST'])
def evolve():
    generations = int(request.json.get('generations', 1))
    for _ in range(generations):
        ga.evolve()
    return jsonify(ga.get_stats())

@app.route(f'{app_prefix}/reset', methods=['POST'])
def reset():
    global ga
    target = str(request.json.get('target', "target par defaut dans reset"))
    population_size = int(request.json.get('population_size', 100))
    mutation_rate = float(request.json.get('mutation_rate', 0.05))
    ga = GeneticAlgorithm(
        target=target, 
        population_size=population_size, 
        mutation_rate=mutation_rate
    )
    return jsonify(ga.get_stats())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)