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

Sending a basic email (requires the `MAILERSEND_API_KEY` environment variable).

``` python
import mailersend

mailer = mailersend.NewApiClient()

subject = "Subject"
text = "This is the text content"
html = "<p>This is the HTML content</p>"

my_mail = "owner@verified_domain.com
subscriber_list = [ 'pamela@dundermifflin.com',
'dwight@dunderfmifflin.com', 'jim@dundermifflin.com']

mailer.send(my_mail, subscriber_list, subject, html, text)

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