from serokellwarrior import taskwarrior, timewarrior, youtrack

import subprocess

def index_to_id(idx):
    return '@' + str(idx + 1)

EXPORT_TAG = 'serokellwarrior_is_exported'

def main():
    service = youtrack.service()

    # TODO: Timewarrior should implement a way to export all entries.
    # 2018-05-05 is when this program was first written, placing this
    # further in the past causes slower export.
    entries = timewarrior.project_entries(['2018-05-05', '-', 'tomorrow'])

    for idx, entry in enumerate(reversed(list(entries))):
        if {'start', 'end', 'uuid'} <= set(entry) and not entry.get(EXPORT_TAG):
            task = taskwarrior.import_task(entry['uuid'])
            if 'youtrackissue' in task and service.track_time(
                    task['youtrackissue'], entry['start'], entry['end']):
                subprocess.call([
                    'timew', 'tag', index_to_id(idx),
                    timewarrior.pair_tag(EXPORT_TAG, 'true')])
