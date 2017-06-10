

## Get Started

1. Read the [Zappa.io documentation](https://github.com/Miserlou/Zappa)
1. Set up python
    ```
    cd hellolambda_api
    python3 --version # ==> confirm >= 3.6.0
    python3 -m venv pyvenv
    source pyvenv/bin/activate `
    pip install flask flask_cors  awscli boto3 zappa
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
1. Update config.py `CORS_ACCEPTABLE_ORIGINS` with your domain
1. Push the static part of your site to your new S3 bucket
    * A convenience function: `bin/update -s`
    * What this does: `aws s3 sync <a lot of parameters>`
1. Use zappa.io
    1. `zappa deploy`
    1. copy the API Gateway url it prints at the end. EG:
    `Deployment complete!: https://xxx.execute-api.us-west-2.amazonaws.com/dev`
    1. Test it in the browser (append '/api/ping?does_it_work=yes'):
        `https://xxx.execute-api.us-west-2.amazonaws.com/dev/api/ping?does_it_work=yes`
    1. If it gives you an internal error, check your CloudWatch logs
1. Test ping in your static test page
    1. `http://hellolambda.xxx.com/test/`
    1. Open console to make sure there are no errors
    1. Click the 'Test Ping' button
    1. If error
        * Check cloudwatch logs
        * Trace execution of the JS. Is it sending the URLs you expect?
        * Switch the "API Endpoint Selector" to 'use localhost', run the devserver in your debugger, and trace the python side
        * Pay particular attention to CORS
        * As you do your debugging, use `bin/update` to update the S3 static site and lambda code
        * Good luck!
    1. If success - Hooray!

You now have a working static site with a flask-powered, runs-on-lambda backend.

Now lets get your services running: A DynamoDB table to store the form content, and SES to send emails to the administrator.

