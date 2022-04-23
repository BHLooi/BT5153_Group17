import requests, re

#Website that lists top twitter accounts
url='https://viralpitch.co/topinfluencers/twitter/top-200-twitter-influencers/'

r=requests.get(url)

#Extract list of Twitter Accounts in the url through regular expressions pattern matching
accounts = re.findall('data-toggle="tooltip" title="(.*?)"',r.text)
for a in accounts:
    if a[:4] == 'View':
        accounts.remove(a)

#Extract Category of each Twitter Account using re
cats= re.findall('<div class="top-channel-item-cell top-channel-item-followers flex-2">(.*?)</div>', r.text.replace('\n',''))
for i in range(len(cats)):
    raw = cats[i]
    cats[i] = ', '.join(re.findall('<span class="inf_cntn">(.*?)</span>', raw))


#Consolidate Accounts and Categories to a DataFrame and save as csv
import pandas as pd
df=pd.DataFrame()
df['account'] = accounts
df['category'] = cats
df = df.drop_duplicates()
df.to_csv('Top_200.csv', index=False)


#Create a dictionary of {account: category}
accounts_dict = {}
for i in df.index:
    account = df['account'][i]
    category = df['category'][i]
    accounts_dict[account] = category


#start scraping each Twitter Account using snscrape library
import snscrape.modules.twitter as sntwitter
import csv

# open a file in the write mode
f = open('compiled tweets.csv', 'w')

# create csv writer
writer = csv.writer(f)

# write a row of column labels to the csv file
row = ['username', 'category', 'followers', 'date', 'url', 'tweet_id', 'content', 'replies', 'retweets', 'likes', 'quotes', 'in_reply_to']
writer.writerow(row)


# Creating list to append tweet data to
tweets_list1 = []
n=1

for account in accounts_dict:
    # Using TwitterSearchScraper to scrape data and append tweets to list

    for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:'+account+' since:2021-12-01').get_items()):
        try:
            in_reply_to = tweet.inReplyToUser.username
        except:
            in_reply_to = 'None'

        row= [tweet.user.username, accounts_dict[account], tweet.user.followersCount, tweet.date, tweet.url, tweet.id, tweet.content, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount , 
                             in_reply_to]
        writer.writerow(row)
    print(n, account, 'done')
    n+=1
    
# close the file
f.close()



