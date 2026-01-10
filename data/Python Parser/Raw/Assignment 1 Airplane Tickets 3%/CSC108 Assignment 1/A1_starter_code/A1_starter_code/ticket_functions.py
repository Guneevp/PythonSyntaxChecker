"""CSC108: Fall 2024 -- Assignment 1: Airline Tickets

This code is provided solely for the personal and private use of students taking
CSC108 at the University of Toronto Mississauga. Copying for purposes other than this use is
expressly prohibited. All forms of distribution of this code, whether as given 
or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2024 Rutwa Engineer, Dan Zingaro, Peter Dixon, Randy Hickey, Romina Piunno
"""


# Constants
YEAR = 0
MONTH = 4
DAY = 6
FROM = 8
TO = 11
SEAT = 14
FLYER = 17

WINDOW = 'window'
AISLE = 'aisle'
MIDDLE = 'middle'


def get_flyer_info(ticket: str) -> str:
    """Return the flyer number of the flyer for this ticket, if present. 
    Otherwise, return the empty string.
    
    >>> get_flyer_info('20230915YYZYEG12F')
    ''
    >>> get_flyer_info('20230915YYZYEG12F1236')
    '1236'
    """
    return ticket[FLYER:]


def visits_airport(ticket: str, airport: str) -> bool:
    """
    Returns True if the airport is in the ticket's from or to section.
    Returns False otherwise.
    Case-sensitive

    >>> visits_airport("20230915YYZYEG12F1236", "YEG")
    True
    >>> visits_airport("20230915YYZYEG12F1236", "LHR")
    False
    """
    return airport in ticket[FROM:SEAT]


def get_seat_type(ticket: str) -> str:
    """
    Returns the position of the passenger seat if valid seat.
    Possible positions are Window, Middle, Aisle
    Returns an empty string if invalid seat

    >>> get_seat_type("20230915YYZYEG12F1236")
    'window'
    >>> get_seat_type("20230915YYZYEG12R1236")
    ''
    """
    if ticket[SEAT + 2] in "AF":
        return WINDOW
    elif ticket[SEAT + 2] in "BE":
        return MIDDLE
    elif ticket[SEAT + 2] in "CD":
        return AISLE
    return ""


def is_valid_seat(ticket: str) -> bool:
    """
    Returns true if the ticket's seat information is valid.
    Returns false if invalid
    Valid seats have a row number between 01 and 30
    Valid seats have a row letter that is any character ABCDEF

    >>> is_valid_seat("20230915YYZYEG12F1236")
    True
    >>> is_valid_seat("20230915YYZYEG12G1236")
    False
    >>> is_valid_seat("20230915YYZYEG31F1236")
    False
    >>> is_valid_seat("20230915YYZYEG00F1236")
    False
    """
    seat = int(ticket[SEAT:SEAT + 2])
    return 30 >= seat >= 1 and (ticket[SEAT + 2] in "ABCDEF")


def is_valid_flyer(ticket: str) -> bool:
    """
    Returns True if the flyer number is valid
    Returns True if the flyer number is empty
    A valid flyer number consists of exactly four
    digits and the sum of the first three digits taken
    modulo 10 is equal to the fourth digit

    >>> is_valid_flyer("20230915YYZYEG00F1236")
    True
    >>> is_valid_flyer("20230915YYZYEG00F1237")
    False
    >>> is_valid_flyer("20230915YYZYEG00F")
    True
    """
    if len(ticket) == 17:
        return True
    elif len(ticket) == 21:
        calculation = int(ticket[FLYER]) + int(ticket[FLYER + 1])
        calculation2 = calculation + int(ticket[FLYER + 2])
        return calculation2 % 10 == int(ticket[FLYER + 3])
    else:
        return False


def is_valid_ticket(ticket: str) -> bool:
    """
    Takes a ticket of valid length and returns True if
    and only if the ticket has a valid flyer number,
    a valid seat number, and if the to and from airports
    are different.

    >>> is_valid_ticket("20230915YYZYEG01F1236")
    True
    >>> is_valid_ticket("20230915YYZYEG01F")
    True
    >>> is_valid_ticket("20230915YYZYEG01F1237")
    False
    >>> is_valid_ticket("20230915YYZYEG01R1236")
    False
    >>> is_valid_ticket("20230915YYZYEG00F1236")
    False
    >>> is_valid_ticket("20230915YYZYYZ01F1236")
    False
    """
    seat = is_valid_seat(ticket)
    flyer = is_valid_flyer(ticket)
    return ticket[FROM:TO] != ticket[TO:SEAT] and seat and flyer


def days_until(ticket: str, date: str) -> int:
    """
    Returns the number of days from the date it is
    to the ticket date.
    Return value may be negative

    >>> days_until('20230908YULYYZ07C2349', '20230901')
    7
    >>> days_until('20240430YYCYEG11E', '20230901')
    244
    >>> days_until('20220101YQUYEG03D6411', '20230901')
    -605
    """
    ticket_date = (int(ticket[YEAR:MONTH]) * 365 + int(ticket[MONTH:DAY])
                   * 30 + int(ticket[DAY:FROM]))
    today = (int(date[YEAR:MONTH]) * 365 + int(date[MONTH:DAY])
             * 30 + int(date[DAY:FROM]))
    return ticket_date - today
