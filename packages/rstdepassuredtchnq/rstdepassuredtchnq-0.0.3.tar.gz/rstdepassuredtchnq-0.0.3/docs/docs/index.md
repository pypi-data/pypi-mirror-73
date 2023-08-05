# Welcome to Deepika Python Testing Site

This is the Sample site for Python Testing Documentation.

##Execution

``` 
> pytest tests/test_api.py 
> pytest 
> pytest -sv test-first-post.py
> pytest --cov=myproj tests/
> pytest -sv test/test_api_auth.py 
> pytest -sv tests/test_api.py --html report/target/index.html
``` 

##Sample Script

```
@pytest.mark.regression
    def test_put_json(self):
        url = '{}/api/users/2'.format(self.Base_url)
        req_payload = self.common_data.read_payload(self.paylod_log_dir, 'update_user.json')

        resp = self.api_req.put_request_no_header(url, req_payload)
        self.api_req.check_status(resp, '200')

        get_name_value = self.common_data.fetch_json(resp.text, 'name')
        self.log.info('Fetched Json Value - name - in Put Request {} '.format(get_name_value))
        assert get_name_value == 'morpheus', 'Validated Updated Name with payload file'

        get_updated_at_value = self.common_data.fetch_json(resp.text, 'updatedAt')
        self.log.info('Fetched Json Value - updatedAt - in Put Request {} '.format(get_updated_at_value))
```

## Sample logs

```
deepirms2619@Deepikas-MBP python-api-testing % pytest tests/test_api.py
============================================================= test session starts ==============================================================
platform darwin -- Python 3.7.8, pytest-5.4.3, py-1.8.0, pluggy-0.13.0 -- /usr/local/bin/python3
cachedir: .pytest_cache
metadata: {'Python': '3.7.8', 'Platform': 'Darwin-19.4.0-x86_64-i386-64bit', 'Packages': {'pytest': '5.4.3', 'py': '1.8.0', 'pluggy': '0.13.0'}, 'Plugins': {'tavern': '1.2.2', 'rerunfailures': '9.0', 'allure-pytest': '2.8.5', 'metadata': '1.10.0', 'reportportal': '5.0.3', 'forked': '1.2.0', 'cov': '2.10.0', 'html': '2.1.1', 'dependency': '0.5.1', 'ordering': '0.6', 'xdist': '1.32.0'}}
rootdir: /Users/deepirms2619/Documents/Project/GitHub/Python/python-api-testing, inifile: pytest.ini
plugins: tavern-1.2.2, rerunfailures-9.0, allure-pytest-2.8.5, metadata-1.10.0, reportportal-5.0.3, forked-1.2.0, cov-2.10.0, html-2.1.1, dependency-0.5.1, ordering-0.6, xdist-1.32.0
collected 5 items                                                                                                                              

tests/test_api.py::TestAPI::test_get_users_page PASSED
tests/test_api.py::TestAPI::test_get_reqre_api PASSED
tests/test_api.py::TestAPI::test_delete_reqre_api PASSED
tests/test_api.py::TestAPI::test_post_body_json_no_header PASSED
tests/test_api.py::TestAPI::test_put_json PASSED

=============================================================== warnings summary ===============================================================
tests/test_api.py::TestAPI::test_get_reqre_api
tests/test_api.py::TestAPI::test_post_body_json_no_header
tests/test_api.py::TestAPI::test_put_json
  /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/urllib3/connectionpool.py:986: InsecureRequestWarning: Unverified HTTPS request is being made to host 'reqres.in'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
    InsecureRequestWarning,

-- Docs: https://docs.pytest.org/en/latest/warnings.html

---------- coverage: platform darwin, python 3.7.8-final-0 -----------
Coverage HTML written to dir htmlcov

======================================================== 5 passed, 3 warnings in 3.34s =========================================================
```