# Python API Testing

_Ref : https://medium.com/@peter.jp.xie/rest-api-testing-using-python-751022c364b8_

_Youtube Ref : https://www.youtube.com/watch?v=5EPaVXz6A4o&list=PLwkyDFh-TwzL5pQseZGHY0DgVl2-dECif&index=1_

##Installation

```bash
git clone https://github.com/seleniumbase/SeleniumBase.git
cd SeleniumBase/
pip install -r requirements.txt
python setup.py install
```
Installing pytest

```bash
> pip install -U requests Flask pytest pytest-html

> pip3 install -U requests Flask pytest pytest-html
```

## Start the Mock Server first to check the Mock Test cases

Starting Mock Services 
```bash
> python mock/mock-simple-service.py
```

Executing Mock Tests

```bash
> pytest -sv tests/test_mock_service.py
```

Reports:

```bash
> pytest -sv test/test-first.py --html report/target/index.html
```

##DEBUG

Add the below code to Debug in the command line:

```bash
>  import pdb;pdb.set_trace()
```
