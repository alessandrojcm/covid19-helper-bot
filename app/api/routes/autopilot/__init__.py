from fastapi import APIRouter

from .user_greeting import user_greeting

autopilot = APIRouter()
autopilot.include_router(user_greeting)
