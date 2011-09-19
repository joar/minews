import re
import datetime


from jinja2 import Environment, PackageLoader


TEMPLATE_ENV = Environment(
    loader=PackageLoader('minews', 'templates'),
    autoescape=False)

def get_template(*args):
    return TEMPLATE_ENV.get_template(*args)

def generate_entries(query, db = None, project = None):
    project_data = dict()

    for entry in query:
        if not project:
            try: 
                entry['project_data'] = project_data[entry['project']]
            except KeyError:
                entry['project_data'] = db.ProjectEntry.find_one({'_id': entry['project']})
                project_data[entry['project']] = entry['project_data']
        else:
            entry['project_data'] = project

        yield entry
