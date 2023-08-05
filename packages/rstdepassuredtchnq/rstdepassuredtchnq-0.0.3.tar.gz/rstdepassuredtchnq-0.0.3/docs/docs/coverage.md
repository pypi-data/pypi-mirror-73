# Code Coverage Report
_Ref: https://www.youtube.com/watch?v=7BJ_BKeeJyM_
> pip3 install coverage

## Check coverage

``` 
> coverage run rstdepassuredtchnq/core/base/apihelpers/request_methods.py 
>  coverage run tests/test_end_to_end.py
``` 

# check for the coverage report

``` 
>  coverage report
``` 

# Check the detailed coverage report

``` 
>  coverage report -m 
``` 

## Get coverage report in HTML

``` 
> coverage html
>>> then go to folder 'htmlcov' for HTML report
``` 

## PyTest - Test Coverage Report
_Ref: https://www.youtube.com/watch?v=VF0JvmredAI_

``` 
> pip3 install pytest-cov
>  pytest --cov=.     (Execute all the files in the project)
>  pytest --cov=. --cov-report=html   (generate HTML report)
>>> go to htmlcov folder and check for index.html report 
>>> add the excluding files/path in '.coveragerc'
``` 

# MkDocs

_Ref: https://www.youtube.com/watch?v=aXxt9OZNhnU&t=3s_

## Installation 

Install the mkdocs package using pip:

``` 
> pip3 install mkdocs
``` 

You should now have the mkdocs command installed on your system. Run mkdocs
--version to check that everything worked okay.

``` 
> mkdocs --version
``` 

## Getting Started

``` 
> mkdocs new docs
> cd docs
``` 

MkDocs comes with a built-in dev-server that lets you preview your documentation as you work on it. Make sure you're in the same directory as the mkdocs.yml configuration file, and then start the server by running the mkdocs serve command:

``` 
>  mkdocs serve
``` 

Open up http://127.0.0.1:8000/ in your browser, and you'll see the default home page being displayed.