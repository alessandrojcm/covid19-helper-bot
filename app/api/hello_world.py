from fastapi import APIRouter

hello_world_router = APIRouter()


@hello_world_router.get("/")
def hello_world():
    """
        Just a friendly reminder ;)
    """
    return "Twilio & Dev Hackathon 2020 API <Alessandro Cuppari me@alessandrojcm.dev>"
