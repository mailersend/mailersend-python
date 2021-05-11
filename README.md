<a href="https://www.mailersend.com"><img src="https://www.mailersend.com/images/logo.svg" width="200px"/></a>

MailerSend Python SDK

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE.md)

# Table of Contents
* [Installation](#installation)
* [Usage](#usage)
* [Testing](#testing)
* [Support and Feedback](#support-and-feedback)
* [License](#license)

<a name="installation"></a>
# Installation

```
$ python3 -m pip install mailersend
```

<a name="usage"></a>
# Usage

### Requires the `MAILERSEND_API_KEY` environment variable

### Sending a basic email.

``` python
import mailersend

mailer = mailersend.NewApiClient()

subject = "Subject"
text = "This is the text content"
html = "<p>This is the HTML content</p>"

my_mail = "owner@verified_domain.com"
recipient_list = [ 'pamela@dundermifflin.com',
'dwight@dunderfmifflin.com', 'jim@dundermifflin.com']

mailer.send(my_mail, recipient_list, subject, html, text, None, None)
```

### Sending a basic email using template ID.

``` python
import mailersend

mailer = mailersend.NewApiClient()

subject = "Subject"
template_id = '351ndrxrx45zqx8k'

my_mail = "owner@verified_domain.com"
recipient_list = [ 'pamela@dundermifflin.com',
'dwight@dunderfmifflin.com', 'jim@dundermifflin.com']

mailer.send(my_mail, recipient_list, subject, None, None, template_id, None)
```

### Sending an email with simple personalization.

``` python
import mailersend

mailer = mailersend.NewApiClient()

subject = "Hello from {$company}"
text = "This is the text content"
html = "<p>This is the HTML content, {$name}</p>"

my_mail = "owner@verified_domain.com"
recipient_list = [ 'pamela@dundermifflin.com',
'dwight@dunderfmifflin.com', 'jim@dundermifflin.com']
variables = [{
    "email": "pamela@dundermifflin.com",
    "substitutions": [{
        "var": "name",
        "value": "Pam",
    },
    {
        "var": "company",
        "value": "Dunder Mifflin",
    },]
}]

mailer.send(my_mail, recipient_list, subject, html, text, None, variables)
```

### Get ID by name

This helper function allows to programatically gather IDs for domains and subscribers for later
use in the code. Takes 2 arguments, `category` and `name`, and returns the respective ID of the searched-for item.

Available options for category:
 
- domains
- recipients



``` python
import mailersend

mailer = mailersend.NewApiClient()

mailer.getIdByName("domains", "mailersend.com")
```

### Get activity list

The activity list can be filtered using the [available query parameters](https://developers.mailersend.com/api/v1/activity.html#request-parameters),
found at [MailerSend official documentation](https://developers.mailersend.com).

``` python
import mailersend

mailer = mailersend.NewApiClient()

mailer.getDomainActivity("DOMAIN_ID")

```

### Get domain list

The activity list can be filtered using the [available query parameters](https://developers.mailersend.com/api/v1/domains.html#get-a-list-of-domains),
found at [MailerSend official documentation](https://developers.mailersend.com).

``` python
import mailersend

mailer = mailersend.NewApiClient()

mailer.getDomains("DOMAIN_ID")

```

### Update domain settings

There is a function that can be used per domain setting ([available domain settings](https://developers.mailersend.com/api/v1/domains.html#update-domain-settings)).

A full example for all domain settings is showcased here:

``` python
import mailersend

mailer = mailersend.NewApiClient()

# enable send_paused
mailer.sendPaused('<domainID>', True)

# enable clicks tracking
mailer.trackClicks('<domainID>', True)

# enable opens tracking
mailer.trackOpens('<domainID>', True)

# enable unsubscribes tracking
mailer.trackUnsubscribe('<domainID>', True)

# add unsubscribe custom plaintext string
mailer.trackUnsubscribePlain('<domainID>', 'Click here to unsubscribe')

# add unsubscribe custom HTML string
mailer.trackUnsubscribeHtml('<domainID>', '<p>Click here to <a href=\"{$unsubscribe}\">unsubscribe<\/a><\/p>')

# enable content tracking
mailer.trackContent('<domainID>', True)

# enable custom tracking
mailer.customTracking('<domainID>', True)

# set custom tracking subdomain
mailer.setCustomTrackingSubdomain('<domainID>', 'track.dundermifflin.com')
```

### Delete a domain

```python
import mailersend

mailer = mailersend.NewApiClient()

mailer.deleteDomain(mailer.getIdByName('<domainID>')
```

<a name="testing"></a>

# Testing

To be implemented

<a name="support-and-feedback"></a>
# Support and Feedback

In case you find any bugs, submit an issue directly here in GitHub.

You are welcome to create SDK for any other programming language.

If you have any troubles using our API or SDK free to contact our support by email [info@mailersend.com](mailto:info@mailersend.com)

The official documentation is at [https://developers.mailersend.com](https://developers.mailersend.com)

<a name="license"></a>
# License

[The MIT License (MIT)](LICENSE)
