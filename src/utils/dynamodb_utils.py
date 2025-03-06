import boto3
from typing import Dict, Any, List
from src.config import AWS_REGION, DYNAMODB_TABLE_NAME
import random

class DynamoDBManager:
    def __init__(self):
        """Initialize DynamoDB client and create table if it doesn't exist."""
        self.dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
        self.table_name = DYNAMODB_TABLE_NAME
        self.table = self._get_or_create_table()

    def _get_or_create_table(self):
        """Get existing table or create a new one if it doesn't exist."""
        try:
            # Try to get the table
            table = self.dynamodb.Table(self.table_name)
            table.table_status  # This will raise an exception if table doesn't exist
            return table
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            # Create the table if it doesn't exist
            print(f"Creating DynamoDB table '{self.table_name}'...")
            table = self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'},  # Partition key
                    {'AttributeName': 'date', 'KeyType': 'RANGE'}  # Sort key
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                    {'AttributeName': 'date', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            table.wait_until_exists()
            print("Table created successfully!")
            return table

    def store_reports(self, reports: List[Dict[str, Any]]):
        """Store multiple medical reports in DynamoDB."""
        with self.table.batch_writer() as batch:
            for report in reports:
                batch.put_item(Item=report)
        print(f"Stored {len(reports)} reports in DynamoDB")

    def get_report(self, report_id: str, date: str) -> Dict[str, Any]:
        """Retrieve a specific medical report by ID and date."""
        response = self.table.get_item(
            Key={
                'id': report_id,
                'date': date
            }
        )
        return response.get('Item')

    def get_all_reports(self) -> List[Dict[str, Any]]:
        """Retrieve all medical reports from DynamoDB."""
        response = self.table.scan()
        return response.get('Items', [])

    def get_random_report(self) -> Dict[str, Any]:
        """Retrieve a random medical report from DynamoDB."""
        reports = self.get_all_reports()
        return random.choice(reports) if reports else None 