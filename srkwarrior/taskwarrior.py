from srkwarrior import import_json

def import_task(selector):
    return import_json(['task', selector, 'export'])[0]
