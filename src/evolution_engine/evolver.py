"""
AETHER Evolution Engine - Autonomous Strategy Evolution
"""
import random
import asyncio
import numpy as np
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass
import json
import logging
from src.core.database import TradingStrategy, TradeSignal, get_db
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

@dataclass
class Gene:
    """Represents a strategy parameter gene"""
    name: str
    value: float
    min_value: float
    max_value: float
    mutation_rate: float = 0.1

@dataclass
class Organism:
    """Represents a trading strategy organism"""
    strategy_id: str
    genes: List[Gene]
    fitness: float = 0.0
    generation: int = 0

class EvolutionEngine:
    """Evolves trading strategies through genetic algorithms"""
    
    def __init__(self, population_size: int = 50, mutation_rate: float = 0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population: List[Organism] = []
        self.generation = 0
        
    def initialize_population(self, base_strategy: Dict[str, Any]):
        """Initialize population with variations of base strategy"""
        self.population = []
        
        # Define genes based on strategy parameters
        gene_definitions = self._extract_gene_definitions(base_strategy)
        
        # Create initial population
        for i in range(self.population_size):
            genes = []
            for gene_def in gene_definitions:
                # Add random variation to base values
                value = gene_def['value'] * (1 + random.uniform(-0.2, 0.2))
                value = max(gene_def['min'], min(gene_def['max'], value))
                
                genes.append(Gene(
                    name=gene_def['name'],
                    value=value,
                    min_value=gene_def['min'],
                    max_value=gene_def['max']
                ))
            
            organism = Organism(
                strategy_id=f"gen{self.generation}_org{i}",
                genes=genes,
                generation=self.generation
            )
            self.population.append(organism)
    
    def _extract_gene_definitions(self, strategy: Dict[str, Any]) -> List[Dict]:
        """Extract gene definitions from strategy parameters"""
        return [
            {
                'name': 'min_profit_threshold',
                'value': strategy.get('min_profit_threshold', 0.02),
                'min': 0.001,
                'max': 0.1
            },
            {
                'name': 'max_gas_price',
                'value': strategy.get('max_gas_price', 100),
                'min': 10,
                'max': 500
            },
            {
                'name': 'position_size',
                'value': strategy.get('position_size', 0.1),
                'min': 0.01,
                'max': 0.5
            },
            {
                'name': 'slippage_tolerance',
                'value': strategy.get('slippage_tolerance', 0.005),
                'min': 0.001,
                'max': 0.02
            },
            {
                'name': 'stop_loss',
                'value': strategy.get('stop_loss', 0.05),
                'min': 0.01,
                'max': 0.2
            },
            {
                'name': 'take_profit',
                'value': strategy.get('take_profit', 0.1),
                'min': 0.02,
                'max': 0.5
            }
        ]
    
    async def evaluate_fitness(self, organism: Organism, market_data: Dict) -> float:
        """Evaluate fitness of an organism through backtesting"""
        # Simplified fitness evaluation
        # In production, this would run full backtest
        
        genes_dict = {gene.name: gene.value for gene in organism.genes}
        
        # Fitness factors
        profit_factor = genes_dict.get('min_profit_threshold', 0.02) * 100
        risk_factor = 1 / (genes_dict.get('stop_loss', 0.05) * 10)
        efficiency_factor = 1 / (genes_dict.get('max_gas_price', 100) / 100)
        
        # Add random noise to simulate market conditions
        market_factor = random.uniform(0.8, 1.2)
        
        fitness = (profit_factor * risk_factor * efficiency_factor * market_factor)
        
        # Penalize extreme values
        for gene in organism.genes:
            if gene.value <= gene.min_value * 1.1 or gene.value >= gene.max_value * 0.9:
                fitness *= 0.8
        
        organism.fitness = fitness
        return fitness
    
    def select_parents(self) -> Tuple[Organism, Organism]:
        """Select parents using tournament selection"""
        tournament_size = 5
        
        def tournament():
            candidates = random.sample(self.population, tournament_size)
            return max(candidates, key=lambda x: x.fitness)
        
        parent1 = tournament()
        parent2 = tournament()
        
        return parent1, parent2
    
    def crossover(self, parent1: Organism, parent2: Organism) -> Organism:
        """Create offspring through crossover"""
        genes = []
        
        for i in range(len(parent1.genes)):
            # Uniform crossover
            if random.random() < 0.5:
                gene = parent1.genes[i]
            else:
                gene = parent2.genes[i]
            
            # Create new gene with copied values
            genes.append(Gene(
                name=gene.name,
                value=gene.value,
                min_value=gene.min_value,
                max_value=gene.max_value,
                mutation_rate=gene.mutation_rate
            ))
        
        offspring = Organism(
            strategy_id=f"gen{self.generation}_offspring",
            genes=genes,
            generation=self.generation
        )
        
        return offspring
    
    def mutate(self, organism: Organism):
        """Mutate organism's genes"""
        for gene in organism.genes:
            if random.random() < self.mutation_rate:
                # Gaussian mutation
                mutation = np.random.normal(0, 0.1)
                gene.value *= (1 + mutation)
                
                # Ensure within bounds
                gene.value = max(gene.min_value, min(gene.max_value, gene.value))
    
    async def evolve_generation(self, market_data: Dict):
        """Evolve one generation"""
        # Evaluate fitness for all organisms
        for organism in self.population:
            await self.evaluate_fitness(organism, market_data)
        
        # Sort by fitness
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        
        # Elite preservation (keep top 10%)
        elite_size = int(self.population_size * 0.1)
        new_population = self.population[:elite_size]
        
        # Generate offspring
        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents()
            offspring = self.crossover(parent1, parent2)
            self.mutate(offspring)
            new_population.append(offspring)
        
        self.population = new_population
        self.generation += 1
        
        logger.info(f"Generation {self.generation} - Best fitness: {self.population[0].fitness:.4f}")
    
    def get_best_strategy(self) -> Dict[str, Any]:
        """Get the best strategy from current population"""
        best = max(self.population, key=lambda x: x.fitness)
        
        strategy = {
            gene.name: gene.value
            for gene in best.genes
        }
        strategy['fitness'] = best.fitness
        strategy['generation'] = best.generation
        
        return strategy
    
    async def save_evolved_strategy(self, db: Session):
        """Save the best evolved strategy to database"""
        best_strategy = self.get_best_strategy()
        
        strategy = TradingStrategy(
            name=f"evolved_gen{self.generation}",
            version=self.generation,
            parameters=best_strategy,
            performance_score=best_strategy['fitness'],
            backtest_results={
                "generation": self.generation,
                "population_size": self.population_size,
                "mutation_rate": self.mutation_rate
            }
        )
        
        db.add(strategy)
        db.commit()
        
        logger.info(f"Saved evolved strategy with fitness {best_strategy['fitness']:.4f}")

async def run_evolution_engine():
    """Run the evolution engine continuously"""
    engine = EvolutionEngine(population_size=30)
    
    # Initialize with base strategy
    base_strategy = {
        'min_profit_threshold': 0.02,
        'max_gas_price': 100,
        'position_size': 0.1,
        'slippage_tolerance': 0.005,
        'stop_loss': 0.05,
        'take_profit': 0.1
    }
    
    engine.initialize_population(base_strategy)
    
    while True:
        try:
            # Mock market data (in production, fetch real data)
            market_data = {
                'volatility': random.uniform(0.01, 0.05),
                'trend': random.choice(['bullish', 'bearish', 'neutral']),
                'volume': random.uniform(1000000, 10000000)
            }
            
            # Evolve one generation
            await engine.evolve_generation(market_data)
            
            # Save best strategy every 10 generations
            if engine.generation % 10 == 0:
                db = next(get_db())
                await engine.save_evolved_strategy(db)
            
            # Log progress
            best = engine.get_best_strategy()
            logger.info(f"Generation {engine.generation} complete. Best parameters: {json.dumps(best, indent=2)}")
            
            # Evolution cycle delay
            await asyncio.sleep(10)
            
        except Exception as e:
            logger.error(f"Evolution engine error: {e}")
            await asyncio.sleep(30)