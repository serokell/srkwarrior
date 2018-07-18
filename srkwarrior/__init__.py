import json
import os
import subprocess

def project():
    return os.getenv('SRKWARRIOR_PROJECT', 'serokell')

def section():
    return os.getenv('SRKWARRIOR_SECTION', 'serokell')

def import_json(args):
    return json.loads(subprocess.check_output(args))
