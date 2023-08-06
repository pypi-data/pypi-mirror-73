# kenetsu

## Install

Uploaded to [PyPI](https://pypi.org/project/kenetsu/)

```console
pip install kenetsu
```

## Usage

This tool is intended to process `/var/log/maillog`, of which the permission is `root:root` `0600`, so it should be run as `root`.

```console
kenetsu SECOND [LOGPATH]
```

- Default LOGPATH: `/var/log/maillog`

## References

- [All possible postfix maillog statuses](https://www.linuxquestions.org/questions/linux-software-2/postfix-logs-all-possible-status%3D-798938/)
