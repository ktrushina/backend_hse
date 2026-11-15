from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routers.predict import router as predict_router

app = FastAPI(title="Ad Moderation API")
app.include_router(predict_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Expose invalid request data as HTTP 400, as required by the assignment."""
    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid request data", "errors": exc.errors()},
    )
