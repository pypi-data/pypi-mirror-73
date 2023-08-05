# Styler Identity


[![Pypi link](https://img.shields.io/pypi/v/styler_identity.svg)](https://pypi.python.org/pypi/styler_identity)


Simple library used to handle user data from Firebase generated JWT tokens.


## Installation


```batch

    $ pip install styler_identity
```

## Usage

```python

from styler_identity import Identity

identity = Identity('JWT token')

identity.get_user_id()          # user_id
identity.get_shops()            # list of shop_ids
identity.get_organizations()    # list of organization_ids
identity.get_token()            # Original JWT token

```