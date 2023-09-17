# Import necessary packages here

from math import isclose

from mortgage_calc.mortgage import Mortgage

# ==========================================================================================
# ==========================================================================================
# File:    test.py
# Date:    September 14, 2023
# Author:  Jonathan A. Webb
# Purpose: Describe the types of testing to occur in this file.
# Instruction: This code can be run in hte following ways
#              - pytest # runs all functions beginnning with the word test in the
#                         directory
#              - pytest file_name.py # Runs all functions in file_name beginning
#                                      with the word test
#              - pytest file_name.py::test_func_name # Runs only the function
#                                                      titled test_func_name in
#                                                      the file_name.py file
#              - pytest -s # Runs tests and displays when a specific file
#                            has completed testing, and what functions failed.
#                            Also displays print statments
#              - pytest -v # Displays test results on a function by function
#              - pytest -p no:warnings # Runs tests and does not display warning
#                          messages
#              - pytest -s -v -p no:warnings # Displays relevant information and
#                                supports debugging
#              - pytest -s -p no:warnings # Run for record
# ==========================================================================================
# ==========================================================================================
# Insert Code here


def test_mortgage_rate():
    """
    Calculate monthly mortgage value
    """
    home = Mortgage(600000.0, 500000.0, interest=3.15, tax=0.45)
    assert isclose(home.mortgage_payment, 429.74, rel_tol=1.0e-3)
    assert isclose(home.monthly_taxes, 225.0, rel_tol=1.0e-3)


# ------------------------------------------------------------------------------------------


def test_pmi_calc():
    """
    Test the PMI calculator
    """
    home = Mortgage(600000.0, 100000.0, interest=3.15, tax=0.45)
    pmi = home.total_pmi()
    assert isclose(10203.35, pmi, rel_tol=1.0e-3)


# ------------------------------------------------------------------------------------------


def test_interest_calc():
    """
    Test the interest calculator
    """
    home = Mortgage(600000.0, 400000.0, interest=3.15, tax=0.45)
    interest = home.total_interest()
    assert isclose(109410.55, interest, rel_tol=1.0e-3)


# ==========================================================================================
# ==========================================================================================
# eof
