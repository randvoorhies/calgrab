try:
  from xml.etree import ElementTree
except ImportError:
  from elementtree import ElementTree
import gdata.calendar.data
import gdata.calendar.client
import gdata.acl.data
import atom
import getopt
import sys
import string
import time
import datetime


query = gdata.calendar.client.CalendarEventQuery()
query.start_min = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000-07:00') 
query.start_max = (datetime.datetime.now() + datetime.timedelta(days=14)).strftime('%Y-%m-%dT%H:%M:%S.000-07:00')

calendar_client = gdata.calendar.client.CalendarClient()
username = 'rand.voorhies@gmail.com'
visibility = open('/Users/rand/bin/calgrab_visibility.txt', 'r').read().strip()
projection = 'full'
feed_uri = calendar_client.GetCalendarEventFeedUri(calendar=username, visibility=visibility, projection=projection)

events = {}

feed = calendar_client.GetCalendarEventFeed(q=query, uri=feed_uri)
for i, an_event in enumerate(feed.entry):
    for a_when in an_event.when:
      time_format='%Y-%m-%dT%H:%M:%S'
      start_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(a_when.start.split('.')[0], time_format)))
      end_time = datetime.datetime.fromtimestamp(time.mktime(time.strptime(a_when.end.split('.')[0], time_format)))

      events[start_time] = []
      events[start_time].append(an_event)

day = ''
dates = events.keys()
dates.sort()
for date in dates:
  for event in events[date]:
    eventstr = ''
    curr_day = date.strftime('%A')
    if curr_day != day:
      print ''
      eventstr = '{:<10}'.format(curr_day) + '@' 
      day = curr_day
    else:
      eventstr = '{:<10}'.format('') + '@' 
    eventstr += '{:<6}'.format(date.strftime(' %I:%M%p')) + ' - ' + event.title.text
    print eventstr


