-"""
Testing handler customer subscription
"""
import pytest
import requests
from unittest import mock
from handlerSubCustomer import handlerSubCustomer

@mock.patch('requests.get')
def test_error_handling_on_get_request(mock_get):
    mock_get.return_value.status_code = 404
    result = handlerSubCustomer(123, 'free')
    assert result == None

@mock.patch('requests.put')
def test_error_handling_on_put_request(mock_put):
    mock_put.return_value.status_code = 500
    result = handlerSubCustomer(123, 'free')
    assert result == None

@mock.patch('requests.put')
@mock.patch('requests.get')
def test_customer_exists(mock_get, mock_put):
    mock_get.return_value.status_code = 200
    mock_put.return_value.status_code = 200
    result = handlerSubCustomer(123, 'free')
    assert result == None