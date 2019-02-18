from datetime import datetime

class Review:
  def __init__(self, review):
    self.title = review['title']
    self.number = review['number']
    self.author = review['author']['login']
    self.url = review['url']
    self.createdAt = review['createdAt']

  def itemize(self):
    days_delta = datetime.today() - datetime.strptime(self.createdAt, '%Y-%m-%dT%H:%M:%SZ')
    return {
      'title': '#{number} {title}'.format(number=self.number, title=self.title),
      'subtitle': 'By @{author}, created {days_ago} days ago'.format(
        author=self.author,
        days_ago=days_delta.days
      )
    }