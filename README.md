# Kelma Backend

FastAPI backend for the Kelma conlang dictionary application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your MongoDB Atlas connection string:
```
MONGODB_URI=your_mongodb_atlas_connection_string
DATABASE_NAME=kelma
```

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

## Deployment

This backend is designed to be deployed on Render.
