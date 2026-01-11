# API-For-LLM

A lightweight FastAPI-based REST API for interacting with LLM models using Ollama. Features API key authentication with credit-based rate limiting.

## Features

- 🚀 FastAPI for high-performance async API
- 🔐 API key authentication
- 💳 Credit-based usage limiting
- 🤖 Ollama integration for local LLM inference

## Requirements

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- Llama2 model pulled (`ollama pull llama2`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AyoubJebali/API-For-LLM.git
cd API-For-LLM
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your API key:
```bash
echo "API_KEY=your-secret-api-key" > .env
```

## Usage

### Start the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### POST /generate

Generate a response from the LLM.

**Headers:**
- `x-api-key`: Your API key (required)

**Query Parameters:**
- `promt`: The prompt to send to the LLM (required)

**Example:**
```bash
curl -X POST "http://localhost:8000/generate?promt=Hello" \
  -H "x-api-key: your-secret-api-key"
```

**Response:**
```json
{
  "response": "Hello! How can I help you today?"
}
```

### API Documentation

FastAPI provides interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run the tests with pytest:

```bash
pip install pytest
pytest test_main.py -v
```

## Project Structure

```
API-For-LLM/
├── main.py           # FastAPI application
├── test_main.py      # Unit tests
├── requirements.txt  # Python dependencies
├── .env              # Environment variables (not in git)
├── .gitignore        # Git ignore rules
└── README.md         # This file
```

## License

MIT License
