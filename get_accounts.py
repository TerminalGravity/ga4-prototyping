from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import os
from google.analytics.admin import AnalyticsAdminServiceClient
from google.analytics.admin_v1alpha.types import (
    ListPropertiesRequest, AccessDateRange, AccessDimension, AccessMetric, RunAccessReportRequest
)

# Path to your service account key file
SERVICE_ACCOUNT_FILE = '/Users/jack/ADR Repositories/google-analytics-tag-mangager/credentials.json'

# Define the required scopes
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

# Create a credentials object
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the Analytics Admin API service object
admin_service = build('analyticsadmin', 'v1beta', credentials=credentials)

# Retrieve list of accounts
try:
    accounts_response = admin_service.accounts().list().execute()
    print("Accounts response:", accounts_response)  # Debugging line
except Exception as e:
    print(f"Error retrieving accounts: {e}")
    accounts_response = {}

# Extract account information
account_data = []
if 'accounts' in accounts_response:
    for account in accounts_response['accounts']:
        account_id = account['name'].split('/')[-1]
        account_name = account['displayName']
        account_data.append({
            'account_id': account_id,
            'account_name': account_name
        })
else:
    print("No accounts found.")

# Convert account_data to DataFrame
df_accounts = pd.DataFrame(account_data)

# Print DataFrame to verify data
print(df_accounts)

# Save DataFrame to CSV
df_accounts.to_csv('google_analytics_accounts.csv', index=False)

print("CSV file 'google_analytics_accounts.csv' has been created with account IDs and names.")

# Function to list properties for a given account
def list_properties(account_id: str, transport: str = None):
    client = AnalyticsAdminServiceClient(transport=transport)
    results = client.list_properties(
        ListPropertiesRequest(filter=f"parent:accounts/{account_id}", show_deleted=True)
    )

    properties = []
    for property_ in results:
        properties.append({
            'property_id': property_.name.split('/')[-1],
            'property_name': property_.display_name
        })
    return properties

# Function to run access report for a given property
def run_access_report(property_id: str, transport: str = None):
    client = AnalyticsAdminServiceClient(transport=transport)
    request = RunAccessReportRequest(
        entity=f"properties/{property_id}",
        dimensions=[
            AccessDimension(dimension_name="userEmail"),
            AccessDimension(dimension_name="accessedPropertyId"),
            AccessDimension(dimension_name="reportType"),
            AccessDimension(dimension_name="revenueDataReturned"),
            AccessDimension(dimension_name="costDataReturned"),
            AccessDimension(dimension_name="userIP"),
            AccessDimension(dimension_name="mostRecentAccessEpochTimeMicros"),
        ],
        metrics=[AccessMetric(metric_name="accessCount")],
        date_ranges=[AccessDateRange(start_date="yesterday", end_date="today")],
    )
    return client.run_access_report(request)

# Retrieve properties for each account and save to CSV
all_properties = []
for account in account_data:
    account_id = account['account_id']
    properties = list_properties(account_id)
    for prop in properties:
        prop['account_id'] = account_id
        all_properties.append(prop)

df_properties = pd.DataFrame(all_properties)

# Print DataFrame to verify data
print(df_properties)

# Save DataFrame to CSV
df_properties.to_csv('google_analytics_properties.csv', index=False)

print("CSV file 'google_analytics_properties.csv' has been created with property IDs and names.")

# Generate access report for properties
access_report_data = []
for prop in all_properties:
    property_id = prop['property_id']
    access_report = run_access_report(property_id)
    for row in access_report.rows:
        access_report_data.append({
            'property_id': property_id,
            'property_name': prop['property_name'],
            'access_count': row.metric_values[0].value,
            'most_recent_access': row.dimension_values[6].value
        })

df_access_report = pd.DataFrame(access_report_data)

# Print DataFrame to verify data
print(df_access_report)

# Save DataFrame to CSV
df_access_report.to_csv('google_analytics_access_report.csv', index=False)

print("CSV file 'google_analytics_access_report.csv' has been created with property activity data.")