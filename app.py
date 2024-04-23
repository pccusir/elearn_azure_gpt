from flask import Flask, render_template, request
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.data.tables import TableServiceClient

def authenticate_client():
    key = "<your_azure_key>"
    endpoint = "<your_azure_endpoint>"
    ta_credential = AzureKeyCredential(key)
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
    connection_string = "<your_azure_sql_database_connection_string>"
    table_name = "<your_table_name>"
    table_service_client = TableServiceClient.from_connection_string(connection_string)
    table_client = table_service_client.get_table_client(table_name)
    rows = table_client.query_entities()
    return render_template('database.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
