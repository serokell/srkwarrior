import json
import os
import subprocess

def project():
    return os.getenv('SEROKELLWARRIOR_PROJECT', 'serokell')

def section():
    return os.getenv('SEROKELLWARRIOR_SECTION', 'serokell')

def import_json(args):
    return json.loads(subprocess.check_output(args))
