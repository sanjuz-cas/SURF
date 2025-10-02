# Multi-Agent System

A comprehensive multi-agent system built with FastAPI, LangGraph, and React.

## Project Structure

```
├── backend/       # Python backend with FastAPI + LangGraph agents
│   ├── agents/    # Multi-agent modules
│   ├── routes/    # API endpoints
│   └── main.py    # FastAPI entrypoint
├── frontend/      # React + TypeScript dashboard
├── db/            # Postgres migrations + schema.sql
├── integrations/  # Slack, Notion, Email connectors
├── README.md
├── requirements.txt
└── package.json
```

## Getting Started

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the FastAPI server:
```bash
cd backend
python main.py
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
npm install
```

2. Start the React development server:
```bash
cd frontend
npm start
```

### Database Setup

1. Create a PostgreSQL database
2. Run the schema migrations:
```bash
psql -d your_database -f db/schema.sql
```

## Features

- Multi-agent system using LangGraph
- FastAPI backend with RESTful APIs
- React + TypeScript frontend dashboard
- PostgreSQL database integration
- Slack, Notion, and Email integrations

## Contributing

Please read the contributing guidelines before submitting pull requests.

## License

This project is licensed under the MIT License.