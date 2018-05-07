from datetime import datetime, timezone
from functools import partial
from serokellwarrior import import_json, project, taskwarrior

def _utc_to_local(dt):
    return dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

def parse_datetime(s):
    return _utc_to_local(datetime.strptime(s, '%Y%m%dT%H%M%SZ'))

PAIR_TAG_DELIMETER = '@=>'

def parse_pair_tag(s):
    pair = s.split(PAIR_TAG_DELIMETER, 1)

    if len(pair) == 2:
        return pair

def pair_tag(k, v):
    return k + PAIR_TAG_DELIMETER + v

def parse_entry(m):
    entry = dict(filter(None, map(parse_pair_tag, m.get('tags', {}))))

    for k in ['start', 'end']:
        if k in m:
            entry[k] = parse_datetime(m[k])

    return entry

def entries(interval):
    return map(parse_entry, import_json(['timew', 'export'] + interval))

def belongs_to_project(project, entry):
    if 'uuid' in entry:
        task = taskwarrior.import_task(entry['uuid'])
        if 'project' in task:
            return task['project'].startswith(project)

    return False

def project_entries(interval, project=project()):
    return filter(partial(belongs_to_project, project), entries(interval))
