# gcloud-tail

The `gcloud` CLI provides a way to "tail" logs from Google App Engine, but not from Stackdriver.  Which is
odd, because it's not especially difficult to do so.  That's what this utility accomplishes.

## Usage

Run this as `gcloud-tail FILTER`.  The result is in JSON format, with one line per log message.
You can process the results with `jq`.  For example:

```shell
$ gcloud-tail 'severity>=ERROR' | jq -r .textPayload
```

## Installation

This is a simple Python distribution.  The easiest way to install is

```shell
pip install gcloud-tail
```
