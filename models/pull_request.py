def reviewer_names(reviewers):
  return ' ,'.join(map(lambda reviewer: '@' + reviewer['author']['login'], reviewers))

def generate_status(pr):
  if len(pr.reviewers) == 0:
    red_circle = u'\U0001F354'
    return '{emoji} Needs Review'.format(emoji=red_circle)

  approved_reviewers = None
  rejected_reviewers = None
  if len(pr.approved_reviewers) > 0:
    white_check_mark = u'\U00002705'
    approved_reviewers = u'{emoji} Approved by: {reviewers}'.format(
      emoji=white_check_mark,
      reviewers=reviewer_names(pr.approved_reviewers)
    )

  if len(pr.rejected_reviewers) > 0:
    red_x = u'\U0000274C'
    rejected_reviewers = u'{emoji} Rejected by: {reviewers}'.format(
      emoji=red_x,
      reviewers=reviewer_names(pr.rejected_reviewers)
    )

  return approved_reviewers or rejected_reviewers

class PullRequest:
  def __init__(self, pr):
    self.title = pr['title']
    self.number = pr['number']
    self.url = pr['url']
    self._set_reviewers(pr)

  def _set_reviewers(self, pr):
    self.reviewers = pr['reviews']['nodes']
    self.approved_reviewers = filter(lambda review: review['state'] == 'APPROVED', self.reviewers)
    self.rejected_reviewers = filter(lambda review: review['state'] == 'CHANGES_REQUESTED', self.reviewers)

  def itemize(self):
    return {
        'title': '#{number} {title}'.format(number=self.number, title=self.title),
        'subtitle': generate_status(self),
        'arg': self.url
    }
