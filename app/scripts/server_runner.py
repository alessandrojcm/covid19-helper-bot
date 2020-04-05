import uvicorn as asgi


def run_app(app, port=8000, host="0.0.0.0", *args):
    return asgi.run(app, *args, port=port, host=host)
