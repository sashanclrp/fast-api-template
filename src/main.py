from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import uvicorn

# Import config and utils
from config.env import PORT, CORS_ALLOW_ALL, ALLOWED_ORIGINS, MODE
from utils.logger import logger

# Import routes
from routes.webhook_routes import router as webhook_router
from routes.template_routes import router as template_router

# Create FastAPI app
app = FastAPI(
    title="FastAPI Template",
    description="A template for FastAPI applications",
    version="0.1.0",
)

# ============
# MIDDLEWARES
# ============

# Add CORS middleware based on environment settings
if CORS_ALLOW_ALL:
    # Development mode - allow all origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS configured for development mode (allowing all origins)")
else:
    # Production mode - only allow specified origins
    origins = ALLOWED_ORIGINS.split(",") if ALLOWED_ORIGINS else []
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["Authorization", "Content-Type"],
    )
    logger.info(f"CORS configured for production mode with origins: {origins}")

# Add request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    
    # Log request info in DEV mode
    if MODE == "DEV":
        # Get request path and method
        path = request.url.path
        method = request.method
        
        # Get query params as string
        query_params = str(request.query_params) if request.query_params else "None"
        
        # Log before processing
        logger.info(f"Request: {method} {path} | Params: {query_params}")
        
        # Attempt to log body for non-GET requests (could be empty for some requests)
        if method != "GET":
            try:
                body = await request.body()
                if body:
                    # Limit body size in logs to avoid huge outputs
                    body_str = body.decode('utf-8')
                    if len(body_str) > 1000:
                        body_str = body_str[:1000] + "... [truncated]"
                    logger.info(f"Request Body: {body_str}")
            except Exception:
                # Some bodies can't be read twice, so we'll just ignore errors
                pass
    
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log completion time in DEV mode
    if MODE == "DEV":
        logger.info(f"Request to {request.url.path} processed in {process_time:.4f} seconds")
    
    return response

# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )

# ============
# ROUTES
# ============

# Include routers
app.include_router(webhook_router, prefix="/api/webhook", tags=["Webhooks"])
app.include_router(template_router, prefix="/api/template", tags=["Templates"])

# ============
# ENDPOINTS
# ============

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the FastAPI Template"}

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}


# Start the server when executed directly
if __name__ == "__main__":
    logger.info(f"Starting server on port {PORT}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        reload=False  # Watchdog handles reloading
    )