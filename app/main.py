from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import get_settings
from app.database import init_db
from app.routers import auth, dashboard, travel, health, agro, education, chat, nexo_paisa, calendar, admin
from app.security import CSRFProtection

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    init_db()
    yield
    # Shutdown (add cleanup if needed)


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth.router, tags=["auth"])
app.include_router(dashboard.router, tags=["dashboard"])
app.include_router(travel.router, tags=["travel"])
app.include_router(health.router, tags=["health"])
app.include_router(agro.router, tags=["agro"])
app.include_router(education.router, tags=["education"])
app.include_router(chat.router, tags=["chat"])
app.include_router(nexo_paisa.router, tags=["nexo-paisa"])
app.include_router(calendar.router, tags=["calendar"])
app.include_router(admin.router, tags=["admin"])


@app.get("/", response_class=HTMLResponse)
async def welcome(request: Request):
    """Welcome page"""
    csrf_token = CSRFProtection.generate_csrf_token()
    return templates.TemplateResponse(
        "welcome.html",
        {
            "request": request,
            "csrf_token": csrf_token,
            "page": "welcome"
        }
    )


@app.get("/health-check")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "app": settings.app_name}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
