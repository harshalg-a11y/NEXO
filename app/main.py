from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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

app = FastAPI(title="NEXO API")

# Static and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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
    return templates.TemplateResponse("index.html", {"request": request, "message": "Welcome to NEXO"})
