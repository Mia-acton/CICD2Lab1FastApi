# CICD-2 Lab 5: Two FastAPI Microservices with HTTPX
This project contains two independent FastAPI services:

- User API (port 8000): Keeps the existing user endpoints and SQLAlchemy/SQLite database, and calls the Product Service using HTTPX.
- Product Service (port 8001): Returns predefined product information.

### Run both services in GitHub Codespaces

Open two separate terminals in the same Codespace.

**Terminal 1 — Product Service:**
python -m uvicorn product_service.main:app --host 0.0.0.0 --port 8001 --reload

**Terminal 2 — User API:**
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Keep both processes running. 

### PRODUCT_SERVICE_URL
