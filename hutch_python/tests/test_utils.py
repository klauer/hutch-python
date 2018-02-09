import logging

from hutch_python import utils

logger = logging.getLogger(__name__)


def test_iterable_namespace():
    logger.debug('test_iterable_namespace')

    ns = utils.IterableNamespace(a=1, b=2, c=3)

    assert list(ns) == [1, 2, 3]


def test_extract_objs():
    logger.debug('test_extract_objs')
    # Has no __all__ keyword
    objs = utils.extract_objs('sample_module_1')
    assert objs['hey'] == '4horses'
    assert objs['milk'] == 'cows'
    assert objs['some_int'] == 5
    # Has an __all__ keyword
    objs = utils.extract_objs('sample_module_2.py')
    assert objs == dict(just_this=5.0)
    # Doesn't exist
    objs = utils.extract_objs('fake_module_243esd')
    assert objs == {}
    objs = utils.extract_objs('sample_module_1.hey')
    assert objs['hey'] == '4horses'
    objs = utils.extract_objs('sample_module_1.some_func()')
    assert objs['some_func'] == 4


def test_find_class():
    logger.debug('test_find_class')
    # Find some standard type that needs an import
    found_Request = utils.find_class('urllib.request.Request')
    from urllib.request import Request
    assert found_Request is Request
    # Find some built-in type
    found_float = utils.find_class('float')
    assert found_float is float
