from celery import Celery

from core.settings import settings


celery_app = Celery("worker", broker=settings.BROKER_URL)

if settings.SENTRY_DSN is not None:
    import sentry_sdk
    from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

    sentry_sdk.init(dsn=settings.SENTRY_DSN)
    SentryAsgiMiddleware(celery_app)

celery_app.conf.task_routes = {
    "worker.sample_task": "main-queue",
    "worker.scheduled_task": "main-queue",
}
