"""CSC108: Fall 2024 -- Assignment 1: Airline Tickets

This code is provided solely for the personal and private use of students taking
CSC108 at the University of Toronto Mississauga. Copying for purposes other than this use is
expressly prohibited. All forms of distribution of this code, whether as given 
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Rutwa Engineer, Dan Zingaro, Peter Dixon, Randy Hickey, Romina Piunno
"""

import pytest
import checker_generic
import ticket_functions
from typing import Any

FILENAME = 'ticket_functions.py'
PYTA_CONFIG = 'a1_pythonta.json'
TARGET_LEN = 79
SEP = '='

CONSTANTS = {
    'YEAR': 0,
    'MONTH': 4,
    'DAY': 6,
    'FROM': 8,
    'TO': 11,
    'SEAT': 14,
    'FLYER': 17,
    'WINDOW': 'window',
    'AISLE': 'aisle',
    'MIDDLE': 'middle',
}


class TestChecker:
    """Sanity checker for assignment functions."""
    module = ticket_functions

    def test_00_get_flyer_info(self):
        """Function get_flyer_info."""
        self._check_simple_type(
            self.module.get_flyer_info,
            ['20230915YYZYEG12F1236'],
            str)

    def test_01_visits_airport(self):
        """Function visits_airport."""
        self._check_simple_type(
            self.module.visits_airport,
            ['20230915YYZYEG12F1236', 'YVR'],
            bool)

    def test_02_get_seat_type(self):
        """Function get_seat_type."""
        self._check_simple_type(
            self.module.get_seat_type,
            ['20230915YYZYEG12F1236'],
            str)

    def test_03_is_valid_seat(self):
        """Function is_valid_seat."""
        self._check_simple_type(
            self.module.is_valid_seat,
            ['20230915YYZYEG12F1236'],
            bool)

    def test_04_is_valid_flyer(self):
        """Function is_valid_flyer."""
        self._check_simple_type(
            self.module.is_valid_flyer,
            ['20230915YYZYEG12F1236'],
            bool)

    def test_05_is_valid_ticket(self):
        """Function is_valid_ticket."""
        self._check_simple_type(
            self.module.is_valid_ticket,
            ['20230915YYZYEG12F1236'],
            bool)

    def test_06_days_until(self):
        """Function days_until."""
        self._check_simple_type(
            self.module.days_until,
            ['20230908YULYYZ07C2349', '20230901'],
            int)

    def _check_simple_type(self, func: callable, args: list, ret_type: type):
        """Check that func called with arguments args returns a value of type
        ret_type. Display the progress and the result of the check.
        """

        print('\nChecking {}...'.format(func.__name__))
        result = checker_generic.type_check_simple(func, args, ret_type)
        assert result[0], result[1]

        print('  check complete')

    def _check_list_of_Ts(self, func: callable, args: list, ret_type: type):
        """Check that func called with arguments args returns a value of type
        ret_type.

        """

        result = checker_generic.returns_list_of_Ts(func, args, ret_type)
        assert result[0], result[1]
        return result

    def _is_dict_of_Ks_and_list_Vs(self, result: object, key_tp: type,
                                   val_tp: type, msg: str):
        """Check if result is a dict with keys of type key_tp and values
         of type list that are non-empty and with elements of type val_tp.

        """

        assert isinstance(result, dict), msg

        for (key, val) in result.items():
            assert isinstance(key, key_tp), (
                    msg + ', but one or more keys is not of type ' + str(key_tp))
            assert isinstance(val, list), (msg + ', but one or more values is not of type list')

            assert val != [], msg + ' and the values should be non-empty lists'
            for item in val:
                assert isinstance(item, val_tp), \
                    msg + ', but one or more items in the values list(s) is not of type ' + str(
                        val_tp)

    def test_check_constants(self) -> None:
        """Check that, for each (name, value) pair in name2value, the value of
        a variable named name in module mod is value.
        """

        for name, expected in CONSTANTS.items():
            actual = getattr(self.module, name)
            msg = 'The value of constant {} should be {} but is {}.'.format(
                name, expected, actual)
            assert expected == actual, msg


print(''.center(TARGET_LEN, SEP))
print(' Start: checking coding style with PythonTA '.center(TARGET_LEN, SEP))
checker_generic.run_pyta(FILENAME, PYTA_CONFIG)
print(' End checking coding style with PythonTA '.center(TARGET_LEN, SEP))

print(' Start: checking type contracts '.center(TARGET_LEN, SEP))
pytest.main(['--show-capture', 'no', '--disable-warnings', '--tb=short',
             'a1_checker.py'])
print(' End checking type contracts '.center(TARGET_LEN, SEP))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style with Python TA')
print('  - checking type contract\n')
