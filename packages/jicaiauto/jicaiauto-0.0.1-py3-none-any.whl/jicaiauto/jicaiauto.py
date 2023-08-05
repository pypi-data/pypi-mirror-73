#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiTools'
__script__ = 'core.py'
__create_time__ = '2020/7/2 18:20'

from jicaiauto.jicaiautodb import DB
from requests import request
from jsonpath import jsonpath
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver, WebElement, WebDriverException
from selenium.webdriver.support.wait import WebDriverWait, TimeoutException

def action(b=None, cmd=None, loc=None, data=None, contains_assert=None, equal_assert=None):
    db = DB()
    r = db.select(f"select is_element,is_driver,code from keyword where command like '%{cmd}%' or key='{cmd}' limit 1;")
    if r[0][0] == 1:
        if loc not in ('', None):
            if isinstance(b, WebDriver):
                WebDriverWait(b, 30, 0.5).until(lambda b: b.find_element_by_xpath(loc))
                e = b.find_element_by_xpath(loc)
                if '%s' in r[0][2] or '%d' in r[0][2]:
                    eval(r[0][2] % data)
                    if contains_assert:
                        assert contains_assert in eval(r[0][2] % data)
                    elif equal_assert:
                        assert equal_assert == eval(r[0][2] % data)
                else:
                    eval(r[0][2])
                    if contains_assert:
                        assert contains_assert in eval(r[0][2])
                    elif equal_assert:
                        assert equal_assert == eval(r[0][2])
    elif r[0][1] == 1:
        if isinstance(b, WebDriver):
            if '%s' in r[0][2] or '%d' in r[0][2]:
                eval(r[0][2] % data)
                if contains_assert:
                    assert contains_assert in eval(r[0][2] % data)
                elif equal_assert:
                    assert equal_assert == eval(r[0][2] % data)
            else:
                eval(r[0][2])
                if contains_assert:
                    assert contains_assert in eval(r[0][2])
                elif equal_assert:
                    assert equal_assert == eval(r[0][2])
    else:
        if '%s' in r[0][2] or '%d' in r[0][2]:
            eval(r[0][2] % data)
            if contains_assert:
                assert contains_assert in eval(r[0][2] % data)
            elif equal_assert:
                assert equal_assert == eval(r[0][2] % data)
        else:
            eval(r[0][2])
            if contains_assert:
                assert contains_assert in eval(r[0][2])
            elif equal_assert:
                assert equal_assert == eval(r[0][2])

def api_step(func):
    def wrapper(url, method, headers, params, body, json_path, json_assert, contains_assert, *args, **kwargs):
        res = request(method=method, url=url, headers=headers, params=params, body=body, verify=False)
        try:
            if json_path:
                assert json_assert == jsonpath(res.json(), '$' + json_path)
            else:
                assert contains_assert in res.text
        except:
            if contains_assert:
                assert contains_assert in res.text
        return func(*args, **kwargs)
    return wrapper
