import random
from typing import Dict, Any
from src.utils.dynamodb_utils import DynamoDBManager
from src.utils.data_utils import DataManager

class PatientManager:
    def __init__(self):
        self.dynamodb_manager = DynamoDBManager()
        self.data_manager = DataManager()
        self.current_patient = None
        self.current_report = None
        self._initialize_reports()

    def _initialize_reports(self):
        """Initialize patient reports in DynamoDB if the table is empty."""
        reports = self.dynamodb_manager.get_all_reports()
        if not reports:
            print("No reports found in DynamoDB. Initializing with sample data...")
            sample_reports = self.data_manager.load_data()
            self.dynamodb_manager.store_reports(sample_reports)

    def assign_random_patient(self) -> Dict[str, Any]:
        """Assign a random patient report to the current session."""
        self.current_report = self.dynamodb_manager.get_random_report()
        if not self.current_report:
            raise ValueError("No reports found in DynamoDB")
            
        self.current_patient = {
            'name': self.current_report['patient_name'],
            'condition': self.current_report['condition'],
            'department': self.current_report['department'],
            'doctor': self.current_report['doctor']
        }
        return self.current_patient

    def get_current_patient_info(self) -> Dict[str, Any]:
        """Get information about the currently assigned patient."""
        if not self.current_patient:
            raise ValueError("No patient has been assigned yet. Call assign_random_patient() first.")
        return self.current_patient

    def get_current_report(self) -> Dict[str, Any]:
        """Get the current patient's medical report."""
        if not self.current_report:
            raise ValueError("No report has been assigned yet. Call assign_random_patient() first.")
        return self.current_report

    def format_patient_context(self) -> str:
        """Format the current patient's information for context."""
        if not self.current_report:
            raise ValueError("No report has been assigned yet. Call assign_random_patient() first.")
        
        report = self.current_report
        context = f"Patient Information:\n"
        context += f"Name: {report['patient_name']}\n"
        context += f"Condition: {report['condition']}\n"
        context += f"Department: {report['department']}\n"
        context += f"Doctor: {report['doctor']}\n"
        context += f"Date: {report['date']}\n"
        context += f"Report Type: {report['report_type']}\n"
        context += f"\nReport Content:\n{report['content']}\n"
        return context 