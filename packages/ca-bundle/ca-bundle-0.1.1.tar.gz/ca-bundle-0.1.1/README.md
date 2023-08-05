# CA-bundle

No more `SSLError`s because of unset `REQUESTS_CA_BUNDLE`.

This package searches through common locations of SLL certificates on linux and sets
the first existing location to `REQUESTS_CA_BUNDLE` and `HTTPLIB2_CA_CERTS` environment variables.

## Installation

```sh
pip install ca-bundle
```

## Usage

```python
import ca_bundle

ca_bundle.install()
```

Inspired by [Go's implementation](https://golang.org/src/crypto/x509/root_linux.go).
