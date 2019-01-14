#!/usr/bin/env python3
from github import Github
import config
import jsonlines

gh = Github(config.GITHUB_TOKEN)

with jsonlines.open(config.GITHUB_PROJECTS_FILE) as reader:
    for repo_data in reader:
        try:
            name = repo_data.get('full_name', repo_data.get('name'))
            print('Repo {}:'.format(name), end=' ')
            id = repo_data.get('id', None)
            if not id:
                print('No ID found, skipping.')
                continue
            if not repo_data.get('archive', False):
                print('Not to be archived, skipping.')
                continue
            repo = gh.get_repo(id, lazy=True)
            if repo.archived:
                print('Already archived, skipping.')
                continue
            import_status = repo.get_source_import()
            if import_status.status != 'complete':
                print('Import status: {}, skipping.'.format(import_status.status))
                continue
            repo.edit(archived=True)
            print('Archived')
        except Exception as e:
            print('Error: {}'.format(repr(e)))