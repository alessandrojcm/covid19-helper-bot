from fastapi import APIRouter

from .user_greeting import user_greeting
from .main_menu import main_menu

autopilot = APIRouter()
autopilot.include_router(user_greeting)
autopilot.include_router(main_menu)
