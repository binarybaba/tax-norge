#!/usr/bin/env python
import sys
from decimal import Decimal


def tax_norge(amount):
    year = Decimal(12)
    minimal_deduction_min = Decimal(89050)
    minimal_deduction_percent = Decimal(0.43)
    foreign_worker_deduction_max = Decimal(40000)
    foreign_worker_deduction_percent = Decimal(0.10)
    nis_rate = Decimal(0.082)
    tax_rate = Decimal(0.27)
    surtaxes = [
        (Decimal(550550), Decimal(0.09)),
        (Decimal(885600), Decimal(0.03)),
    ]

    total_income = Decimal(amount)
    months = year

    income = total_income * months / year
    minimal_deduction = min(minimal_deduction_min, total_income * minimal_deduction_percent) * months / year

    if '-n' in sys.argv:
        foreign_worker_deduction = Decimal(0.0)
    else:
        foreign_worker_deduction = min(
            foreign_worker_deduction_max, foreign_worker_deduction_percent * income) * months / year
    income_after_deductions = income - minimal_deduction - foreign_worker_deduction

    tax = tax_rate * income_after_deductions
    tax_details = "{tax_rate:.1%} * "\
                  "{income_after_deductions:.2f}".format(**locals())
    tax_details = "| {tax_details:<39} |".format(tax_details=tax_details)
    for total_surtax_amount, surtax_rate in surtaxes:
        surtax_amount = total_surtax_amount * months / year
        if surtax_amount < income_after_deductions:
            tax += (income_after_deductions - surtax_amount) * surtax_rate
            details = "+ ({income_after_deductions:.2f} - {surtax_amount:.2f}) * {surtax_rate:.1%}".format(**locals())
            tax_details += "\n| {details:<39} |".format(details=details)

    nis = nis_rate * income
    total_tax = nis + tax
    total_tax_percent = total_tax / income
    december_tax = total_tax / year / Decimal(2)
    monthly_tax = december_tax * Decimal('2') + december_tax / Decimal('11')
    monthly_pay = income / year - monthly_tax
    december_pay = income / year - december_tax

    nis_details = "{nis_rate:.1%} * {income:.2f}".format(**locals())

    output = """
    +-----------------------------------------+
    | Months in Norway             {months:>10.0f} |
    | Income                       {income:>10.2f} |
    +-----------------------------------------+
    | Deductions:                             |
    |                                         |
    | Minimal deduction            {minimal_deduction:>10.2f} |
    | Standard deduction for                  |
    |   foreign workers            {foreign_worker_deduction:>10.2f} |
    |                                         |
    | Income after deductions      {income_after_deductions:>10.2f} |
    +-----------------------------------------+
    | Taxes:                                  |
    |                                         |
    | NIS                          {nis:>10.2f} |
    | {nis_details:>39} |
    | Tax                          {tax:>10.2f} |
    {tax_details}
    +-----------------------------------------+
    | Total Tax                    {total_tax:>10.2f} |
    | Total Tax %                  {total_tax_percent:>10.1%} |
    |                                         |
    | Monthly take-home pay        {monthly_pay:>10.2f} |
    | December take-home pay        {december_pay:>9.2f} |
    +-----------------------------------------+\n"""
    return output.format(**locals())

if __name__ == '__main__':
    sys.stdout.write(tax_norge(sys.argv[-1]))
