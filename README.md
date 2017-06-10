

## Get Started

1. Read the [Zappa.io documentation](https://github.com/Miserlou/Zappa)
1. Set up python
    ```
    cd hellolambda_api
    python3 --version # ==> confirm >= 3.6.0
    python3 -m venv pyvenv
    source pyvenv/bin/activate
    pip install flask flask_cors  awscli boto3
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
1. Create an S3 bucket for your static website
    * Read [the docummentation](http://docs.aws.amazon.com/AmazonS3/latest/dev/WebsiteHosting.html)
    * Note the bucket name should match the URL you will be using. EG hellolambda.yourdomain.com
1. Set your DNS to point to your new bucket
1. Push the static part of your site to your new S3 bucket
    * A convenience function: `bin/update -s`
    * What this does: `aws s3 sync <a lot of parameters>`
1. Use zappa.io
    1.

