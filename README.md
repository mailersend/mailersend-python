<a href="https://www.mailersend.com"><img src="https://www.mailersend.com/images/logo.svg" width="200px"/></a>

MailerSend Python SDK

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

# Table of Contents
- [Installation](#installation)
- [Usage](#usage)
    - [Email](#email)
        - [Send an email](#send-an-email)
        - [Add CC, BCC recipients](#add-cc-bcc-recipients)
        - [Send a template-based email](#send-a-template-based-email)
        - [Advanced personalization](#advanced-personalization)
        - [Simple personalization](#simple-personalization)
        - [Send email with attachment](#send-email-with-attachment)
    - [Activity](#activity)
        - [Get a list of activities (simple)](#get-a-list-of-activities-simple)
        - [Get a list of activities (full)](#get-a-list-of-activities-full)
    - [Analytics](#analytics)
        - [Activity data by date](#activity-data-by-date)
        - [Opens by country](#opens-by-country)
        - [Opens by user-agent name](#opens-by-user-agent-name)
        - [Opens by reading environment](#opens-by-reading-environment)
    - [Domains](#domains)
        - [Get a list of domains](#get-a-list-of-domains)
        - [Get a single domain](#get-a-single-domain)
        - [Get a single domain using helper function](#get-a-single-domain-using-helper-function)
        - [Delete a domain](#delete-a-domain)
        - [Get a list of recipients per domain](#get-a-list-of-recipients-per-domain)
        - [Update domain settings](#update-domain-settings)
    - [Messages](#messages)
        - [Get a list of messages](#get-a-list-of-messages)
        - [Get a single message](#get-a-single-message)
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
      - [Add recipients to unsubscribe list](#add-recipients-to-unsubcribe-list)
      - [Delete recipients from blocklist](#delete-recipients-from-blocklist)
      - [Delete hard bounced recipients](#delete-hard-bounced-recipients)
      - [Delete spam complaints](#delete-spam-complaints)
      - [Delete recipients from unsubscribe list](#delete-recipients-from-unsubscribe-list)
    - [Tokens](#tokens)
      - [Create a token](#create-a-token)
      - [Pause / Unpause Token](#pause--unpause-token)
      - [Delete a token](#delete-a-token)
    - [Webhooks](#webhooks)
      - [Get a list of webhooks](#get-a-list-of-webhooks)
      - [Get a single webhook](#get-a-single-webhook)
      - [Create a webhook](#create-a-webhook)
      - [Create a disabled webhook](#create-a-disabled-webhook)
      - [Update a Webhook](#update-a-webhook)
      - [Delete a Webhook](#delete-a-webhook)
- [Testing](#testing)
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
- A `MAILERSEND_API_KEY` environment variable

# Usage

## Email 

### Send an email

```python
from mailersend import emails

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

mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Hello!", mail_body)
mailer.set_html_content("This is the HTML content", mail_body)
mailer.set_plaintext_content("This is the text content", mail_body)

# using print() will also return status code and data
mailer.send(mail_body)
```

### Add CC, BCC recipients

```python
from mailersend import emails

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
mailer.set_simple_personalization(variables, mail_body)

mailer.send(mail_body)
```

### Advanced personalization

```python
from mailersend import emails

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
mailer.set_advanced_personalization(personalization, mail_body)

mailer.send(mail_body)
```

### Simple personalization

```python
from mailersend import emails

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
mailer.set_subject("Hello from {$foo}", mail_body)
mailer.set_html_content("This is the HTML content, {$foo}", mail_body)
mailer.set_plaintext_content("This is the text content, {$foo}", mail_body)
mailer.set_simple_personalization(variables, mail_body)

mailer.send(mail_body)
```

### Send email with attachment

```python
from mailersend import emails
import base64

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
        "content": f"{att_base64.decode('ascii')}"
    }
]

mailer.set_mail_from(mail_from, mail_body)
mailer.set_mail_to(recipients, mail_body)
mailer.set_subject("Hello from {$foo}", mail_body)
mailer.set_html_content("This is the HTML content, {$foo}", mail_body)
mailer.set_plaintext_content("This is the text content, {$foo}", mail_body)
mailer.set_simple_personalization(variables, mail_body)
mailer.set_attachments(attachments, mail_body)

mailer.send(mail_body)
```

<a name="activity"></a>

## Activity

### Get a list of activities (simple)

```python
from mailersend import activity

mailer = activity.NewActivity()

mailer.get_domain_activity("domain-id")
```

### Get a list of activities (full)

```python
from mailersend import activity

mailer = activity.NewActivity()

page = 1
limit = 20
date_from = 1623073576
date_to = 1623074976
events = [
    "processed",
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

mailer = analytics.NewAnalytics()

date_from = 1623073576
date_to = 1623074976
events = [
    "processed",
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

mailer = analytics.NewAnalytics()

date_from = 1623073576
date_to = 1623074976

# optional arguments
domain_id = "domain-id"

mailer.get_opens_by_country(date_from, date_to, domain_id)
```

### Opens by user-agent name

```python
from mailersend import analytics

mailer = analytics.NewAnalytics()

date_from = 1623073576
date_to = 1623074976

# optional arguments
domain_id = "domain-id"

mailer.get_opens_by_user_agent(date_from, date_to, domain_id)
```

### Opens by reading environment

```python
from mailersend import analytics

mailer = analytics.NewAnalytics()

date_from = 1623073576
date_to = 1623074976

# optional arguments
domain_id = "domain-id"

mailer.get_opens_by_reading_environment(date_from, date_to, domain_id)
```

## Domains

### Get a list of domains

```python
from mailersend import domains

mailer = domains.NewDomain()

mailer.get_domains()
```

### Get a single domain

```python
from mailersend import domains

mailer = domains.NewDomain()

mailer.get_domain_by_id("domain-id")
```

### Get a single domain using helper function

```python
from mailersend import domains
from mailersend import utils

mailer = domains.NewDomain()
helper = utils.NewHelper()

mailer.get_domain_by_id(helper.get_id_by_name("domains","domain-name"))
```

### Delete a domain

```python
from mailersend import domains

mailer = domains.NewDomain()

mailer.delete_domain("domain-id")
```

### Get a list of recipients per domain

```python
from mailersend import domains

mailer = domains.NewDomain()

mailer.get_recipients_for_domain("domain-id")
```

### Update domain settings

You can find a full list of settings [here](https://developers.mailersend.com/api/v1/domains.html#request-body).

```python
from mailersend import domains

mailer = domains.NewDomain()

mailer.update_domain_setting("domain-id", "send_paused", True)
```

## Messages

### Get a list of messages

```python
from mailersend import messages

mailer = messages.NewMessage()

mailer.get_messages()
```

### Get a single message

```python
from mailersend import messages

mailer = messages.NewMessage()

mailer.get_message_by_id("message-id")
```

## Recipients

### Get a list of recipients

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

mailer.get_recipients()
```

### Get a single recipient

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

mailer.get_recipient_by_id("recipient-id")
```

### Delete a recipient

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

mailer.delete_recipient("recipient-id")
```

### Get recipients from a blocklist

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

mailer.get_recipients_from_blocklist("domain-id")
```

### Get recipients from hard bounces

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

mailer.get_hard_bounces("domain-id")
```

### Get recipients from spam complaints

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

mailer.get_spam_complaints("domain-id")
```

### Get recipients from unsubscribes

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

mailer.get_unsubscribes("domain-id")
```

### Add recipients to blocklist

Using recipients:

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

recipient_list = [
    'blocked@client.com'
]

mailer.add_to_blocklist("domain-id", recipients=recipient_list)
```

Using patterns:

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

recipient_patterns = [
    '*@client.com'
]

mailer.add_to_blocklist("domain-id", patterns=recipient_patterns)
```

### Add hard bounced recipients

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

recipient_list = [
    "your@client.com"
]

mailer.add_hard_bounces("domain-id", recipient_list)
```

### Add spam complaints

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

recipient_list = [
    "your@client.com"
]

mailer.add_spam_complaints("domain-id", recipient_list)
```

### Add recipients to unsubscribe list

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

recipient_list = [
    "your@client.com"
]

mailer.add_unsubscribes("domain-id", recipient_list)
```

### Delete recipients from blocklist

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

recipient_list = [
    "your@client.com"
]

mailer.delete_from_blocklist("domain-id", recipient_list)
```

### Delete hard bounced recipients 

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

recipient_list = [
    "your@client.com"
]

mailer.delete_hard_bounces("domain-id", recipient_list)
```

### Delete spam complaints 

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

recipient_list = [
    "your@client.com"
]

mailer.delete_spam_complaints("domain-id", recipient_list)
```

### Delete recipients from unsubscribe list

```python
from mailersend import recipients

mailer = recipients.NewRecipient()

recipient_list = [
    "your@client.com"
]

mailer.delete_unsubscribes("domain-id", recipient_list)
```

## Tokens

### Create a token

```python
from mailersend import tokens

mailer = tokens.NewToken()

scopes = ["email_full", "analytics_read"]

mailer.create_token("my-token", scopes)
```

Because of security reasons, we only allow access token appearance once during creation. In order to see the access token created you can do:

```python
from mailersend import tokens

mailer = tokens.NewToken()

scopes = ["email_full", "analytics_read"]

print(mailer.create_token("my-token", scopes))
```

### Pause / Unpause Token

```python
from mailersend import tokens

mailer = tokens.NewToken()

# pause
mailer.update_token("my-token")

# unpause
mailer.update_token("my-token", pause=False)
```

### Delete a Token

```python
from mailersend import tokens

mailer = tokens.NewToken()

mailer.delete_token("token-id")
```

## Webhooks

### Get a list of webhooks

```python
from mailersend import webhooks

mailer = webhooks.NewWebhook()

mailer.get_webhooks("domain-id")
```

### Get a single webhook

```python
from mailersend import webhooks

mailer = webhooks.NewWebhook()

mailer.get_webhook_by_id("webhook-id")
```

### Create a Webhook

```python
from mailersend import webhooks

webhookEvents = ['activity.sent', 'activity.delivered']

webhook = webhooks.NewWebhook()
webhook.set_webhook_url("https://webhooks.mysite.com")
webhook.set_webhook_name("my first webhook")
webhook.set_webhook_events(webhookEvents)
webhook.set_webhook_domain("domain-id")

webhook.create_webhook()
```

### Create a disabled webhook

```python
from mailersend import webhooks

webhookEvents = ['activity.sent', 'activity.delivered']

webhook = webhooks.NewWebhook()
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

webhook = webhooks.NewWebhook()

webhook.update_webhook("webhook-id", "name", "a new webhook name")
```

### Disable/Enable a Webhook

```python
from mailersend import webhooks

webhook = webhooks.NewWebhook()

webhook.update_webhook("webhook-id", "enabled", False)
```

### Delete a Webhook

```python
from mailersend import webhooks

webhook = webhooks.NewWebhook()

webhook.delete_webhook("webhook-id")
```

# Testing

TBD

<a name="endpoints"></a>
# Available endpoints

| Feature group | Endpoint    | Available |
| ------------- | ----------- | --------- |
| Activity         | `GET activity` | ✅         |
| Analytics         | `GET analytics` | ✅         |
| Domains         | `{GET,PUT,DELETE} domains` | ✅         |
| Emails         | `POST send` | ✅         |
| Messages         | `GET messages` | ✅         |
| Recipients         | `{GET,DELETE} recipients` | ✅         |
| Templates         | `{GET,DELETE} templates` | ✅         |
| Tokens         | `{POST,PUT,DELETE} tokens` | ✅         |
| Webhooks         | `{GET,POST,PUT,DELETE} webhooks` | ✅         |

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