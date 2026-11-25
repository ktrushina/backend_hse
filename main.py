from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routers.predict import router as predict_router
from routers.simple_predict import router as simple_predict_router

app = FastAPI(title="Ad Moderation API")
app.include_router(predict_router)
app.include_router(simple_predict_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = [
        {"loc": error["loc"], "msg": error["msg"], "type": error["type"]}
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=400,
        content={"detail": "Invalid request data", "errors": errors},
    )
