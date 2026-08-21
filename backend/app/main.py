from fastapi import FastAPI

from app.api.routes.recovery import router as recovery_router


def create_application() -> FastAPI:
    app = FastAPI(
        title="RevX",
        version="0.1.0",
    )

    app.include_router(recovery_router)

    return app


app = create_application()