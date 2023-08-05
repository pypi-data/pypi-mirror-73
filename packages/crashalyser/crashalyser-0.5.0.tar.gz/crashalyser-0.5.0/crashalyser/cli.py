import os
import sys
import click
import glob
import subprocess
import re
import configparser
import smtplib
import platform
from crontab import CronTab
from email.message import EmailMessage
from pathlib import Path
from datetime import datetime, timezone

if __name__ == "__main__" and __package__ is None:
    script = Path(__file__).resolve()
    parent, top = script.parent, script.parents[1]
    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError:  # Already removed
        pass

    __package__ = 'crashalyser'

from . import __version__

config_ini = {
    'smtp.host': 'some.smtp.server',
    'smtp.port': '25',
    'smtp.tls': 'false',
    'smtp.user': 'smtp_user',
    'smtp.password': 'smtp_password',
    'smtp.fromaddr': 'user@domain.com'
}

merged_config = {}


@click.version_option(__version__)
@click.group()
def cli():
    global merged_config
    merged_config = {**config_ini, **(read_config())}


@cli.command()
def config():
    pass


@cli.command()
@click.option('--path', default='/var/crash/*.core', help="path glob to process")
@click.option('--email', default=None, help="email address to send crash report to")
@click.option('--file', default=None, help="file to output crash report to")
@click.option('--user', default='root', help="user that will run cronjob")
@click.option('--schedule', default='', help="cron expression schedule")
def install(email, file, path, user, schedule):
    tab_file = '/etc/cron.d/crashalyser'

    if not os.path.exists(tab_file):
        with open(tab_file, mode='a'):
            pass

    cron = CronTab(tabfile=tab_file, user=False)
    cron.remove_all()

    command = f'crashalyser run --path {path}'
    if email:
        command = command + f' --email {email}'
    if file:
        command = command + f' --file {file}'

    job = cron.new(command=command, user=user)
    job.user = user
    job.setall(schedule)

    cron.write()


@click.option('--path', default='/var/crash/*.core', help="path glob to process")
@click.option('--email', default=None, help="email address to send crash report to")
@click.option('--file', default=None, help="file to output crash report to")
@cli.command()
def run(email, file, path):
    global merged_config
    files_to_process = glob.glob(path)

    if len(files_to_process) == 0:
        click.echo(f'WARNING: path "{path}" is either invalid or has no files to process')
        click.echo("Exiting...")
        sys.exit(0)

    aggregate_output = bytearray()
    success = []

    for coredump in files_to_process:
        coredump_abs = os.path.abspath(coredump)
        process_core_output = subprocess.run(["gdb", "--batch", "-c", coredump_abs], stdout=subprocess.PIPE)
        match_exe = re.search(r"\/(.+\/[^/|^']+)", process_core_output.stdout.decode("utf-8"))

        if not match_exe:
            click.echo(f'ERROR: Could not determine source executable of core dump')
            click.echo(f"Skipping `{coredump_abs}'...")
            continue

        source_exe = match_exe.group(0)

        if not os.path.exists(source_exe):
            click.echo(f"Executable `{source_exe}' for `{coredump_abs}' does not exist on filesystem")
            continue

        modified_date = datetime.fromtimestamp(os.path.getmtime(coredump_abs), tz=timezone.utc)
        click.echo(f"Running backtrace using executable {source_exe} on core {coredump_abs}")

        backtrace = subprocess.run(["gdb", "--batch", "-ex", "bt", source_exe, coredump_abs], stdout=subprocess.PIPE)

        success.append(coredump_abs)

        aggregate_output.extend(b'=' * 80 + b'\n')
        aggregate_output.extend(b'DATE:'.ljust(10) + bytes(modified_date.strftime('%d/%b/%Y %H:%M %Z'), 'utf-8') + b'\n')
        aggregate_output.extend(b'EXE:'.ljust(10) + bytes(source_exe, 'utf-8') + b'\n')
        aggregate_output.extend(b'CORE:'.ljust(10) + bytes(coredump_abs, 'utf-8') + b'\n')
        aggregate_output.extend(b'-' * 80 + b'\n')
        aggregate_output.extend(b'OUTPUT:\n\n')
        aggregate_output.extend(backtrace.stdout)
        aggregate_output.extend(b'\n' + b'=' * 80 + b'\n\n\n')

    if email and success:
        msg = EmailMessage()
        msg.set_content(aggregate_output.decode('UTF-8'))
        msg['Subject'] = f'[CRASHALYSER] Automated email: backtraces from core dumps on {platform.node()}'
        msg['From'] = merged_config['smtp.fromaddr']
        msg['To'] = email

        server = smtplib.SMTP(host=merged_config['smtp.host'], port=merged_config['smtp.port'], timeout=30)
        if merged_config['smtp.tls'] == 'true':
            server.starttls()
        if merged_config['smtp.user'] and merged_config['smtp.password']:
            server.login(merged_config['smtp.user'], merged_config['smtp.password'])
        server.send_message(msg)
        server.quit()
        click.echo(f"Sent email report to {email}")

    if file and success:
        with open(file, 'w') as f:
            f.write(aggregate_output.decode('utf-8'))
        click.echo(f"Wrote {len(success)} backtraces to {file}")

    if success:
        for f in success:
            if os.path.exists(f):
                os.remove(f)


def read_config():
    cfg_system = os.path.join('/etc/crashalyser', 'config.ini')
    cfg_user = os.path.join(click.get_app_dir('crashalyser', force_posix=True), 'config.ini')

    cfg = cfg_system if os.path.exists(cfg_system) else cfg_user
    rv = {}
    if os.path.exists(cfg):
        parser = configparser.ConfigParser()
        try:
            parser.read([cfg])
        except configparser.DuplicateSectionError:
            click.echo(f"Invalid config file `{cfg}': DUPLICATE SECTION, ignoring config file...")
        except configparser.DuplicateOptionError:
            click.echo(f"Invalid config file `{cfg}': DUPLICATE OPTION, ignoring config file...")
        else:
            for section in parser.sections():
                for key, value in parser.items(section):
                    rv['%s.%s' % (section, key)] = value

    return rv


if __name__ == '__main__':
    cli()
