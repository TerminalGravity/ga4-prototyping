

gcloud api key = AIzaSyBOVtJ0KKSqPrtYx0221hd0WetU6iRHjew

export GOOGLE_APPLICATION_CREDENTIALS="/Users/jack/ADR Repositories/google-analytics-tag-mangager/credentials.json"

pip3 install virtualenv
virtualenv gcloud1
source gcloud1/bin/activate
gcloud1/bin/pip install google-api-python-client

pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

had to use: pip install google-analytics-data to resolve The error ModuleNotFoundError: No module named 'google.analytics.data_v1beta' indicates that the google-analytics-data library is not installed.