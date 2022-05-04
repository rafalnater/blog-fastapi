from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.settings import settings
from blog.controllers import router as blog_router
from articles.controllers import router as article_router
from comments.controllers import router as comment_router
from item.controllers import router as item_router
from user.controllers import router as user_router


app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
if settings.SENTRY_DSN is not None:
    import sentry_sdk
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

    sentry_sdk.init(dsn=settings.SENTRY_DSN, environment=settings.SENTRY_ENVIRONMENT)
    SentryAsgiMiddleware(app)

app.include_router(user_router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(item_router, prefix=f"{settings.API_V1_STR}/items", tags=["items"])
app.include_router(blog_router, prefix=f"{settings.API_V1_STR}/entries", tags=["entries"])
app.include_router(
    comment_router,
    prefix=f"{settings.API_V1_STR}/comments",
    tags=["comments"],
)
app.include_router(
    article_router,
    prefix=f"{settings.API_V1_STR}/articles",
    tags=["articles"],
)
