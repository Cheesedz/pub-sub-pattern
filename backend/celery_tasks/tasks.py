import logging, json
from models.model import Package, Payment
from celery_tasks.app_worker import app
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from services.package_service import PackageService

# Initialize the service once outside the task
package_service = PackageService()

@app.task(bind=True, retry=5, default_retry_delay=60)
def package_consumer(self, data):
    try:
        # Deserialize data if it's a JSON string
        if isinstance(data, str):
            data = json.loads(data)

        package_data = Payment(**data)
        logging.info(f"[Package Data] Data: {package_data}")
        result = package_service.package(package_data)

        return {'status': 'SUCCESS', 'result': result.dict()}
    
    except json.JSONDecodeError as json_error:
        logging.error(f"Failed to decode JSON: {json_error}")
        return {'status': 'FAIL', 'result': 'Invalid JSON format'}

    except Exception as ex:
        logging.error(f"Exception in task: {ex}")
        try:
            self.retry(countdown=2, exc=ex)
        except MaxRetriesExceededError:
            logging.error(f"Max retries exceeded for task {self.request.id}")
            return {'status': 'FAIL', 'result': 'Max retries achieved'}
