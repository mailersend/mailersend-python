from mailersend import sms_sending
from mailersend import sms_activity
from mailersend import sms_phone_numbers
from mailersend import sms_recipients
from mailersend import sms_messages
from mailersend import sms_webhooks


api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiY2ZhMzNhZmE1Y2FkMzRhN2FkYjY2YmE3YzlmMzNhZDViNjhhMmY1NzdkNDhlYjRmMzU4YWY3NDMzMTUwNmE0M2E5NGMzNzUzYTFhN2NjOWEiLCJpYXQiOjE2NTUyOTI5MzQuODM2NDU0LCJuYmYiOjE2NTUyOTI5MzQuODM2NDU5LCJleHAiOjQ4MTA5NjY1MzQuODMyMTg4LCJzdWIiOiIyOTU5MSIsInNjb3BlcyI6WyJlbWFpbF9mdWxsIiwiZG9tYWluc19mdWxsIiwiYWN0aXZpdHlfZnVsbCIsImFuYWx5dGljc19mdWxsIiwidG9rZW5zX2Z1bGwiLCJ3ZWJob29rc19mdWxsIiwidGVtcGxhdGVzX2Z1bGwiLCJzdXBwcmVzc2lvbnNfZnVsbCIsInNtc19mdWxsIl19.F9vzAC3MvJ24fIoaeGnBwfAjt5WnKpbVMx9JgotKnwCGQAbH8TCX-Z7yf9eoJKlKWq-7VhRfhvdJZac0NQ002WLUoO4tcvrzRvRKgKPxpEw7VFZb-5dkA3ndA0LmtCzKhqtWxe0I9K3WFuFqQrTHexfS6SlZMpLwoMrLiqZHaiMG7nqk4oZsyJGt4PtvlAtm3qU87tus7miF0YwQkccbglzeJhwmYk_z_skP3-Qjsxmeo1X9ruxgN5AvKjp3yb4GCTf8hvdxGPvr1WczBjKlscfwUP2odITZuvi06Oe-eX8qMK2W4Y-SauJFR7ZYCT6gix0edccdwSFABqJHnn0tmXu2qwt9-_n-qhNb7Wdc6Kbsy2Kfyge1e_0wbWXFr-mmUGXbpF7JPUMcI2hzr-SwtunnogArkmBdU1wZhpNchtKT1H1ra8XRwYGhzR2Te4y6lQTMVj5Nntx5aeJWj-TMpis65Nli4k4Kt-M5AdVVWCSPqAladRhQH2fnrlGhonqqDTJ-RJs7IaQYc9bJq_wfwnWk3O_tJ1Y8JLAA0dem-f3-4PWwm1vnwK1eC_JvH0cn3D8otWO3NghdnvRCJEZ120H8009XlZVDeb_TqWWt10DC1UgJ4cqzt5PY5c9r9TqayRwqywSffvIQSl2kduLQbA20egzAGkSWVllHpqV5NLU"

# mailer = sms_sending.NewSmsSending(api_key)
#
# number_from = "+18332552485"
# numbers_to = [
#     "+381600688008",
#     "+381642621087"
# ]
# text = "This is a test message"
#
# print(mailer.send_sms(number_from, ["+12513099289"], text))


# mailer = sms_activity.NewSmsActivity(api_key)
#
# sms_number_id = 1
# date_from = 1655157601
# date_to = 1655158601
# status = ["processed"]
# page = 1
# limit = 200

# response = mailer.get_activities(date_from=date_from, date_to=date_to)
# print(response)


# sms_message_id = "62a9d12b07852eaf2207b417"
# print(mailer.get_activity(sms_message_id))


# mailer = sms_phone_numbers.NewSmsNumbers(api_key)
# #print(mailer.get_phone_numbers(paused=False))
# #print(mailer.get_phone_number("9pq3enl6842vwrzx"))
# print(mailer.update_phone_number("9pq3enl6842vwrzx", False))

# mailer = sms_recipients.NewSmsRecipients(api_key)
#
# status = "active"
# sms_number_id = "9pq3enl6842vwrzx"
# # print(mailer.get_recipients(status=status, sms_number_id=sms_number_id))
# print(mailer.get_recipient("627e756fd30078fb2208cc87"))
# print(mailer.update_recipient("627e756fd30078fb2208cc87", "active"))

# mailer = sms_messages.NewSmsMessages(api_key)
#
# # print(mailer.get_messages())
#
# sms_message_id = "62a8f340569370cf820227f6"
# print(mailer.get_message(sms_message_id))

mailer = sms_webhooks.NewSmsWebhooks(api_key)

print(mailer.get_webhooks("9pq3enl6842vwrzx"))

url = "https://someurl.com"
name = "My fancy webhook", \
events = 
sms_number_id = "9pq3enl6842vwrzx"