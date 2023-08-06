# Hydrator

Hydrate your development environment from a YAML configuration file.

__Synopsis__

```
Usage: hydrator [OPTIONS] COMMAND [ARGS]...

  Hydrate your development environment.

  Without arguments, all hydrators will be run.

Options:
  -c, --config path  The config file to load. Defaults to "hydrator.yml"
  -v, --verbose
  --dry              Do not commit changes to disk.
  --select TEXT      Select a subset of hydrators to run (comma separated).
  --help             Show this message and exit.

Commands:
  auth-status  Check the filesystem authentication status.
  login        Authenticate for a filesystem.
  logout       Revoke existing credentials for a filesystem.
```

__Features__

* YAML-configuration for Bash profile and Git config.
* Do not repeat yourself: Layer multiple YAML configurations for multiple environments.
* Execute shell commands with access to external file systems (e.g. Nextcloud).

__Roadmap__

* [ ] Application directory finders (e.g. to discover VScode application directory)

## Example

In a Git repository, create a file called `hydrator.yml`. In that file you can configure files
that will be produced from the YAML configuration or from external sources. External sources are
"file systems" that can be configured in the same file.

```yaml
filesystems:
  nextcloud: {type: nextcloud, server-url: https://my-cloud.example.org}

hydrators:
  gpg:
    type: commands
    commands:
    - gpg --import [[nextcloud://dotfiles/gpgp/master.key]]

  ssh:
    type: commands
    commands:
    - cp nextcloud://dotfiles/ssh/ida_rsa{,.pub} ~./ssh
    - chmod 600 ~/.ssh/id_rsa{,.pub}

  bash_profile:
    type: bash_profile
    aliases:
      ll: ls -l
    path:
    - ~/.local/bin
```

In order to access files your Nextcloud, Hydrator first needs to authenticate.

    $ hydrator login nextcloud

Then you simply run Hydrator to execute all steps. You can select a subset of hydrators
using the `--select h1,h2,...` option. Add `--dry` to not commit changes to disk, and
`-v,--verbose` or more logs.

    $ hydrator

## Layering

You can have multiple YAML configuration files, where one extends the other by adding or
overwriting keys. This is useful to customize a basic configuration for another environment.

```yaml
extends: ./base.yml
hydrators:
  gpg: '{{exclude}}'
  gitconfig:
    Personal.user: '{{user}}'
    user:
      email: work@email.com
      signingkey: DEADBEEF
```

---

<p align="center">Copyright 2020 &copy; Niklas Rosenstein</p>
