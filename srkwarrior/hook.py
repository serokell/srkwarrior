from srkwarrior import timewarrior

import json
import subprocess
import sys

def read_line():
    return json.loads(sys.stdin.readline())

def start_or_stop(old, new):
    start_or_stop = None
    
    if 'start' in new and 'start' not in old:
        start_or_stop = 'start'
    elif 'start' not in new and 'start' in old:
        start_or_stop = 'stop'

    return start_or_stop

def main():
    old = read_line()
    new = read_line()
    print(json.dumps(new))
    
    verb = start_or_stop(old, new)

    if verb:
        tags = [timewarrior.pair_tag(k, new[k]) for k in ['project', 'uuid']]
        subprocess.call(["timew", verb, new['description']] + tags + [":yes"])
