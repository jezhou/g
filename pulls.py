#!/usr/bin/env python

import requests
import json
import subprocess

github_api_url = 'https://api.github.com/graphql'
headers = {
    'authorization': 'bearer ***REMOVED***'
}

gqlQuery = """
query { 
  viewer { 
    login
    pullRequests(last:10) {
      nodes {
        title
        url
        updatedAt
        number
        reviews(states: [APPROVED, CHANGES_REQUESTED], last:10) {
        	nodes {
        	  id
            author {
              login
            }
            state
        	}
        }
      }
    }
  }
}
"""

r = requests.post(
    github_api_url,
    headers=headers,
    json={'query': gqlQuery}
)

pull_requests = r.json()['data']['viewer']['pullRequests']['nodes']
pull_requests = sorted(pull_requests, reverse=True,
                       key=lambda k: k['updatedAt'])


def get_subtitle(pr):
  subtitle = '#' + str(pr['number'])
  approved_reviewers = []
  rejected_reviewers = []
  for review in pr['reviews']['nodes']:
    if review['state'] == 'APPROVED':
      approved_reviewers += ['@' + review['author']['login']]
    elif review['state'] == 'CHANGES_REQUESTED':
      rejected_reviewers += ['@' + review['author']['login']]

  if len(approved_reviewers) > 0:
    white_check_mark = u'\U00002705'
    subtitle = white_check_mark + ' ' + subtitle
    approved_reviewers = 'Approved by: ' + ' ,'.join(approved_reviewers)
  elif len(rejected_reviewers) > 0:
    red_x = u'\U0000274C'
    subtitle = red_x + ' ' + subtitle
    approved_reviewers = 'Rejected by: ' + ' ,'.join(approved_reviewers) 
  else:
    red_circle = u'\U0001F354'
    subtitle = red_circle + ' ' + subtitle
    approved_reviewers = 'Needs Review'

  return subtitle + " | " + approved_reviewers


def pr_to_alfred_item(pr):
  return {
      'title': pr['title'],
      'subtitle': get_subtitle(pr),
      'arg': pr['url']
  }


alfred_items = {'items': map(pr_to_alfred_item, pull_requests)}

print(json.dumps(alfred_items))
