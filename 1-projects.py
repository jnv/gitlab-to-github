#!/usr/bin/env python3
import gitlab
import json
import config

def remap_project(project):
    return {
        'url': project.http_url_to_repo,
        'name': project.path,
        'archived': project.archived,
        'visibility': project.visibility,
        'description': project.description,
    }

gl = gitlab.Gitlab('https://gitlab.com', private_token=config.GITLAB_TOKEN)

projects = [remap_project(project) for project in gl.projects.list(owned=True, all=True)]
print('Writing {} projects to {}'.format(len(projects), config.GITLAB_PROJECTS_FILE))
with open(config.GITLAB_PROJECTS_FILE, mode='w') as projects_file:
    json.dump(projects, projects_file, indent=2)