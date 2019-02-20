#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Alfred Item for pull request
"""

def reviewer_names(reviewers):
  reviewer_list = map(lambda reviewer: '@' + reviewer['author']['login'], reviewers)
  uniq_reviewers = list(set(reviewer_list))
  return ', '.join(uniq_reviewers)

def review_byline(pr):
  if len(pr.reviewers) == 0:
    return u'🍔 Waiting for review...'

  approved_reviewers = u'✅ {reviewers}'.format(
    reviewers=reviewer_names(pr.approved_reviewers)
  ) if len(pr.approved_reviewers) > 0 else None

  rejected_reviewers = u'❌ {reviewers}'.format(
    reviewers=reviewer_names(pr.rejected_reviewers)
  ) if len(pr.rejected_reviewers) > 0 else None

  return ', '.join(filter(None, (approved_reviewers, rejected_reviewers)))

def build_byline(pr):
  build_status = {
    'FAILURE': u'👎 build Failed',
    'SUCCESS': u'👍 build succeeded'    
  }.get(pr.build_status)
  return build_status or u'🤞 building...'

def merge_byline(pr):
  return {
    'MERGEABLE': u'❤️ no conflicts',
    'UNKNOWN': u'🤔 calculating conflicts...'
  }.get(pr.mergeable) or u'🔂 needs rebase'

class PullRequestItem:
  def __init__(self, pr):
    self.pull_request = pr
    self.title = '#{number} {title}'.format(number=pr.number, title=pr.title)
    self.subtitle = ' | '.join([review_byline(pr), build_byline(pr), merge_byline(pr)])
    self.arg = pr.url

  def itemize(self):
    return {
        'title': self.title,
        'subtitle': self.subtitle,
        'arg': self.arg
    }
  
  def itemize_landable(self):
    return {
        'title': self.title,
        'subtitle': u'🚢 {bn}'.format(bn=self.pull_request.branch_name),
        'arg': '{owner} {repo} {number} {branch_name}'.format(
          owner=self.pull_request.owner,
          repo=self.pull_request.repo,
          number=self.pull_request.number,
          branch_name=self.pull_request.branch_name
        )
    }
