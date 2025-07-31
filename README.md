<a href="https://www.mailersend.com"><img src="https://www.mailersend.com/images/logo.svg" width="200px"/></a>

MailerSend Python SDK

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

# Table of Contents
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
  - [Requirements](#requirements)
  - [Authentication](#authentication)
    - [Environment Variable (Recommended)](#environment-variable-recommended)
      - [Option 1: System Environment Variable](#option-1-system-environment-variable)
      - [Option 2: Using .env File](#option-2-using-env-file)
    - [Direct API Key](#direct-api-key)
- [SDK Architecture](#sdk-architecture)
  - [Builder Pattern](#builder-pattern)
  - [Resource Classes](#resource-classes)
  - [Request and Response Models](#request-and-response-models)
- [Response Data Access](#response-data-access)
  - [Multiple Access Patterns](#multiple-access-patterns)
    - [Dict-like Access](#dict-like-access)
    - [Attribute Access](#attribute-access)
    - [Safe Access with Defaults](#safe-access-with-defaults)
    - [Handling Method Name Conflicts](#handling-method-name-conflicts)
  - [Data Format Conversion](#data-format-conversion)
    - [Convert to Dictionary](#convert-to-dictionary)
    - [Convert to JSON](#convert-to-json)
    - [Extract Raw Data](#extract-raw-data)
  - [Headers and Metadata](#headers-and-metadata)
    - [Access Response Headers](#access-response-headers)
    - [Response Metadata](#response-metadata)
  - [Error Handling with Responses](#error-handling-with-responses)
    - [Check Response Status](#check-response-status)
    - [Access Error Information](#access-error-information)
    - [Working with Different Response Types](#working-with-different-response-types)
- [Logging](#logging)
  - [Enable Debug Logging](#enable-debug-logging)
  - [Custom Logging Configuration](#custom-logging-configuration)
- [Usage](#usage)
  - [Email](#email)
    - [Send an email](#send-an-email)
    - [Add CC, BCC recipients](#add-cc-bcc-recipients)
    - [Send a template-based email](#send-a-template-based-email)
    - [Personalization](#personalization)
    - [Send email with attachment](#send-email-with-attachment)
    - [Send bulk email](#send-bulk-email)
    - [Get bulk email status](#get-bulk-email-status)
  - [Activity](#activity)
    - [Get a list of activities](#get-a-list-of-activities)
    - [Get activity with filters](#get-activity-with-filters)
    - [Get a single activity](#get-a-single-activity)
  - [Analytics](#analytics)
    - [Activity data by date](#activity-data-by-date)
    - [Opens by country](#opens-by-country)
    - [Opens by user-agent name](#opens-by-user-agent-name)
    - [Opens by reading environment](#opens-by-reading-environment)
  - [Domains](#domains)
    - [Get a list of domains](#get-a-list-of-domains)
    - [Get a single domain](#get-a-single-domain)
    - [Add a domain](#add-a-domain)
    - [Delete a domain](#delete-a-domain)
    - [Get a list of recipients per domain](#get-a-list-of-recipients-per-domain)
    - [Update domain settings](#update-domain-settings)
    - [Get DNS Records](#get-dns-records)
    - [Verify a domain](#verify-a-domain)
  - [Sender Identities](#sender-identities)
    - [Get a list of sender identities](#get-a-list-of-sender-identities)
    - [Get a sender identity](#get-a-sender-identity)
    - [Create a sender identity](#create-a-sender-identity)
    - [Update a sender identity](#update-a-sender-identity)
    - [Delete a sender identity](#delete-a-sender-identity)
  - [Inbound Routes](#inbound-routes)
    - [Get a list of inbound routes](#get-a-list-of-inbound-routes)
    - [Get a single inbound route](#get-a-single-inbound-route)
    - [Add an inbound route](#add-an-inbound-route)
    - [Update an inbound route](#update-an-inbound-route)
    - [Delete an inbound route](#delete-an-inbound-route)
  - [Messages](#messages)
    - [Get a list of messages](#get-a-list-of-messages)
    - [Get a single message](#get-a-single-message)
  - [Scheduled messages](#scheduled-messages)
    - [Get a list of scheduled messages](#get-a-list-of-scheduled-messages)
    - [Get a single scheduled message](#get-a-single-scheduled-message)
    - [Delete a scheduled message](#delete-a-scheduled-message)
  - [Recipients](#recipients)
    - [Get a list of recipients](#get-a-list-of-recipients)
    - [Get a single recipient](#get-a-single-recipient)
    - [Delete a recipient](#delete-a-recipient)
    - [Get recipients from a blocklist](#get-recipients-from-a-blocklist)
    - [Get recipients from hard bounces](#get-recipients-from-hard-bounces)
    - [Get recipients from spam complaints](#get-recipients-from-spam-complaints)
    - [Get recipients from unsubscribes](#get-recipients-from-unsubscribes)
    - [Add recipients to blocklist](#add-recipients-to-blocklist)
    - [Add hard bounced recipients](#add-hard-bounced-recipients)
    - [Add spam complaints](#add-spam-complaints)
    - [Add recipients to unsubscribe list](#add-recipients-to-unsubscribe-list)
    - [Delete recipients from blocklist](#delete-recipients-from-blocklist)
    - [Delete hard bounced recipients](#delete-hard-bounced-recipients)
    - [Delete spam complaints](#delete-spam-complaints)
    - [Delete recipients from unsubscribe list](#delete-recipients-from-unsubscribe-list)
  - [Templates](#templates)
    - [Get a list of templates](#get-a-list-of-templates)
    - [Get a single template](#get-a-single-template)
    - [Delete template](#delete-template)
  - [Webhooks](#webhooks)
    - [Get a list of webhooks](#get-a-list-of-webhooks)
    - [Get a single webhook](#get-a-single-webhook)
    - [Create a Webhook](#create-a-webhook)
    - [Create a disabled webhook](#create-a-disabled-webhook)
    - [Update a Webhook](#update-a-webhook)
    - [Disable/Enable a Webhook](#disableenable-a-webhook)
    - [Delete a Webhook](#delete-a-webhook)
  - [Email Verification](#email-verification)
    - [Get all email verification lists](#get-all-email-verification-lists)
    - [Get a single email verification list](#get-a-single-email-verification-list)
    - [Create an email verification list](#create-an-email-verification-list)
    - [Verify a list](#verify-a-list)
    - [Get list results](#get-list-results)
  - [SMS](#sms)
    - [Sending SMS messages](#sending-sms-messages)
  - [SMS Activity](#sms-activity)
    - [Get a list of SMS activities](#get-a-list-of-sms-activities)
  - [Webhooks](#webhooks-1)
    - [Get a list of webhooks](#get-a-list-of-webhooks-1)
    - [Get a single webhook](#get-a-single-webhook-1)
    - [Create a Webhook](#create-a-webhook-1)
    - [Create a disabled webhook](#create-a-disabled-webhook-1)
    - [Update a Webhook](#update-a-webhook-1)
    - [Disable/Enable a Webhook](#disableenable-a-webhook-1)
    - [Delete a Webhook](#delete-a-webhook-1)
  - [Email Verification](#email-verification-1)
    - [Get all email verification lists](#get-all-email-verification-lists-1)
    - [Get a single email verification list](#get-a-single-email-verification-list-1)
    - [Create an email verification list](#create-an-email-verification-list-1)
    - [Verify a list](#verify-a-list-1)
    - [Get list results](#get-list-results-1)
  - [SMS](#sms-1)
    - [Sending SMS messages](#sending-sms-messages-1)
  - [SMS Activity](#sms-activity-1)
    - [Get a list of SMS activities](#get-a-list-of-sms-activities-1)
    - [Get activity of a single SMS message](#get-activity-of-a-single-sms-message)
  - [SMS Phone Numbers](#sms-phone-numbers)
    - [Get a list of SMS phone numbers](#get-a-list-of-sms-phone-numbers)
    - [Get an SMS phone number](#get-an-sms-phone-number)
    - [Update a single SMS phone number](#update-a-single-sms-phone-number)
    - [Delete an SMS phone number](#delete-an-sms-phone-number)
  - [SMS Recipients](#sms-recipients)
    - [Get a list of SMS recipients](#get-a-list-of-sms-recipients)
    - [Get an SMS recipient](#get-an-sms-recipient)
    - [Update a single SMS recipient](#update-a-single-sms-recipient)
  - [SMS Messages](#sms-messages)
    - [Get a list of SMS messages](#get-a-list-of-sms-messages)
    - [Get an SMS message](#get-an-sms-message)
  - [SMS Webhooks](#sms-webhooks)
    - [Get a list of SMS webhooks](#get-a-list-of-sms-webhooks)
    - [Get a single SMS webhook](#get-a-single-sms-webhook)
    - [Create an SMS webhook](#create-an-sms-webhook)
    - [Update a single SMS webhook](#update-a-single-sms-webhook)
    - [Delete an SMS webhook](#delete-an-sms-webhook)
  - [SMS Inbound Routing](#sms-inbound-routing)
    - [Get a list of SMS inbound routes](#get-a-list-of-sms-inbound-routes)
    - [Get a single SMS inbound route](#get-a-single-sms-inbound-route)
    - [Create an SMS inbound route](#create-an-sms-inbound-route)
    - [Update an SMS inbound route](#update-an-sms-inbound-route)
    - [Delete an SMS inbound route](#delete-an-sms-inbound-route)
  - [Tokens](#tokens)
    - [Create a token](#create-a-token)
    - [Pause / Unpause Token](#pause--unpause-token)
    - [Delete a Token](#delete-a-token)
  - [Other Endpoints](#other-endpoints)
    - [Get API Quota](#get-api-quota)
- [Error Handling](#error-handling)
- [Testing](#testing)
  - [Running Unit Tests](#running-unit-tests)
  - [Testing with VCR](#testing-with-vcr)
- [Available endpoints](#available-endpoints)
- [Support and Feedback](#support-and-feedback)
- [License](#license)

<a name="installation"></a>

# Installation

```bash
pip install mailersend
```

## Requirements

- Python 3.7+
- An API Key from [mailersend.com](https://www.mailersend.com)

## Authentication

The SDK supports multiple authentication methods:

### Environment Variable (Recommended)

#### Option 1: System Environment Variable

Set your API key as a system environment variable:

```bash
export MAILERSEND_API_KEY="your-api-key"
```

Then initialize the client:

```python
from mailersend import MailerSendClient

# Automatically uses MAILERSEND_API_KEY environment variable
ms = MailerSendClient()
```

#### Option 2: Using .env File

For development, you can use a `.env` file. First install `python-dotenv`:

```bash
pip install python-dotenv
```

Create a `.env` file in your project root:

```bash
# .env
MAILERSEND_API_KEY=your-api-key
```

Then load it in your Python code:

```python
from mailersend import MailerSendClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Client automatically uses the loaded MAILERSEND_API_KEY
ms = MailerSendClient()
```

### Direct API Key

```python
from mailersend import MailerSendClient

ms = MailerSendClient(api_key="your-api-key")
```

<a name="sdk-architecture"></a>

# SDK Architecture

The MailerSend Python SDK v2 introduces a modern, clean architecture that follows industry best practices:

## Builder Pattern

The SDK uses the builder pattern for constructing API requests. This provides a fluent, readable interface for setting parameters:

```python
from mailersend import MailerSendClient
from mailersend import SmsRecipientsBuilder

ms = MailerSendClient()

# Build a request using the fluent builder pattern
request = (SmsRecipientsBuilder()
          .sms_number_id("sms123")
          .status("active")
          .page(1)
          .limit(25)
          .build_list_request())

# Execute the request
response = ms.sms_recipients.list_sms_recipients(request)
```

## Resource Classes

Each API endpoint group has its own resource class that provides clean method interfaces:

```python
# Access different API resources
ms.sms_recipients    # SMS Recipients operations
ms.sms_webhooks      # SMS Webhooks operations  
ms.sms_inbounds      # SMS Inbound Routing operations
ms.email             # Email operations
ms.domains           # Domain operations
# ... and more
```

## Request and Response Models

All data is validated using Pydantic models ensuring type safety and data integrity:

```python
# All responses are strongly typed
response = ms.sms_recipients.get_sms_recipient(request)
print(response.id)           # Validated string
print(response.number)       # Validated phone number
print(response.created_at)   # Validated datetime object
```

<a name="response-data-access"></a>

# Response Data Access

The MailerSend SDK provides flexible ways to access and work with API response data. All API calls return a unified `APIResponse` object that supports multiple access patterns and data formats.

## Multiple Access Patterns

### Dict-like Access
Access response data using dictionary-style syntax:

```python
from mailersend import MailerSendClient
from mailersend import SmsRecipientsBuilder

ms = MailerSendClient()
request = SmsRecipientsBuilder().sms_recipient_id("recipient-123").build_get_request()
response = ms.sms_recipients.get_sms_recipient(request)

# Dict-style access
recipient_id = response["data"]["id"]
phone_number = response["data"]["number"]
status = response["data"]["status"]

# Nested access
if "sms" in response["data"]:
    latest_sms = response["data"]["sms"][0]["text"]

# Check if key exists
if "error" in response:
    error_message = response['error']
```

### Attribute Access
Access data using dot notation for cleaner code:

```python
# Attribute-style access (most convenient)
recipient_id = response.id
phone_number = response.number
status = response.status

# Nested attribute access for complex data
if hasattr(response, 'sms') and response.sms:
    latest_sms = response.sms[0].text
```

### Safe Access with Defaults
Use the `get()` method for safe access with fallback values:

```python
# Safe access with defaults
recipient_id = response.get("data", {}).get("id", "unknown")
error_message = response.get("error", "No error")

# Safe nested access
meta_info = response.get("meta", {})
total_count = meta_info.get("total", 0)
current_page = meta_info.get("page", 1)
```

### Handling Method Name Conflicts
When response data contains fields that conflict with built-in methods, use the `data_` prefix:

```python
# If response contains fields like 'items', 'keys', 'values', etc.
response_data = {
    "items": [{"id": 1, "name": "Item 1"}],
    "keys": ["key1", "key2"],
    "values": [100, 200]
}

# Use dict access (recommended for conflicts)
items_list = response["items"]
key_list = response["keys"]

# Or use data_ prefix for attribute access
items_list = response.data_items
key_list = response.data_keys
value_list = response.data_values
```

## Data Format Conversion

### Convert to Dictionary
Get the complete response as a dictionary:

```python
# Convert entire response to dict
response_dict = response.to_dict()
# Returns:
# {
#     "data": {"id": "123", "number": "+1234567890", ...},
#     "headers": {"x-request-id": "req-456", ...},
#     "status_code": 200,
#     "request_id": "req-456",
#     "rate_limit_remaining": 1000,
#     "success": True
# }

# Or use dict() constructor
response_dict = dict(response)

# Access specific parts
data_only = response_dict["data"]
headers_only = response_dict["headers"]
```

### Convert to JSON
Get JSON string representation with various formatting options:

```python
# Compact JSON
json_string = response.to_json()

# Pretty-printed JSON with indentation
pretty_json = response.to_json(indent=2)

# Custom JSON options
unicode_json = response.to_json(ensure_ascii=False, indent=4)

# Direct json.dumps() also works
import json
json_string = json.dumps(response)
```

### Extract Raw Data
Access just the API response data without metadata:

```python
# Get raw response data
raw_data = response.data

# For paginated responses
if isinstance(raw_data, dict) and "data" in raw_data:
    items = raw_data["data"]        # List of items
    meta = raw_data.get("meta", {}) # Pagination info
    links = raw_data.get("links", {}) # Pagination links
else:
    # Single item response
    item_data = raw_data
```

## Headers and Metadata

### Access Response Headers
Headers can be accessed in multiple ways with automatic case handling:

```python
# Dictionary-style access (case-sensitive)
request_id = response.headers["x-request-id"]
content_type = response.headers["content-type"]

# Attribute-style access (dashes become underscores)
request_id = response.headers.x_request_id
content_type = response.headers.content_type
rate_limit = response.headers.x_rate_limit_remaining

# Nested dictionary access
request_id = response["headers"]["x-request-id"]

# Safe access with defaults
retry_after = response.headers.get("retry-after", "0")
```

### Response Metadata
Access useful metadata about the API response:

```python
# HTTP status information
status_code = response.status_code
is_successful = response.success  # True for 2xx status codes

# Rate limiting information
remaining_requests = response.rate_limit_remaining
retry_delay = response.retry_after  # Seconds to wait before retry

# Request tracking
request_id = response.request_id

# Pagination (for list responses)
if "meta" in response.data:
    total_items = response.data["meta"]["total"]
    current_page = response.data["meta"]["current_page"]
    per_page = response.data["meta"]["per_page"]
```

## Error Handling with Responses

### Check Response Status
Always check if the response was successful:

```python
from mailersend import MailerSendClient, EmailBuilder

ms = MailerSendClient()

try:
    email = EmailBuilder().from_email("sender@domain.com").build()
    response = ms.emails.send(email)
    
    if response.success:
        email_id = response.id
        remaining_quota = response.rate_limit_remaining
    else:
        status_code = response.status_code
        error_details = response.data
        
        # Handle rate limiting
        if response.status_code == 429 and response.retry_after:
            retry_seconds = response.retry_after
            
except Exception as e:
    # Handle exception
```

### Access Error Information
When requests fail, error details are available in the response:

```python
if not response.success:
    error_data = response.data
    
    # API error response structure
    error_message = error_data.get("message", "Unknown error")
    error_code = error_data.get("code")
    
    # Validation errors (422 responses)
    if "errors" in error_data:
        for field, messages in error_data["errors"].items():
            validation_errors = {field: messages}
```

### Working with Different Response Types

```python
# Single item responses (get operations)
user_response = ms.users.get_user(request)
if user_response.success:
    user_name = user_response.name
    user_email = user_response.email

# List responses (paginated)
users_response = ms.users.list_users(request)
if users_response.success:
    users = users_response.data["data"]  # Array of users
    total_count = users_response.data["meta"]["total"]
    
    for user in users:
        user_name = user['name']
        user_email = user['email']

# Empty responses (delete operations)
delete_response = ms.users.delete_user(request)
if delete_response.success:
    # delete_response.data is typically empty or contains confirmation
    deletion_confirmed = True
```

<a name="logging"></a>

# Logging

The SDK includes comprehensive logging to help with debugging and monitoring:

## Enable Debug Logging

```python
import logging
from mailersend import MailerSendClient

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

ms = MailerSendClient()

# All API calls will now be logged with detailed information
```

## Custom Logging Configuration

```python
import logging
from mailersend import MailerSendClient

# Configure logging with custom format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mailersend.log'),
        logging.StreamHandler()
    ]
)

ms = MailerSendClient()

# Logs will include:
# - API request details
# - Response status codes
# - Parameter information
# - Error details
```

<a name="usage"></a>

# Usage

## Email

### Send an email

```python
from mailersend import MailerSendClient, EmailBuilder

ms = MailerSendClient()

email = (EmailBuilder()
         .from_email("sender@domain.com", "Your Name")
         .to_many([{"email": "recipient@domain.com", "name": "Recipient"}])
         .subject("Hello from MailerSend!")
         .html("<h1>Hello World!</h1>")
         .text("Hello World!")
         .build())

response = ms.emails.send(email)
print(f"Email sent: {response.message_id}")
```

### Add CC, BCC recipients

```python
from mailersend import MailerSendClient, EmailBuilder

ms = MailerSendClient()

email = (EmailBuilder()
         .from_email("sender@domain.com", "Your Name")
         .to_many([{"email": "recipient@domain.com", "name": "Recipient"}])
         .cc("cc@domain.com", "CC Recipient")
         .bcc("bcc@domain.com", "BCC Recipient")
         .subject("Hello with CC/BCC!")
         .html("<h1>Hello World!</h1>")
         .build())

response = ms.emails.send(email)
```

### Send a template-based email

```python
from mailersend import MailerSendClient, EmailBuilder

ms = MailerSendClient()

email = (EmailBuilder()
         .from_email("sender@domain.com", "Your Name")
         .to_many([{"email": "recipient@domain.com", "name": "Recipient"}])
         .template("template-id")
         .personalize_many([{
             "email": "recipient@domain.com",
             "data": {
                 "name": "John",
                 "company": "MailerSend"
             }
         }])
         .build())

response = ms.emails.send(email)
```

### Personalization

```python
from mailersend import MailerSendClient, EmailBuilder

ms = MailerSendClient()

email = (EmailBuilder()
         .from_email("sender@domain.com", "Your Name")
         .to_many([{"email": "recipient@domain.com", "name": "Recipient"}])
         .subject("Hello {$name}!")
         .html("<h1>Hello {$name} from {$company}!</h1>")
         .personalize_many([{
             "email": "recipient@domain.com",
             "data": {
                 "name": "John",
                 "company": "MailerSend",
                 "items": ["item1", "item2"],
                 "total": 99.99
             }
         }])
         .build())

response = ms.emails.send(email)
```

### Send email with attachment

```python
from mailersend import MailerSendClient, EmailBuilder

ms = MailerSendClient()

email = (EmailBuilder()
         .from_email("sender@domain.com", "Your Name")
         .to_many([{"email": "recipient@domain.com", "name": "Recipient"}])
         .subject("Email with attachment")
         .html("<h1>Please find attached document</h1>")
         .attach_file("document.pdf")
         .build())

response = ms.emails.send(email)
```

### Send bulk email

```python
from mailersend import MailerSendClient, EmailBuilder

ms = MailerSendClient()

# Create individual EmailRequest objects
emails = [
    EmailBuilder()
        .from_email("sender@domain.com", "Sender")
        .to_many([{"email": "recipient1@domain.com", "name": "Recipient 1"}])
        .subject("Bulk email 1")
        .html("<h1>Hello from bulk email 1</h1>")
        .text("Hello from bulk email 1")
        .build(),
    EmailBuilder()
        .from_email("sender@domain.com", "Sender")
        .to_many([{"email": "recipient2@domain.com", "name": "Recipient 2"}])
        .subject("Bulk email 2")
        .html("<h1>Hello from bulk email 2</h1>")
        .text("Hello from bulk email 2")
        .build()
]

response = ms.emails.send_bulk(emails)
print(f"Bulk email ID: {response.bulk_email_id}")
```

### Get bulk email status

```python
from mailersend import MailerSendClient

ms = MailerSendClient()

response = ms.emails.get_bulk_status("bulk-email-id")
print(f"Status: {response.state}")
```

## Activity

### Get a list of activities

```python
from mailersend import MailerSendClient, ActivityBuilder
from datetime import datetime, timedelta

ms = MailerSendClient()

# Get activities from last 7 days (maximum allowed timeframe)
date_from = int((datetime.now() - timedelta(days=7)).timestamp())
date_to = int(datetime.now().timestamp())

request = (ActivityBuilder()
          .domain_id("domain-id")
          .date_from(date_from)
          .date_to(date_to)
          .page(1)
          .limit(25)
          .build_list_request())

response = ms.activities.get(request)
```

### Get activity with filters

```python
from mailersend import MailerSendClient, ActivityBuilder
from datetime import datetime, timedelta

ms = MailerSendClient()

# Get activities from last 7 days
date_from = int((datetime.now() - timedelta(days=7)).timestamp())
date_to = int(datetime.now().timestamp())

request = (ActivityBuilder()
          .domain_id("domain-id")
          .date_from(date_from)
          .date_to(date_to)
          .events(["sent", "delivered", "opened"])
          .page(1)
          .limit(50)
          .build_list_request())

response = ms.activities.get(request)
```

### Get a single activity

```python
from mailersend import MailerSendClient, SingleActivityBuilder

ms = MailerSendClient()

request = (SingleActivityBuilder()
          .activity_id("activity-id")
          .build_get_request())

response = ms.activities.get_single(request)
```

## Analytics

### Activity data by date

```python
from mailersend import MailerSendClient, AnalyticsBuilder
from datetime import datetime, timedelta

ms = MailerSendClient()

date_from = int((datetime.now() - timedelta(days=30)).timestamp())
date_to = int(datetime.now().timestamp())

request = (AnalyticsBuilder()
          .date_from(date_from)
          .date_to(date_to)
          .events("sent", "delivered", "opened")
          .domain_id("domain-id")
          .group_by("days")
          .build())

response = ms.analytics.get_activity_by_date(request)
for stat in response.data:
    print(f"Date: {stat.date}, Sent: {stat.sent}, Delivered: {stat.delivered}")
```

### Opens by country

```python
from mailersend import MailerSendClient, AnalyticsBuilder

ms = MailerSendClient()

request = (AnalyticsBuilder()
          .date_from(date_from)
          .date_to(date_to)
          .domain_id("domain-id")
          .build())

response = ms.analytics.get_opens_by_country(request)
```

### Opens by user-agent name

```python
from mailersend import MailerSendClient, AnalyticsBuilder

ms = MailerSendClient()

request = (AnalyticsBuilder()
          .date_from(date_from)
          .date_to(date_to)
          .domain_id("domain-id")
          .build())

response = ms.analytics.get_opens_by_user_agent(request)
```

### Opens by reading environment

```python
from mailersend import MailerSendClient, AnalyticsBuilder

ms = MailerSendClient()

request = (AnalyticsBuilder()
          .date_from(date_from)
          .date_to(date_to)
          .domain_id("domain-id")
          .build())

response = ms.analytics.get_opens_by_reading_environment(request)
```

## Domains

### Get a list of domains

```python
from mailersend import MailerSendClient
from mailersend import DomainsBuilder

ms = MailerSendClient()

request = (DomainsBuilder()
          .verified(True)
          .page(1)
          .limit(25)
          .build_list_request())

response = ms.domains.list_domains(request)
for domain in response.data:
    print(f"Domain: {domain.name}, Verified: {domain.domain_settings.is_verified}")
```

### Get a single domain

```python
from mailersend import MailerSendClient
from mailersend import DomainsBuilder

ms = MailerSendClient()

request = (DomainsBuilder()
          .domain_id("domain-id")
          .build_get_request())

response = ms.domains.get_domain(request)
print(f"Domain: {response.name}")
```

### Add a domain

```python
from mailersend import MailerSendClient
from mailersend import DomainsBuilder

ms = MailerSendClient()

request = (DomainsBuilder()
          .name("mydomain.com")
          .return_path_subdomain("rp")
          .custom_tracking_subdomain("ct")
          .inbound_routing_subdomain("ir")
          .build_create_request())

response = ms.domains.create_domain(request)
print(f"Created domain with ID: {response.id}")
```

### Delete a domain

```python
from mailersend import MailerSendClient
from mailersend import DomainsBuilder

ms = MailerSendClient()

request = (DomainsBuilder()
          .domain_id("domain-id")
          .build_delete_request())

response = ms.domains.delete_domain(request)
print("Domain deleted successfully")
```

### Get a list of recipients per domain

```python
from mailersend import MailerSendClient
from mailersend import DomainsBuilder

ms = MailerSendClient()

request = (DomainsBuilder()
          .domain_id("domain-id")
          .page(1)
          .limit(25)
          .build_recipients_request())

response = ms.domains.get_domain_recipients(request)
for recipient in response.data:
    print(f"Recipient: {recipient.email}")
```

### Update domain settings

```python
from mailersend import MailerSendClient
from mailersend import DomainsBuilder

ms = MailerSendClient()

request = (DomainsBuilder()
          .domain_id("domain-id")
          .send_paused(False)
          .track_clicks(True)
          .track_opens(True)
          .track_unsubscribe(True)
          .track_content(True)
          .custom_tracking_enabled(True)
          .custom_tracking_subdomain("email")
          .precedence_bulk(False)
          .build_settings_request())

response = ms.domains.update_domain_settings(request)
print("Domain settings updated")
```

### Get DNS Records

```python
from mailersend import MailerSendClient
from mailersend import DomainsBuilder

ms = MailerSendClient()

request = (DomainsBuilder()
          .domain_id("domain-id")
          .build_dns_request())

response = ms.domains.get_dns_records(request)
for record in response.data:
    print(f"Type: {record.type}, Name: {record.name}, Value: {record.value}")
```

### Verify a domain

```python
from mailersend import MailerSendClient
from mailersend import DomainsBuilder

ms = MailerSendClient()

request = (DomainsBuilder()
          .domain_id("domain-id")
          .build_verify_request())

response = ms.domains.verify_domain(request)
print(f"Verification status: {response.domain_settings.is_verified}")
```

## Sender Identities

### Get a list of sender identities

```python
from mailersend import MailerSendClient
from mailersend import IdentityBuilder

ms = MailerSendClient()

request = (IdentityBuilder()
          .domain_id("domain-id")
          .page(1)
          .limit(25)
          .build_list_request())

response = ms.identities.list_identities(request)
for identity in response.data:
    print(f"Identity: {identity.email}, Name: {identity.name}")
```

### Get a sender identity

```python
from mailersend import MailerSendClient
from mailersend import IdentityBuilder

ms = MailerSendClient()

request = (IdentityBuilder()
          .identity_id("identity-id")
          .build_get_request())

response = ms.identities.get_identity(request)
print(f"Identity: {response.email}")
```

### Create a sender identity

```python
from mailersend import MailerSendClient
from mailersend import IdentityBuilder

ms = MailerSendClient()

request = (IdentityBuilder()
          .domain_id("domain-id")
          .name("John Doe")
          .email("john@yourdomain.com")
          .reply_to_email("support@yourdomain.com")
          .reply_to_name("Support Team")
          .add_note("Marketing campaigns")
          .build_create_request())

response = ms.identities.create_identity(request)
print(f"Created identity with ID: {response.id}")
```

### Update a sender identity

```python
from mailersend import MailerSendClient
from mailersend import IdentityBuilder

ms = MailerSendClient()

request = (IdentityBuilder()
          .identity_id("identity-id")
          .name("Jane Doe")
          .reply_to_email("support@yourdomain.com")
          .reply_to_name("Support Team")
          .add_note("Updated for new campaign")
          .build_update_request())

response = ms.identities.update_identity(request)
print("Identity updated successfully")
```

### Delete a sender identity

```python
from mailersend import MailerSendClient
from mailersend import IdentityBuilder

ms = MailerSendClient()

request = (IdentityBuilder()
          .identity_id("identity-id")
          .build_delete_request())

response = ms.identities.delete_identity(request)
print("Identity deleted successfully")
```

## Inbound Routes

### Get a list of inbound routes

```python
from mailersend import MailerSendClient
from mailersend import InboundBuilder

ms = MailerSendClient()

request = (InboundBuilder()
          .domain_id("domain-id")
          .page(1)
          .limit(25)
          .build_list_request())

response = ms.inbound.list_inbound_routes(request)
for route in response.data:
    print(f"Route: {route.name}, Domain: {route.domain}")
```

### Get a single inbound route

```python
from mailersend import MailerSendClient
from mailersend import InboundBuilder

ms = MailerSendClient()

request = (InboundBuilder()
          .inbound_id("inbound-id")
          .build_get_request())

response = ms.inbound.get_inbound_route(request)
print(f"Route name: {response.name}")
```

### Add an inbound route

```python
from mailersend import MailerSendClient
from mailersend import InboundBuilder
from mailersend.models.inbound import FilterType, ForwardType

ms = MailerSendClient()

request = (InboundBuilder()
          .domain_id("domain-id")
          .name("My Inbound Route")
          .enabled(True)
          .catch_filter(FilterType.CATCH_RECIPIENT, "equal", "support")
          .forward(ForwardType.WEBHOOK, "https://example.com/webhook")
          .build_create_request())

response = ms.inbound.create_inbound_route(request)
print(f"Created route with ID: {response.id}")
```

### Update an inbound route

```python
from mailersend import MailerSendClient
from mailersend import InboundBuilder

ms = MailerSendClient()

request = (InboundBuilder()
          .inbound_id("inbound-id")
          .name("Updated Route Name")
          .enabled(False)
          .build_update_request())

response = ms.inbound.update_inbound_route(request)
print(f"Updated route: {response.name}")
```

### Delete an inbound route

```python
from mailersend import MailerSendClient
from mailersend import InboundBuilder

ms = MailerSendClient()

request = (InboundBuilder()
          .inbound_id("inbound-id")
          .build_delete_request())

response = ms.inbound.delete_inbound_route(request)
print("Inbound route deleted successfully")
```

## Messages

### Get a list of messages

```python
from mailersend import MailerSendClient
from mailersend import MessagesBuilder

ms = MailerSendClient()

request = (MessagesBuilder()
          .page(1)
          .limit(25)
          .build_list_request())

response = ms.messages.list_messages(request)
for message in response.data:
    print(f"Message ID: {message.id}, Subject: {message.subject}")
```

### Get a single message

```python
from mailersend import MailerSendClient
from mailersend import MessagesBuilder

ms = MailerSendClient()

request = (MessagesBuilder()
          .message_id("message-id")
          .build_get_request())

response = ms.messages.get_message(request)
print(f"Message: {response.subject}")
```

## Scheduled messages

### Get a list of scheduled messages

```python
from mailersend import MailerSendClient
from mailersend import SchedulesBuilder

ms = MailerSendClient()

request = (SchedulesBuilder()
          .domain_id("domain-id")
          .page(1)
          .limit(25)
          .build_list_request())

response = ms.schedules.list_scheduled_messages(request)
for scheduled in response.data:
    print(f"Message: {scheduled.subject}, Send at: {scheduled.send_at}")
```

### Get a single scheduled message

```python
from mailersend import MailerSendClient
from mailersend import SchedulesBuilder

ms = MailerSendClient()

request = (SchedulesBuilder()
          .scheduled_message_id("scheduled-id")
          .build_get_request())

response = ms.schedules.get_scheduled_message(request)
print(f"Scheduled message: {response.subject}")
```

### Delete a scheduled message

```python
from mailersend import MailerSendClient
from mailersend import SchedulesBuilder

ms = MailerSendClient()

request = (SchedulesBuilder()
          .scheduled_message_id("scheduled-id")
          .build_delete_request())

response = ms.schedules.delete_scheduled_message(request)
print("Scheduled message deleted")
```

## Recipients

### Get a list of recipients

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

request = (RecipientsBuilder()
          .domain_id("domain-id")
          .page(1)
          .limit(25)
          .build_list_request())

response = ms.recipients.list_recipients(request)
for recipient in response.data:
    print(f"Recipient: {recipient.email}")
```

### Get a single recipient

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

request = (RecipientsBuilder()
          .recipient_id("recipient-id")
          .build_get_request())

response = ms.recipients.get_recipient(request)
print(f"Recipient: {response.email}")
```

### Delete a recipient

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

request = (RecipientsBuilder()
          .recipient_id("recipient-id")
          .build_delete_request())

response = ms.recipients.delete_recipient(request)
print("Recipient deleted")
```

### Get recipients from a blocklist

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

request = (RecipientsBuilder()
          .domain_id("domain-id")
          .page(1)
          .limit(25)
          .build_blocklist_request())

response = ms.recipients.get_blocklist(request)
for blocked in response.data:
    print(f"Blocked: {blocked.pattern}")
```

### Get recipients from hard bounces

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

request = (RecipientsBuilder()
          .domain_id("domain-id")
          .build_hard_bounces_request())

response = ms.recipients.get_hard_bounces(request)
for bounce in response.data:
    print(f"Hard bounce: {bounce.recipient}")
```

### Get recipients from spam complaints

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

request = (RecipientsBuilder()
          .domain_id("domain-id")
          .build_spam_complaints_request())

response = ms.recipients.get_spam_complaints(request)
for spam in response.data:
    print(f"Spam complaint: {spam.recipient}")
```

### Get recipients from unsubscribes

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

request = (RecipientsBuilder()
          .domain_id("domain-id")
          .build_unsubscribes_request())

response = ms.recipients.get_unsubscribes(request)
for unsub in response.data:
    print(f"Unsubscribed: {unsub.recipient}")
```

### Add recipients to blocklist

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

# Using specific emails
request = (RecipientsBuilder()
          .domain_id("domain-id")
          .recipients(["blocked@example.com", "spam@example.com"])
          .build_add_blocklist_request())

response = ms.recipients.add_to_blocklist(request)

# Using patterns
request = (RecipientsBuilder()
          .domain_id("domain-id")
          .patterns(["*@spammer.com", "*@blocked-domain.com"])
          .build_add_blocklist_request())

response = ms.recipients.add_to_blocklist(request)
```

### Add hard bounced recipients

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

request = (RecipientsBuilder()
          .domain_id("domain-id")
          .recipients(["bounced@example.com"])
          .build_add_hard_bounces_request())

response = ms.recipients.add_hard_bounces(request)
```

### Add spam complaints

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

request = (RecipientsBuilder()
          .domain_id("domain-id")
          .recipients(["complainer@example.com"])
          .build_add_spam_complaints_request())

response = ms.recipients.add_spam_complaints(request)
```

### Add recipients to unsubscribe list

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

request = (RecipientsBuilder()
          .domain_id("domain-id")
          .recipients(["unsubscribed@example.com"])
          .build_add_unsubscribes_request())

response = ms.recipients.add_unsubscribes(request)
```

### Delete recipients from blocklist

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

request = (RecipientsBuilder()
          .domain_id("domain-id")
          .recipients(["unblocked@example.com"])
          .build_delete_blocklist_request())

response = ms.recipients.delete_from_blocklist(request)
```

### Delete hard bounced recipients

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

request = (RecipientsBuilder()
          .domain_id("domain-id")
          .recipients(["recovered@example.com"])
          .build_delete_hard_bounces_request())

response = ms.recipients.delete_hard_bounces(request)
```

### Delete spam complaints

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

request = (RecipientsBuilder()
          .domain_id("domain-id")
          .recipients(["resolved@example.com"])
          .build_delete_spam_complaints_request())

response = ms.recipients.delete_spam_complaints(request)
```

### Delete recipients from unsubscribe list

```python
from mailersend import MailerSendClient
from mailersend import RecipientsBuilder

ms = MailerSendClient()

request = (RecipientsBuilder()
          .domain_id("domain-id")
          .recipients(["resubscribed@example.com"])
          .build_delete_unsubscribes_request())

response = ms.recipients.delete_unsubscribes(request)
```

## Templates

### Get a list of templates

```python
from mailersend import MailerSendClient
from mailersend import TemplatesBuilder

ms = MailerSendClient()

request = (TemplatesBuilder()
          .domain_id("domain-id")
          .page(1)
          .limit(25)
          .build_list_request())

response = ms.templates.list_templates(request)
for template in response.data:
    print(f"Template: {template.name} (ID: {template.id})")
```

### Get a single template

```python
from mailersend import MailerSendClient
from mailersend import TemplatesBuilder

ms = MailerSendClient()

request = (TemplatesBuilder()
          .template("template-id")
          .build_get_request())

response = ms.templates.get_template(request)
print(f"Template: {response.name}")
```

### Delete template

```python
from mailersend import MailerSendClient
from mailersend import TemplatesBuilder

ms = MailerSendClient()

request = (TemplatesBuilder()
          .template("template-id")
          .build_delete_request())

response = ms.templates.delete_template(request)
print("Template deleted")
```

## Webhooks

### Get a list of webhooks

```python
from mailersend import MailerSendClient
from mailersend import WebhooksBuilder

ms = MailerSendClient()

request = (WebhooksBuilder()
          .domain_id("domain-id")
          .limit(25)
          .build_list_request())

response = ms.webhooks.list_webhooks(request)
for webhook in response.data:
    print(f"Webhook: {webhook.name} - {webhook.url}")
```

### Get a single webhook

```python
from mailersend import MailerSendClient
from mailersend import WebhooksBuilder

ms = MailerSendClient()

request = (WebhooksBuilder()
          .webhook_id("webhook-id")
          .build_webhook_get_request())

response = ms.webhooks.get_webhook(request)
print(f"Webhook: {response.name}")
```

### Create a Webhook

```python
from mailersend import MailerSendClient
from mailersend import WebhooksBuilder

ms = MailerSendClient()

request = (WebhooksBuilder()
          .domain_id("domain-id")
          .url("https://yourdomain.com/webhook")
          .name("My webhook")
          .events(["activity.sent", "activity.delivered"])
          .enabled(True)
          .build_webhook_create_request())

response = ms.webhooks.create_webhook(request)
print(f"Created webhook with ID: {response.id}")
```

### Create a disabled webhook

```python
from mailersend import MailerSendClient
from mailersend import WebhooksBuilder

ms = MailerSendClient()

request = (WebhooksBuilder()
          .domain_id("domain-id")
          .url("https://yourdomain.com/webhook")
          .name("My disabled webhook")
          .events(["activity.sent", "activity.delivered"])
          .enabled(False)
          .build_webhook_create_request())

response = ms.webhooks.create_webhook(request)
print(f"Created disabled webhook with ID: {response.id}")
```

### Update a Webhook

```python
from mailersend import MailerSendClient
from mailersend import WebhooksBuilder

ms = MailerSendClient()

request = (WebhooksBuilder()
          .webhook_id("webhook-id")
          .url("https://yourdomain.com/webhook-updated")
          .name("My updated webhook")
          .events(["activity.sent"])
          .enabled(True)
          .build_webhook_update_request())

response = ms.webhooks.update_webhook(request)
print("Webhook updated")
```

### Disable/Enable a Webhook

```python
from mailersend import MailerSendClient
from mailersend import WebhooksBuilder

ms = MailerSendClient()

# Disable webhook
request = (WebhooksBuilder()
          .webhook_id("webhook-id")
          .enabled(False)
          .build_webhook_update_request())

response = ms.webhooks.update_webhook(request)
print("Webhook disabled")

# Enable webhook
request = (WebhooksBuilder()
          .webhook_id("webhook-id")
          .enabled(True)
          .build_webhook_update_request())

response = ms.webhooks.update_webhook(request)
print("Webhook enabled")
```

### Delete a Webhook

```python
from mailersend import MailerSendClient
from mailersend import WebhooksBuilder

ms = MailerSendClient()

request = (WebhooksBuilder()
          .webhook_id("webhook-id")
          .build_webhook_delete_request())

response = ms.webhooks.delete_webhook(request)
print("Webhook deleted")
```

## Email Verification

### Get all email verification lists

```python
from mailersend import MailerSendClient, EmailVerificationBuilder

ms = MailerSendClient()

request = EmailVerificationBuilder().build_list_request()
response = ms.email_verification.list_verification_lists(request)

for verification_list in response.data:
    print(f"List: {verification_list.name}, Status: {verification_list.status}")
```

### Get a single email verification list

```python
from mailersend import MailerSendClient, EmailVerificationBuilder

ms = MailerSendClient()

request = (EmailVerificationBuilder()
          .verification_list_id("list-id")
          .build_get_request())

response = ms.email_verification.get_verification_list(request)
print(f"List name: {response.name}")
```

### Create an email verification list

```python
from mailersend import MailerSendClient, EmailVerificationBuilder

ms = MailerSendClient()

request = (EmailVerificationBuilder()
          .name("My Verification List")
          .emails(["test1@example.com", "test2@example.com"])
          .build_create_request())

response = ms.email_verification.create_verification_list(request)
print(f"Created list with ID: {response.id}")
```

### Verify a list

```python
from mailersend import MailerSendClient, EmailVerificationBuilder

ms = MailerSendClient()

request = (EmailVerificationBuilder()
          .verification_list_id("list-id")
          .build_verify_request())

response = ms.email_verification.verify_list(request)
print(f"Verification started: {response.message}")
```

### Get list results

```python
from mailersend import MailerSendClient, EmailVerificationBuilder

ms = MailerSendClient()

request = (EmailVerificationBuilder()
          .verification_list_id("list-id")
          .build_results_request())

response = ms.email_verification.get_verification_results(request)
for result in response.data:
    print(f"Email: {result.email}, Status: {result.status}")
```

## SMS

### Sending SMS messages

```python
from mailersend import MailerSendClient
from mailersend import SmsSendingBuilder

ms = MailerSendClient()

request = (SmsSendingBuilder()
          .from_number("sms-number-id")
          .to("+1234567890")
          .text("Hello from MailerSend!")
          .build())

response = ms.sms.send(request)
print(f"SMS sent with ID: {response.id}")
```

## SMS Activity

### Get a list of SMS activities

```python
from mailersend import MailerSendClient
from mailersend import TemplatesBuilder

ms = MailerSendClient()

request = (TemplatesBuilder()
          .template("template-id")
          .build_delete_request())

response = ms.templates.delete_template(request)
print("Template deleted")
```

## Webhooks

### Get a list of webhooks

```python
from mailersend import MailerSendClient
from mailersend import WebhooksBuilder

ms = MailerSendClient()

request = (WebhooksBuilder()
          .domain_id("domain-id")
          .build_webhooks_list_request())

response = ms.webhooks.list_webhooks(request)
for webhook in response.data:
    print(f"Webhook: {webhook.name} - {webhook.url}")
```

### Get a single webhook

```python
from mailersend import MailerSendClient
from mailersend import WebhooksBuilder

ms = MailerSendClient()

request = (WebhooksBuilder()
          .webhook_id("webhook-id")
          .build_webhook_get_request())

response = ms.webhooks.get_webhook(request)
print(f"Webhook: {response.name}")
```

### Create a Webhook

```python
from mailersend import MailerSendClient
from mailersend import WebhooksBuilder

ms = MailerSendClient()

request = (WebhooksBuilder()
          .domain_id("domain-id")
          .url("https://webhook.example.com")
          .name("My Webhook")
          .events(["activity.sent", "activity.delivered", "activity.opened"])
          .enabled(True)
          .build_webhook_create_request())

response = ms.webhooks.create_webhook(request)
print(f"Created webhook with ID: {response.id}")
```

### Create a disabled webhook

```python
from mailersend import MailerSendClient
from mailersend import WebhooksBuilder

ms = MailerSendClient()

request = (WebhooksBuilder()
          .domain_id("domain-id")
          .url("https://webhook.example.com")
          .name("Disabled Webhook")
          .events(["activity.sent", "activity.delivered"])
          .enabled(False)  # Create disabled
          .build_webhook_create_request())

response = ms.webhooks.create_webhook(request)
```

### Update a Webhook

```python
from mailersend import MailerSendClient
from mailersend import WebhooksBuilder

ms = MailerSendClient()

request = (WebhooksBuilder()
          .webhook_id("webhook-id")
          .name("Updated Webhook Name")
          .url("https://new-webhook.example.com")
          .enabled(True)
          .build_webhook_update_request())

response = ms.webhooks.update_webhook(request)
```

### Disable/Enable a Webhook

```python
from mailersend import MailerSendClient
from mailersend import WebhooksBuilder

ms = MailerSendClient()

# Disable webhook
request = (WebhooksBuilder()
          .webhook_id("webhook-id")
          .enabled(False)
          .build_webhook_update_request())

response = ms.webhooks.update_webhook(request)

# Enable webhook
request = (WebhooksBuilder()
          .webhook_id("webhook-id")
          .enabled(True)
          .build_webhook_update_request())

response = ms.webhooks.update_webhook(request)
```

### Delete a Webhook

```python
from mailersend import MailerSendClient
from mailersend import WebhooksBuilder

ms = MailerSendClient()

request = (WebhooksBuilder()
          .webhook_id("webhook-id")
          .build_webhook_delete_request())

response = ms.webhooks.delete_webhook(request)
print("Webhook deleted")
```

## Email Verification

### Get all email verification lists

```python
from mailersend import MailerSendClient, EmailVerificationBuilder

ms = MailerSendClient()

request = EmailVerificationBuilder().build_list_request()
response = ms.email_verification.list_verification_lists(request)

for verification_list in response.data:
    print(f"List: {verification_list.name}, Status: {verification_list.status}")
```

### Get a single email verification list

```python
from mailersend import MailerSendClient, EmailVerificationBuilder

ms = MailerSendClient()

request = (EmailVerificationBuilder()
          .verification_list_id("list-id")
          .build_get_request())

response = ms.email_verification.get_verification_list(request)
print(f"List name: {response.name}")
```

### Create an email verification list

```python
from mailersend import MailerSendClient, EmailVerificationBuilder

ms = MailerSendClient()

request = (EmailVerificationBuilder()
          .name("My Verification List")
          .emails(["test1@example.com", "test2@example.com"])
          .build_create_request())

response = ms.email_verification.create_verification_list(request)
print(f"Created list with ID: {response.id}")
```

### Verify a list

```python
from mailersend import MailerSendClient, EmailVerificationBuilder

ms = MailerSendClient()

request = (EmailVerificationBuilder()
          .verification_list_id("list-id")
          .build_verify_request())

response = ms.email_verification.verify_list(request)
print(f"Verification started: {response.message}")
```

### Get list results

```python
from mailersend import MailerSendClient, EmailVerificationBuilder

ms = MailerSendClient()

request = (EmailVerificationBuilder()
          .verification_list_id("list-id")
          .build_results_request())

response = ms.email_verification.get_verification_results(request)
for result in response.data:
    print(f"Email: {result.email}, Status: {result.status}")
```

## SMS

### Sending SMS messages

```python
from mailersend import MailerSendClient
from mailersend import SmsSendingBuilder

ms = MailerSendClient()

# Simple SMS
request = (SmsSendingBuilder()
          .from_number("sms-number-id")
          .to(["+1234567890", "+1234567891"])
          .text("Hello from MailerSend SMS!")
          .build())

response = ms.sms_sending.send(request)
print(f"SMS sent: {response.message}")

# SMS with personalization
request = (SmsSendingBuilder()
          .from_number("sms-number-id")
          .to(["+1234567890", "+1234567891"])
          .text("Hello {{name}}, your order {{order_id}} is ready!")
          .personalization([
              {
                  "phone_number": "+1234567890",
                  "data": {"name": "John", "order_id": "12345"}
              },
              {
                  "phone_number": "+1234567891", 
                  "data": {"name": "Jane", "order_id": "12346"}
              }
          ])
          .build())

response = ms.sms_sending.send(request)
```

## SMS Activity

### Get a list of SMS activities

```python
from mailersend import MailerSendClient
from mailersend import SmsActivityBuilder
from datetime import datetime, timedelta

ms = MailerSendClient()

# Get activities from last 7 days
date_from = int((datetime.now() - timedelta(days=7)).timestamp())
date_to = int(datetime.now().timestamp())

request = (SmsActivityBuilder()
          .from_number("sms-number-id")
          .date_from(date_from)
          .date_to(date_to)
          .events(["sent", "delivered", "failed"])
          .page(1)
          .limit(25)
          .build_list_request())

response = ms.sms_activity.list(request)
for activity in response.data:
    print(f"SMS to {activity.to}: {activity.status}")
```

### Get activity of a single SMS message

```python
from mailersend import MailerSendClient
from mailersend import SmsActivityBuilder

ms = MailerSendClient()

request = (SmsActivityBuilder()
          .sms_message_id("sms-message-id")
          .build_get_request())

response = ms.sms_activity.get(request)
print(f"SMS status: {response.status}")
```

## SMS Phone Numbers

### Get a list of SMS phone numbers

```python
from mailersend import MailerSendClient
from mailersend import SmsNumbersBuilder

ms = MailerSendClient()

request = (SmsNumbersBuilder()
          .paused(False)
          .page(1)
          .limit(25)
          .build_list_request())

response = ms.sms_numbers.list_sms_numbers(request)
for number in response.data:
    print(f"Number: {number.phone_number}, Paused: {number.paused}")
```

### Get an SMS phone number

```python
from mailersend import MailerSendClient
from mailersend import SmsNumbersBuilder

ms = MailerSendClient()

request = (SmsNumbersBuilder()
          .from_number("sms-number-id")
          .build_get_request())

response = ms.sms_numbers.get_sms_number(request)
print(f"Number: {response.phone_number}")
```

### Update a single SMS phone number

```python
from mailersend import MailerSendClient
from mailersend import SmsNumbersBuilder

ms = MailerSendClient()

request = (SmsNumbersBuilder()
          .from_number("sms-number-id")
          .paused(True)
          .build_update_request())

response = ms.sms_numbers.update_sms_number(request)
print("SMS number updated")
```

### Delete an SMS phone number

```python
from mailersend import MailerSendClient
from mailersend import SmsNumbersBuilder

ms = MailerSendClient()

request = (SmsNumbersBuilder()
          .from_number("sms-number-id")
          .build_delete_request())

response = ms.sms_numbers.delete_sms_number(request)
print("SMS number deleted")
```

## SMS Recipients

### Get a list of SMS recipients

```python
from mailersend import MailerSendClient
from mailersend import SmsRecipientsBuilder
from mailersend.models.sms_recipients import SmsRecipientStatus

ms = MailerSendClient()

request = (SmsRecipientsBuilder()
          .from_number("sms-number-id")
          .status(SmsRecipientStatus.ACTIVE)
          .page(1)
          .limit(25)
          .build_list_request())

response = ms.sms_recipients.list_sms_recipients(request)

# Multiple ways to access the same data
for recipient in response.data:
    print(f"Recipient: {recipient.number}, Status: {recipient.status}")

# Alternative access patterns
total_recipients = response['meta']['total']        # Dict access
request_id = response.headers.x_request_id         # Header attribute access
status_code = response.status_code                 # Direct property access

# Convert to different formats
json_response = response.to_json(indent=2)  # Pretty JSON
dict_response = response.to_dict()          # Full dictionary
```

### Get an SMS recipient

```python
from mailersend import MailerSendClient
from mailersend import SmsRecipientsBuilder

ms = MailerSendClient()

request = (SmsRecipientsBuilder()
          .sms_recipient_id("recipient-id")
          .build_get_request())

response = ms.sms_recipients.get_sms_recipient(request)
print(f"Recipient: {response.number}")
```

### Update a single SMS recipient

```python
from mailersend import MailerSendClient
from mailersend import SmsRecipientsBuilder
from mailersend.models.sms_recipients import SmsRecipientStatus

ms = MailerSendClient()

request = (SmsRecipientsBuilder()
          .sms_recipient_id("recipient-id")
          .build_update_request(SmsRecipientStatus.OPT_OUT))

response = ms.sms_recipients.update_sms_recipient(request)
print("SMS recipient updated to opt-out")
```

## SMS Messages

### Get a list of SMS messages

```python
from mailersend import MailerSendClient
from mailersend import SmsMessagesBuilder

ms = MailerSendClient()

request = (SmsMessagesBuilder()
          .page(1)
          .limit(25)
          .build_list_request())

response = ms.sms_messages.list_sms_messages(request)
for message in response.data:
    print(f"Message to {message.to}: {message.text}")
```

### Get an SMS message

```python
from mailersend import MailerSendClient
from mailersend import SmsMessagesBuilder

ms = MailerSendClient()

request = (SmsMessagesBuilder()
          .sms_message_id("message-id")
          .build_get_request())

response = ms.sms_messages.get_sms_message(request)
print(f"Message: {response.text}")
```

## SMS Webhooks

### Get a list of SMS webhooks

```python
from mailersend import MailerSendClient
from mailersend import SmsWebhooksBuilder

ms = MailerSendClient()

request = (SmsWebhooksBuilder()
          .from_number("sms-number-id")
          .build_list_request())

response = ms.sms_webhooks.list_sms_webhooks(request)
for webhook in response.data:
    print(f"Webhook: {webhook.name} - {webhook.url}")
```

### Get a single SMS webhook

```python
from mailersend import MailerSendClient
from mailersend import SmsWebhooksBuilder

ms = MailerSendClient()

request = (SmsWebhooksBuilder()
          .sms_webhook_id("webhook-id")
          .build_get_request())

response = ms.sms_webhooks.get_sms_webhook(request)
print(f"Webhook: {response.name}")
```

### Create an SMS webhook

```python
from mailersend import MailerSendClient
from mailersend import SmsWebhooksBuilder
from mailersend.models.sms_webhooks import SmsWebhookEvent

ms = MailerSendClient()

request = (SmsWebhooksBuilder()
          .from_number("sms-number-id")
          .url("https://webhook.example.com/sms")
          .name("SMS Webhook")
          .add_event(SmsWebhookEvent.SMS_SENT)
          .add_event(SmsWebhookEvent.SMS_DELIVERED)
          .add_event(SmsWebhookEvent.SMS_FAILED)
          .enabled(True)
          .build_create_request())

response = ms.sms_webhooks.create_sms_webhook(request)
print(f"Created SMS webhook with ID: {response.id}")
```

### Update a single SMS webhook

```python
from mailersend import MailerSendClient
from mailersend import SmsWebhooksBuilder
from mailersend.models.sms_webhooks import SmsWebhookEvent

ms = MailerSendClient()

request = (SmsWebhooksBuilder()
          .sms_webhook_id("webhook-id")
          .name("Updated SMS Webhook")
          .url("https://new-webhook.example.com/sms")
          .events([SmsWebhookEvent.SMS_DELIVERED, SmsWebhookEvent.SMS_FAILED])
          .enabled(False)
          .build_update_request())

response = ms.sms_webhooks.update_sms_webhook(request)
print("SMS webhook updated")
```

### Delete an SMS webhook

```python
from mailersend import MailerSendClient
from mailersend import SmsWebhooksBuilder

ms = MailerSendClient()

request = (SmsWebhooksBuilder()
          .sms_webhook_id("webhook-id")
          .build_delete_request())

response = ms.sms_webhooks.delete_sms_webhook(request)
print("SMS webhook deleted")
```

## SMS Inbound Routing

### Get a list of SMS inbound routes

```python
from mailersend import MailerSendClient
from mailersend import SmsInboundsBuilder

ms = MailerSendClient()

request = (SmsInboundsBuilder()
          .from_number("sms-number-id")
          .enabled(True)
          .page(1)
          .limit(25)
          .build_list_request())

response = ms.sms_inbounds.list_sms_inbounds(request)
for route in response.data:
    print(f"Route: {route.name} -> {route.forward_url}")
```

### Get a single SMS inbound route

```python
from mailersend import MailerSendClient
from mailersend import SmsInboundsBuilder

ms = MailerSendClient()

request = (SmsInboundsBuilder()
          .sms_inbound_id("inbound-id")
          .build_get_request())

response = ms.sms_inbounds.get_sms_inbound(request)
print(f"Route: {response.name}")
```

### Create an SMS inbound route

```python
from mailersend import MailerSendClient
from mailersend import SmsInboundsBuilder
from mailersend.models.sms_inbounds import FilterComparer

ms = MailerSendClient()

request = (SmsInboundsBuilder()
          .from_number("sms-number-id")
          .name("Support Route")
          .forward_url("https://api.example.com/sms/support")
          .filter(FilterComparer.STARTS_WITH, "SUPPORT")
          .enabled(True)
          .build_create_request())

response = ms.sms_inbounds.create_sms_inbound(request)
print(f"Created SMS inbound route with ID: {response.id}")
```

### Update an SMS inbound route

```python
from mailersend import MailerSendClient
from mailersend import SmsInboundsBuilder
from mailersend.models.sms_inbounds import FilterComparer

ms = MailerSendClient()

request = (SmsInboundsBuilder()
          .sms_inbound_id("inbound-id")
          .name("Updated Support Route")
          .forward_url("https://api.example.com/sms/new-support")
          .filter(FilterComparer.CONTAINS, "HELP")
          .enabled(False)
          .build_update_request())

response = ms.sms_inbounds.update_sms_inbound(request)
print("SMS inbound route updated")
```

### Delete an SMS inbound route

```python
from mailersend import MailerSendClient
from mailersend import SmsInboundsBuilder

ms = MailerSendClient()

request = (SmsInboundsBuilder()
          .sms_inbound_id("inbound-id")
          .build_delete_request())

response = ms.sms_inbounds.delete_sms_inbound(request)
print("SMS inbound route deleted")
```

## Tokens

### Create a token

```python
from mailersend import MailerSendClient
from mailersend import TokensBuilder

ms = MailerSendClient()

request = (TokensBuilder()
          .name("My API Token")
          .scopes(["email_full", "analytics_read"])
          .domain_id("domain-id")
          .build_token_create())

response = ms.tokens.create_token(request)
print(f"Created token: {response.accessToken}")
```

### Pause / Unpause Token

```python
from mailersend import MailerSendClient
from mailersend import TokensBuilder

ms = MailerSendClient()

# Pause token
request = (TokensBuilder()
          .token_id("token-id")
          .status("pause")
          .build_token_update())

response = ms.tokens.update_token(request)
print("Token paused")

# Unpause token
request = (TokensBuilder()
          .token_id("token-id")
          .status("unpause")
          .build_token_update())

response = ms.tokens.update_token(request)
print("Token unpaused")
```

### Delete a Token

```python
from mailersend import MailerSendClient
from mailersend import TokensBuilder

ms = MailerSendClient()

request = (TokensBuilder()
          .token_id("token-id")
          .build_token_delete())

response = ms.tokens.delete_token(request)
print("Token deleted")
```

## Other Endpoints

### Get API Quota

```python
from mailersend import MailerSendClient

ms = MailerSendClient()

response = ms.api_quota.get_quota()
print(f"Quota used: {response.used}/{response.limit}")
print(f"Resets at: {response.reset_date}")
```

<a name="error-handling"></a>

# Error Handling

The SDK provides comprehensive error handling with detailed error information:

```python
from mailersend import MailerSendClient
from mailersend.exceptions import MailerSendError
from mailersend import EmailBuilder

ms = MailerSendClient()

try:
    email = (EmailBuilder()
             .from_email("invalid-email", "Sender")  # Invalid email
             .to_many([{"email": "recipient@domain.com", "name": "Recipient"}])
             .subject("Test")
             .html("<h1>Test</h1>")
             .build())
    
    response = ms.emails.send(email)
    
except MailerSendError as e:
    print(f"MailerSend API Error: {e}")
    print(f"Status Code: {e.status_code}")
    print(f"Error Details: {e.details}")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

Common error types:

- **ValidationError**: Invalid data in request models (handled by Pydantic)
- **AuthenticationError**: Invalid or missing API key
- **RateLimitError**: API rate limit exceeded
- **APIError**: General API errors (4xx, 5xx responses)
- **NetworkError**: Network connectivity issues

# Testing

## Running Unit Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run specific test module
pytest tests/unit/test_sms_recipients_*.py

# Run with coverage
pytest --cov=mailersend --cov-report=html
```

## Testing with VCR

The SDK uses VCR.py for integration tests to record and replay API responses:

```python
import pytest
from mailersend import MailerSendClient
from mailersend import SmsRecipientsBuilder

@pytest.mark.vcr
def test_list_sms_recipients():
    ms = MailerSendClient()
    request = SmsRecipientsBuilder().build_list_request()
    response = ms.sms_recipients.list_sms_recipients(request)
    assert response.data is not None
```

<a name="endpoints"></a>

# Available endpoints

| Feature group         | Endpoint                                | Available |
|-----------------------|-----------------------------------------|-----------|
| Activity              | `GET activity`                          | ✅         |
| Analytics             | `GET analytics`                         | ✅         |
| Domains               | `{GET, POST, PUT, DELETE} domains`      | ✅         |
| Email                 | `POST send`                             | ✅         |
| Email Verification    | `{GET, POST, PUT} email-verification`   | ✅         |
| Bulk Email           | `POST bulk-email`                       | ✅         |
| Inbound Routes       | `{GET, POST, PUT, DELETE} inbound`      | ✅         |
| Messages             | `GET messages`                          | ✅         |
| Scheduled Messages   | `{GET, DELETE} scheduled-messages`      | ✅         |
| Recipients           | `{GET, POST, DELETE} recipients`        | ✅         |
| Templates            | `{GET, DELETE} templates`               | ✅         |
| Tokens               | `{POST, PUT, DELETE} tokens`            | ✅         |
| Webhooks             | `{GET, POST, PUT, DELETE} webhooks`     | ✅         |
| SMS Sending          | `POST sms`                              | ✅         |
| SMS Activity         | `GET sms-activity`                      | ✅         |
| SMS Phone Numbers    | `{GET, PUT, DELETE} sms-numbers`        | ✅         |
| SMS Recipients       | `{GET, PUT} sms-recipients`             | ✅         |
| SMS Messages         | `GET sms-messages`                      | ✅         |
| SMS Webhooks         | `{GET, POST, PUT, DELETE} sms-webhooks` | ✅         |
| SMS Inbound Routing  | `{GET, POST, PUT, DELETE} sms-inbounds` | ✅         |
| Sender Identities    | `{GET, POST, PUT, DELETE} identities`   | ✅         |
| API Quota            | `GET api-quota`                         | ✅         |

*All endpoints are available and fully tested. Refer to [official API docs](https://developers.mailersend.com/) for the most up-to-date API specifications.*

<a name="support-and-feedback"></a>

# Support and Feedback

In case you find any bugs, submit an issue directly here in GitHub.

If you have any troubles using our API or SDK free to contact our support by email [info@mailersend.com](mailto:info@mailersend.com)

The official documentation is at [https://developers.mailersend.com](https://developers.mailersend.com)

<a name="license"></a>

# License

[The MIT License (MIT)](LICENSE)
