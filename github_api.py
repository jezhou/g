import requests
from models.pull_request import PullRequest
from models.review import Review

class GithubAPI:
  def __init__(self):
    self.github_api_url = 'https://api.github.com/graphql'
    self.github_api_rest_url = 'https://api.github.com'
    self.token = open('.github_token', 'r').read()
    self.headers = {
        'authorization': 'bearer {token}'.format(token=self.token)
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

  def pending_reviews(self):
    reviews = self.response['data']['search']['nodes']
    return map(lambda r: Review(r), reviews)

  def merge_pull_request(self, owner, repo, number):
    r = requests.put(
      '{base_url}/repos/{owner}/{repo}/pulls/{number}/merge'.format(
        base_url=self.github_api_rest_url,
        owner=owner,
        repo=repo,
        number=number
      ),
      headers={'authorization': 'token {token}'.format(token=self.token)},
      json={'merge_method': 'squash'}
    )

    # Gets merged status as true or false (This is why I hate python)
    return not not r.json().get('merged')

  def delete_pull_request_ref(self, owner, repo, branch_name):
    r = requests.delete(
      '{base_url}/repos/{owner}/{repo}/git/refs/heads/{branch_name}'.format(
        base_url=self.github_api_rest_url,
        owner=owner,
        repo=repo,
        branch_name=branch_name
      ),
      headers={'authorization': 'token {token}'.format(token=self.token)}
    )

    return r
