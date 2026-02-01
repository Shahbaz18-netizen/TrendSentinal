from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import analyzer

# 1. Initialize the FastAPI Application
app = FastAPI(
    title="TrendSentinel AI",
    description="24/7 AI-Powered YouTube Market Intelligence Agent",
    version="1.0.0",
    docs_url="/docs"  # This is where the Swagger UI lives
)

# 2. Setup CORS (Cross-Origin Resource Sharing)
# Logic: This allows our Streamlit frontend to communicate with this API.
# In production, you would replace "*" with your actual domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Include our Routers
# Logic: We keep the '/analyze' logic in a separate file to stay modular.
app.include_router(analyzer.router)

# 4. Root / Health Check Endpoint
@app.get("/")
async def root():
    """
    LOGIC: A basic 'Heartbeat' to ensure the server is running.
    """
    return {
        "message": "TrendSentinel API is operational",
        "status": "online",
        "documentation": "/docs"
    }

# This allows running the file directly for debugging
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)