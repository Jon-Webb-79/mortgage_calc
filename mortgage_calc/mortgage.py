# Import necessary packages here
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
    HOA fees.  This class has the following public attributes.

    :ivar value: The value of the property.
    :ivar payment: The down payment on the property.
    :ivar interest: The interests rate for the loan.
    :ivar months: The number of months over which the loan is distributed.
    :ivar tax: The rate the property is taxed at.
    :ivar ins_rate: The insurance rate for the property.
    :ivar pmi_rate: The Private Mortgage Inusrance. Only applicable when the down
                    payment is less than 20% of the home value.
    :ivar loan_amount: The value of the loan, value - payment.
    :ivar monthly_taxes: The tax value paid per month.
    :ivar monthly_insurance: The insurance paid monthly.
    :ivar monthly_total: The total amount paid on the property per month.

    Examples
    --------

    Example showing how to instantiate a class and how to access and print attributes.

    .. code-block:: python

       from mortgage_calc.mortgage import Mortgage

       # Instantiate class with custom mortage period and interest rate
       value = 500000.0  # Propertry value
       payment = 300000.0  # down payment on property
       rate = 4.5
       months = 150.0
       property = Mortgage(value, payments, interest=rate, months=months)
       # Print all attributes
       print(property)
       # Print specifc attribute
       print(property.monthly_total)

    .. code-block:: bash

       Down Payment: $400000.00
       Loan Amount: $200000.00
       Primary Mortgage: $63986.77
       Taxes: $580.00
       Insurance: $210.00
       Total Monthly Payment: $64776.77

       64776.77

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
        self.monthly_total = self._monthly_total()

    # ------------------------------------------------------------------------------------------

    def total_interest(self) -> float:
        """
        Calculate the total amount of interest paid over the amortized period.

        Example
        -------

        .. code-block:: python

           from mortgage_calc.mortgage import Mortgage
           home = Mortgage(600000.0, 400000.0, interest=3.15, tax=0.45)
           interest = home.total_interest()
           print(f"Total Interest: {interest:.2f}")

        .. code-block:: bash

           >> Total Interest: 109410.55
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

        Example
        -------

        .. code-block:: python

           from mortgage_calc.mortgage import Mortgage

           home = Mortgage(600000.0, 100000.0, interest=3.15, tax=0.45)
           pmi = home.total_pmi()
           print("Total PMI paid: {pmi:.2f}")

        .. code-block:: bash

           >> Total PMI paid: 10203.35

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

    # ------------------------------------------------------------------------------------------

    def _monthly_total(self) -> float:
        percent_down = self.payment / self.value
        pmi = self.loan_amount * (self.pmi_rate / 100.0) / 12.0
        if percent_down < 0.20:
            total_value = (
                self.mortgage_payment + self.monthly_taxes + self.monthly_insurance + pmi
            )
        else:
            total_value = (
                self.mortgage_payment + self.monthly_taxes + self.monthly_insurance
            )
        return total_value


# ==========================================================================================
# ==========================================================================================


def affordable_home_value(
    monthly_total: float,
    down_payment: float,
    interest: float = 7.145,
    months: float = 360,
    tax: float = 1.16,
    ins_rate: float = 0.42,
) -> float:
    """
    Calculate the total value of a home that can be afforded based on a given
    monthly payment and down payment.

    :param monthly_total: The total monthly payment, including tax and insurance but
                          excluding PMI.
    :param down_payment: The down payment for the home.
    :param interest: The annual interest rate for the loan (defaulted to 7.145%).
    :param months: The duration of the loan in months (defaulted to 360).
    :param tax: The annual tax rate for the property (defaulted to 1.16%).
    :param ins_rate: The annual insurance rate for the property
                     (defaulted to 0.42%).

    :return: The total value of the home that can be afforded.

    Example
    -------

    .. code-block:: python

       from mortgage_calc.Mortgage import affordable_home_value)

       val = affordable_home_value(2815.21, 300000.0, months=360,
                                   interest=7.145, tax=1.16)
       print(f"Home Value: {val:.2f}")

    .. code-block:: bash

       >> 600000.00
    """
    tolerance = 1e-4

    # Set an initial guess for the affordable home value
    affordable_home_value = down_payment + (monthly_total * months)

    # Create an instance of the Mortgage class to access the monthly_total attribute
    while True:
        home = Mortgage(
            affordable_home_value, down_payment, interest, months, tax, ins_rate
        )
        calculated_monthly_total = home.monthly_total

        if abs(calculated_monthly_total - monthly_total) < tolerance:
            break

        # Adjust the affordable home value based on the difference in monthly totals
        affordable_home_value += (monthly_total - calculated_monthly_total) * (
            months / 12.0
        )

    return affordable_home_value


# ==========================================================================================
# ==========================================================================================
# eof
