# Readme

A essential tool for retreiving current and past data from the South African Large Telescope.

Based on original code from the SALT ELS-WebViewer and powered by SQLalchemy and the pymysql database driver.

Please contact SALT Software for a username and password for access to the database.

## Let's Get To It

```
from salt_cellar import salt_cellar

cellar = salt_cellar.SaltCellar("mysql+pymysql://username:password@db.suth.saao.ac.za/els_view")

results = cellar.single_query(
    [
        "BMS:analogue status:Glycol tank temp>dbl",
    ],
    start=datetime(2020, 1, 23, 18, 0, 0),
    end=datetime(2020, 1, 23, 18, 10, 0),
)

for row in results:
    print(row)
```

## Development

Requirements

* Python 3.6
* Pipenv

Clone from BitBucket

Run installation command: `make install`

Copy `config.py.example` to `config.py` and update the `username` and `password`

Execute `./example.py`

This project uses Semantic Versioning, for more details see https://semver.org/
