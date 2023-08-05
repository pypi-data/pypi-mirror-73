skelate
========

A utility to create directory from skeletons, with templating support.

This is a tool inspired by the functionality provided by `ansible-galaxy init`.

Requirements
------------

* python 3.8+

Installing
-----------

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```
pip install -U skelate
```

Alternatively, you can package and run `skelate` in a docker container:

```
make image
```

Usage
------

Basic usage is to treat skelate like `cp -r`, with expansion of `j2` files.

```
skelate this/dir that/dir
```

If `this/dir` contains no files with a `j2` extension, this will act _exactly_
like `cp -r`.

If `this/dir` does contain files with a `j2` extension, these will be expanded
into `that/dir`, minus their `.j2` suffix.

You can pass variables to templates in two ways:

```
# Read variables from a JSON file
skelate --vars path/to/vars.json this/dir that/dir

# Read variables from command line
skelate --extra-vars "key=value" \
  --extra-vars 'key={"key": ["value", "value"]}' \
  this/dir that/dir
```

For more options:

```
skelate --help
```



Authors
--------

* [iwaseatenbyagrue](https://gitlab.com/iwaseatenbyagrue)
