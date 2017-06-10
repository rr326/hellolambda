

## Get Started

1. Read the [Zappa.io documentation](https://github.com/Miserlou/Zappa)
1. Set up python
    ```
    cd hellolambda_api
    python3 --version # ==> confirm >= 3.6.0
    python3 -m venv pyvenv
    source pyvenv/bin/activate
    pip install flask flask_cors click boto3
    pip install -e ..
    python devserver.py
    ```
    1. In browser: `http://127.0.0.1:5285/api/ping?does_it_work=yes` ==> {"does_it_work": "yes"}
    1. Python debugger - set up your python debugger or IDE (I use pycharm) so you can debug your flask API
1. Confirm Jekyll works
    1. `cd ../site`
    1. `jekyll serve`
    1. In browser: `http://127.0.0.1:4000/` ==> Hello, Lambda! page should show (in yellow)
    1. In browser: `http://127.0.0.1:4000/test` ==> Test page should show (in yellow)
1. Use zappa.io
    1.


