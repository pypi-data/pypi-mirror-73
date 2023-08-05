Changelog
==========

This file documents notable changes to `skelate`.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

[0.0.2] - 2020-07-05
---------------------

Documentation fixes.

### Changed

* fix typos in CHANGELOG and README.
* fix broken support for user-specified worker pool size.
* fix PEP8 issues in CLI and tests.



[0.0.1] - 2020-07-05
---------------------

Initial release of `skelate`.

### Added

* create a directory from a directory of raw files and templates.
* handle raw files like `cp -r`, retaining the file mode from the original.
* support parsing template variables from a JSON file and/or CLI arguments.
* support configurable (async) worker pool size.
* support configurable log level via CLI (default/warning, verbose/info, and debug).
* support (multiple) configurable template extensions
