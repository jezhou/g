class PullRequest:
  """
    Class data for pull request
  """
  def __init__(self, pr):
    self.id = pr['id']
    self.title = pr['title']
    self.number = pr['number']
    self.url = pr['url']
    self.build_status = pr['commits']['nodes'][0]['commit']['status']['state']
    self.mergeable = pr['mergeable']

    self.repo = pr['headRepository']['name']
    self.owner = pr['headRepositoryOwner']['login']

    self.branch_name = pr['headRef']['name']

    self.reviewers = pr.get('reviews', {}).get('nodes')
    self.approved_reviewers = []
    self.rejected_reviewers = []
    if len(self.reviewers) > 0:
      self.approved_reviewers = filter(lambda review: review['state'] == 'APPROVED', self.reviewers)
      self.rejected_reviewers = filter(lambda review: review['state'] == 'CHANGES_REQUESTED', self.reviewers)