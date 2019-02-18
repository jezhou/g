#!/usr/bin/env python

import json
from github_api import GithubAPI

gql_query = open('./queries/reviews_query.graphql', 'r').read()
api = GithubAPI()
reviews = api.execute(gql_query).pending_reviews()

if len(reviews) > 0:
  alfred_items = {'items': map(lambda review: review.itemize(), reviews)}
  print(json.dumps(alfred_items))
else:
  broom_emoji = u'\U0001F9F9'
  print(json.dumps(
    { 'items': [{
      'title': u'{emoji} Completed all reviews'.format(emoji=broom_emoji),
      'subtitle': 'Nice job! Go to /reviews-requested anyway.',
      'arg': 'https://github.com/pulls/review-requested'
    }] }
  ))
