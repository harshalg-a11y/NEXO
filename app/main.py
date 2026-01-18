from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers import auth as auth_router
from app.routers import user as user_router
from app.routers import travel as travel_router
from app.routers import health as health_router
from app.routers import agro as agro_router
from app.routers import education as education_router
from app.routers import chat as chat_router
from app.routers import nexo_paisa as nexo_paisa_router
from app.routers import calendar as calendar_router
from app.routers import admin as admin_router
from app.config import settings

app = FastAPI(
    title="NEXO API",
    description="Super App for Nepal - Travel, Health, Education, Agriculture and more",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body}
    )

# Routers
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(travel_router.router)
app.include_router(health_router.router)
app.include_router(agro_router.router)
app.include_router(education_router.router)
app.include_router(chat_router.router)
app.include_router(nexo_paisa_router.router)
app.include_router(calendar_router.router)
app.include_router(admin_router.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "app_name": settings.app_name}
    )

@app.get("/api/health")
async def health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": "1.0.0"
    }
