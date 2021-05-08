STOCK = "TSLA"
COMPANY_NAME = "tesla"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

import os, requests, json
from datetime import datetime, timedelta
import smtplib

## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
# HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
# HINT 2: Work out the value of 5% of yerstday's closing stock price.
api_price_key = os.environ.get("APIVANTAGE_API_KEY")
news_api_key = os.environ.get("NEWS_API_KEY")
my_email = "arun.dvlpr01123@gmail.com"
password = "Muruga123#"

stock_price_parameter = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_price_key
}

news_parameter = {
    "q": COMPANY_NAME,
    "from": (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'),
    "sortBy": "publishedAt",
    "language": "en",
    "apiKey": news_api_key
}


def get_price(day):
    counter = 1
    price_date = day
    has_error = True
    price_response = requests.get(STOCK_ENDPOINT, params=stock_price_parameter).json()

    while has_error:
        price_date_formatted = (price_date - timedelta(days=counter)).strftime('%Y-%m-%d')

        try:
            stock_price = price_response['Time Series (Daily)']

        except KeyError:
            counter += 1
        else:

            close_price = list(stock_price.items())[1:3]
            print(close_price)
            return close_price


def get_news():
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameter).json()['articles']
    top_news_list = news_response[0:10]
    return top_news_list


close_price_yesterday = dict(get_price(datetime.today())[0][1])
close_price_yesterday_before = dict(get_price(datetime.today())[1][1])
price_difference = float(close_price_yesterday['4. close']) - float(close_price_yesterday_before['4. close'])
percentage_diff = abs((price_difference * 100) / float(close_price_yesterday_before['4. close']))
actual_percent = (price_difference * 100) / float(close_price_yesterday_before['4. close'])
print(percentage_diff)
## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
# HINT 1: Think about using the Python Slice Operator
if (percentage_diff <= 5):
    raw_news_list = get_news()
    formatted_news_list = []
    for news in raw_news_list:
        temp_dict = {'Headline': news['title'], 'Brief': news['content']}
        formatted_news_list.append(temp_dict)
    print(formatted_news_list)
news_body = f"The Stock {STOCK} has changed by {actual_percent}\n\n"
for news in formatted_news_list:
    news_body += ("HEADLINE: " + news['Headline'] + "\n" + "BREIF: " + "\n" + news['Brief'] + "\n")
print(news_body)
# STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
# HINT 1: Consider using a List Comprehension.
connection = smtplib.SMTP("smtp.gmail.com", 587)
connection.starttls()
connection.login(user=my_email, password=password)
connection.sendmail(from_addr=my_email, to_addrs="textile.arun@gmail.com",
                    msg=f"Subject:STOCK ALERT\n\n{str(news_body.encode('ascii', 'replace'))}")
connection.close()

# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
