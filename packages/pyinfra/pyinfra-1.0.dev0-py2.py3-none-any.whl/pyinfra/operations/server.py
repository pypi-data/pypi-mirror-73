'''
The server module takes care of os-level state. Targets POSIX compatibility, tested on
Linux/BSD.
'''

from __future__ import division, unicode_literals

from time import sleep

import six

from six.moves import shlex_quote

from pyinfra import logger
from pyinfra.api import FunctionCommand, operation, StringCommand

from . import files
from .util.files import chmod, sed_replace


@operation
def reboot(state, host, delay=10, interval=1, reboot_timeout=300):
    '''
    Reboot the server and wait for reconnection.

    + delay: number of seconds to wait before attempting reconnect
    + interval: interval (s) between reconnect attempts
    + reboot_timeout: total time before giving up reconnecting

    Note: Probably want sudo enabled.

    Example:

    .. code:: python

        server.reboot(
            name='Reboot the server and wait to reconnect',
            delay=5,
            timeout=30,
        )
    '''

    logger.warning('The server.reboot operation is in beta!')

    yield StringCommand('reboot', success_exit_codes=[-1])  # -1 being error/disconnected

    def wait_and_reconnect(state, host):  # pragma: no cover
        sleep(delay)
        max_retries = round(reboot_timeout / interval)

        host.connection = None  # remove the connection object
        retries = 0

        while True:
            host.connect(state, show_errors=False)
            if host.connection:
                break

            if retries > max_retries:
                raise Exception((
                    'Server did not reboot in time (reboot_timeout={0}s)'
                ).format(reboot_timeout))

            sleep(interval)
            retries += 1

    yield FunctionCommand(wait_and_reconnect, (), {})


@operation
def wait(state, host, port=None):
    '''
    Waits for a port to come active on the target machine. Requires netstat, checks every
    second.

    + port: port number to wait for

    Example:

    .. code:: python

        server.wait(
            name='Wait for webserver to start',
            port=80,
        )
    '''

    yield r'''
        while ! (netstat -an | grep LISTEN | grep -e "\.{0}" -e ":{0}"); do
            echo "waiting for port {0}..."
            sleep 1
        done
    '''.format(port)


@operation
def shell(state, host, commands, chdir=None):
    '''
    Run raw shell code on server during a deploy. If the command would
    modify data that would be in a fact, the fact would not be updated
    since facts are only run at the start of a deploy.

    + commands: command or list of commands to execute on the remote server
    + chdir: directory to cd into before executing commands

    Example:

    .. code:: python

        server.shell(
            name='Run lxd auto init',
            commands=['lxd init --auto'],
        )
    '''

    # Ensure we have a list
    if isinstance(commands, six.string_types):
        commands = [commands]

    for command in commands:
        if chdir:
            yield 'cd {0} && ({1})'.format(chdir, command)
        else:
            yield command


@operation
def script(state, host, src, chdir=None):
    '''
    Upload and execute a local script on the remote host.

    + src: local script filename to upload & execute
    + chdir: directory to cd into before executing the script

    Example:

    .. code:: python

        # Note: This assumes there is a file in files/hello.bash locally.
        server.script(
            name='Hello',
            src='files/hello.bash',
        )
    '''

    temp_file = state.get_temp_filename(src)
    yield files.put(state, host, src, temp_file)

    yield chmod(temp_file, '+x')

    if chdir:
        yield 'cd {0} && {1}'.format(chdir, temp_file)
    else:
        yield temp_file


@operation
def script_template(state, host, src, chdir=None, **data):
    '''
    Generate, upload and execute a local script template on the remote host.

    + src: local script template filename
    + chdir: directory to cd into before executing the script

    Example:

    .. code:: python

        # Example showing how to pass python variable to a script template file.
        # The .j2 file can use `{{ some_var }}` to be interpolated.
        # To see output need to run pyinfra with '-v'
        # Note: This assumes there is a file in templates/hello2.bash.j2 locally.
        some_var = 'blah blah blah '
        server.script_template(
            name='Hello from script',
            src='templates/hello2.bash.j2',
            some_var=some_var,
        )
    '''

    temp_file = state.get_temp_filename('{0}{1}'.format(src, data))
    yield files.template(state, host, src, temp_file, **data)

    yield chmod(temp_file, '+x')

    if chdir:
        yield 'cd {0} && {1}'.format(chdir, temp_file)
    else:
        yield temp_file


@operation
def modprobe(state, host, module, present=True, force=False):
    '''
    Load/unload kernel modules.

    + module: name of the module to manage
    + present: whether the module should be loaded or not
    + force: whether to force any add/remove modules

    Example:

    .. code:: python

        server.modprobe(
            name='Silly example for modprobe',
            module='floppy',
        )
    '''

    modules = host.fact.kernel_modules
    is_present = module in modules

    args = ''
    if force:
        args = ' -f'

    # Module is loaded and we don't want it?
    if not present and is_present:
        yield 'modprobe{0} -r {1}'.format(args, module)

    # Module isn't loaded and we want it?
    elif present and not is_present:
        yield 'modprobe{0} {1}'.format(args, module)


@operation
def mount(
    state, host, path,
    mounted=True, options=None,
    # TODO: do we want to manage fstab here?
    # update_fstab=False, device=None, fs_type=None,
):
    '''
    Manage mounted filesystems.

    + path: the path of the mounted filesystem
    + mounted: whether the filesystem should be mounted
    + options: the mount options

    Options:
        If the currently mounted filesystem does not have all of the provided
        options it will be remounted with the options provided.

    ``/etc/fstab``:
        This operation does not attempt to modify the on disk fstab file - for
        that you should use the `files.line operation <./files.html#files-line>`_.
    '''

    options = options or []
    options_string = ','.join(options)

    mounts = host.fact.mounts
    is_mounted = path in mounts

    # Want mount but don't have?
    if mounted and not is_mounted:
        yield 'mount{0} {1}'.format(
            ' -o {0}'.format(options_string) if options_string else '',
            path,
        )

    # Want no mount but mounted?
    elif mounted is False and is_mounted:
        yield 'umount {0}'.format(path)

    # Want mount and is mounted! Check the options
    elif is_mounted and mounted and options:
        mounted_options = mounts[path]['options']
        needed_options = set(options) - set(mounted_options)
        if needed_options:
            yield 'mount -o remount,{0} {1}'.format(options_string, path)


@operation
def hostname(state, host, hostname, hostname_file=None):
    '''
    Set the system hostname.

    + hostname: the hostname that should be set
    + hostname_file: the file that permanently sets the hostname

    Hostname file:
        By default pyinfra will auto detect this by targetting ``/etc/hostname``
        on Linux and ``/etc/myname`` on OpenBSD.

        To completely disable writing the hostname file, set ``hostname_file=False``.

    Example:

    .. code:: python

        server.hostname(
            name='Set the hostname',
            hostname='server1.example.com',
        )
    '''

    if hostname_file is None:
        os = host.fact.os

        if os == 'Linux':
            hostname_file = '/etc/hostname'
        elif os == 'OpenBSD':
            hostname_file = '/etc/myname'

    current_hostname = host.fact.hostname

    if current_hostname != hostname:
        yield 'hostname {0}'.format(hostname)

    if hostname_file:
        # Create a whole new hostname file
        file = six.StringIO('{0}\n'.format(hostname))

        # And ensure it exists
        yield files.put(
            state, host,
            file, hostname_file,
        )


@operation
def sysctl(
    state, host, key, value,
    persist=False, persist_file='/etc/sysctl.conf',
):
    '''
    Edit sysctl configuration.

    + key: name of the sysctl setting to ensure
    + value: the value or list of values the sysctl should be
    + persist: whether to write this sysctl to the config
    + persist_file: file to write the sysctl to persist on reboot

    Example:

    .. code:: python

        server.sysctl(
            name='Change the fs.file-max value',
            key='fs.file-max',
            value='100000',
            persist=True,
        )
    '''

    string_value = (
        ' '.join(value)
        if isinstance(value, list)
        else value
    )

    existing_value = host.fact.sysctl.get(key)
    if not existing_value or existing_value != value:
        yield 'sysctl {0}={1}'.format(key, string_value)

    if persist:
        yield files.line(
            state, host,
            persist_file,
            '{0}[[:space:]]*=[[:space:]]*{1}'.format(key, string_value),
            replace='{0} = {1}'.format(key, string_value),
        )


@operation
def crontab(
    state, host, command, present=True, user=None, cron_name=None,
    minute='*', hour='*', month='*', day_of_week='*', day_of_month='*',
    interpolate_variables=False,
):
    '''
    Add/remove/update crontab entries.

    + command: the command for the cron
    + present: whether this cron command should exist
    + user: the user whose crontab to manage
    + cron_name: name the cronjob so future changes to the command will overwrite
    + minute: which minutes to execute the cron
    + hour: which hours to execute the cron
    + month: which months to execute the cron
    + day_of_week: which day of the week to execute the cron
    + day_of_month: which day of the month to execute the cron
    + interpolate_variables: whether to interpolate variables in ``command``

    Cron commands:
        Unless ``name`` is specified the command is used to identify crontab entries.
        This means commands must be unique within a given users crontab. If you require
        multiple identical commands, provide a different name argument for each.

    Example:

    .. code:: python

        # simple example for a crontab
        server.crontab(
            name='Backup /etc weekly',
            command='/bin/tar cf /tmp/etc_bup.tar /etc',
            name='backup_etc',
            day_of_week=0,
            hour=1,
            minute=0,
        )

    '''

    def comma_sep(value):
        if isinstance(value, (list, tuple)):
            return ','.join('{0}'.format(v) for v in value)
        return value

    minute = comma_sep(minute)
    hour = comma_sep(hour)
    month = comma_sep(month)
    day_of_week = comma_sep(day_of_week)
    day_of_month = comma_sep(day_of_month)

    crontab = host.fact.crontab(user)
    name_comment = '# pyinfra-name={0}'.format(cron_name)

    existing_crontab = crontab.get(command)
    existing_crontab_match = command

    if not existing_crontab and cron_name:  # find the crontab by name if provided
        for cmd, details in crontab.items():
            if name_comment in details['comments']:
                existing_crontab = details
                existing_crontab_match = cmd

    exists = existing_crontab is not None

    edit_commands = []
    temp_filename = state.get_temp_filename()

    new_crontab_line = '{minute} {hour} {day_of_month} {month} {day_of_week} {command}'.format(
        command=command,
        minute=minute,
        hour=hour,
        month=month,
        day_of_week=day_of_week,
        day_of_month=day_of_month,
    )
    existing_crontab_match = '.*{0}.*'.format(existing_crontab_match)

    # Don't want the cron and it does exist? Remove the line
    if not present and exists:
        edit_commands.append(sed_replace(
            temp_filename, existing_crontab_match, '',
            interpolate_variables=interpolate_variables,
        ))

    # Want the cron but it doesn't exist? Append the line
    elif present and not exists:
        if cron_name:
            edit_commands.append('echo {0} >> {1}'.format(
                shlex_quote(name_comment), temp_filename,
            ))

        edit_commands.append('echo {0} >> {1}'.format(
            shlex_quote(new_crontab_line), temp_filename,
        ))

    # We have the cron and it exists, do it's details? If not, replace the line
    elif present and exists:
        if any((
            minute != existing_crontab['minute'],
            hour != existing_crontab['hour'],
            month != existing_crontab['month'],
            day_of_week != existing_crontab['day_of_week'],
            day_of_month != existing_crontab['day_of_month'],
        )):
            edit_commands.append(sed_replace(
                temp_filename, existing_crontab_match, new_crontab_line,
                interpolate_variables=interpolate_variables,
            ))

    if edit_commands:
        crontab_args = []
        if user:
            crontab_args.append('-u {0}'.format(user))

        # List the crontab into a temporary file if it exists
        if crontab:
            yield 'crontab -l {0} > {1}'.format(' '.join(crontab_args), temp_filename)

        # Now yield any edits
        for edit_command in edit_commands:
            yield edit_command

        # Finally, use the tempfile to write a new crontab
        yield 'crontab {0} {1}'.format(' '.join(crontab_args), temp_filename)


@operation
def group(
    state, host, group, present=True, system=False, gid=None,
):
    '''
    Add/remove system groups.

    + group: name of the group to ensure
    + present: whether the group should be present or not
    + system: whether to create a system group

    System users:
        System users don't exist on BSD, so the argument is ignored for BSD targets.

    Examples:

    .. code:: python

        server.group(
            name='Create docker group',
            group='docker',
        )

        # multiple groups
        for group in ['wheel', 'lusers']:
            server.group(
                name=f'Create the group {group}',
                group=group,
            )


    '''

    groups = host.fact.groups or []
    is_present = group in groups

    # Group exists but we don't want them?
    if not present and is_present:
        yield 'groupdel {0}'.format(group)

    # Group doesn't exist and we want it?
    elif present and not is_present:
        args = []

        # BSD doesn't do system users
        if system and 'BSD' not in host.fact.os:
            args.append('-r')

        args.append(group)

        if gid:
            args.append('--gid {0}'.format(gid))

        yield 'groupadd {0}'.format(' '.join(args))


@operation
def user(
    state, host, user,
    present=True, home=None, shell=None, group=None, groups=None,
    public_keys=None, delete_keys=False, ensure_home=True,
    system=False, uid=None,
):
    '''
    Add/remove/update system users & their ssh `authorized_keys`.

    + user: name of the user to ensure
    + present: whether this user should exist
    + home: the users home directory
    + shell: the users shell
    + group: the users primary group
    + groups: the users secondary groups
    + public_keys: list of public keys to attach to this user, ``home`` must be specified
    + delete_keys: whether to remove any keys not specified in ``public_keys``
    + ensure_home: whether to ensure the ``home`` directory exists
    + system: whether to create a system account

    Home directory:
        When ``ensure_home`` or ``public_keys`` are provided, ``home`` defaults to
        ``/home/{name}``.

    Examples:

    .. code:: python

        server.user(
            name='Ensure user is removed',
            user='kevin',
            present=False,
        )

        server.user(
            name='Ensure myweb user exists',
            user='myweb',
            shell='/bin/bash',
        )

        # multiple users
        for user in ['kevin', 'bob']:
            server.user(
                name=f'Ensure user {user} is removed',
                user=user,
                present=False,
            )

    '''

    users = host.fact.users or {}
    existing_user = users.get(user)

    if groups is None:
        groups = []

    if home is None:
        home = '/home/{0}'.format(user)

    # User not wanted?
    if not present:
        if existing_user:
            yield 'userdel {0}'.format(user)
        return

    # User doesn't exist but we want them?
    if present and existing_user is None:
        # Create the user w/home/shell
        args = []

        if home:
            args.append('-d {0}'.format(home))

        if shell:
            args.append('-s {0}'.format(shell))

        if group:
            args.append('-g {0}'.format(group))

        if groups:
            args.append('-G {0}'.format(','.join(groups)))

        if system and 'BSD' not in host.fact.os:
            args.append('-r')

        if uid:
            args.append('--uid {0}'.format(uid))

        yield 'useradd {0} {1}'.format(' '.join(args), user)

    # User exists and we want them, check home/shell/keys
    else:
        args = []

        # Check homedir
        if home and existing_user['home'] != home:
            args.append('-d {0}'.format(home))

        # Check shell
        if shell and existing_user['shell'] != shell:
            args.append('-s {0}'.format(shell))

        # Check primary group
        if group and existing_user['group'] != group:
            args.append('-g {0}'.format(group))

        # Check secondary groups, if defined
        if groups and set(existing_user['groups']) != set(groups):
            args.append('-G {0}'.format(','.join(groups)))

        # Need to mod the user?
        if args:
            yield 'usermod {0} {1}'.format(' '.join(args), user)

    # Ensure home directory ownership
    if ensure_home:
        yield files.directory(
            state, host, home,
            user=user, group=user,
        )

    # Add SSH keys
    if public_keys is not None:
        if isinstance(public_keys, six.string_types):
            public_keys = [public_keys]

        # Ensure .ssh directory
        # note that this always outputs commands unless the SSH user has access to the
        # authorized_keys file, ie the SSH user is the user defined in this function
        yield files.directory(
            state, host,
            '{0}/.ssh'.format(home),
            user=user, group=user,
            mode=700,
        )

        filename = '{0}/.ssh/authorized_keys'.format(home)

        if delete_keys:
            # Create a whole new authorized_keys file
            keys_file = six.StringIO('{0}\n'.format(
                '\n'.join(public_keys),
            ))

            # And ensure it exists
            yield files.put(
                state, host,
                keys_file, filename,
                user=user, group=user,
                mode=600,
            )

        else:
            # Ensure authorized_keys exists
            yield files.file(
                state, host, filename,
                user=user, group=user,
                mode=600,
            )

            # And every public key is present
            for key in public_keys:
                yield files.line(
                    state, host,
                    filename, key,
                )
