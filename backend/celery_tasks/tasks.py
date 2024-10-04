import logging
from models.model import Package
from celery import Task
from celery.exceptions import MaxRetriesExceededError
from .app_worker import app
from services.package_service import PackageService


class PackageTask(Task):
    def __init__(self):
        super().__init__()
        self.package_service = PackageService()

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logging.warning(f"Retrying task {task_id} due to {exc}")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logging.error(f"Task {task_id} failed due to {exc}")


@app.task(ignore_result=False, bind=True, base=PackageTask)
def package_consumer(self, data):
    try:
        package_data = Package(**data)
        logging.info(f"[Package Data] Data: {package_data}")
        result = self.package_service.package(package_data)

        return {'status': 'SUCCESS', 'result': result.dict()}
    except Exception as ex:
        try:
            self.retry(countdown=2)
        except MaxRetriesExceededError as ex:
            logging.error(f"Max retries exceeded for task {self.request.id}")
            return {'status': 'FAIL', 'result': 'max retried achieved'}
