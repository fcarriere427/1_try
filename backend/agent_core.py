from dataclasses import dataclass
from typing import List, Dict
import random
from datetime import datetime

@dataclass
class AgentDNA:
    """Représente l'ADN d'un agent avec ses caractéristiques"""
    web_search_ability: float  # Capacité à faire des recherches pertinentes (0-1)
    synthesis_ability: float   # Capacité à faire des synthèses (0-1)
    web_action_ability: float  # Capacité à agir sur le web (0-1)
    creativity: float         # Niveau de créativité (0-1)
    focus: float             # Capacité à rester concentré sur une tâche (0-1)
    
    @classmethod
    def random(cls):
        """Crée un ADN aléatoire"""
        return cls(
            web_search_ability=random.random(),
            synthesis_ability=random.random(),
            web_action_ability=random.random(),
            creativity=random.random(),
            focus=random.random()
        )
    
    def mutate(self, mutation_rate: float = 0.1) -> 'AgentDNA':
        """Applique une mutation à l'ADN"""
        new_dna = AgentDNA(**self.__dict__)
        for field in self.__dataclass_fields__:
            if random.random() < mutation_rate:
                current_value = getattr(new_dna, field)
                mutation = random.gauss(0, 0.1)  # Mutation gaussienne
                new_value = max(0, min(1, current_value + mutation))
                setattr(new_dna, field, new_value)
        return new_dna

class Agent:
    """Représente un agent intelligent"""
    def __init__(self, name: str, dna: AgentDNA):
        self.name = name
        self.dna = dna
        self.fitness = 0.0
        self.actions_history: List[Dict] = []
        
    def execute_task(self, task: str) -> Dict:
        """Exécute une tâche en fonction de son ADN"""
        success_probability = self._calculate_success_probability(task)
        success = random.random() < success_probability
        
        result = {
            'task': task,
            'success': success,
            'timestamp': datetime.now().isoformat(),
            'dna_state': self.dna.__dict__
        }
        
        self.actions_history.append(result)
        return result
    
    def _calculate_success_probability(self, task: str) -> float:
        """Calcule la probabilité de succès d'une tâche selon l'ADN"""
        # Exemple simple - à adapter selon vos besoins
        task_type_weights = {
            'web_search': self.dna.web_search_ability,
            'synthesis': self.dna.synthesis_ability,
            'web_action': self.dna.web_action_ability
        }
        base_probability = task_type_weights.get(task, 0.5)
        return base_probability * (0.5 + 0.5 * self.dna.focus)

class AgentPopulation:
    """Gère une population d'agents avec évolution génétique"""
    def __init__(self, size: int):
        self.agents = [
            Agent(f"Agent_{i}", AgentDNA.random())
            for i in range(size)
        ]
    
    def evolve(self, elite_size: int = 2):
        """Fait évoluer la population"""
        # Trie les agents par fitness
        self.agents.sort(key=lambda x: x.fitness, reverse=True)
        
        # Garde l'élite
        new_population = self.agents[:elite_size]
        
        # Croise et mute pour remplir la population
        while len(new_population) < len(self.agents):
            parent1, parent2 = random.sample(self.agents[:len(self.agents)//2], 2)
            child_dna = self._crossover(parent1.dna, parent2.dna)
            child_dna = child_dna.mutate()
            new_population.append(Agent(f"Agent_{len(new_population)}", child_dna))
        
        self.agents = new_population
    
    def _crossover(self, dna1: AgentDNA, dna2: AgentDNA) -> AgentDNA:
        """Croise deux ADN"""
        child_data = {}
        for field in dna1.__dataclass_fields__:
            if random.random() < 0.5:
                child_data[field] = getattr(dna1, field)
            else:
                child_data[field] = getattr(dna2, field)
        return AgentDNA(**child_data)