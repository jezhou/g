#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from github_api import GithubAPI
from string import Template

owner, repo, number, branch_name = sys.argv[1].split()

api = GithubAPI()

if api.merge_pull_request(owner, repo, number):
  api.delete_pull_request_ref(owner, repo, branch_name)
  print(u'Landed #{number}'.format(number=number))
else:
  print(u'Could not merge #{number}'.format(number=number))

