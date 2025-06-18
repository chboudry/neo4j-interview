from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import neo4j_client
import uvicorn
from routes import routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        neo4j_client.connect()
        # Ensure unique constraints
        neo4j_client.ensure_unique_constraints()
        print("Initialization successfull.")
    except Exception as e:
        print(f"Failed to initialize database: {e}")
        raise
    
    yield
    
    # Shutdown
    neo4j_client.close()

app = FastAPI(
    title="Neo4j Interview API",
    description="A FastAPI application with Neo4j database for managing employees",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
