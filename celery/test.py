from celery import Celery
from celery.schedules import crontab


celery = Celery("worker hello", 
                backend='redis://localhost:6379/0', 
                broker="redis://localhost:6379/1",
                broker_connection_retry_on_startup=True
                )


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        1.0,
        enrolled.s(),
    )



@celery.task
def enrolled():
    print("Done!")