# Installation and Usage

This package has only been developed and tested against GitHub repositories. 
Other hosted repositories may work but have not been tested. It is only 
 tested on Ubuntu and OS X and is not tested or supported on Windows. 

## Installation

`pip install import-git-files`

## Usage

`import-git-files` is offered both as an command-line executable and a module
that you can import into your project. To use as a module, continue to the 
module documentation. To use on the command-line, the usage is:

<pre>
usage: import-git-files [-h] [--version] [-v] [-t TEMPORARY_DIRECTORY_PARENT]
                        [--ssh-key SSH_KEY]
                        input

Import files from other repositories. Define the imports in a JSON file and
pass as input argument. If the repositories are private and require
authentication but you do not have cached credentials and are using it in a
non-interactive way, you can either define a Personal Access Token in your
Environment under variable GITHUB_TOKEN or you can specify a path to an SSH
Deploy Key.

positional arguments:
  input                 The input json with a hash of repo URLs and their
                        value being hash of source path and destination path.
                        Source path should be relative to root of repository
                        and the destination path can be absolute or it can be
                        relative to the PWD.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         Set logging to verbose
  -t TEMPORARY_DIRECTORY_PARENT, --temporary-directory-parent TEMPORARY_DIRECTORY_PARENT
                        Optionally set the parent directory for temporary
                        directories or else will use system tmp default.
  --ssh-key SSH_KEY     Path to an SSH Key with access to the repository. This
                        file needs 600 permissions. This cannot be defined in
                        combination with GITHUB_TOKEN environment variable.
</pre>

### Example

An example could include creating a JSON file to define an import from a
release of a public repository such as:

```json
{
  "https://github.com/<username>/<repo>": {
    "README.md": "README.md"
  }
}
```

We can checkout a specific version:

```json
{
  "https://github.com/<username>/<repo>@<revision>": {
    "README.md": "README.md"
  }
}
```

revision can be a commit sha, branch name, release, or tag.

The destination can be an absolute path or relative to PWD:

```json
{
  "https://github.com/<username>/<repo>": {
    "README.md": "another_directory/README.md",
    "CHANGES.md": "/home/users/test/CHANGES.md"
  }
}
```

After saving any of these formats to a file, such as `test.json`, we can 
run the command-line tool:

`import-git-pages test.json`

Relative destination values will be relative to where we execute this command.
Some logging will indicate exactly what is happening and verbosity can be increased
 by passing `-v`
 
### Private Repositories

Private repositories are supported by `import-git-files`. The default method 
will used cached credentials or prompt interactively for them. If you are 
in an environment where the credentials are not cached and there is not an 
interactive TTY, then you can supply an SSH Deploy Key or a GitHub Personal Access Token.

#### SSH Deploy Key

To utilize an SSH deploy key define the path to it via `--ssh-key`. This file 
needs to have 600 (owner read only) permissions. Do not use this in combination 
with a token.

There is no need to update the URLs from HTTPS to SSH protocol in your JSON file
as these will be automagically handled.

#### Personal Access Token

If you cannot use an SSH deploy key, you can use a Personal Access Token.
Set the Environment Variable `GITHUB_TOKEN` to this value to use it with the 
command-line tool. Do not use this in combination with the SSH key. If you use
this method, it is recommended not to enable verbose logging as this can expose
the token in logs.
