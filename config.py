from os import environ

GITLAB_TOKEN = environ.get('GITLAB_TOKEN', None)
GITLAB_PROJECTS_FILE = 'gitlab_projects.json'

GITHUB_TOKEN = environ.get('GITHUB_TOKEN', None)
GITHUB_PROJECTS_FILE = 'github_projects.jsonl'