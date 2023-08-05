#!/usr/bin/env python

'''
`popsingleton` tests for `iterpop` package.
'''

import pytest


from iterpop import iterpop as ip


def test_pophomogenous_homogenous():
    '''
    pophomogenous should pop out homogenous values.
    '''
    assert ip.pophomogenous([0, 0]) == 0
    assert ip.pophomogenous(['a']) == 'a'
    assert ip.pophomogenous('aaaaaaa') == 'a'
    assert ip.pophomogenous((42 for __ in range(10))) == 42
    assert ip.pophomogenous({"monty"}) == "monty"

def test_pophomogenous_empty():
    '''
    pophomogenous should pop throw or provide default on empty.
    '''
    for container in [], '', set(), range(0), {}:
        with pytest.raises(ValueError) as excinfo:
            ip.pophomogenous(container)
        assert 'is empty' in str(excinfo.value)

    for container in [], '', set(), range(0), {}:
        assert ip.pophomogenous(container, catch_empty=True) == None

def test_pophomogenous_heterogeneous():
    '''
    pophomogenous should pop throw or provide default on heterogenous.
    '''
    for container in [1,2], 'ab', {'al','bb'}, range(2), {1:'2', 3:'4'}:
        with pytest.raises(ValueError) as excinfo:
            ip.pophomogenous(container)
        assert 'is heterogeneous' in str(excinfo.value)

    for container in [1,2], 'ab', {'al','bb'}, range(2), {1:'2', 3:'4'}:
        assert ip.pophomogenous(container, catch_heterogeneous=True) == None

def test_pophomogenous_default():
    '''
    pophomogenous default should be configurable.
    '''
    for container in [], '', set(), range(0), {}:
        assert ip.pophomogenous(
            container,
            catch_empty=True,
            default='Madonna'
        ) == 'Madonna'

    for container in [1,2], 'ab', {'al','bb'}, range(2), {1:'2', 3:'4'}:
        assert ip.pophomogenous(
            container,
            catch_heterogeneous=True,
            default='Cher',
        ) == 'Cher'
