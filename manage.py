#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import boto3

s3 = boto3.client(
    's3',
    endpoint_url='https://5ef76ef2fdafa0e2960c1af220affe01.r2.cloudflarestorage.com',
    aws_access_key_id='557245eab7acd5383ee209f3c8cc1187',
    aws_secret_access_key='e8ba2bea3a6e44bdab96b47026e59cb0d92eeb6a80fa3bda90a46eebe935d2a1',
    region_name='auto'
)

# List buckets to verify connection
response = s3.list_buckets()
print(response)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
