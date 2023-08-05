# Python API Testing

_Ref : https://medium.com/@peter.jp.xie/rest-api-testing-using-python-751022c364b8_

_Youtube Ref : https://www.youtube.com/watch?v=5EPaVXz6A4o&list=PLwkyDFh-TwzL5pQseZGHY0DgVl2-dECif&index=1_

##Installation:
```
> pip install -U requests Flask pytest pytest-html
> pip3 install -U requests Flask pytest pytest-html
```

##Execution:
```
> pytest 
> pytest tests/test_api.py
> pytest -sv test-first-post.py
> pytest --cov=myproj tests/
> pytest -sv test/test_api_auth.py 
> pytest -sv tests/test_api.py --html report/target/index.html
```

### Start the Mock Server first to check the Mock Test cases

Starting Mock Services 
```
> python mock/mock-simple-service.py
```

Executing Mock Tests
```
> pytest -sv tests/test_mock_service.py
```

Reports:
```
> pytest -sv test/test-first.py --html report/target/index.html
```

##DEBUG

Add the below code to Debug in the command line:
```
>  import pdb;pdb.set_trace()
```

## Setup tools
_Ref: https://www.youtube.com/watch?v=RgfOjrjhCMY_

Building package

```
> python3 setup.py sdist bdist_wheel   (Create wheel with Zip files)
> > python3 setup.py  bdist_wheel

> pip3 install twine
```

Check distribution

```
> twine check dist/*
> twine upload --repository rstdepassuredtchnq dist/*
```

Upload the Package to PyPi

```
> twine upload dist/*  
> twine upload dist/* --skip-existing      (Skip if file already Existing in the repo)
```

Check for the package uploaded:

_https://pypi.org/project/pythondeeprestassured/_

Go to terminal 

```
> pip3 install rstdepassuredtchnq
> python3 
```

Execute the below code to check:

```
from rstdepassuredtchnq.core.base.apihelpers.request_methods import BaseAPIHelper

from rstdepassuredtchnq.core.base.apihelpers.api_methods import APIMethods
api_req = APIMethods()

resp = api_req.get_request("https://reqres.in/api/users", "page=2")

resp.text
```

```
> pip3 uninstall restdeepassuredtool
```

## Code Coverage Report
_Ref: https://www.youtube.com/watch?v=7BJ_BKeeJyM_

```
> pip3 install coverage
```

###### Check coverage

```
> coverage run rstdepassuredtchnq/core/base/apihelpers/request_methods.py 
>  coverage run tests/test_end_to_end.py
```


###### check for the coverage report

```
>  coverage report
```

######Check the detailed coverage report 

```
>  coverage report -m 
```

######Get coverage report in HTML

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

## MkDocs

_Ref: https://www.youtube.com/watch?v=aXxt9OZNhnU&t=3s_

### Installation 

Install the mkdocs package using pip:

> pip3 install mkdocs

You should now have the mkdocs command installed on your system. Run mkdocs
--version to check that everything worked okay.

> mkdocs --version

### Getting Started

> mkdocs new docs
> cd docs

MkDocs comes with a built-in dev-server that lets you preview your documentation as you work on it. Make sure you're in the same directory as the mkdocs.yml configuration file, and then start the server by running the mkdocs serve command:

>  mkdocs serve

Open up http://127.0.0.1:8000/ in your browser, and you'll see the default home page being displayed.