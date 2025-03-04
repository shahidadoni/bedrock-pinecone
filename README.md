# Medical Report Chatbot with Pinecone and AWS Bedrock

This project implements a medical report chatbot using Pinecone for vector storage and AWS Bedrock for model inference. The chatbot can analyze medical reports and provide insights based on the stored knowledge.

## Prerequisites

- Python 3.8+
- AWS Account with Bedrock access
- Pinecone Account and API key
- Required environment variables

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_REGION=your_aws_region
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment
   ```

## Project Structure

```
.
├── requirements.txt
├── .env
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── pinecone_utils.py
│   │   ├── bedrock_utils.py
│   │   └── data_utils.py
│   └── data/
│       └── medical_reports.json
└── README.md
```

## Usage

1. Run the main application:
   ```bash
   python src/main.py
   ```

2. The application will:
   - Load medical report data
   - Create embeddings and store them in Pinecone
   - Start an interactive chat session where you can ask questions about medical reports

## Features

- Vector storage of medical report embeddings using Pinecone
- Natural language processing using AWS Bedrock
- Interactive chat interface
- Context-aware responses based on medical report content