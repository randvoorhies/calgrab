#!/usr/bin/env python
try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import time
import datetime
import os
import sys

# Make sure the ~/.calgrabrc file exists
calgrabrc = os.environ['HOME'] + '/.calgrabrc'
if not os.path.exists(calgrabrc):
  sys.stderr.write('No ' + calgrabrc + ' settings file found. See the README for details.')
  exit(-1)

# A little functional programming magic to parse our settings file
settings = dict(map(str.strip, line.split(':',1)) for line in open(calgrabrc).read().strip().splitlines())

username   = settings['username']
visibility = settings['visibility']

query = gdata.calendar.client.CalendarEventQuery()
query.start_min = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000-07:00') 
query.start_max = (datetime.datetime.now() + datetime.timedelta(days=20)).strftime('%Y-%m-%dT%H:%M:%S.000-07:00')

calendar_client = gdata.calendar.client.CalendarClient()
projection = 'full'
feed_uri = calendar_client.GetCalendarEventFeedUri(calendar=username, visibility=visibility, projection=projection)

events = {}

feed = calendar_client.GetCalendarEventFeed(q=query, uri=feed_uri)
for i, an_event in enumerate(feed.entry):
    for a_when in an_event.when:
      time_format='%Y-%m-%dT%H:%M:%S'
      try:
        start_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(a_when.start.split('.')[0], time_format)))
        end_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(a_when.end.split('.')[0], time_format)))

        events[start_time] = []
        events[start_time].append(an_event)
      except:
        pass

day = ''
dates = events.keys()
dates.sort()
for date in dates:
  for event in events[date]:
    eventstr = ''
    curr_day = date.strftime('%A')
    if date != dates[0]:
      eventstr = '\n'
    if curr_day != day:
      eventstr += '{0:<10}'.format(curr_day) + '@' 
      day = curr_day
    else:
      eventstr = '{0:<10}'.format('') + '@' 
    eventstr += '{0:<6}'.format(date.strftime(' %I:%M%p')) + ' - ' + event.title.text
    print eventstr


