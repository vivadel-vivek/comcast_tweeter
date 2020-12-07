# SETUP FOR THIS PROGRAM
## This file will explain how to use our comcast twitter bot.

### Get python set up
1. Download python https://www.python.org/ftp/python/3.9.0/python-3.9.0-macosx10.9.pkg
    - If you are on windows, be sure to add python to PATH when requested!
2. Download the zip file of this project (or download it with git) and unzip into a folder like "Documents"

### Create a twitter developer account
1. Log into twitter
2. Apply for a dev account here: https://developer.twitter.com/en/apply-for-access
3. Say you are a "Hobbyist", and you are "Making a bot", then click next
4. Put in whatever info is needed
5. Under the "What should we call you" input, say "comcast_tweeter"
6. Describe the app:
    This bot tweets at comcast when internet is out. The bot will log weekly outage time and tweet at comcast when internet returns after an outage to notify them of how long the internet was out, and how much that is costing the customer.
7. *Are you planning on analyzing twitter data?* No
8. *Will your app use Tweet, Retweet, like, follow, or Direct Message functionality?* Yes
9. Describe your usage of these features:
    The app will use python's Tweepy API to update twitter status and notify comcast when the host computer becomes disconnected from internet services.
10. *Do you plan to display Tweets or aggregate data about Twitter content outside of Twitter?* No
11. *Will your product, service or analysis make Twitter content or derived information available to a government entity?* No
12. Accept terms of use and submit.
13. Confirm/verify your email if needed for the dev account.
14. Name your app "Comcast Outage Tweeter" followed by your initials, eg "Comcast Outage Tweeter VS"
15. Go back to your Developer portal and the "Projects and Apps" tab
16. Click on your "Comcast Outage Tweeter" project
17. Under the "settings" tab scroll to "App Permissions" and hit "edit"
18. Click "Read, Write and Access direct messages" and save.
19. Go to the "keys and tokens" tab
20. Click "regenerate" for all keys
21. Copy your consumer API keys and paste them into the "info.yaml" file
22. Click "generate" for your access token and paste those tokens into the "info.yaml" file

### Set Your Info
1. Open "info.yaml"
2. If you've added your twitter keys, you can customize enter more data here:
    - Monthly comcast payment in dollars.
    - A custom message to go with your tweet. If you don't want a custom message, leave the message in the yaml file.

### Run the code!
- If you are on windows, you can double click "run_comcast_tweeter.bat" to run the code.
- If you are on mac (or you're a fancy windows user) you can right click "tweet_at_comcast.py", click "open with..." and open with "python launcher 3.app"

You should see a terminal pop up and install some python modules, then it'll start watching for when your power goes out and should tweet to comcast when it is restored!
