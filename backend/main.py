from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent_core import AgentPopulation, Agent, AgentDNA

app = FastAPI()

# Permettre les requêtes CORS depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instance globale de notre population d'agents
population = AgentPopulation(size=5)

@app.get("/agents")
async def get_agents():
    return {
        "agents": [
            {
                "name": agent.name,
                "dna": agent.dna.__dict__,
                "fitness": agent.fitness,
                "actions_history": agent.actions_history
            }
            for agent in population.agents
        ]
    }

@app.post("/evolve")
async def evolve_population():
    population.evolve()
    return {"status": "Population evolved"}

@app.post("/execute_task/{agent_id}")
async def execute_task(agent_id: int, task: str):
    if 0 <= agent_id < len(population.agents):
        result = population.agents[agent_id].execute_task(task)
        return result
    return {"error": "Agent not found"}