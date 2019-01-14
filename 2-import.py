#!/usr/bin/env python3
from github import Github
import config
import json
import jsonlines

gh = Github(config.GITHUB_TOKEN)
user = gh.get_user()

with open(config.GITLAB_PROJECTS_FILE, 'r') as f:
    gitlab_projects = json.load(f)

output = jsonlines.open('github_projects.jsonl', mode='w')
for gl_project in gitlab_projects:
    gh_params = {
        'name': gl_project['name'],
        'private': gl_project['visibility'] != 'public',
        'description': gl_project['description'] or '',
    }
    try:
        repo = user.create_repo(**gh_params)
        print('Created {} ({})'.format(repo.full_name, repo.html_url))
        gh_params['id'] = repo.id
        gh_params['full_name'] = repo.full_name
        gh_params['archive'] = gl_project['archived']
        repo.create_source_import(vcs='git', vcs_url=gl_project['url'], vcs_username='oauth2', vcs_password=config.GITLAB_TOKEN)
        gh_params['imported'] = True
        print('Import started from {}'.format(gl_project['url']))
    except Exception as e:
        print("Skipping {}: {}".format(gh_params['name'], repr(e)))
        gh_params['skipped'] = True
    finally:
        output.write(gh_params)
output.close()
