#!/usr/bin/env python

import json
from github_api import GithubAPI

gql_query = open('./queries/pull_query.graphql', 'r').read()
api = GithubAPI()
pull_requests = api.execute(gql_query).pull_requests(reversed=True)

if len(pull_requests) > 0:
  alfred_items = {'items': map(lambda pr: pr.itemize(), pull_requests)}
  print(json.dumps(alfred_items))
else:
  print(json.dumps(
      {'items': [{
        'title': 'Go to /pulls',
        'arg': 'https://github.com/pulls/'
        }]}
  ))
