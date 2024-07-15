# Problems and Solutions
In this file, I will state the problems I encountered during the development of this project as well as the corresponding solutions.

# Problem 1
Initially, I used a very simple API call [from weatherapi](http://api.weatherapi.com/v1/current.json?key=*********************&q=Hong Kong&aqi=no) to get the weather condition descriptive texts. One text describes a whole day's weather. For example, "patchy raining" or "clear". They are correct, because most of the time in a day, the weather is like how the text described. But the problem is, often, in Hong Kong, there will be case that most of the time in a day, it's clear like the text stated, but there might be sudden heavy rain lasting for a short period of time. In this case,  if we follow the program message to leave the umbrella home, we might be soaked by the rain.

# Solution to Problem 1
I want to be more precise about the raining reminder. So I decided to get all the raining periods in day to indicate them in the reminding message. Luckily, I found another more advanced API call [from weatherapi](http://api.weatherapi.com/v1/forecast.json?key=******************&q=Hong Kong&days=1&aqi=no&alerts=no) so I can get the weather condition descriptive texts for each hour in the current. By having the hourly weather condition texts, I can detect all the hours with raining related texts so that I can acquire all the raining periods in the current day to be dry in the sudden rain case.

# Problem 2
I need a platform to send notification to me. Initially, I decided to use email for notifications, specifically Gmail. I tried to set up app passwords and authentication but repeatedly failed to send messages, receiving the following error:
Failed to send email: (535, b'5.7.8 Username and Password not accepted. For more information, go to\n5.7.8 https://support.google.com/mail/?p=BadCredentials d2e1a72fcca58-70b7eb9c7d8sm2984381b3a.11 - gsmtp')
Next, I attempted to use the Gmail API to send emails but encountered another issue:
An error occurred: <HttpError 400 when requesting https://gmail.googleapis.com/gmail/v1/users/me/messages/send?alt=json returned "Precondition check failed.". Details: "[{'message': 'Precondition check failed.', 'domain': 'global', 'reason': 'failedPrecondition'}]">

Following these setbacks, I switched to AWS SES (Simple Email Service). After verifying my sender email, I faced a new problem: my Gmail account was in sandbox mode. This restriction meant I could only send emails to verified addresses. While I could verify my own and receive rain reminders, I also wanted others, including friends and my girlfriend, to receive these notifications easily. Verifying each email individually on the AWS SES console was too inconvenient. Switching to production mode required AWS approval, which involved providing an application website and usage details—an impractical and time-consuming process for a small Python automation project.

I soon realized that using email for notifications was overly complicated and inefficient. I then considered using iMessage but found it required a macOS development environment, whereas I use Windows.

# Solution to Problem 2
Finally, I turned to Telegram. With Telegram, I could create a bot in a channel, allowing the bot to send messages to the channel, enabling everyone to easily join and receive notifications. Telegram's API is straightforward and doesn't require complex authentication or app passwords. This approach proved to be much simpler and more efficient.

Here are the two lines of code that send a message via Telegram:

send_url = f'https://api.telegram.org/bot{bot_api_key}/sendMessage'
response = requests.get(send_url, params={'chat_id': channel_name, 'text': text})

This solution is significantly more efficient than the others I tried.

# Problem 3
In the test phase, I generated a lot of message in telegram. And it looks so overloaded with many message. I want the channel screen to be clean. I only want to see Today's message.

# Solution to Problem 3 -> Last_Message_ID.txt
My solution is to delete the previous message whenever a new message was sent. So I need to know the message ID of the last message to delete it. In order to do that, I created a separate file Last_Message_ID.txt to record the last message ID. Why in a separate file but not in the main function? Because every day when we run the script, all the variables in the main function will be refreshed as default, that is why we need a separate file to record the last message ID.


