#!/usr/bin/env python

import json
from github_api import GithubAPI
from pr_alfred_item import PrAlfredItem

gql_query = open('./queries/pull_query.graphql', 'r').read()
api = GithubAPI()
pull_requests = api.execute(gql_query).pull_requests(reversed=True)

# Function to map PRs to Alfred Items, which can be used in script filters
mapPrToAlfredItem = lambda pr: PrAlfredItem(pr).to_item()

alfred_items = {'items': map(mapPrToAlfredItem, pull_requests)}

print(json.dumps(alfred_items))
