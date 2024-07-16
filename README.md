<a href="https://www.mailersend.com"><img src="https://www.mailersend.com/images/logo.svg" width="200px"/></a>

MailerSend Python SDK

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

# Table of Contents
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
  - [Requirements](#requirements)
  - [Authentication](#authentication)
- [Usage](#usage)
  - [Email](#email)
    - [Send an email](#send-an-email)
    - [Add CC, BCC recipients](#add-cc-bcc-recipients)
    - [Send a template-based email](#send-a-template-based-email)
    - [Personalization](#personalization)
    - [Send email with attachment](#send-email-with-attachment)
  - [Email Verification](#email-verification)
    - [Get all email verification lists](#get-all-email-verification-lists)
    - [Get a single email verification list](#get-a-single-email-verification-list)
    - [Create a email verification list](#create-a-email-verification-list)
    - [Verify a list](#verify-a-list)
    - [Get list results](#get-list-results)
  - [Bulk Email](#bulk-email)
    - [Send bulk email](#send-bulk-email)
    - [Get bulk email status](#get-bulk-email-status)
  - [Activity](#activity)
    - [Get a list of activities (simple)](#get-a-list-of-activities-simple)
    - [Get a list of activities (full)](#get-a-list-of-activities-full)
  - [Analytics](#analytics)
    - [Activity data by date](#activity-data-by-date)
    - [Opens by country](#opens-by-country)
    - [Opens by user-agent name](#opens-by-user-agent-name)
    - [Opens by reading environment](#opens-by-reading-environment)
  - [Inbound Routes](#inbound-routes)
    - [Get a list of inbound routes](#get-a-list-of-inbound-routes)
    - [Get a single inbound route](#get-a-single-inbound-route)
    - [Add an inbound route](#add-an-inbound-route)
    - [Update an inbound route](#update-an-inbound-route)
    - [Delete an inbound route](#delete-an-inbound-route)
  - [Domains](#domains)
    - [Get a list of domains](#get-a-list-of-domains)
    - [Get a single domain](#get-a-single-domain)
    - [Get a single domain using helper function](#get-a-single-domain-using-helper-function)
    - [Add a domain](#add-a-domain)
    - [Delete a domain](#delete-a-domain)
    - [Get a list of recipients per domain](#get-a-list-of-recipients-per-domain)
    - [Update domain settings](#update-domain-settings)
    - [Get DNS Records](#get-dns-records)
    - [Verify a domain](#verify-a-domain)
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
  - [Tokens](#tokens)
    - [Create a token](#create-a-token)
    - [Pause / Unpause Token](#pause--unpause-token)
    - [Delete a Token](#delete-a-token)
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
  - [SMS](#sms)
    - [Sending SMS messages](#sending-sms-messages)
  - [SMS Activity](#sms-activity)
    - [Get a list of activities](#get-a-list-of-activities)
    - [Get activity of a single message](#get-activity-of-a-single-message)
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
    - [Get a list of SMS webhooks](#get-a-list-of-sms-webhooks-1)
  - [SMS Inbouds](#sms-inbouds)
    - [Get a list of SMS inbound routes](#get-a-list-of-sms-inbound-routes)
    - [Get a single SMS inbound route](#get-a-single-sms-inbound-route)
    - [Create an SMS inbound route](#create-an-sms-inbound-route)
    - [Update an SMS inbound route](#update-an-sms-inbound-route)
    - [Delete an SMS inbound route](#delete-an-sms-inbound-route)
  - [Sender Identities](#sender-identities)
    - [Get a list of sender identities](#get-a-list-of-sender-identities)
    - [Get a sender identity](#get-a-sender-identity)
    - [Create a sender identity](#create-a-sender-identity)
    - [Update a sender identity](#update-a-sender-identity)
    - [Delete a sender identity](#delete-a-sender-identity)
  - [API Quota](#api-quota)
    - [Get API Quota](#get-api-quota)
- [Troubleshooting](#troubleshooting)
  - [Emails not being sent](#emails-not-being-sent)
- [Testing](#testing)
- [Available endpoints](#available-endpoints)
- [Support and Feedback](#support-and-feedback)
- [License](#license)

<a name="installation"></a>

# Installation

```
$ python -m pip install mailersend
```

## Requirements

- Python > 3.6.1
- Python `pip`
- An API Key from [mailersend.com](https://www.mailersend.com)

## Authentication

We recommend you to define `MAILERSEND_API_KEY` environment variable in the `.env` file, and use it to store the API key.

- Using environment variable
```python
from mailersend import emails

# assigning NewEmail() without params defaults to MAILERSEND_API_KEY env var
mailer = emails.NewEmail()

# define an empty dict to populate with mail values
mail_body = {}

mail_from = {
    "name": "Your Name",
    "email": "your@domain.com",
}

recipients = [
    {
        "name": "Your Client",
        "email": "your@client.com",
    }
]

reply_to = {
    "name": "Name",
    "email": "reply@domain.com",
}

mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Hello!", mail_body)
mailer.set_html_content("This is the HTML content", mail_body)
mailer.set_plaintext_content("This is the text content", mail_body)
mailer.set_reply_to(reply_to, mail_body)

# using print() will also return status code and data
mailer.send(mail_body)
```

- Explicit declaration
```python
from mailersend import emails

mailer = emails.NewEmail("my-api-key")

# define an empty dict to populate with mail values
mail_body = {}

mail_from = {
    "name": "Your Name",
    "email": "your@domain.com",
}

recipients = [
    {
        "name": "Your Client",
        "email": "your@client.com",
    }
]

reply_to = {
    "name": "Name",
    "email": "reply@domain.com",
}

mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Hello!", mail_body)
mailer.set_html_content("This is the HTML content", mail_body)
mailer.set_plaintext_content("This is the text content", mail_body)
mailer.set_reply_to(reply_to, mail_body)

# using print() will also return status code and data
mailer.send(mail_body)
```

# Usage

## Email

### Send an email

```python
from mailersend import emails
from dotenv import load_dotenv

load_dotenv()

mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

# define an empty dict to populate with mail values
mail_body = {}

mail_from = {
    "name": "Your Name",
    "email": "your@domain.com",
}

recipients = [
    {
        "name": "Your Client",
        "email": "your@client.com",
    }
]

reply_to = {
    "name": "Name",
    "email": "reply@domain.com",
}

mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Hello!", mail_body)
mailer.set_html_content("This is the HTML content", mail_body)
mailer.set_plaintext_content("This is the text content", mail_body)
mailer.set_reply_to(reply_to, mail_body)

# using print() will also return status code and data
mailer.send(mail_body)
```

### Add CC, BCC recipients

```python
from mailersend import emails
from dotenv import load_dotenv

load_dotenv()

mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

# define an empty dict to populate with mail values
mail_body = {}

mail_from = {
    "name": "Your Name",
    "email": "your@domain.com",
}

recipients = [
    {
        "name": "Your Client",
        "email": "your@client.com",
    }
]

cc = [
    {
        "name": "CC",
        "email": "cc@client.com"
    }
]

bcc = [
    {
        "name": "BCC",
        "email": "bcc@client.com"
    }
]

mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Hello!", mail_body)
mailer.set_html_content("This is the HTML content", mail_body)
mailer.set_plaintext_content("This is the text content", mail_body)
mailer.set_cc_recipients(cc, mail_body)
mailer.set_bcc_recipients(bcc, mail_body)

mailer.send(mail_body)
```

### Send a template-based email

```python
from mailersend import emails
from dotenv import load_dotenv

load_dotenv()

mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

# define an empty dict to populate with mail values
mail_body = {}

mail_from = {
    "name": "Your Name",
    "email": "your@domain.com",
}

recipients = [
    {
        "name": "Your Client",
        "email": "your@client.com",
    }
]


variables = [
    {
        "email": "your@client.com",
        "substitutions": [
            {
                "var": "foo",
                "value": "bar"
            },
        ]
    }
]


mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Hello from {$company}", mail_body)
mailer.set_template("templateID", mail_body)
mailer.set_personalization(variables, mail_body)

mailer.send(mail_body)
```

### Personalization

```python
from mailersend import emails
from dotenv import load_dotenv

load_dotenv()

mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

# define an empty dict to populate with mail values
mail_body = {}

mail_from = {
    "name": "Your Name",
    "email": "your@domain.com",
}

recipients = [
    {
        "name": "Your Client",
        "email": "your@client.com",
    }
]

personalization = [
    {
        "email": "test@mailersend.com",
        "data": {
            "var": "value",
            "boolean": True,
            "object": {
                "key" : "object-value"
            },
            "number": 2,
            "array": [
                1,
                2,
                3
            ]
        }
    }
]


mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Hello from {$company}", mail_body)
mailer.set_html_content("This is the HTML content, {$name}", mail_body)
mailer.set_plaintext_content("This is the text content, {$name}", mail_body)
mailer.set_personalization(personalization, mail_body)

mailer.send(mail_body)
```

### Send email with attachment

```python
from mailersend import emails
import base64
from dotenv import load_dotenv

load_dotenv()

mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

# define an empty dict to populate with mail values
mail_body = {}

mail_from = {
    "name": "Your Name",
    "email": "your@domain.com",
}

recipients = [
    {
        "name": "Your Client",
        "email": "your@client.com",
    }
]

variables = [
    {
        "email": "your@client.com",
        "substitutions": [
            {
                "var": "foo",
                "value": "bar"
            },
        ]
    }
]

attachment = open('path-to-file', 'rb')
att_read = attachment.read()
att_base64 = base64.b64encode(bytes(att_read))
attachments = [
    {
        "id": "my-attached-file",
        "filename": "file.jpg",
        "content": f"{att_base64.decode('ascii')}",
        "disposition": "attachment"
    }
]

mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Hello from {$foo}", mail_body)
mailer.set_html_content("This is the HTML content, {$foo}", mail_body)
mailer.set_plaintext_content("This is the text content, {$foo}", mail_body)
mailer.set_personalization(variables, mail_body)
mailer.set_attachments(attachments, mail_body)

mailer.send(mail_body)
```

## Email Verification

### Get all email verification lists

```python
from mailersend import email_verification
from dotenv import load_dotenv

load_dotenv()

mailer = email_verification.NewEmailVerification(os.getenv('MAILERSEND_API_KEY'))

mailer.get_all_lists()
```

### Get a single email verification list

```python
from mailersend import email_verification
from dotenv import load_dotenv

load_dotenv()

mailer = email_verification.NewEmailVerification(os.getenv('MAILERSEND_API_KEY'))

email_verification_list_id = 123456

mailer.get_list(email_verification_list_id)
```

### Create a email verification list

```python
from mailersend import email_verification
from dotenv import load_dotenv

load_dotenv()

mailer = email_verification.NewEmailVerification(os.getenv('MAILERSEND_API_KEY'))

name = "My List"
emails = [
    "some@email.com",
    "another@email.com"
]

mailer.create_list(name, emails)
```

### Verify a list

```python
from mailersend import email_verification
from dotenv import load_dotenv

load_dotenv()

mailer = email_verification.NewEmailVerification(os.getenv('MAILERSEND_API_KEY'))

email_verification_list_id = 123456

mailer.verify_list(email_verification_list_id)
```

### Get list results

```python
from mailersend import email_verification
from dotenv import load_dotenv

load_dotenv()

mailer = email_verification.NewEmailVerification(os.getenv('MAILERSEND_API_KEY'))

email_verification_list_id = 123456

mailer.get_list_results(email_verification_list_id)
```


## Bulk Email

### Send bulk email

```python
from mailersend import emails
from dotenv import load_dotenv

load_dotenv()

mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

mail_list = [
  {
    "from": {
      "email": "your@domain.com",
      "name": "Your Name"
    },
    "to": [
      {
        "email": "your@client.com",
        "name": "Your Client"
      }
    ],
    "subject": "Subject",
    "text": "This is the text content",
    "html": "<p>This is the HTML content</p>",
  },
  {
    "from": {
      "email": "your@domain.com",
      "name": "Your Name"
    },
    "to": [
      {
        "email": "your@client.com",
        "name": "Your Client"
      }
    ],
    "subject": "Subject",
    "text": "This is the text content",
    "html": "<p>This is the HTML content</p>",
  }
]

print(mailer.send_bulk(mail_list))
```

### Get bulk email status

```python
from mailersend import emails
from dotenv import load_dotenv

load_dotenv()

mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

print(mailer.get_bulk_status_by_id("bulk-email-id"))
```

<a name="activity"></a>

## Activity

### Get a list of activities (simple)

```python
from mailersend import activity
from dotenv import load_dotenv

load_dotenv()

mailer = activity.NewActivity(os.getenv('MAILERSEND_API_KEY'))

mailer.get_domain_activity("domain-id")
```

### Get a list of activities (full)

```python
from mailersend import activity
from dotenv import load_dotenv

load_dotenv()

mailer = activity.NewActivity(os.getenv('MAILERSEND_API_KEY'))

page = 1
limit = 20
date_from = 1623073576
date_to = 1623074976
events = [
    "queued",
    "sent",
    "delivered",
    "soft-bounced",
    "hard-bounced",
    "junk",
    "opened",
    "clicked",
    "unsubscribed",
    "spam_complaints",
]

mailer.get_domain_activity("domain-id", page, limit, date_from, date_to, events)
```

## Analytics

### Activity data by date

```python
from mailersend import analytics
from dotenv import load_dotenv

load_dotenv()

mailer = analytics.NewAnalytics(os.getenv('MAILERSEND_API_KEY'))

date_from = 1623073576
date_to = 1623074976
events = [
    "sent",
]

# optional arguments
domain_id = "domain-id"
group_by = "days"

mailer.get_activity_by_date(date_from, date_to, events, domain_id, group_by)
```

### Opens by country

```python
from mailersend import analytics
from dotenv import load_dotenv

load_dotenv()

mailer = analytics.NewAnalytics(os.getenv('MAILERSEND_API_KEY'))

date_from = 1623073576
date_to = 1623074976

# optional arguments
domain_id = "domain-id"

mailer.get_opens_by_country(date_from, date_to, domain_id)
```

### Opens by user-agent name

```python
from mailersend import analytics
from dotenv import load_dotenv

load_dotenv()

mailer = analytics.NewAnalytics(os.getenv('MAILERSEND_API_KEY'))

date_from = 1623073576
date_to = 1623074976

# optional arguments
domain_id = "domain-id"

mailer.get_opens_by_user_agent(date_from, date_to, domain_id)
```

### Opens by reading environment

```python
from mailersend import analytics
from dotenv import load_dotenv

load_dotenv()

mailer = analytics.NewAnalytics(os.getenv('MAILERSEND_API_KEY'))

date_from = 1623073576
date_to = 1623074976

# optional arguments
domain_id = "domain-id"

mailer.get_opens_by_reading_environment(date_from, date_to, domain_id)
```

## Inbound Routes

### Get a list of inbound routes

```python
from mailersend import inbound_routing
from dotenv import load_dotenv

load_dotenv()

mailer = inbound_routing.NewInbound(os.getenv('MAILERSEND_API_KEY'))

print(mailer.get_inbound_routes())
```

### Get a single inbound route

```python
from mailersend import inbound_routing
from dotenv import load_dotenv

load_dotenv()

mailer = inbound_routing.NewInbound(os.getenv('MAILERSEND_API_KEY'))

print(mailer.get_inbound_by_id("inbound-id"))
```

### Add an inbound route

```python
from mailersend import inbound_routing
from dotenv import load_dotenv

load_dotenv()

mailer = inbound_routing.NewInbound(os.getenv('MAILERSEND_API_KEY'))

options = {}

_catch_filter = {
    "type": "catch_recipient",
    "filters": [
        {
            "comparer": "equal",
            "value": "test"
        }
    ]
}

_match_filter = {
    "type": "match_all"
}

_forwards = [
    {
        "type": "webhook",
        "value": "https://www.mailersend.com/hook"
    }
]
mailer.set_name("Example route", options)
mailer.set_domain_enabled(True, options)
mailer.set_inbound_domain("test.mailersend.com", options)
mailer.set_catch_filter(_catch_filter, options)

print(mailer.add_inbound_route())
```

### Update an inbound route

```python
from mailersend import inbound_routing
from dotenv import load_dotenv

load_dotenv()

route_id = "inbound-route-id"

mailer = inbound_routing.NewInbound(os.getenv('MAILERSEND_API_KEY'))

options = {}

_catch_filter = {
    "type": "catch_recipient",
    "filters": [
        {
            "comparer": "equal",
            "value": "test"
        }
    ]
}

_match_filter = {
    "type": "match_all"
}

_forwards = [
    {
        "type": "webhook",
        "value": "https://www.mailersend.com/hook"
    }
]
mailer.set_name("Example route", options)
mailer.set_domain_enabled(True, options)
mailer.set_inbound_domain("test.mailersend.com", options)
mailer.set_catch_filter(_catch_filter, options)

print(mailer.update_inbound_route(route_id))
```

### Delete an inbound route

```python
from mailersend import inbound_routing
from dotenv import load_dotenv

load_dotenv()

route_id = "inbound-route-id"

mailer = inbound_routing.NewInbound(os.getenv('MAILERSEND_API_KEY'))

print(mailer.delete_inbound_route(route_id))
```

## Domains

### Get a list of domains

```python
from mailersend import domains
from dotenv import load_dotenv

load_dotenv()

mailer = domains.NewDomain(os.getenv('MAILERSEND_API_KEY'))

mailer.get_domains()
```

### Get a single domain

```python
from mailersend import domains
from dotenv import load_dotenv

load_dotenv()

mailer = domains.NewDomain(os.getenv('MAILERSEND_API_KEY'))

mailer.get_domain_by_id("domain-id")
```

### Get a single domain using helper function

```python
from mailersend import domains
from mailersend import utils
from dotenv import load_dotenv

load_dotenv()

mailer = domains.NewDomain(os.getenv('MAILERSEND_API_KEY'))
helper = utils.NewHelper(os.getenv('MAILERSEND_API_KEY'))

mailer.get_domain_by_id(helper.get_id_by_name("domains","domain-name"))
```

### Add a domain

You can find a full list of settings [here](https://developers.mailersend.com/api/v1/domains.html#request-parameters-3).

```python
from mailersend import domains
from dotenv import load_dotenv

load_dotenv()

mailer = domains.NewDomain(os.getenv('MAILERSEND_API_KEY'))

domain_data = {
    "name": "mydomain.com",
    "return_path_subdomain": "rpsubdomain",
    "custom_tracking_subdomain": "ctsubdomain",
    "inbound_routing_subdomain": "irsubdomain"
}
mailer.add_domain("name", domain_data)
```


### Delete a domain

```python
from mailersend import domains
from dotenv import load_dotenv

load_dotenv()

mailer = domains.NewDomain(os.getenv('MAILERSEND_API_KEY'))

mailer.delete_domain("domain-id")
```

### Get a list of recipients per domain

```python
from mailersend import domains
from dotenv import load_dotenv

load_dotenv()

mailer = domains.NewDomain(os.getenv('MAILERSEND_API_KEY'))

mailer.get_recipients_for_domain("domain-id")
```

### Update domain settings

You can find a full list of settings [here](https://developers.mailersend.com/api/v1/domains.html#request-body).

```python
from mailersend import domains
from dotenv import load_dotenv

load_dotenv()

mailer = domains.NewDomain(os.getenv('MAILERSEND_API_KEY'))

domain_data = {
    "send_paused": True,
    "track_clicks": True,
    "track_opens": True,
    "track_unsubscribe": True,
    "track_unsubscribe_html": "<p>Click to <a href='{$unsubscribe}'>unsubscribe</a></p>",
    "track_unsubscribe_plain": "Click to unsubscribe: {$unsubscribe}",
    "track_content": True,
    "custom_tracking_enabled": True,
    "custom_tracking_subdomain": "email",
    "precedence_bulk": False
}

mailer.update_domain_setting("domain-id", domain_data)
```

### Get DNS Records

```python
from mailersend import domains
from dotenv import load_dotenv

load_dotenv()

mailer = domains.NewDomain(os.getenv('MAILERSEND_API_KEY'))

mailer.get_dns_records("domain-id")
```

### Verify a domain

```python
from mailersend import domains
from dotenv import load_dotenv

load_dotenv()

mailer = domains.NewDomain(os.getenv('MAILERSEND_API_KEY'))

mailer.verify_domain("domain-id")
```


## Messages

### Get a list of messages

```python
from mailersend import messages
from dotenv import load_dotenv

load_dotenv()

mailer = messages.NewMessage(os.getenv('MAILERSEND_API_KEY'))

mailer.get_messages()
```

### Get a single message

```python
from mailersend import messages
from dotenv import load_dotenv

load_dotenv()

mailer = messages.NewMessage(os.getenv('MAILERSEND_API_KEY'))

mailer.get_message_by_id("message-id")
```

## Scheduled messages

### Get a list of scheduled messages

```python
from mailersend import scheduled_messages
from dotenv import load_dotenv

load_dotenv()

mailer = scheduled_messages.NewMessageSchedule(os.getenv('MAILERSEND_API_KEY'))

print(mailer.get_scheduled_messages())
```

### Get a single scheduled message

```python
from mailersend import scheduled_messages
from dotenv import load_dotenv

load_dotenv()

mailer = scheduled_messages.NewMessageSchedule(os.getenv('MAILERSEND_API_KEY'))

print(mailer.get_scheduled_message_by_id("scheduled-message-id"))
```

### Delete a scheduled message

```python
from mailersend import scheduled_messages
from dotenv import load_dotenv

load_dotenv()

mailer = scheduled_messages.NewMessageSchedule(os.getenv('MAILERSEND_API_KEY'))

print(mailer.delete_scheduled_message("scheduled-message-id"))
```

## Recipients

### Get a list of recipients

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

mailer.get_recipients()
```

### Get a single recipient

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

mailer.get_recipient_by_id("recipient-id")
```

### Delete a recipient

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

mailer.delete_recipient("recipient-id")
```

### Get recipients from a blocklist

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

mailer.get_recipients_from_blocklist("domain-id")
```

### Get recipients from hard bounces

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

mailer.get_hard_bounces("domain-id")
```

### Get recipients from spam complaints

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

mailer.get_spam_complaints("domain-id")
```

### Get recipients from unsubscribes

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

mailer.get_unsubscribes("domain-id")
```

### Add recipients to blocklist

Using recipients:

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

recipient_list = [
    'blocked@client.com'
]

mailer.add_to_blocklist("domain-id", recipients=recipient_list)
```

Using patterns:

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

recipient_patterns = [
    '*@client.com'
]

mailer.add_to_blocklist("domain-id", patterns=recipient_patterns)
```

### Add hard bounced recipients

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

recipient_list = [
    "your@client.com"
]

mailer.add_hard_bounces("domain-id", recipient_list)
```

### Add spam complaints

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

recipient_list = [
    "your@client.com"
]

mailer.add_spam_complaints("domain-id", recipient_list)
```

### Add recipients to unsubscribe list

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

recipient_list = [
    "your@client.com"
]

mailer.add_unsubscribes("domain-id", recipient_list)
```

### Delete recipients from blocklist

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

recipient_list = [
    "your@client.com"
]

mailer.delete_from_blocklist("domain-id", recipient_list)
```

### Delete hard bounced recipients

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

recipient_list = [
    "your@client.com"
]

mailer.delete_hard_bounces("domain-id", recipient_list)
```

### Delete spam complaints

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

recipient_list = [
    "your@client.com"
]

mailer.delete_spam_complaints("domain-id", recipient_list)
```

### Delete recipients from unsubscribe list

```python
from mailersend import recipients
from dotenv import load_dotenv

load_dotenv()

mailer = recipients.NewRecipient(os.getenv('MAILERSEND_API_KEY'))

recipient_list = [
    "your@client.com"
]

mailer.delete_unsubscribes("domain-id", recipient_list)
```

## Tokens

### Create a token

```python
from mailersend import tokens
from dotenv import load_dotenv

load_dotenv()

mailer = tokens.NewToken(os.getenv('MAILERSEND_API_KEY'))

scopes = ["email_full", "analytics_read"]

mailer.create_token("my-token", scopes)
```

Because of security reasons, we only allow access token appearance once during creation. In order to see the access token created you can do:

```python
from mailersend import tokens
from dotenv import load_dotenv

load_dotenv()

mailer = tokens.NewToken(os.getenv('MAILERSEND_API_KEY'))

scopes = ["email_full", "analytics_read"]

print(mailer.create_token("my-token", scopes))
```

### Pause / Unpause Token

```python
from mailersend import tokens
from dotenv import load_dotenv

load_dotenv()

mailer = tokens.NewToken(os.getenv('MAILERSEND_API_KEY'))

# pause
mailer.update_token("my-token")

# unpause
mailer.update_token("my-token", pause=False)
```

### Delete a Token

```python
from mailersend import tokens
from dotenv import load_dotenv

load_dotenv()

mailer = tokens.NewToken(os.getenv('MAILERSEND_API_KEY'))

mailer.delete_token("token-id")
```

## Templates

### Get a list of templates

```python
from mailersend import templates
from dotenv import load_dotenv

load_dotenv()

mailer = templates.NewTemplate(os.getenv('MAILERSEND_API_KEY'))

mailer.get_templates()
```

### Get a single template

```python
from mailersend import templates
from dotenv import load_dotenv

load_dotenv()

mailer = templates.NewTemplate(os.getenv('MAILERSEND_API_KEY'))
template_id = 1234

mailer.get_template_by_id()
```

### Delete template

```python
from mailersend import templates
from dotenv import load_dotenv

load_dotenv()

mailer = templates.NewTemplate(os.getenv('MAILERSEND_API_KEY'))
template_id = 1234

mailer.delete_template()
```

## Webhooks

### Get a list of webhooks

```python
from mailersend import webhooks
from dotenv import load_dotenv

load_dotenv()

mailer = webhooks.NewWebhook(os.getenv('MAILERSEND_API_KEY'))

mailer.get_webhooks("domain-id")
```

### Get a single webhook

```python
from mailersend import webhooks
from dotenv import load_dotenv

load_dotenv()

mailer = webhooks.NewWebhook(os.getenv('MAILERSEND_API_KEY'))

mailer.get_webhook_by_id("webhook-id")
```

### Create a Webhook

```python
from mailersend import webhooks
from dotenv import load_dotenv

load_dotenv()

webhookEvents = ['activity.sent', 'activity.delivered']

webhook = webhooks.NewWebhook(os.getenv('MAILERSEND_API_KEY'))
webhook.set_webhook_url("https://webhooks.mysite.com")
webhook.set_webhook_name("my first webhook")
webhook.set_webhook_events(webhookEvents)
webhook.set_webhook_domain("domain-id")

webhook.create_webhook()
```

### Create a disabled webhook

```python
from mailersend import webhooks
from dotenv import load_dotenv

load_dotenv()

webhookEvents = ['activity.sent', 'activity.delivered']

webhook = webhooks.NewWebhook(os.getenv('MAILERSEND_API_KEY'))
webhook.set_webhook_url("https://webhooks.mysite.com")
webhook.set_webhook_name("my first webhook")
webhook.set_webhook_events(webhookEvents)
webhook.set_webhook_domain("domain-id")
webhook.set_webhook_enabled(False)

webhook.create_webhook()
```

### Update a Webhook

```python
from mailersend import webhooks
from dotenv import load_dotenv

load_dotenv()

webhook = webhooks.NewWebhook(os.getenv('MAILERSEND_API_KEY'))

webhook.update_webhook("webhook-id", "name", "a new webhook name")
```

### Disable/Enable a Webhook

```python
from mailersend import webhooks
from dotenv import load_dotenv

load_dotenv()

webhook = webhooks.NewWebhook(os.getenv('MAILERSEND_API_KEY'))

webhook.update_webhook("webhook-id", "enabled", False)
```

### Delete a Webhook

```python
from mailersend import webhooks
from dotenv import load_dotenv

load_dotenv()

webhook = webhooks.NewWebhook(os.getenv('MAILERSEND_API_KEY'))

webhook.delete_webhook("webhook-id")
```

## SMS

### Sending SMS messages

Without personalization:
```python
from mailersend import sms_sending
from dotenv import load_dotenv

load_dotenv()

mailer = sms_sending.NewSmsSending(os.getenv('MAILERSEND_API_KEY'))

# Number belonging to your account in E164 format
number_from = "+11234567890"

# You can add up to 50 recipient numbers
numbers_to = [
    "+11234567891",
    "+11234567892"
]
text = "This is the text content"

print(mailer.send_sms(number_from, numbers_to, text))
```

With personalization:
```python
from mailersend import sms_sending
from dotenv import load_dotenv

load_dotenv()

mailer = sms_sending.NewSmsSending(os.getenv('MAILERSEND_API_KEY'))

# Number belonging to your account in E164 format
number_from = "+11234567890"

# You can add up to 50 recipient numbers
numbers_to = [
    "+11234567891",
    "+11234567892"
]
text = "Hi {{name}} how are you?"
personalization = [
    {
        "phone_number": "+11234567891",
        "data": {
            "name": "Mike"
        }
    },
    {
        "phone_number": "+11234567892",
        "data": {
            "name": "John"
        }
    }
]

print(mailer.send_sms(number_from, numbers_to, text, personalization))
```

## SMS Activity

### Get a list of activities
```python
from mailersend import sms_activity
from dotenv import load_dotenv

load_dotenv()

mailer = sms_activity.NewSmsActivity(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_number_id = 1365743
date_from = 1655157601
date_to = 1655158601
status = ["queued", "failed"]
page = 1
limit = 200

print(mailer.get_activities(sms_number_id=sms_number_id, date_from=date_from, date_to=date_to, status=status, page=page, limit=limit))
```

### Get activity of a single message
```python
from mailersend import sms_activity
from dotenv import load_dotenv

load_dotenv()

mailer = sms_activity.NewSmsActivity(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_message_id = "62a9d12b07852eaf2207b417"

print(mailer.get_activity(sms_message_id))
```

## SMS Phone Numbers

### Get a list of SMS phone numbers
```python
from mailersend import sms_phone_numbers
from dotenv import load_dotenv

load_dotenv()

mailer = sms_phone_numbers.NewSmsNumbers(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
paused = False

print(mailer.get_phone_numbers(paused))
```

### Get an SMS phone number
```python
from mailersend import sms_phone_numbers
from dotenv import load_dotenv

load_dotenv()

mailer = sms_phone_numbers.NewSmsNumbers(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_number_id = "9pq3enl6842vwrzx"

print(mailer.get_phone_number(sms_number_id))
```

### Update a single SMS phone number
```python
from mailersend import sms_phone_numbers
from dotenv import load_dotenv

load_dotenv()

mailer = sms_phone_numbers.NewSmsNumbers(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_number_id = "9pq3enl6842vwrzx"
paused = True

print(mailer.update_phone_number(sms_number_id, paused))
```

### Delete an SMS phone number
```python
from mailersend import sms_phone_numbers
from dotenv import load_dotenv

load_dotenv()

mailer = sms_phone_numbers.NewSmsNumbers(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_number_id = "9pq3enl6842vwrzx"

print(mailer.delete_phone_number(sms_number_id))
```

## SMS Recipients

### Get a list of SMS recipients
```python
from mailersend import sms_recipients
from dotenv import load_dotenv

load_dotenv()

mailer = sms_recipients.NewSmsRecipients(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_number_id = "9pq3enl6842vwrzx"
status = "active"

print(mailer.get_recipients(status=status, sms_number_id=sms_number_id))
```

### Get an SMS recipient
```python
from mailersend import sms_recipients
from dotenv import load_dotenv

load_dotenv()

mailer = sms_recipients.NewSmsRecipients(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_recipient_id = "627e756fd30078fb2208cc87"

print(mailer.get_recipient(sms_recipient_id))
```

### Update a single SMS recipient
```python
from mailersend import sms_recipients
from dotenv import load_dotenv

load_dotenv()

mailer = sms_recipients.NewSmsRecipients(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_recipient_id = "627e756fd30078fb2208cc87"
status = "opt_out"

print(mailer.update_recipient(sms_recipient_id, status))
```

## SMS Messages

### Get a list of SMS messages
```python
from mailersend import sms_messages
from dotenv import load_dotenv

load_dotenv()

mailer = sms_messages.NewSmsMessages(os.getenv('MAILERSEND_API_KEY'))

print(mailer.get_messages())
```

### Get an SMS message
```python
from mailersend import sms_messages
from dotenv import load_dotenv

load_dotenv()

#Request parameters
sms_message_id = "627e756fd30078fb2208cc87"

mailer = sms_messages.NewSmsMessages(os.getenv('MAILERSEND_API_KEY'))

print(mailer.get_message(sms_message_id))
```

## SMS Webhooks

### Get a list of SMS webhooks
```python
from mailersend import sms_webhooks
from dotenv import load_dotenv

load_dotenv()

mailer = sms_webhooks.NewSmsWebhooks(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_number_id = "9pq3enl6842vwrzx"

print(mailer.get_webhooks(sms_number_id))
```

### Get a single SMS webhook
```python
from mailersend import sms_webhooks
from dotenv import load_dotenv

load_dotenv()

mailer = sms_webhooks.NewSmsWebhooks(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_webhook_id = "aaui13enl12f2vzx"

print(mailer.get_webhook(sms_webhook_id))
```

### Create an SMS webhook
```python
from mailersend import sms_webhooks
from dotenv import load_dotenv

load_dotenv()

mailer = sms_webhooks.NewSmsWebhooks(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
url = "https://webhook-url.com"
name = "My Webhook Name"
events = ["sms.sent"]
sms_number_id = "9pq3enl6842vwrzx"
enabled = True

print(mailer.create_webhook(url, name, events, sms_number_id, enabled))
```

### Update a single SMS webhook
```python
from mailersend import sms_webhooks
from dotenv import load_dotenv

load_dotenv()

mailer = sms_webhooks.NewSmsWebhooks(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
url = "https://different-url.com"
name = "New Webhook Name"
events = ["sms.sent", "sms.failed"],
sms_webhook_id = "aaui13enl12f2vzx"
enabled = False

print(mailer.update_webhook(sms_webhook_id, url, name, events, enabled))
```

### Delete an SMS webhook
```python
from mailersend import sms_webhooks
from dotenv import load_dotenv

load_dotenv()

mailer = sms_webhooks.NewSmsWebhooks(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_webhook_id = "aaui13enl12f2vzx"

print(mailer.delete_webhook(sms_webhook_id))
```

### Get a list of SMS webhooks
```python
from mailersend import sms_webhooks
from dotenv import load_dotenv

load_dotenv()

mailer = sms_webhooks.NewSmsWebhooks(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_number_id = "9pq3enl6842vwrzx"

print(mailer.get_webhooks(sms_number_id))
```

## SMS Inbouds

### Get a list of SMS inbound routes
```python
from mailersend import sms_inbounds
from dotenv import load_dotenv

load_dotenv()

mailer = sms_inbounds.NewSmsInbounds(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_number_id = "123456789"
enabled = True
page = 1
limit = 25

print(mailer.get_inbound_routes(sms_number_id, enabled, page, limit))
```

### Get a single SMS inbound route
```python
from mailersend import sms_inbounds
from dotenv import load_dotenv

load_dotenv()

mailer = sms_inbounds.NewSmsInbounds(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_inbound_id = "123456789"

print(mailer.get_inbound_route(sms_inbound_id))
```

### Create an SMS inbound route
```python
from mailersend import sms_inbounds
from dotenv import load_dotenv

load_dotenv()

mailer = sms_inbounds.NewSmsInbounds(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_number_id = "123456789"
name = "My route"
forward_url = "https://some.url"
filter = {
    "comparer": "equal",
    "value": "START"
}
enabled = True

print(mailer.create_inbound_route(sms_number_id, name, forward_url, filter, enabled))
```

### Update an SMS inbound route
```python
from mailersend import sms_inbounds
from dotenv import load_dotenv

load_dotenv()

mailer = sms_inbounds.NewSmsInbounds(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_number_id = "123456789"
name = "New name"
forward_url = "https://news.url"
filter = {
    "comparer": "contains",
    "value": "some-value"
}
enabled = True

print(mailer.update_inbound_route(sms_number_id, name, forward_url, filter, enabled))
```

### Delete an SMS inbound route
```python
from mailersend import sms_inbounds
from dotenv import load_dotenv

load_dotenv()

mailer = sms_inbounds.NewSmsInbounds(os.getenv('MAILERSEND_API_KEY'))

#Request parameters
sms_inbound_id = "123456789"

print(mailer.delete_inbound_route()(sms_inbound_id))
```

## Sender Identities

### Get a list of sender identities
```python
from mailersend import sender_identities
from dotenv import load_dotenv

load_dotenv()

mailer = sender_identities.NewSenderIdentity(os.getenv('MAILERSEND_API_KEY'))

print(mailer.get_identities())
```

### Get a sender identity
```python
from mailersend import sender_identities
from dotenv import load_dotenv

load_dotenv()

mailer = sender_identities.NewSenderIdentity(os.getenv('MAILERSEND_API_KEY'))

print(mailer.get_identity(identity_id="12345"))
```

### Create a sender identity
```python
from mailersend import sender_identities
from dotenv import load_dotenv

load_dotenv()

mailer = sender_identities.NewSenderIdentity(os.getenv('MAILERSEND_API_KEY'))

print(mailer.create_identity(
    domain_id="123456",
    name="John Doe",
    email="email@domain.com",
    reply_to_email="reply@domain.com",
    reply_to_name="Doe John",
    add_note=True,
    personal_note="My awesome note",
))
```

### Update a sender identity
```python
from mailersend import sender_identities
from dotenv import load_dotenv

load_dotenv()

mailer = sender_identities.NewSenderIdentity(os.getenv('MAILERSEND_API_KEY'))

print(mailer.update_identity(
    identity_id="123456",
    domain_id="123456",
    name="Abe Doe",
    email="email@mydomain.com",
    reply_to_email="reply@mydomain.com",
    reply_to_name="Doe Abe",
    add_note=False
))
```

### Delete a sender identity
```python
from mailersend import sender_identities
from dotenv import load_dotenv

load_dotenv()

mailer = sender_identities.NewSenderIdentity(os.getenv('MAILERSEND_API_KEY'))

print(mailer.delete_identity(identity_id="123456"))
```

## API Quota
### Get API Quota
```python
from mailersend import api_quota
from dotenv import load_dotenv

load_dotenv()

mailer = api_quota.NewApiQuota(os.getenv('MAILERSEND_API_KEY'))

print(mailer.get_quota())
```

# Troubleshooting

## Emails not being sent

Print the output of `mailer.send()` to view status code and errors.

```python
from mailersend import emails

mailer = emails.NewEmail()

mail_body = {}

print(mailer.send(mail_body))
```

# Testing

TBD

<a name="endpoints"></a>
# Available endpoints

| Feature group     | Endpoint                                | Available |
|-------------------|-----------------------------------------|-----------|
| Activity          | `GET activity`                          | ✅         |
| Analytics         | `GET analytics`                         | ✅         |
| Domains           | `{GET, PUT, DELETE} domains`            | ✅         |
| Emails            | `POST send`                             | ✅         |
| Messages          | `GET messages`                          | ✅         |
| Recipients        | `{GET, DELETE} recipients`              | ✅         |
| Templates         | `{GET, DELETE} templates`               | ✅         |
| Tokens            | `{POST, PUT, DELETE} tokens`            | ✅         |
| Webhooks          | `{GET, POST, PUT, DELETE} webhooks`     | ✅         |
| SMS Sending       | `{POST} sms`                            | ✅         |
| SMS Activity      | `{GET} sms-activity`                    | ✅         |
| SMS Phone numbers | `{GET, PUT, DELETE} sms-numbers`        | ✅         |
| SMS Recipients    | `{GET, PUT} sms-recipients`             | ✅         |
| SMS Messages      | `{GET} sms-messages`                    | ✅         |
| SMS Webhooks      | `{GET, POST, PUT, DELETE} sms-webhooks` | ✅         |
| SMS Inbounds      | `{GET, POST, PUT, DELETE} sms-inbounds` | ✅         |
| Sender Identities | `{GET, POST, PUT, DELETE} identities`   | ✅         |
| API Quota         | `{GET} api-quota`                       | ✅         |

*If, at the moment, some endpoint is not available, please use other available tools to access it. [Refer to official API docs for more info](https://developers.mailersend.com/).*


<a name="support-and-feedback"></a>
# Support and Feedback

In case you find any bugs, submit an issue directly here in GitHub.

You are welcome to create SDK for any other programming language.

If you have any troubles using our API or SDK free to contact our support by email [info@mailersend.com](mailto:info@mailersend.com)

The official documentation is at [https://developers.mailersend.com](https://developers.mailersend.com)

<a name="license"></a>
# License

[The MIT License (MIT)](LICENSE)
