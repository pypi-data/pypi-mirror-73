import os
import tarfile

import click
import requests

from core.api_key import get_api_key, set_api_key, is_api_key_valid
from core.constants import ARCHIVE_FOR_SENDING_NAME, SEAMLESS_SERVICE_URL, ARCHIVE_SIZE_LIMIT, \
    EXCLUDE_FOLDERS_AND_FILES, SEAMLESS_SERVICE_RUN_ROUTE, SEAMLESS_SERVICE_PUBLISH_ROUTE, SEAMLESS_HOST


def _package_project(folder_to_archive):
    def filtr(file):
        for name in EXCLUDE_FOLDERS_AND_FILES:
            if file.name.startswith(f"./{name}"):
                return None
        return file

    tar = tarfile.open(ARCHIVE_FOR_SENDING_NAME, "w:gz")
    tar.add(folder_to_archive, filter=filtr)
    tar.close()
    # TODO we should have this limit only on server side and return meaningful error
    # TODO it should be doable with the production WSGI server and catching 413 error
    if os.stat(ARCHIVE_FOR_SENDING_NAME).st_size > ARCHIVE_SIZE_LIMIT:
        print(f"Your project is too big."
              f" After we compressed the folder {folder_to_archive} the resulting file is more than 10 MB."
              f"In order to have a really seamless experience we recommend to remove non-essential files."
              f"If you need to increase the limit - please shoot us an email at hello@seamlesscloud.io")
        exit(1)
    return ARCHIVE_FOR_SENDING_NAME


@click.group()
# This is just an entry point for the CLI, all other commands are registered in this group
def cli():
    pass


@cli.command()
def run():
    api_key = get_api_key()
    package_name = None
    try:
        package_name = _package_project(folder_to_archive='.')
        resp = requests.post(SEAMLESS_SERVICE_URL + SEAMLESS_SERVICE_RUN_ROUTE,
                             headers={'Authorization': api_key},
                             files={'seamless_project': open(package_name, 'rb')},
                             stream=True)
        resp.raise_for_status()
        for line in resp.iter_lines(decode_unicode=True, chunk_size=1):
            click.echo(line)
    finally:
        try:
            if package_name:
                os.remove(package_name)
        except OSError:
            pass


@cli.command()
@click.option(
    "--name",
    help="name of the job you publish",
    required=True
)
@click.option(
    "--schedule",
    help="cron expression that identifies the schedule your code runs on",
)
def publish(name, schedule):
    api_key = get_api_key()
    package_name = None
    try:
        package_name = _package_project(folder_to_archive='.')
        params = {'name': name}
        if schedule:
            click.echo(
                "By default if you publish your job schedule for the first time, it is disabled. "
                "You can enable the schedule in the web app."
            )
            params.update({'schedule': schedule})
        resp = requests.put(SEAMLESS_SERVICE_URL + SEAMLESS_SERVICE_PUBLISH_ROUTE,
                            params=params,
                            headers={'Authorization': api_key},
                            files={'seamless_project': open(package_name, 'rb')})
        resp.raise_for_status()
        data = resp.json()
        link_to_job = f"{SEAMLESS_HOST}/jobs/{data['job_id']}"
        if not data['existing_job']:
            click.echo(f"Congratulations, you have created a new job. "
                       f"You can find it at {link_to_job}")
        else:
            click.echo(f"Congratulations, you have updated your '{name}' job. "
                       f"You can find it at {link_to_job}")
    finally:
        try:
            if package_name:
                os.remove(package_name)
        except OSError:
            pass


@cli.command()
@click.option(
    "--api-key",
    "api_key",
    help="api-key to associate the user on this machine with",
    required=True
)
def init(api_key):
    if not is_api_key_valid(api_key):
        click.echo("The API KEY provided is not valid. "
                   "API key should be a sting exactly 20 characters long.")
        exit(0)
    set_api_key(api_key)
    click.echo("Welcome to the Seamless Cloud community! "
               "(TODO for developers: we need to generate a sample project at this point)")
