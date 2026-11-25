from fastapi.openapi.utils import get_openapi
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

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    # Убираем стандартный 422 там, где валидация возвращает 400
    for path in schema["paths"].values():
        for operation in path.values():
            responses = operation.get("responses", {})
            if "400" in responses:
                responses.pop("422", None)

    app.openapi_schema = schema
    return schema


app.openapi = custom_openapi