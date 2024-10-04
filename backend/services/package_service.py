from models.model import Package
import logging

class PackageService:
    def package(self, data: Package):
        logging.info(f"Processing package...")
        return data