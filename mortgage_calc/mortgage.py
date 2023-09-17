# Import necessary packages here

# import sys
# import os
# ==========================================================================================
# ==========================================================================================

# File:    mortgage.py
# Date:    September 14, 2023
# Author:  Jonathan A. Webb
# Purpose: This file contains functions and classes that can be used to estimate
#          purchasing power when buying a home
# ==========================================================================================
# ==========================================================================================
# Insert Code here


class Mortgage:
    """

    :param value: The total value of the property to be purchased
    :param payment: The total down-payment for the property
    :param interest: The annual interest rate for the loan, defaulted to the
                     2023 value of 7.145%
    :param months: The duration of the loan in units of months.  Defaulted to 360
    :param tax: The annual tax rate for the property, defaulted to 1.16%
    :param ins_rate: The annual insurance rate for the property, defaulted
                     to 0.42%.
    :param pmi_rate: The annual rate for private mortgage insurance, defaulted
                     to 1.0%

    This class will determine the monthly payments to be made on a purchased property
    over an entire Amoratized mortgage time line.  This class does not account for
    HOA fees.
    """

    def __init__(
        self,
        value: float,
        payment: float,
        interest: float = 7.145,
        months: float = 360,
        tax: float = 1.16,
        ins_rate: float = 0.42,
        pmi_rate: float = 1.0,
    ):
        self.value = value
        self.payment = payment
        self.interest = interest
        self.months = months
        self.tax = tax
        self.ins_rate = ins_rate
        self.pmi_rate = pmi_rate
        self.loan_amount = value - payment
        self.mortgage_payment = self._amoratized_payments()
        self.monthly_taxes = value * (tax / 100.0) / 12.0
        self.monthly_insurance = value * (ins_rate / 100.0) / 12.0
        pmi = self.loan_amount * (self.pmi_rate / 100.0) / 12.0
        self.monthly_total = (
            self.mortgage_payment + self.monthly_taxes + self.monthly_insurance + pmi
        )

    # ------------------------------------------------------------------------------------------

    def total_interest(self) -> float:
        """
        Calculate the total amount of interest paid over the amortized period.
        """
        total_interest_paid = 0
        remaining_loan = self.loan_amount

        for month in range(int(self.months)):
            monthly_interest_payment = remaining_loan * (self.interest / 100.0) / 12.0
            total_interest_paid += monthly_interest_payment
            remaining_loan -= self.mortgage_payment - monthly_interest_payment

        return total_interest_paid

    # ------------------------------------------------------------------------------------------

    def total_pmi(self) -> float:
        """
        Calculate the total amount paid in Private Mortgage Insurance (PMI).
        Assumes PMI is paid until 20% equity is achieved.
        """
        total_pmi_paid = 0
        percent_down = self.payment / self.value
        remaining_loan = self.loan_amount

        for month in range(int(self.months)):
            if percent_down < 0.20:
                monthly_pmi_payment = remaining_loan * (self.pmi_rate / 100.0) / 12.0
                total_pmi_paid += monthly_pmi_payment

                # Check if 20% equity has been achieved, and stop PMI payments
                if (self.value - remaining_loan) / self.value >= 0.20:
                    break

            monthly_interest_payment = remaining_loan * (self.interest / 100.0) / 12.0
            remaining_loan -= self.mortgage_payment - monthly_interest_payment

        return total_pmi_paid

    # ==========================================================================================
    # PRIVE-LIKE METHODS

    def _amoratized_payments(self) -> None:
        """
        This method will determine the monthly mortgage payment based on the loan
        value, the total valu of the property, and the interest rage
        """
        # Convert annual interest rate to monthly rate
        monthly_interest_rate = (self.interest / 100.0) / 12.0

        # Calcuate the monthly mortgage payment using the formula
        monthly_payment = (self.loan_amount * monthly_interest_rate) / (
            1.0 - (1.0 + monthly_interest_rate) ** -self.months
        )

        return monthly_payment

    # ------------------------------------------------------------------------------------------

    def __str__(self) -> str:
        print_value = f"Property Value: ${self.value}\n"
        print_value += f"Down Payment: ${self.payment:.2f}\n"
        print_value += f"Loan Amount: ${self.loan_amount:.2f}\n"
        print_value += f"Primary Mortgage: ${self.mortgage_payment:.2f}\n"
        print_value += f"Taxes: ${self.monthly_taxes:.2f}\n"
        print_value += f"Insurance: ${self.monthly_insurance:.2f}\n"
        percent_down = self.payment / self.value
        pmi = self.loan_amount * (self.pmi_rate / 100.0) / 12.0
        if percent_down < 0.20:
            total_value = (
                self.mortgage_payment + self.monthly_taxes + self.monthly_insurance + pmi
            )
            print_value += f"PMI: {pmi}"
        else:
            total_value = (
                self.mortgage_payment + self.monthly_taxes + self.monthly_insurance
            )

        print_value += f"Total Monthly Payment: ${total_value:.2f}"
        return print_value


# ==========================================================================================
# ==========================================================================================
# eof
