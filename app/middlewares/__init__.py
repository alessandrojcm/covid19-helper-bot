from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# Middlewares to add to the app
MIDDLEWARES = [HTTPSRedirectMiddleware]
