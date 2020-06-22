"""Celery app module"""
from celery import Celery
from celery.utils.log import get_task_logger

from app import app


logger = get_task_logger(__name__)


def configure_celery(app):
    """Configures celery app

    Args:
        app (object): Flask application object

    Returns:
        object: configured celery app object

    """
    celery = Celery("app", include=['src.tasks.plans'])
    celery.conf.update(app.config)

    # subclass task base for app context
    # http://flask.pocoo.org/docs/0.12/patterns/celery/
    TaskBase = celery.Task

    class AppContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = AppContextTask

    # run finalize to process decorated tasks
    celery.finalize()

    return celery


celery = configure_celery(app)
