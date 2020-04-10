from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from .twilio_request_validator import TwilioRequestValidator

MIDDLEWARES = [HTTPSRedirectMiddleware, TwilioRequestValidator]
