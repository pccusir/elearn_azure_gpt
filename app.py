from flask import Flask, render_template, request
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.data.tables import TableServiceClient

import tempfile, os

def authenticate_client():
    endpoint = os.getenv('END_POINT')
    ta_credential = AzureKeyCredential(os.getenv('AZURE_KEY'))
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, 
            credential=ta_credential)
    return text_analytics_client

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    client = authenticate_client()
    text = request.form['text']
    response = client.analyze_sentiment(documents=[text])[0]
    return render_template('result.html', sentiment=response.sentiment)

@app.route('/database')
def database_access():
    connection_string = os.getenv('SQL_CONNECTION_STRING')
    table_name = os.getenv('TABLE_NAME')
    table_service_client = TableServiceClient.from_connection_string(connection_string)
    table_client = table_service_client.get_table_client(table_name)
    rows = table_client.query_entities()
    return render_template('database.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
