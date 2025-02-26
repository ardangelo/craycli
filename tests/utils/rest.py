""" REST Utils for testing

MIT License

(C) Copyright [2020] Hewlett Packard Enterprise Development LP

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""
# pylint: disable=redefined-outer-name, invalid-name, unused-import
# pylint: disable=too-many-arguments, unused-argument, import-error
# pylint: disable=wrong-import-order
import json

import requests_mock as req_mock
import pytest


def _request_cb(request, context):
    resp = {
        'method': request.method,
        'url': request.url,
    }
    if request.body is not None:
        try:
            resp['body'] = json.loads(request.body)
        except Exception:  # pylint: disable=broad-except
            resp['body'] = request.body
    return json.dumps(resp)


@pytest.fixture()
def rest_mock(requests_mock):
    """ Catch any rest callouts and return the request info instead """
    # pylint: disable=protected-access
    requests_mock._adapter.register_uri(req_mock.ANY, req_mock.ANY,
                                        text=_request_cb)
