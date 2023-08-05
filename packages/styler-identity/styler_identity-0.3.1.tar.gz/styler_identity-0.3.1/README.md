# Styler Identity


[![Pypi link](https://img.shields.io/pypi/v/styler_identity.svg)](https://pypi.python.org/pypi/styler_identity)


Simple library used to handle user data from Firebase generated JWT tokens.


## Installation


```batch

    $ pip install styler-identity
```

## Usage

```python

from styler_identity import Identity

identity = Identity('JWT token')

identity.user_id()          # user_id
identity.shops()            # list of shop_ids
identity.organizations()    # list of organization_ids
identity.token()            # Original JWT token

```