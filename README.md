# FastAPI Template

A simple FastAPI template with a structured project layout for building asynchronous APIs.

## Project Structure

```
├── src/
│   ├── config/
│   │   └── env.py
│   ├── controllers/
│   │   └── webhook_controller.py
│   ├── routes/
│   │   ├── webhook_routes.py
│   │   └── template_routes.py
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
├── watch.py
├── .env
├── requirements.txt
└── README.md
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your environment variables.

## Running the Application

### Normal mode:
```bash
uvicorn src.main:app --reload
```

### With file watcher:
```bash
python watch.py
```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 