import settings

from celery import Celery

app = Celery("notify", broker=settings.CELERY_BROKER_URL, include=["core.celery_app.tasks"])
app.conf.timezone = settings.TIMEZONE

if __name__ == "__main__":
    app.start()
