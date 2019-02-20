#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from github_api import GithubAPI
from models.pull_request_item import PullRequestItem

gql_query = open('./queries/pull_query.graphql', 'r').read()
api = GithubAPI()
pull_requests = api.execute(gql_query).pull_requests(reversed=True)

def is_landable(pr):
  return pr.build_status == 'SUCCESS' and len(pr.approved_reviewers) > 0 and pr.mergeable == 'MERGEABLE'

landable_prs = filter(is_landable, pull_requests)

if len(landable_prs) > 0:
  alfred_items = {'items': map(lambda pr: PullRequestItem(pr).itemize_landable(), landable_prs)}
  print(json.dumps(alfred_items))
else:
  print(json.dumps(
      {'items': [{
        'title': u'🏖 Nothing to ship',
        'subtitle': "Let's get to work!",
        'arg': 'https://github.com/pulls/'
        }]}
  ))
