# Bulk Migrate Repositories From GitLab to GitHub

A set of Python scripts to migrate repositories from GitLab to GitHub using [GitHub Importer](https://help.github.com/articles/importing-a-repository-with-github-importer/) (i.e. without creating a local clone).


## Prerequisities

- Python 3.7 or newer
- [Pipenv](https://pipenv.readthedocs.io/)

## Setup

Install dependencies by running `pipenv install`.

### Access Tokens

Create personal access token both for GitLab and GitHub.

For GitLab, visit [Settings / Access Tokens](https://gitlab.com/profile/personal_access_tokens). Create a new token with any name and the scopes: `api` and `read_repository`.

For GitHub, follow the [documentation](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/). Create a new token with scope `repo`.

Export the resulting tokens either as environment variables:

```sh
export GITLAB_TOKEN=<paste your GitLab token here>
export GITHUB_TOKEN=<paste your GitHub token here>
```

or modify [config.py](config.py) and paste the tokens as value of `GITLAB_TOKEN` and `GITHUB_TOKEN` respectively.

## Usage

With tokens setup, you can start import process. The process is separated into three phases.

### 1. Get a list of GitLab projects

Run:

```
pipenv run python 1-projects.py
```

This will create a file `gitlab_projects.json` with a list of projects to be imported in the following phase.
You can modify this list, for example change `name` property if you wish to import the project under different name, set `visibility` to `"private"` if the imported project should be private or delete the project completely if you don't wish to import it.

### 2. Create GitHub repositories and start import

Run:

```
pipenv run python 2-import.py
```

This will use a list of projects from the previous step, create a new repository (respecting privacy of the original project) and start an import task using the GitLab's HTTPS URL and access token. If the repository of the same name exists, it will be skipped. The results are stored into `github_projects.jsonl` file for the next step.

You will receive an e-mail from GitHub for each repository as the import finishes (or fails).

### 3. Archive imported repositories

Once the repositories are imported, you can optionally re-archive the imported GitHub repositories by running:

```
pipenv run python 3-archive.py
```

This will use the output file from the previous phase. Repositories which were skipped, not originally archived, or not completely imported will be ignored.

## License

MIT