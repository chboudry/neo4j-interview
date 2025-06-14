# Neo4j Interview Project

A full-stack application with FastAPI backend, React TypeScript frontend, and Neo4j database with Graph Data Science (GDS) plugin.

## Project Structure

```
├── .devcontainer/           # Development container configuration
│   ├── devcontainer.json    # VS Code dev container config
│   ├── docker-compose.yml   # Docker compose for development
│   └── Dockerfile          # Development environment dockerfile
├── api/                    # FastAPI backend
│   ├── main.py            # FastAPI application entry point
│   ├── models.py          # Pydantic models
│   ├── database.py        # Neo4j database client
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Environment variables
└── frontend/              # React TypeScript frontend
    ├── public/            # Static assets
    ├── src/              # React source code
    ├── package.json      # Node.js dependencies
    └── tsconfig.json     # TypeScript configuration
```

## Features

- **FastAPI Backend**: Modern Python web framework with automatic API documentation
- **Neo4j Database**: Graph database with Graph Data Science (GDS) plugin
- **React TypeScript Frontend**: Modern React application with TypeScript
- **Dev Container**: Complete development environment with Docker
- **Employee Management**: API endpoint to list employees from Neo4j

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Visual Studio Code with Dev Containers extension

### Setup

1. Open this project in VS Code
2. When prompted, reopen in Dev Container (or use Command Palette: "Dev Containers: Reopen in Container")
3. Wait for the containers to build and start

### Running the Application

The project uses two containers:
- **App Container**: Contains both Python and Node.js for full-stack development
- **Neo4j Container**: Database with GDS plugin

#### Step 1: Install Dependencies
```bash
# Install Python dependencies
cd api
pip install -r requirements.txt

# Install Node.js dependencies  
cd ../frontend
npm install
```

#### Step 2: Start the API
```bash
cd api
python main.py
```
You should see: `INFO:     Uvicorn running on http://0.0.0.0:8000`

#### Step 3: Start the Frontend (In a new terminal)
```bash
cd frontend
npm start
```

That's it! Both services run in the same container with different terminals.

### Useful Commands

```bash
# View running containers
docker-compose ps

# View logs for all services
docker-compose logs

# View logs for specific service
docker-compose logs neo4j

# Restart Neo4j service
docker-compose restart neo4j

# Access the dev container shell
docker-compose exec app bash
```

### Access Points

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Neo4j Browser**: http://localhost:7474 (username: neo4j, password: password)

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /employees` - List all employees

## Database

The Neo4j database comes pre-configured with:
- Neo4j 5.15 Enterprise Edition
- Graph Data Science (GDS) plugin
- Sample employee data

### Sample Data

The application automatically creates sample employee data on startup:
- 5 sample employees with various departments and positions
- Employee nodes with properties: id, name, email, department, position, hire_date

## Development

### Environment Variables

API environment variables (in `api/.env`):
- `NEO4J_URI`: Neo4j connection URI
- `NEO4J_USERNAME`: Neo4j username
- `NEO4J_PASSWORD`: Neo4j password
- `NEO4J_DATABASE`: Neo4j database name

### Adding New Features

1. **Backend**: Add new endpoints in `api/main.py`
2. **Frontend**: Add new components in `frontend/src/`
3. **Database**: Modify queries in `api/database.py`

## Technologies Used

- **Backend**: FastAPI, Python 3.11, Neo4j Python Driver
- **Frontend**: React 18, TypeScript, Create React App
- **Database**: Neo4j 5.15 Enterprise with GDS plugin
- **Development**: Docker, Docker Compose, VS Code Dev Containers
