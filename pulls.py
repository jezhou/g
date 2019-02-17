#!/usr/bin/env python

import json
from github_api import GithubAPI

gql_query = open('./queries/pull_query.graphql', 'r').read()
api = GithubAPI()
pull_requests = api.execute(gql_query).pull_requests(reversed=True)
alfred_items = {'items': map(lambda pr: pr.itemize(), pull_requests)}

print(json.dumps(alfred_items))
