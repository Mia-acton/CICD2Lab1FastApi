# Lab 5 – Two FastAPI Microservices with HTTPX 

## Running the services

From the project folder, open two separate Codespaces terminals and leave both running.

**Terminal 1 – Product Service (port 8001):**
python -m uvicorn product_service.main:app --host 0.0.0.0 --port 8001 --reload

**Terminal 2 – User API (port 8000):**
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

## Getting a product

`GET /api/products/{product_id}` asks the User API to fetch a product from the Product Service using HTTPX.

To try it, open port 8000 from the Codespaces Ports tab, add `/docs` to the URL and test `GET /api/products/1`.

## PRODUCT_SERVICE_URL
`PRODUCT_SERVICE_URL` is an environment variable that tells the User API where to find the Product Service. It defaults to `http://127.0.0.1:8001` in Codespaces and can be changed without editing the code.