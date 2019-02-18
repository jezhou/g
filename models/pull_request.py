#!/usr/bin/env python
# -*- coding: utf-8 -*-

def reviewer_names(reviewers):
  reviewer_list = map(lambda reviewer: '@' + reviewer['author']['login'], reviewers)
  uniq_reviewers = list(set(reviewer_list))
  return ', '.join(uniq_reviewers)

def generate_review_status(pr):
  if len(pr.reviewers) == 0:
    return u'🍔 Waiting for review...'

  approved_reviewers = None
  rejected_reviewers = None
  if len(pr.approved_reviewers) > 0:
    approved_reviewers = u'✅ {reviewers}'.format(
      reviewers=reviewer_names(pr.approved_reviewers)
    )

  if len(pr.rejected_reviewers) > 0:
    rejected_reviewers = u'❌ {reviewers}'.format(
      reviewers=reviewer_names(pr.rejected_reviewers)
    )

  return ', '.join(filter(None, (approved_reviewers, rejected_reviewers)))

def generate_build_status(pr):
  build_status = {
    'FAILURE': u'👎',
    'SUCCESS': u'👍'    
  }.get(pr.build_status)
  return build_status or u'🤞'

def generate_status(pr):
  reviewer_byline = generate_review_status(pr)
  build_byline = generate_build_status(pr)
  return ' | '.join([build_byline, reviewer_byline])


class PullRequest:
  def __init__(self, pr):
    self.title = pr['title']
    self.number = pr['number']
    self.url = pr['url']
    self.build_status = pr['commits']['nodes'][0]['commit']['status']['state']
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
