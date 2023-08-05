# Setup tools
_Ref: https://www.youtube.com/watch?v=RgfOjrjhCMY_

##Building package
``` 
> python3 setup.py sdist bdist_wheel   (Create wheel with Zip files)
> > python3 setup.py  bdist_wheel

> pip3 install twine
``` 

##Check distribution
``` 
> twine check dist/*
> twine upload --repository rstdepassuredtchnq dist/*
``` 

##Upload the Package to PyPi
``` 
> twine upload dist/*  
> twine upload dist/* --skip-existing      (Skip if file already Existing in the repo)
``` 

##Check for the package uploaded

_https://pypi.org/project/pythondeeprestassured/_

Go to terminal 

``` 
> pip3 install rstdepassuredtchnq
> python3
```  

##Check the package from PyPi

```
from rstdepassuredtchnq.core.base.apihelpers.request_methods import BaseAPIHelper

from rstdepassuredtchnq.core.base.apihelpers.api_methods import APIMethods
api_req = APIMethods()

resp = api_req.get_request("https://reqres.in/api/users", "page=2")

resp.text
```

##Uninstall the Package from PyPi

``` 
> pip3 uninstall restdeepassuredtool
``` 