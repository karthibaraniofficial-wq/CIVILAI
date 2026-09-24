"""
CIVILAI — Vercel Serverless Function Entrypoint
Exposes the FastAPI application to Vercel's Python runtime.
"""
import sys
import os
from urllib.parse import parse_qs, urlencode

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from main import app
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class VercelPathFixMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        scope = request.scope
        raw_query = scope.get("query_string", b"").decode("utf-8")
        if "__path=" in raw_query:
            params = parse_qs(raw_query)
            if "__path" in params:
                subpath = params.pop("__path")[0]
                if subpath.startswith("/api"):
                    scope["path"] = subpath
                else:
                    scope["path"] = f"/api{subpath}"
                scope["query_string"] = urlencode(params, doseq=True).encode("utf-8")
        elif scope.get("path", "").startswith("/api/index.py"):
            scope["path"] = scope["path"].replace("/api/index.py", "/api", 1) or "/"
            
        response = await call_next(request)
        return response


app.add_middleware(VercelPathFixMiddleware)
