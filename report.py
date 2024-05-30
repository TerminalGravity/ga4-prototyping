from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest
from datetime import datetime, timedelta
import pandas as pd

# Path to the service account key file
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Create a credentials object
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

# Initialize the client
client = BetaAnalyticsDataClient(credentials=credentials)

# Define the date range (last 90 days)
end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=90)).strftime('%Y-%m-%d')

# Function to run a report and return the response
def run_report(dimensions, metrics):
    request = RunReportRequest(
        property='properties/263923988',
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimensions=dimensions,
        metrics=metrics
    )
    return client.run_report(request=request)

# Define Dimensions and Metrics
dimensions_dict = {
    'timeline': [Dimension(name='date'), Dimension(name='dayOfWeek'), Dimension(name='dayOfWeekName')],
    'visitation': [Dimension(name='date')],
    'transaction': [Dimension(name='date')],
    'enrollment': [Dimension(name='date')]
}

metrics_dict = {
    'visitation': [Metric(name='sessions'), Metric(name='activeUsers')],
    'visitation_totals': [
        Metric(name='sessions'),
        Metric(name='activeUsers'),
        Metric(name='screenPageViews'),
        Metric(name='screenPageViewsPerSession'),
        Metric(name='averageSessionDuration'),
        Metric(name='bounceRate')
    ],
    'transaction': [Metric(name='transactions'), Metric(name='purchaseRevenue')],
    'transaction_totals': [
        Metric(name='addToCarts'),
        Metric(name='ecommercePurchases')
    ],
    'enrollment': [Metric(name='newUsers')],
    'enrollment_totals': [Metric(name='newUsers')]
}

# Running Reports
timeline_response = run_report(dimensions_dict['timeline'], [])
visitation_response = run_report(dimensions_dict['visitation'], metrics_dict['visitation'])
visitation_totals_response = run_report([], metrics_dict['visitation_totals'])
transaction_response = run_report(dimensions_dict['transaction'], metrics_dict['transaction'])
transaction_totals_response = run_report([], metrics_dict['transaction_totals'])
enrollment_response = run_report(dimensions_dict['enrollment'], metrics_dict['enrollment'])
enrollment_totals_response = run_report([], metrics_dict['enrollment_totals'])

# Function to convert response to DataFrame
def response_to_dataframe(response):
    rows = []
    for row in response.rows:
        row_data = {}
        for i, dimension_value in enumerate(row.dimension_values):
            row_data[response.dimension_headers[i].name] = dimension_value.value
        for i, metric_value in enumerate(row.metric_values):
            row_data[response.metric_headers[i].name] = metric_value.value
        rows.append(row_data)
    return pd.DataFrame(rows)

# Convert responses to DataFrames
# timeline_df = response_to_dataframe(timeline_response)
visitation_df = response_to_dataframe(visitation_response)
visitation_totals_df = response_to_dataframe(visitation_totals_response)
# transaction_df = response_to_dataframe(transaction_response)
# transaction_totals_df = response_to_dataframe(transaction_totals_response)
enrollment_df = response_to_dataframe(enrollment_response)
enrollment_totals_df = response_to_dataframe(enrollment_totals_response)

# Save DataFrames to CSV
# timeline_df.to_csv('timeline_report.csv', index=False)
visitation_df.to_csv('visitation_report.csv', index=False)
visitation_totals_df.to_csv('visitation_totals_report.csv', index=False)
# transaction_df.to_csv('transaction_report.csv', index=False)
# transaction_totals_df.to_csv('transaction_totals_report.csv', index=False)
enrollment_df.to_csv('enrollment_report.csv', index=False)
enrollment_totals_df.to_csv('enrollment_totals_report.csv', index=False)

print("CSV files have been created with the requested data.")
