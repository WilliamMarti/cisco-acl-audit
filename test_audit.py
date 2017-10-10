# test_capitalize.py

import pytest
from audit import Audit

def test_audit_printArray():


	testinput = ['test1', 'test2', 'test3']

	testaudit = Audit()

	assert testaudit.printArray(testinput) == 'test1\ntest2\ntest3\n'


def test_audit_printArray_raises_exception_on_bad_type():

	testaudit = Audit()

	testinput = 1

	with pytest.raises(Exception):
		testaudit.printArray(testinput)



def test_audit_diff():


	testinput1 = ['test1', 'test2', 'test3']
	testinput2 = ['test1', 'test2']

	testaudit = Audit()

	assert testaudit.diff(testinput1,testinput2) == [u'test3']
