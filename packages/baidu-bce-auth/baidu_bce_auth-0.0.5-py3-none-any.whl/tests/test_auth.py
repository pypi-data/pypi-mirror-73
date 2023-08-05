# -*- coding: utf-8 -*-

from datetime import datetime
from unittest.mock import Mock, patch

from bceauth.auth import _to_canonical_query_string, make_auth


@patch('bceauth.auth.datetime')
def test_make_auth_without_headers_to_sign(mocked):
    # 参考：https://cloud.baidu.com/doc/Reference/s/wjwvz1xt2
    # 这个用例和上述链接的示例，使用相同的输入，得到相同的输出

    mocked.utcnow = Mock(return_value=datetime(2015, 4, 27, 8, 23, 49))

    actual = make_auth(
        ak='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        sk='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
        method='PUT',
        path='/v1/test/myfolder/readme.txt',
        params={
            'partNumber': 9,
            'uploadId': 'a44cc9bab11cbd156984767aad637851',
        },
        headers={
            'Host': 'bj.bcebos.com',
            'Date': 'Mon, 27 Apr 2015 16:23:49 +0800',
            'Content-Type': 'text/plain',
            'Content-Length': 8,
            'Content-Md5': 'NFzcPqhviddjRNnSOGo4rw==',
            'x-bce-date': '2015-04-27T08:23:49Z',
        }
    )

    expect = 'bce-auth-v1/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/2015-04-27T08:23:49Z/1800/host;x-bce-date/1b8de5a23a56eef657c69f94c621e7acd227d049a4ba577f537d5e5cebf0cf32'  # noqa
    assert expect == actual


@patch('bceauth.auth.datetime')
def test_make_auth_with_headers_to_sign(mocked):
    # 参考：https://cloud.baidu.com/doc/Reference/s/wjwvz1xt2
    # 这个用例和上述链接的示例，使用相同的输入，得到相同的输出

    mocked.utcnow = Mock(return_value=datetime(2015, 4, 27, 8, 23, 49))

    actual = make_auth(
        ak='aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        sk='bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
        method='PUT',
        path='/v1/test/myfolder/readme.txt',
        params={
            'partNumber': 9,
            'uploadId': 'a44cc9bab11cbd156984767aad637851',
        },
        headers={
            'Host': 'bj.bcebos.com',
            'Date': 'Mon, 27 Apr 2015 16:23:49 +0800',
            'Content-Type': 'text/plain',
            'Content-Length': 8,
            'Content-Md5': 'NFzcPqhviddjRNnSOGo4rw==',
            'x-bce-date': '2015-04-27T08:23:49Z',
        },
        headers_to_sign={
            'Host',
            'Content-Type',
            'Content-Length',
            'Content-Md5',
        },
    )

    expect = 'bce-auth-v1/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/2015-04-27T08:23:49Z/1800/content-length;content-md5;content-type;host;x-bce-date/d74a04362e6a848f5b39b15421cb449427f419c95a480fd6b8cf9fc783e2999e'  # noqa
    assert expect == actual


def test_to_canonical_query_string():
    # https://cloud.baidu.com/doc/Reference/s/njwvz1yfu#3-canonicalquerystring
    params = {
        'text': None,
        'text1': '测试',
        'text10': 'test',
    }
    actual = _to_canonical_query_string(params)
    expect = 'text10=test&text1=%E6%B5%8B%E8%AF%95&text='
    assert expect == actual
