from __future__ import unicode_literals


def ensure_mode_int(mode):
    # Already an int (/None)?
    if isinstance(mode, int) or mode is None:
        return mode

    try:
        # Try making an int ('700' -> 700)
        return int(mode)

    except (TypeError, ValueError):
        pass

    # Return as-is (ie +x which we don't need to normalise, it always gets run)
    return mode


def sed_replace(filename, line, replace, flags=None, interpolate_variables=False):
    flags = ''.join(flags) if flags else ''

    line = line.replace('/', r'\/')
    replace = replace.replace('/', r'\/')

    string_to_format = (
        'sed -i="" "s/{0}/{1}/{2}" {3}'
        if interpolate_variables else
        "sed -i='' 's/{0}/{1}/{2}' {3}"
    )

    return string_to_format.format(line, replace, flags, filename)


def chmod(target, mode, recursive=False):
    return 'chmod {0}{1} {2}'.format(('-R ' if recursive else ''), mode, target)


def chown(target, user, group=None, recursive=False, dereference=True):
    command = 'chown'
    user_group = None

    if user and group:
        user_group = '{0}:{1}'.format(user, group)

    elif user:
        user_group = user

    elif group:
        command = 'chgrp'
        user_group = group

    return '{0}{1}{2} {3} {4}'.format(
        command,
        ' -R' if recursive else '',
        ' -h' if not dereference else '',
        user_group,
        target,
    )
