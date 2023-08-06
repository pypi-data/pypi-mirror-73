# v1.dev0

The first `1.x` release!

This release deprecates a lot of old/legacy `pyinfra` code and brings fourth a new, stable API. So long as you see no warnings when executing `pyinfra`, upgrading should require no chanages.

What's new:

+ Add new global `name` argument to name operations (deprecate `set` as the first argument)
+ Improve unexpected fact error handling, bad exit codes will be treated as errors unless the fact explicitly expects this could happen (system package managers for example)
+ [CLI] write progress/user info/logs to `stderr` only
+ [API] Consistent ordering when `add_op` and `add_deploy` functions
+ [API] Return a dictionary of `host` -> `OperationMeta` when using `add_op`

Breaking changes:

+ Deprecate using `set` as the first/name argument for operations
+ Rename `files.*` arguments (`name` -> `path`, `destination` -> `dest`)
+ Rename `server.*` arguments (`name` -> `user|group|cron_name|key|path`, `filename` -> `src`)
+ Rename `mysql.*` + `postgresql.*` arguments (`name` -> `user|database|role`)
+ Rename `init.*` arguments (`name` -> `service`)
+ Rename `lxd.container` argument `name` -> `id`
+ Rename `git.repo` argumenets `source` -> `src` & `target` -> `dest`
+ Rename `iptables.chain` argument `name` -> `chain`
+ Rename `python.call` argument `func` -> `function`
+ Rename `size` -> `mask_bits` inside `network_devices` fact
+ Change default of `interpolate_variables` from `True` -> `False`
+ Remove deprecated`hosts`/`when`/`op` global operation arguments
+ Rename reprecated `Config.TIMEOUT` -> `Config.CONNECT_TIMEOUT`
+ Remove deprecated `use_ssh_user` argument from `git.repo` operation
+ Remove deprecated `python.execute` operation
+ Remove deprecated `Inventory.<__getitem__>` & `Inventory.<__getattr__>` methods
+ Remove deprecated `add_limited_op` function
+ Remove deprecated legacy CLI suppot

---


# v0.16.1

+ Declare connectors as setuptools entrypoints (@FooBarQuaxx)
+ Fix `use_sudo_password` with facts
+ Fix actually mask MySQL operation + facts output

# v0.16

+ Add **zypper** module (@FooBarQuaxx)
+ Add **xbps** module (@leahneukirchen)
+ Add first command class, `StringCommand`, with masking support (@meantheory)
    * Mask postgresql, mysql and sudo passwords
+ Fix `pkg.packages`: don't provide `PKG_PATH` envvar if `/etc/installurl` exists
+ Load any SSH certificates when loading private keys


# v0.15

To-be-breaking changes:

+ Rename `pyinfra.modules` -> `pyinfra.operations` (backwards compatible, will remain in v1)

Other changes:

+ Add `use_sudo_password=[True|False|str]` global operation argument
+ Support YAML+JSON `@ansible` connector inventories (@ricardbejarano)
    * requires `pyyaml` which is an extra requirement (`pip install pyinfra[ansible]`)
+ Enable managing all systemd unit types (not just service) (@nikaro)
+ Enable using `venv` instead of `virtualenv` (@nikaro)
+ Add `@chroot` connector (@FooBarQuaxx)
+ Don't include comment lines in `yum_repositories` fact (@FooBarQuaxx)
+ Use `tail -f /dev/null` instead of sleep for `@docker` containers (@FooBarQuaxx)
+ Support `pkg ...` FreeBSD commands in `pkg.packages` operation + fact
+ Support non-RSA key files (DSS/ECDSA/Ed25519)
+ Python2 unicode fixes for `files` operations + facts
+ Properly escape/support paths with spaces
+ Add python3.8 to travis tests


# v0.14.5

+ Fix use `Host` variable when defined in SSH config (@stchris)
+ Prefix temporary filenames with `pyinfra-`
+ Fix custom fact loading from `config.py` when using `pyinfra fact...`
+ Remove max gevent version to support v20+

# v0.14.4

+ Allow leading numbers for brew cask names (@ryanwersal)
+ Correctly hash 1/0 line numbers when ordering operations
+ Fix Docker integration tests

# v0.14.3

+ Gevent 1.5 compatability
+ Improve check detecting whether a virtualenv exists
+ Rename `windows_files` operations (now `windows_files.[file|directory]`)
+ Fix tests when no SSH config is present
+ Dump (to debug) tracebacks from callback exceptions

# v0.14.2

+ Improve PXE example (@mkinney)
+ Properly make commands when using the docker connector

# v0.14.1

+ Fix group names being passed to @connectors
+ Include group names in `debug-inventory` output

# v0.14

+ Add `@winrm` connector, allowing pyinfra to manage Windows instances (@mkinney)
    * Add **windows** module
    * Add **windows_files** module
    * Add many `Windows*` facts
+ Follow redirects when using `curl` in `files.download` operation


# v0.13.5

+ Improve use of `curl` and/or `wget` in `files.download` operation
+ Add `assume_exists` argument to `files.put` operaton
+ Ensure `@local` connector adds the host to the `@local` group
+ Add `--quiet` CLI flag to hide most output

# v0.13.4

+ Improve `pyinfra --support` output (@mkinney)
+ Add print input state flags and don't show input with `exec` command
+ Remove all ANSI escape codes from spinner on Windows
+ Reduce spinner interval to 0.2s

# v0.13.3

+ Add `pyinfra --support`
+ Add `md5sum`/`sha1sum`/`sha256sum` arguments to `files.download` operation
+ Add `server.reboot` example (@mkinney
+ Make SSH a proper connector (ie `@ssh/my-host.net` works)
+ Fix terminal width detection on Windows (again)

# v0.13.2

+ Fix `server.reboot` argument clash (`timeout` -> `reboot_timeout`)

# v0.13.1

+ Add `success_exit_codes` global argument
+ Add `debug-inventory` command
+ Add `-e` to grep calls in `find_in_file` fact
+ Add `server.reboot` operation
+ Parse CLI operation args as JSON
+ Restore/fix `python -m pyinfra` functionality
+ Fix TTY detection on Windows

# v0.13

Gearing up for `v1` release, deprecating the last unused/old features, expanding the tests and documentation, closing off some really old issues (stdin support).

**Improvements**:

+ Add global `use_sudo_login` and `use_su_login` arguments (and config settings)
+ Add `OperationTypeError` exception and reject invalid names for files operations
+ Implement stdin support! There's a global `stdin` argument for all operations
+ Pass `-S` to sudo so the `stdin` argument works
+ Autogenerate the documentation of global arguments
+ Extended examples and documentation (@mkinney)
+ Fully test SSH/local/Docker connectors
+ Add bash complete script (`scripts/pyinfra-complete.sh`)

**Deprecated**:

+ Deprecate global `when` and `hosts` arguments
+ Deprecate hooks

**Fixed**:

+ Fix logging escape sequences to files and on Windows
+ Fix/improve TTY detection for the progress bar
+ Fix issue with no SSH config causing an exception
+ Fix: exit 1 when hosts fail


# v0.12.2

+ Add URL support to `yum.repo` and `dnf.repo` operations
+ Support downloading files with `curl` (preferred over `wget`)
+ Add `pyinfra INVENTORY all-facts` to get all non-arg facts
+ Hide errors when we have a fallback command
+ Fix quotes in `@docker` connector
+ Fix installing packages in `yum.rpm` and `dnf.rpm`
+ Fix `git.config` check where the repository doesn't exist

# v0.12.1

+ Add `flake8-spellcheck` and fix spellings throughout (@mkinney)
+ Add large number of example deploys (@mkinney)
+ Fix multiple issues with the `files.get` operation

# v0.12

+ Add **dnf** module (@mkinney), matching existing yum operations
+ Add `@mech` connector (@mkinney)
+ Add `extra_install_args` and `extra_uninstall_args` to `yum.packages` operation (@mkinney)
+ Remove autogenerated facts/modules docs from git


# v0.11

+ Add **apk** module
    - Operations: `apk.packages`, `apk.update`, `apk.upgrade`
    - Facts: `apk_packages`
+ Add **brew** module
    - Operations: `brew.packages`, `brew.update`, `brew.upgrade`, `brew.casks`, `brew.cask_upgrade`, `brew.tap`
    - Facts: `brew_packages`, `brew_casks`, `brew_taps`
+ Add **pacman** module
    - Operations: `pacman.packages`, `pacman.update`, `pacman.upgrade`
    - Facts: `pacman_packages`
+ Add **Docker** facts (matching `docker inspect` output):
    - `docker_system_info`
    - `docker_containers`
    - `docker_images`
    - `docker_networks`
    - `docker_container(ID)`
    - `docker_image(ID)`
    - `docker_network(ID)`
+ Add `files.get` operation to download remote files
+ Add `server.mount` operation and `mounts` fact to manage mounted filesystems
+ Add `@ansible` connector to read Ansible inventory files
+ Add `ipv4_addresses` and `ipv6_addresses` shortcut facts
+ Support `ip`/iproute2 for `network_devices` fact
+ Large ongoing documentation overhaul
+ Add a `CONTRIBUTORS.md`!
+ Fix passing of `postgresql_password` in `postgresql_*` facts
+ Only open/parse SSH config file once
+ Large expansion of tests - 100% module + facts coverage
+ Remove lots of printing fluff from the CLI
+ Correctly use `with open...` in `files.template` operation
+ Internal change: file upload commands now tuple `('upload', local_file, remote_file)`
    - also add a `download` version to download files


# v0.10

+ Add `State.preserve_loop_order` to execute loops in order
    * See: https://pyinfra.readthedocs.io/en/latest/deploy_process.html#loops
+ Fix: include data for temp filename hash in `server.script_template` operation


# v0.9.9

+ Add `--init` flag to git submodule update (@ryan109)

# v0.9.8

+ Add `assume_present` (default `False`) kwarg to `files.[file|directory|link]` operations
+ Accept lists for time kwargs in `server.crontab`
+ Fix `su` usage and support w/`shell_executable`
+ Fix/cleanup Docker containers on error
+ Move to `.readthedocs.yml`

# v0.9.7

+ Fix `@hook` functions by correctly checking `state.initialised`

# v0.9.6

+ Add `create_remote_dir` to `files.template` operation

# v0.9.5

+ Fix `apt_repos` fact when `/etc/apt/sources.list.d` doesn't exist
+ Fix parsing of apt repos with multiple option values

# v0.9.4

+ **Rename** `shell` global kwarg to `shell_executable`! (`server.user` uses `shell` already)
+ Add `create_remote_dir` arg to `files.put`, `files.file` and `files.link`

# v0.9.3

+ Add `update_submodules` and `recursive_submodules` args to `git.repo` operation (@chrissinclair)
+ Add `name` args to `server.crontab` operation to allow changing of the command
+ Add global `shell_exectuable` kwarg to all operations, defaults to `sh` as before

# v0.9.2

+ Improve parsing of `ifconfig` for `network_devices` fact (@gchazot)
+ Make printing unicode consistent between Python 2/3
+ Fix parsing Ansible inventories with left-padding in ranges

# v0.9.1

+ Fix for Python 3 (use `six` > `unicode`)

# v0.9

+ Add `@docker` connector, to create docker images
    * eg: `pyinfra @docker/ubuntu:bionic deploy.py`
    * this will spawn a container, execute operations on it and save it as an image
+ Add `linux_name` "short" fact
+ Add `allow_downgrades` keyword argument to `apt.packages`
+ [Experimental]: parse Ansible inventory files (ini format)
+ Handle template errors in arguments better
+ Capture/handle template syntax errors
+ Rename `config.TIMEOUT` -> `config.CONNECT_TIMEOUT` (old deprecated)
+ Properly handle logging unicode output
+ Fix execute `git fetch` before changing branch
+ Fix `find_in_file` fact for files with `~` in the name

Internal changes:

+ Remove the `AttrData` and all `Attr*` classes now we have operation ordering


# v0.8

+ Completely new operation ordering:
    * different args *will not* generate imbalanced operations!
    * no more deploy file compile needed

Internal changes:

+ Inline `sshuserclient` package (original no longer maintained)


# v0.7.1

+ Fix `deb_package` fact and don't assume we have a version in `apt.deb` operation

# v0.7

+ Add **mysql** module
    - Operations: `mysql.sql`, `mysql.user`, `mysql.database`, `mysql.privileges`, `mysql.dump`, `mysql.load`
    - Facts: `mysql_databases`, `mysql_users`, `mysql_user_grants`
+ Add **postgresql** module
    - Operations: `postgresql.sql`, `postgresql.role`, `postgresql.database`, `postgresql.dump`, `postgresql.load`
    - Facts: `postgresql_databases`, `postgresql_roles`
+ Add **puppet** module with `puppet.agent` operation (@tobald)
+ Add `server.crontab`, `server.modprobe` and `server.hostname` operations
+ Add `git.config` operation
+ Add `kernel_modules`, `crontab` and `git_config` facts
+ Add global install virtualenv support (like iPython)
+ Massively improved progress bar which highlights remaining hosts and tracks progress per operation or fact
+ Improved SSH config parsing, including proxyjump support (@tobald)
+ Support for CONFIG variables defined in `local.include` files
+ Fix `command` fact now outputs everything not just the first line

Internal changes:

+ **Replace** `--debug-state` with `--debug-operations` and `--debug-facts`
+ pyinfra now compiles the top-level scope of deploy code, meaning if statements no longer generate imbalanced operations
    * This means the recommendations to use `state.when` in place of conditional statements is invalid
    * Updated the warning shown, now once, with a link
    * Included a test `deploy_branches.py` which can be used to verify operations _do_ run in order for each host when compile is disabled
    * Compiling can be disabled by setting `PYINFRA_COMPILE=off` environment variable
+ **Deprecate** `state.limit` and replace with `state.hosts(hosts)` (consistency with global operation kwarg `hosts` not `limit`)
+ Major internal refactor of `AttrData` handling to reduce operation branching:
    * Generate `AttrData` on creation, rather than read
    * Add nesting support for `AttrData` so `host.data.thing['X']` will not create branching operations
    * Turn fact data into `AttrData`
    * Make `host.name` an `AttrDataStr`
    * Hash `True`, `False` and `None` constants as the same so they can change between hosts without branching operations
    * Update docs and warning on operation branching
+ Better default for pool parallel size
+ Show stdout if stderr is empty on command failure (surprisingly common)


# v0.6.1

+ Fix file "uploading" for the `@local` connector

# v0.6

+ Make `--limit` apply the limit similarly to `state.limit`
    - makes it possible to execute facts on hosts outside the `--limit`
    - `--limit` no longer alters the inventory, instead provides an "initial" state limit
+ Add `when=True` kwarg to `local.include`
+ Make it possible to add `data` to individual hosts in `@vagrant.json` configuration files
+ Add `memory` and `cpus` facts
+ Refactor how we track host state throughout deploy
+ Refactor facts to only gather missing ones (enabling partial gathering)
+ Improve check for valid `/etc/init.d/` services by looking for LSB header
+ Fix boolean constant detection with AST in Python3
+ Fix parsing ls output where `setgid` is set
+ Fix sudo/su file uploads with the `@local` connector


# v0.5.3

+ Fix writing unicode data with `@local`
+ Capture `IOError`s when SFTPing, note where remote disks might be full
+ Properly serialise `Host` objects for `--debug-state`

# v0.5.2

+ Add `exclude_dir` and `add_deploy_dir` kwargs to `files.sync`
+ Add pipfile for dev
+ Fix `files.put` when using `@local`

# v0.5.1

+ Make environment variables stick between multiple commands
+ Fix npm packages fact missing a return(!)

# v0.5

What was originally a module release for pyinfra (see the 0.6 milestone!) has become all about proper conditional branching support (previously resulted in best-effort/guess operation order) and improving 0.4's initial `@deploy` concept:

+ Add global `when` kwarg to all operations, similar to `hosts` can be used to prevent operations executing on hosts based on a condition
+ Add `state.limit(hosts)` and `state.when(condition)` context managers to use in place of `if` statements within deploys
+ `@deploy`s and the context managers (`state.limit`, `state.when`) can all be nested as much as needed (although if you need to nest a lot, you're probably doing it wrong!)
+ Add `data_defaults` kwarg to `@deploy` functions, meaning third party pyinfra packages can provide sensible defaults that the user can override individually
+ Display a large warning when imbalanced branches are detected, linking the user to the documentation for the above

Note that if statements/etc still work as before but pyinfra will print out a warning explaining the implications and linking to the docs (http://pyinfra.readthedocs.io/page/using_python.html#conditional-branches).

+ **Vagrant connector**:

```sh
# Run a deploy on all Vagrant machines (vagrant status list)
pyinfra @vagrant deploy.py
pyinfra @vagrant/vm_name deploy.py

# Can be used in tandem with other inventory:
pyinfra @vagrant,my-host.net deploy.py
pyinfra @vagrant,@local,my-host.net fact os
```

+ **Hooks broken**: no longer loaded from deploy files, only from `config.py`, due to changes from `0.4` (removal of `FakeState` nonsense)
+ Add `gpgkey` argument to the `yum.repo` operation
+ Add `lsb_release` fact
+ `apt_sources` fact now supports apt repos with options (`[arch=amd64]`)
+ Improved error output when connecting
+ Update testing box from Ubuntu 15 to Ubuntu 16
+ Ensure `~/.ssh` exists keyscanning in `ssh.keyscan`
+ Don't include tests during setup!
+ Fix caching of local SHA1s on files


# v0.4.1

+ Add `vzctl.unmount` operation (missing from 0.4!)
+ Add script to generate empty test files
+ Increase module test coverage significantly
+ Fix incorrect args in `vzctl.restart` operation
+ Fix `save=False` kwarg on `vzctl.set` not affecting command output (always saved)
+ Fix `gem.packages` install command

# v0.4

+ **Major change**: entirely new, streamlined CLI. Legacy support will remain for the next few releases. Usage is now:

```sh
# Run one or more deploys against the inventory
pyinfra INVENTORY deploy_web.py [deploy_db.py]...

# Run a single operation against the inventory
pyinfra INVENTORY server.user pyinfra,home=/home/pyinfra

# Execute an arbitrary command on the inventory
pyinfra INVENTORY exec -- echo "hello world"

# Run one or more facts on the inventory
pyinfra INVENTORY fact linux_distribution [users]...
```

+ **Major addition**: new `connectors` module that means hosts are no longer limited to SSH targets. Hostnames prefixed in `@` define which non-SSH connector to use. There is a new `local` connector for executing directly on the local machine, use hostname `@local`, eg:

```sh
pyinfra @local fact arch
```

+ **Major addition**: add `@deploy` wrapper for pyinfra related modules (eg [pyinfra-openstack](https://github.com/Oxygem/pyinfra-openstack)) to wrap a deploy (collection of operations) under one function, eg:

```py
from pyinfra.api import deploy
from pyinfra.operations import apt


@deploy('Install Openstack controller')
def install_openstack_controller(state, host):
    apt.packages(
        state, host,
        {'Install openstack-client'},
        ['openstack-client'],
    )
```

+ Add **SSH module** to execute SSH from others hosts: `ssh.keyscan`, `ssh.command`, `ssh.upload`, `ssh.download`
+ Add **vzctl module** to manage OpenVZ containers: `vzctl.create`, `vzctl.stop`, `vzctl.start`, `vzctl.restart`, `vzctl.delete`, `vzctl.set`
+ Add `on_success` and `on_error` callbacks to all operations (args = `(state, host, op_hash)`)
+ Add `server.script_template` operation
+ Add global `hosts` kwarg to all operations, working like `local.include`'s
+ Add `cache_time` kwarg to `apt.update` operation
+ Add `Inventory.get_group` and `Inventory.get_host`
+ Inventory `__len__` now (correctly) looks at active hosts, rather than all
+ Add `Inventory.len_all_hosts` to replace above bug/qwirk
+ Add progress spinner and % indicator to CLI
+ Replace `docopt`/`termcolor` with `click`
+ Moved `pyinfra.cli` to `pyinfra_cli` (internal breaking)
+ Switch to setuptools `entry_points` instead of distutils scripts
+ Expand Travis.ci testing to Python 3.6 and 3.7 nightly
+ Remove unused kwargs (`sudo`, `sudo_user`, `su_user`) from `pyinfra.api.facts.get_facts`

To-be-breaking changes (deprecated):

+ Deprecate `add_limited_op` function, use `hosts` kwarg on `add_op`
+ Deprecate group access via attribute and host access via index on `Inventory`
    * `Inventory.get_group` and `inventory.get_host` replace


# v0.3

+ Add `init.service` operation
+ Add `config.MIN_PYINFRA_VERSION`
+ Add `daemon_reload` to `init.systemd`
+ Add `pip` path to `pip.packages` (@hoh)
+ Add `virtualenv_kwargs` to `pip.packages`
+ Add `socket` fact
+ Display meta and results in groups
+ Fact arguments now parsed with jinja2 like operation args
+ Use full dates in `file`, `directory` and `link` facts
+ Improve `--run` check between operation and/or shell
+ Improve tests with facts that have multiple arguments
+ Fix how `pip.packages` handles pip path
+ Fix `yum.rpm` when downloading already installed rpm's
+ Fix `users` fact with users that have no home directory
+ Fix command overrides with dict objects (git.repo)
+ Removed compatibility for deprecated changes in v0.2


# v0.2.2

+ Fix bug in parsing of network interfaces
+ Fix `--limit` with a group name

# v0.2.1

+ Use wget & pipe when adding apt keys via URL, rather than `apt-key adv` which breaks with HTTPs
+ Fix bug where file-based group names were uppercased incorrectly (ie dev.py made group DEV, rather than dev)

# v0.2

New stuff:

+ Add LXD facts/module
+ Add iptables facts/module
+ Support usernames with non-standard characters (_, capitals, etc)
+ Add global `get_pty` kwarg for all operations to work with certain dodgy programs
+ Add `--fail-percent` CLI arg
+ Add `exclude` kwarg to `files.sync`
+ Enable `--limit` CLI arg to be multiple, comma separated, hostnames
+ Add `no_recommends` kwarg to `apt.packages` operation
+ Make local imports work like calling `python` by adding `.` to `sys.path` in CLI
+ Add key/value release meta to `linux_distribution` fact
+ Improve how the init module handles "unknown" services
+ Add `force` kwarg to `apt.packages` and `apt.deb` and don't `--force-yes` by default

To-be-breaking changes (deprecated):

+ Switch to lowercase inventory names (accessing `inventory.bsd` where the group is defined as `BSD = []` is deprecated)
+ Rename `yum.upgrade` -> `yum.update` (`yum.upgrade` deprecated)
+ Deprecate `pip_virtualenv_packages` fact as `pip_packages` will now accept an argument for the virtualenv
+ Deprecate `npm_local_packages` fact as `npm_packages` will accept an argument for the directory

Internal changes:

+ Operations now `yield`, rather than returning lists of commands


# v0.1.5

+ Fix `--run` arg parsing splutting up `[],`

# v0.1.4

+ Enable passing of multiple, comma separated hosts, as inventory
+ Use `getpass`, not `raw_input` for collecting key passwords in CLI mode

# v0.1.3

+ Fix issue when removing users that don't exist

# v0.1.2

+ Improve private key error handling
+ Ask for encrypted private key passwords in CLI mode

# v0.1.1

+ Don't generate set groups when `groups` is an empty list in `server.user`.

# v0.1

+ First versioned release, start of changelog
+ Full docs @ pyinfra.readthedocs.io
+ Core API with CLI built on top
+ Two-step deploy (diff state, exec commands)
+ Compatibility tested w/Ubuntu/CentOS/Debian/OpenBSD/Fedora
+ Modules/facts implemented:
    * Apt
    * Files
    * Gem
    * Git
    * Init
    * Npm
    * Pip
    * Pkg
    * Python
    * Server
    * Yum
