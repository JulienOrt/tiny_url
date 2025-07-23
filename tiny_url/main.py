from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from tiny_url.models.exceptions import TinyUrlBaseException


async def exception_middleware(api_request: Request, call_next):
    try:
        return await call_next(api_request)
    except TinyUrlBaseException as exc:
        return JSONResponse(status_code=exc.status_code, headers={'Content-Type': 'application/json'}, content=str(exc))
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={'Content-Type': 'application/json'}, content="An unexpected error happened"
        )


def build_api():
    fastapi_app = FastAPI(title='Tiny URL - API')

    from tiny_url.schema import url

    fastapi_app.middleware('http')(exception_middleware)

    fastapi_app.include_router(router=url.router, prefix="/url", tags=["Url"])

    return fastapi_app


local_app = build_api()


if __name__ == "__main__":
    pass
    # UrlMappingController.insert_record(source_url="test", slug_url="jch", end_validity_date=datetime.now(UTC))
