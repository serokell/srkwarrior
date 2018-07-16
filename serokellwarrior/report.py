from serokellwarrior import taskwarrior, timewarrior

import calendar
import sys

def uuids_by_date(interval):
    uuids_by_date = {}

    for entry in timewarrior.project_entries(interval):
        if 'start' in entry:
            start = entry['start']
            start_date = (start.year, start.month, start.day)

            uuids_by_date.setdefault(start_date, set())
            uuids_by_date[start_date].add(entry['uuid'])

    return uuids_by_date
    
def report(interval):
    for date, uuids in uuids_by_date(interval).items():
        print('{} {:02d}:'.format(calendar.month_abbr[date[1]], date[2]))

        for uuid in uuids:
            task = taskwarrior.import_task(uuid)
            if {'youtracknumber', 'youtrackproject', 'youtracksummary'} <= set(task):
                print(' * {}-{} {}'.format(
                    task['youtrackproject'],
                    task['youtracknumber'],
                    task['youtracksummary']))
                for annotation in task.get('annotations', []):
                    dt = timewarrior.parse_datetime(annotation['entry'])
                    # TODO: this presumes that interval always has one-day
                    # granularity, which will be false if you want to send
                    # a report more than once a day:
                    if (dt.year == date[0] and
                        dt.month == date[1] and
                        dt.day == date[2]):
                        print('   -', annotation['description'])

def main():
    report(sys.argv[1:])
