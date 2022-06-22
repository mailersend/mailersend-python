from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    author='Igor Hrček',
    author_email='igor@mailerlite.com',
    description='The official MailerSend Python SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='mailersend',
    url='https://github.com/mailersend/mailersend-python',
    version='0.3.6',
)
