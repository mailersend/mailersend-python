<a href="https://www.mailersend.com"><img src="https://www.mailersend.com/images/logo.svg" width="200px"/></a>

MailerSend Python SDK

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md)

# Table of Contents

* [Installation](#installation)
* [Usage](#usage)
  * [Sending and email](#sending_an_email)
  * [Sending and email with CC and BCC](#cc_and_bcc)
  * [Sending an email with variables (simple personalisation)](#variables)
  * [Sending an email with personalization (advanced personalisation)](#personalization)
  * [Sending a template-based email](#template)
  * [Sending an email with attachment](#attachments)
  * [Activity API](#activity)
  * [Analytics API](#analytics)
  * [Domains API](#domains)
  * [Messages API](#messages)
  * [Recipients API](#recipients)
  * [Tokens API](#tokens)
  * [Webhooks API](#webhooks)
* [Support and Feedback](#support-and-feedback)
* [License](#license)

<a name="installation"></a>

# Installation

## Requirements

- Python > 3.6.1
- Python `pip`
- An API Key from [mailersend.com](https://www.mailersend.com)

## Setup

```bash
python -m pip install mailersend
```

<a name="usage"></a>

# Usage

<a name="sending_an_email"></a>
## Sending a basic email.

```python
import mailersend.emails.emails as emails

mailer = emails.NewEmail()

# define an empty dict to populate with mail values
mail_body = {}

recipients = [
    'your@client.com',
    'another@client.com
]

mailer.setMailFrom('my-verified@mail.com', mail_body)
mailer.setMailTo(recipients, mail_body)
mailer.setSubject("Hello!", mail_body)
mailer.setHTMLContent("This is the HTML content", mail_body)
mailer.setPlaintextContent("This is the text content", mail_body)

# using print() will also return status code and data
mailer.send(mail_body)
```

<a name="cc_and_bcc"></a>
## Sending an email with CC and BCC

Send an email with CC and BCC.

```python
import mailersend.emails.emails as emails

mailer = emails.NewEmail()

# define an empty dict to populate with mail values
mail_body = {}

recipients = [
    'your@client.com',
    'another@client.com
]

cc = [
    'yetanother@client.com',
]

bcc = [
    'myboss@company.com',
]

mailer.setMailFrom('my-verified@mail.com', mail_body)
mailer.setMailTo(recipients, mail_body)
mailer.setSubject("Hello!", mail_body)
mailer.setHTMLContent("This is the HTML content", mail_body)
mailer.setPlaintextContent("This is the text content", mail_body)
mailer.setCCRecipients(cc, mail_body)
mailer.setCCRecipients(bcc, mail_body)

mailer.send(mail_body)
```

<a name="variables"></a>
## Sending an email with variables (simple personalization)

```python
import mailersend.emails.emails as emails

mailer = emails.NewEmail()

# define an empty dict to populate with mail values
mail_body = {}

recipients = [
    'your@client.com',
    'another@client.com
]

variables = [
    {
        "email": "your@client.com",
        "substitutions": [
            {
                "var": "company",
                "value": "MailerSend"
            },
            {
                "var": "name",
                "value": "Mailer"
            }
        ]
    }
]


mailer.setMailFrom('my-verified@mail.com', mail_body)
mailer.setMailTo(recipients, mail_body)
mailer.setSubject("Hello from {$company}", mail_body)
mailer.setHTMLContent("This is the HTML content, {$name}", mail_body)
mailer.setPlaintextContent("This is the text content, {$name}", mail_body)
mailer.setSimplePersonalization(variables, mail_body)

mailer.send(mail_body)
```

<a name="personalization"></a>
## Sending an email with personalization (advanced personalization)

```python
import mailersend.emails.emails as emails

mailer = emails.NewEmail()

# define an empty dict to populate with mail values
mail_body = {}

recipients = [
    'your@client.com',
    'another@client.com
]

personalization = [
    {
        "email": "test@mailersend.com",
        "data": {
        "var": "value",
        "boolean": true,
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


mailer.setMailFrom('my-verified@mail.com', mail_body)
mailer.setMailTo(recipients, mail_body)
mailer.setSubject("Hello from {$company}", mail_body)
mailer.setHTMLContent("This is the HTML content, {$name}", mail_body)
mailer.setPlaintextContent("This is the text content, {$name}", mail_body)
mailer.setAdvancedPersonalization(personalization, mail_body)

mailer.send(mail_body)
```

<a name="template"></a>
## Sending a template-based email

```python
import mailersend.emails.emails as emails

mailer = emails.NewEmail()

# define an empty dict to populate with mail values
mail_body = {}

recipients = [
    'your@client.com',
    'another@client.com
]

variables = [
    {
        "email": "your@client.com",
        "substitutions": [
            {
                "var": "company",
                "value": "MailerSend"
            },
            {
                "var": "name",
                "value": "Mailer"
            }
        ]
    }
]


mailer.setMailFrom('my-verified@mail.com', mail_body)
mailer.setMailTo(recipients, mail_body)
mailer.setSubject("Hello from {$company}", mail_body)
mailer.setTemplate("templateID", mail_body)
mailer.setSimplePersonalization(variables, mail_body)

mailer.send(mail_body)
```

<a name="attachments"></a>
## Sending an email with attachment

```python
import mailersend.emails.emails as emails

mailer = emails.NewEmail()

# define an empty dict to populate with mail values
mail_body = {}

recipients = [
    'your@client.com',
    'another@client.com
]

variables = [
    {
        "email": "your@client.com",
        "substitutions": [
            {
                "var": "company",
                "value": "MailerSend"
            },
            {
                "var": "name",
                "value": "Mailer"
            }
        ]
    }
]

attachment = open('path-to-file', 'rb')
att_read = attachment.read()
att_base64 = base64.b64encode(bytes(att_read))
attachments = [
    {
        "id": "my-attached-file",
        "filename": "filename.pdf",
        "content": f"{att_base64.decode('ascii')}"
    }
]

mailer.setMailFrom('my-verified@mail.com', mail_body)
mailer.setMailTo(recipients, mail_body)
mailer.setSubject("Hello from {$company}", mail_body)
mailer.setHTMLContent("This is the HTML content, {$name}", mail_body)
mailer.setPlaintextContent("This is the text content, {$name}", mail_body)
mailer.setSimplePersonalization(variables, mail_body)
mailer.setAttachments(attachments, mail_body)

mailer.send(mail_body)
```
<a name="activity"></a>
## Activity

**List activities (simple)**

```python
import mailersend.activity.activity as activity

mailersend = activity.NewActivity()

mailersend.getDomainActivity("domain-id")
```

**List activities (full)**

```python
import mailersend.activity.activity as activity

mailersend = activity.NewActivity()

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

mailersend.getDomainActivity("domain-id", page, limit, date_from, date_to, events)
```

<a name="analytics"></a>
## Analytics

**Activity data by date**

```python
import mailersend.analytics.analytics as analytic

analytics = analytic.NewAnalytics()

date_from = 1623073576
date_to = 1623074976
events = [
    "processed",
    "sent",
]

# optional arguments
domain_id = "domain-id"
group_by = "days"

analytics.getActivityByDate(date_from, date_to, events, domain_id, group_by)
```

**Opens by country**

```python
import mailersend.analytics.analytics as analytic

analytics = analytic.NewAnalytics()

date_from = 1623073576
date_to = 1623074976

# optional arguments
domain_id = "domain-id"

analytics.getOpensByCountry(date_from, date_to, domain_id)
```

**Opens by user-agent name**

```python
import mailersend.analytics.analytics as analytic

analytics = analytic.NewAnalytics()

date_from = 1623073576
date_to = 1623074976

# optional arguments
domain_id = "domain-id"

analytics.getOpensByUserAgent(date_from, date_to, domain_id)
```

**Opens by reading environment**

```python
import mailersend.analytics.analytics as analytic

analytics = analytic.NewAnalytics()

date_from = 1623073576
date_to = 1623074976

# optional arguments
domain_id = "domain-id"

analytics.getOpensByReadingEnvironment(date_from, date_to, domain_id)
```

<a name="domains"></a>
## Domains

**Get all domains**

```python
import mailersend.domains.domains as domains

mailersend = domains.NewDomain()

mailersend.getDomains()
```

**Get a single domain**

```python
import mailersend.domains.domains as domains

mailersend = domains.NewDomain()

mailersend.getDomainByID("domain-id")
```

**Get a single domain using helper function**

```python
import mailersend.domains.domains as domains
import mailersend.utils.helpers as helpers

mailersend = domains.NewDomain()

mailersend.getDomainByID(helpers.getIDByName("domains","domain-name"))
```

**Delete a domain**

```python
import mailersend.domains.domains as domains

mailersend = domains.NewDomain()

mailersend.deleteDomain("domain-id")
```

**Get recipients for a domain**

```python
import mailersend.domains.domains as domains

mailersend = domains.NewDomain()

mailersend.getRecipientsForDomain("domain-id")
```

**Update domain settings**

You can find a full list of settings [here](https://developers.mailersend.com/api/v1/domains.html#request-body).

```python
import mailersend.domains.domains as domains

mailersend = domains.NewDomain()

mailersend.updateDomainSetting("domain-id", "send_paused", True)
```
## Messages

**List messages**

```python
import mailersend.messages.messages as messages

mailersend = messages.NewMessage()

mailersend.getMessages()
```

**Find a specific message**

```python
import mailersend.messages.messages as messages

mailersend = messages.NewMessage()

mailersend.getMessageByID("message-id")
```

<a name="recipients"></a>

## Recipients

**List recipients**

```python
import mailersend.recipients.recipients as recipients

mailersend = recipients.NewRecipient()

mailersend.getRecipients()
```

**List recipients in a specific domain**

```python
import mailersend.recipients.recipients as recipients

mailersend = recipients.NewRecipient()

mailersend.getRecipientsForDomain("domain-id")
```

**Find a specific recipient**

```python
import mailersend.recipients.recipients as recipients

mailersend = recipients.NewRecipient()

mailersend.getRecipientByID("recipient-id")
```

**Delete a recipient**

```python
import mailersend.recipients.recipients as recipients

mailersend = recipients.NewRecipient()

mailersend.deleteRecipient("recipient-id")
```

<a name="tokens"></a>

## Tokens

**Create a new token**

```python
import mailersend.token.token as token

mailersend = token.NewToken()

scopes = ["email_full", "analytics_read"]

mailersend.createToken("my-token", scopes)
```

Because of security reasons, we only allow access token appearance once during creation. In order to see the access token created you can do:

```python
import mailersend.token.token as token

mailersend = token.NewToken()

scopes = ["email_full", "analytics_read"]

print(mailersend.createToken("my-token", scopes))
```

**Pause / Unpause Token**

```python
import mailersend.token.token as token

mailersend = token.NewToken()

# pause
mailersend.freezeToken("my-token")

# unpause
mailersend.freezeToken("my-token", pause=False)
```

**Delete Token**

```python
import mailersend.token.token as token

mailersend = token.NewToken()

mailersend.deleteToken("token-id")
```

<a name="webhooks"></a>
## Webhooks

**List Webhooks**

```python
import mailersend.webhooks.webhooks as webhooks

mailersend = webhooks.NewWebhook()

mailersend.getWebhooks("domain-id")
```

**Find a Webhook**

```python
import mailersend.webhooks.webhooks as webhooks

mailersend = webhooks.NewWebhook()

mailersend.getWebhookByID("webhook-id")
```

**Create a Webhook**

```python
import mailersend.webhooks.webhooks as webhooks

webhookEvents = ['activity.sent', 'activity.delivered']

mailersend = webhooks.NewWebhook()
webhook.setWebhookURL("https://webhooks.mysite.com")
webhook.setWebhookName("my first webhook")
webhook.setWebhookEvents(webhookEvents)
webhook.setWebhookDomain("domain-id")

mailersend.createWebhook()
```

**Create a disabled Webhook**

```python
import mailersend.webhooks.webhooks as webhooks

webhookEvents = ['activity.sent', 'activity.delivered']

mailersend = webhooks.NewWebhook()
webhook.setWebhookURL("https://webhooks.mysite.com")
webhook.setWebhookName("my first webhook")
webhook.setWebhookEvents(webhookEvents)
webhook.setWebhookDomain("domain-id")
webhook.setWebhookEnabled(False)

mailersend.createWebhook()
```

**Update a Webhook**

```python
import mailersend.webhooks.webhooks as webhooks

mailersend = webhooks.NewWebhook()

mailersend.updateWebhook("webhook-id", "name", "a new webhook name")
```

**Disable/Enable a Webhook**

```python
import mailersend.webhooks.webhooks as webhooks

mailersend = webhooks.NewWebhook()

mailersend.updateWebhook("webhook-id", "enabled", False)
```

**Delete a Webhook**

```python
import mailersend.webhooks.webhooks as webhooks

mailersend = webhooks.NewWebhook()

mailersend.deleteWebhook("webhook-id")
```

*If, at the moment, some endpoint is not available, please use the `requests` package and other available tools to access it. [Refer to official API docs for more info](https://developers.mailersend.com/).*


<a name="support-and-feedback"></a>
# Support and Feedback

In case you find any bugs, submit an issue directly here in GitHub.

You are welcome to create SDK for any other programming language.

If you have any troubles using our API or SDK free to contact our support by email [info@mailersend.com](mailto:info@mailersend.com)

The official documentation is at [https://developers.mailersend.com](https://developers.mailersend.com)

<a name="license"></a>
# License

[The MIT License (MIT)](LICENSE.md)
