def generate_subtitle(pr):
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

class PrAlfredItem:
  def __init__(self, pr):
    self.pull_request = pr

  def to_item(self):
    pr = self.pull_request
    return {
        'title': pr['title'],
        'subtitle': generate_subtitle(pr),
        'arg': pr['url']
    }
