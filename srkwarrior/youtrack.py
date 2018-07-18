from bugwarrior.config import load_config
from bugwarrior.services.youtrack import YoutrackService as YoutrackParent 
from srkwarrior import section

import json
import math

def date(end):
    return int(end.timestamp()) * 1000

def duration(start, end):
    return math.ceil((end - start).total_seconds() / 60)

def work_item(start, end):
    return json.dumps({'date': date(end),
                       'description': '',
                       'duration': duration(start, end)})

class YoutrackService(YoutrackParent):
    def __init__(self, *args, **kw):
        super(YoutrackService, self).__init__(*args, **kw)
        self.session.headers['Content-Type'] = 'application/json'

    def track_time(self, issue, start, end):
        url = self.rest_url + '/issue/' + issue + '/timetracking/workitem'
        return self.session.post(url, data=work_item(start, end)).ok

MAIN_SECTION = 'general'

def service(target=section()):
    return YoutrackService(load_config(MAIN_SECTION), MAIN_SECTION, target)
