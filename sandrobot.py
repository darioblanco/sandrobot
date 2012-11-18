# coding=utf-8

# Copyright (C) 2012  Darío Blanco Iturriaga

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random

from twitter.api import Twitter, TwitterError, TwitterHTTPError
from twitter.oauth import OAuth

from replies import SANDRO_REPLIES


BYE_MESSAGE = "Bendiciones y buenas noches"

# Words list that you will query to the Twitter API
QUERIES = [
    u"@SoySandroRey",
    u"Sandro Rey",
]

# Bot's Twitter account name
BOT_ACCOUNT = u"SoySandroRey"

# FILL THIS WITH YOUR PERSONAL TWITTER API KEYS
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''


def random_message():
    lucky_number = str(random.randint(10000, 99999)).encode('utf8')
    message = random.choice(SANDRO_REPLIES)
    try:
        message = message % lucky_number
    except TypeError:
        message = (u"Apunta tu número de la suerte, el {0}. Me equivoco "
                   "como cualquiera pero no miento.").format(lucky_number)
    return "{0} {1}".format(message, BYE_MESSAGE)


def twitter_search(query_string, last_id, twitter, poster):
    id = ''
    results = twitter.search(q=query_string,
                             since_id=last_id)['results']

    if not results:
        print '* No results this time...'
        return last_id

    users = []
    for result in results:
        message = result['text']
        user = result['from_user']
        # For avoiding replying twice
        if ((user in users) or (user == BOT_ACCOUNT)
                or message[0:16] == "RT @" + BOT_ACCOUNT
                or message[0:14] == "@" + BOT_ACCOUNT + ":"):
            print "* User already replied or same user"
            break
        else:
            users.append(user)
        id = str(result['id'])
        if id > last_id:  # Always give the greater id
            last_id = id

        # We append part of the ID to avoid duplicates.
        try:
            response_string = random_message()
            msg = '@{0} {1}'.format(user, response_string)
            poster.statuses.update(status=msg,
                                   in_reply_to_status_id=result['id'])
        except (TwitterError, TwitterHTTPError):
            print 'Error connecting to the Twitter API'
            pass

    return last_id


if __name__ == '__main__':
    # Twitter client for searching
    twitter = Twitter(domain='search.twitter.com')
    twitter.uriparts = ()

    # Getting the last id replied (for not answering the same accounts)
    f = open("lastids")
    last_id_replied = f.readline().replace('\n', '')
    f.close()

    # Twitter client for posting
    poster = Twitter(
        auth=OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                   CONSUMER_KEY, CONSUMER_SECRET),
        secure=True,
        api_version='1',
        domain='api.twitter.com'
    )

    # Queries:
    for query in QUERIES:
        last_id_replied = twitter_search(query, last_id_replied,
                                         twitter, poster)

    f = open("lastids", "w")
    f.write(last_id_replied + '\n')
    f.close()
