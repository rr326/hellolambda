# Hello, Lambda!
This is a boilerplate site to help you get started building a simple semi-static site.
* Static pages built with jekyll and hosted on S3
* Backend functionality with flask, powered by lambda and API Gateway, with deployment help from zappa.io
* Simple backend functionality that processes a form, stores the data in a DynamoDB database and sends an email to the administrator with SES

You can read about the motivation behind it [here](https://medium.com/@rrosen326/a-semi-static-site-with-s3-lambda-jekyll-and-flask-93c33c0fc820).

If you know a bit about AWS, you should be up and running in an hour.  If you've never used AWS, budget a day to a day and a half. 

## Instructions

1. Clone this repo
1. Read the [Zappa.io documentation](https://github.com/Miserlou/Zappa)
1. Set up python
    ```
    cd hellolambda_api
    python3 --version # ==> confirm >= 3.6.0
    python3 -m venv pyvenv
    source pyvenv/bin/activate
    pip install flask flask_cors  awscli boto3 zappa
    pip install -e ..
    python devserver.py
    ```
    1. In browser: `http://127.0.0.1:5285/api/ping?does_it_work=yes` ==> {"does_it_work": "yes"}
    1. Python debugger - set up your python debugger or IDE (I use pycharm) so you can debug your flask API
1. [Install Jekyll](http://jekyllrb.com/docs/installation/)
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
    1. Open the browser debug console to make sure there are no errors  
        (Note - there will be a 404 error for private_config.js. Ignore it.)
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
###DynamoDB
1. Create table: hellolambda (or new name and update config.py)
    * Primary Key: "pk" (string)  
    Note: I do not know what the best primary key format is. After some trial and error I've settled on 'tag-<datestr>'. I'm pretty sure this would be frowned on, but its easy, flexible, and probably doesn't matter for the table size I'll be using.
    * Default Setting: *No*
        * Set capacity to 1/1 unless you have a reason not to
1. Test
    * Spin up your local python debugger and run the dev server
    * Open the test page (either on S3, or locally with jekyll serve - it doesn't matter which). 
    * Make sure your test page endpoint selector is selecting localhost
    * Test ping, to confirm everything is running properly
    * Test DynamoDB and debug
1. `zappa update`
1. Test on S3

### SES (Simple Email Service)
Setting up SES is a bit more involved.  Follow [the documentation](https://aws.amazon.com/documentation/ses/).  When complete, do the same process as you did with DynamoDB - test locally with your python debugger, zappa update, test on AWS. 

## Production
Once you've got all your individual services tested, its time to test your production form.

Once that's complete, you should probably either remove your test page or hide it, because it's probably not good to have your test functions out there. To hide it, create a long random number (eg: a [SHA-256](http://www.xorbin.com/tools/sha256-hash-calculator)).  Rename site/test to site/<LONG_RANDOM>.  In config.py, set 'TEST_PATH_PREFIX' to <LONG_RANDOM>.  Redploy (`bin/update`).  Then to try your test page, you'll have to copy / paste it the first time, but after that when you start typing, the hepful browser will autocomplete it. 

## Pull Requests, Please
If you find any errors, please submit a PR. If you don't know how, just submit an issue. 

