import logging, json, requests, os
from datetime import datetime
from os.path import join, dirname
from dotenv import load_dotenv
from models.model import Package, Payment
from celery_tasks.app_worker import app
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from services.package_service import PackageService

load_dotenv()
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
        result = requests.post(
            url=f"{os.environ.get('PACKAGE_SERVICE_URL')}/api/package",
            json=data
        )

        return {'status': 'SUCCESS', 'result': result.request.body}
    
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

@app.task(bind=True, retry=5, default_retry_delay=60)
def delivery_consumer(self, data):
    try:
        # Deserialize data if it's a JSON string
        if isinstance(data, str):
            data = json.loads(data)
        logging.info(f"[Data]: {data['data']}")

        delivery_data = Package(**json.loads(data['data']))

        for key, value in delivery_data.__dict__.items():
            if isinstance(value, datetime):
                delivery_data.__dict__[key] = value.isoformat()
        logging.info(f"[Delivery Data] Data: {delivery_data}")

        result = requests.post(
            url=f"{os.environ.get('DELIVERY_SERVICE_URL')}/api/delivery",
            json=delivery_data.__dict__
        )

        return {'status': 'SUCCESS', 'result': result.request.body}
    
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

@app.task(bind=True, retry=5, default_retry_delay=60)
def mail_noti_consumer(self, data):
    try:
        message = "This message sent via mail"
        # Deserialize data if it's a JSON string
        result = requests.post(
            url=f"{os.environ.get('NOTIFICATION_SERVICE_URL')}/api/mail_send",
            json=message
        )

        return {'status': 'SUCCESS', 'result': result.request.body}
    
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
