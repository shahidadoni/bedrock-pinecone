import json
from typing import List, Dict, Any
from pathlib import Path

class DataManager:
    def __init__(self, data_path: str = "src/data/medical_reports.json"):
        self.data_path = Path(data_path)
        self._create_sample_data()

    def _create_sample_data(self):
        """Create sample medical report data if it doesn't exist."""
        if not self.data_path.exists():
            sample_data = [
                {
                    "id": "report_001",
                    "patient_name": "John Doe",
                    "date": "2024-03-01",
                    "report_type": "Blood Test",
                    "content": "Complete Blood Count (CBC) results:\n- WBC: 7.5 x10^9/L (Normal: 4.5-11.0)\n- RBC: 4.8 x10^12/L (Normal: 4.2-5.4)\n- Hemoglobin: 14.2 g/dL (Normal: 13.5-17.5)\n- Hematocrit: 42% (Normal: 38.8-50)\n- Platelets: 250 x10^9/L (Normal: 150-450)\nAll values within normal range.",
                    "doctor": "Dr. Smith",
                    "department": "Hematology"
                },
                {
                    "id": "report_002",
                    "patient_name": "Jane Smith",
                    "date": "2024-03-02",
                    "report_type": "MRI Scan",
                    "content": "MRI of the lumbar spine shows:\n- Mild degenerative disc disease at L4-L5\n- No significant spinal stenosis\n- No herniated discs\n- Normal alignment of vertebral bodies\n- No compression fractures",
                    "doctor": "Dr. Johnson",
                    "department": "Radiology"
                },
                {
                    "id": "report_003",
                    "patient_name": "Mike Wilson",
                    "date": "2024-03-03",
                    "report_type": "ECG",
                    "content": "12-lead ECG interpretation:\n- Normal sinus rhythm\n- Heart rate: 72 bpm\n- PR interval: 160ms\n- QRS duration: 90ms\n- QT interval: 380ms\n- No ST segment changes\n- No significant abnormalities detected",
                    "doctor": "Dr. Brown",
                    "department": "Cardiology"
                }
            ]
            with open(self.data_path, 'w') as f:
                json.dump(sample_data, f, indent=2)

    def load_data(self) -> List[Dict[str, Any]]:
        """Load medical report data from JSON file."""
        with open(self.data_path, 'r') as f:
            return json.load(f)

    def get_report_by_id(self, report_id: str) -> Dict[str, Any]:
        """Get a specific medical report by ID."""
        data = self.load_data()
        for report in data:
            if report['id'] == report_id:
                return report
        return None 