from typing import Any

from celery import Celery

from core.celery import celery_app


@celery_app.task(acks_late=True)
def sample_task(word: str) -> str:
    return f"Sample task returns: {word}"


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs: Any) -> None:
    sender.add_periodic_task(
        10.0, sample_task.s(word="hello!"), name="Do this every 10 secs"
    )
