import random
from ai_bird import AIBird
from brain import Brain

class Population:
    def __init__(self, size=100):
        self.size = size
        self.generation = 0
        self.birds = [AIBird() for _ in range(size)]
        self.best_bird = None
        self.best_fitness = 0

    def calculate_fitness(self):
        total_fitness = sum(bird.fitness for bird in self.birds)
        
        for bird in self.birds:
            if total_fitness > 0:
                bird.fitness /= total_fitness
            else:
                bird.fitness = 0

    def select_parent(self):
        r = random.random()
        cumulative_fitness = 0
        
        for bird in self.birds:
            cumulative_fitness += bird.fitness
            if r < cumulative_fitness:
                return bird.brain
        
        return random.choice(self.birds).brain

    def crossover(self, brain1, brain2):
        new_weights = []
        for w1, w2 in zip(brain1.weights, brain2.weights):
            if random.random() < 0.5:
                new_weights.append(w1)
            else:
                new_weights.append(w2)
        
        return Brain(new_weights)

    def evolve(self):
        self.calculate_fitness()
        self.generation += 1
        
        new_birds = []
        
        current_best = max(self.birds, key=lambda bird: bird.fitness)
        if current_best.fitness > self.best_fitness:
            self.best_fitness = current_best.fitness
            self.best_bird = AIBird(brain=current_best.brain.copy())
            new_birds.append(self.best_bird)

        while len(new_birds) < self.size:
            parent1 = self.select_parent()
            parent2 = self.select_parent()
            
            child_brain = self.crossover(parent1, parent2)
            
            child_brain.mutate(rate=0.1, strength=0.5) 
            
            new_birds.append(AIBird(brain=child_brain))

        self.birds = new_birds