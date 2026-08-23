from fastapi import FastAPI

from app.api.exception_handlers import register_exception_handlers
from app.api.routes.recovery import router as recovery_router
from app.core.config import get_settings


def create_application() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    register_exception_handlers(app)

    app.include_router( recovery_router)

    return app


app = create_application()