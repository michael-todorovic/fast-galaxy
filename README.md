# fast-galaxy

This is `ansible-galaxy install` on steroids

You should run it with:

```bash
╰ fast-galaxy --help
usage: fast-galaxy [-h] [--parallel PARALLEL] requirements_path

Split and install Ansible Galaxy requirements.

positional arguments:
  requirements_path    Path to the requirements.yml file

options:
  -h, --help           show this help message and exit
  -f, --force          Force overwriting an existing role or collection
  --parallel PARALLEL  Number of parallel installations (default: 10)
```
