#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'jicaiauto'
__script__ = 'jicaiauto.py'
__create_time__ = '2020/7/2 18:20'

from jicaiauto.jicaiautodb import DB
from requests import request
from jsonpath import jsonpath
from re import findall
from appium import webdriver as app_driver
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver, WebElement, WebDriverException
from selenium.webdriver.support.wait import WebDriverWait, TimeoutException
from selenium import webdriver

PUBLIC_VARS = {}

def action(b=None, cmd=None, loc=None, data=None, contains_assert=None, equal_assert=None):
    db = DB()
    r = db.select(f"select is_element,is_driver,code from keyword where testtype = 1 and command like '%{cmd}%' or key='{cmd}' limit 1;")
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

def client(method='POST', url='', headers=None, params=None, body=None, json_path=None, json_assert=None, contains_assert=None,
           _re='left_template(.+?)right_template', _re_var='change_key', file=None, auth=None, proxies=None, verify=True,
           cert=None, *args, **kwargs):
    if method.lower() == 'get':
        res = request(method=method, url=url, headers=headers, params=params, verify=verify, **kwargs)
    else:
        res = request(method=method, url=url, headers=headers, body=body, verify=verify, **kwargs)
    global PUBLIC_VARS
    PUBLIC_VARS[_re_var] = findall(_re, res.text)[0]
    try:
        if json_path:
            assert json_assert == jsonpath(res.json(), '$' + json_path)
        else:
            assert contains_assert in res.text
    except:
        if contains_assert:
            assert contains_assert in res.text

def app(d=None, cmd='', loc='', data='', contains_assert=None, equal_assert=None):
    pass