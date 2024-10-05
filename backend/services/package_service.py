from models.model import Package, Payment
import logging, uuid, random
from datetime import datetime, timedelta

class PackageService:
    def package(self, data: Payment):
        logging.info(f"Processing package...")

        package = Package(
            package_id=str(uuid.uuid4()),  
            order_id=data.order.order_id, 
            weight=2.5, 
            dimensions="10x5x2",  
            packaging_type="Box",  
            shipped_date=datetime.now(),
            expected_delivery_date=datetime.now() + timedelta(days=random.randint(1, 10)), 
            current_status="Shipped",  
            tracking_number="ABC123456789",  
            courier_service="DHL"  
        )

        logging.info(f"Package created: {package}")
        return package