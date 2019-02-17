import requests
from pull_request import PullRequest

class GithubAPI:
  def __init__(self):
    self.github_api_url = 'https://api.github.com/graphql'
    self.headers = {
        'authorization': 'bearer ***REMOVED***'
    }

  def execute(self, query):
    r = requests.post(
        self.github_api_url,
        headers=self.headers,
        json={'query': query}
    )

    self.response = r.json()
    return self

  # Raw JSON response
  def json_response(self):
    return self.response

  def pull_requests(self, reversed=False):
    prs = self.response['data']['viewer']['pullRequests']['nodes']
    if(reversed):
      prs = sorted(prs, reverse=True, key=lambda k: k['updatedAt'])
    
    return map(lambda pr: PullRequest(pr), prs)
