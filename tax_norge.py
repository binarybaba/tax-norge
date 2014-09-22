#!/usr/bin/env python
import sys
from decimal import Decimal


minimal_deduction = Decimal(81300)
foreign_worker_deduction_max = Decimal(40000)
foreign_worker_deduction_percent = Decimal(0.1)
nis_rate = Decimal(0.078)
tax_rate = Decimal(0.28)
surtaxes = [
    (Decimal(509600), Decimal(0.09)),
    (Decimal(828300), Decimal(0.03)),
]

income = Decimal(sys.argv[-1])

foreign_worker_deduction = min(foreign_worker_deduction_max, foreign_worker_deduction_percent * income)
if '-n' in sys.argv:
    foreign_worker_deduction = Decimal(0.0)
income_after_deductions = income - minimal_deduction - foreign_worker_deduction

tax = tax_rate * income_after_deductions
tax_details = "{tax_rate:.1%} * "\
              "{income_after_deductions:.2f}".format(**locals())
tax_details = "| {tax_details:<39} |".format(tax_details=tax_details)
for surtax_amount, surtax_rate in surtaxes:
    if surtax_amount < income_after_deductions:
        tax += (income_after_deductions - surtax_amount) * surtax_rate
        details = "+ ({income_after_deductions:.2f} - {surtax_amount:.2f}) * {surtax_rate:.1%}".format(**locals())
        tax_details += "\n| {details:<39} |".format(details=details)

nis = nis_rate * income
total_tax = nis + tax
total_tax_percent = total_tax / income
monthly_pay = (income - total_tax) / 12

nis_details = "{nis_rate:.1%} * {income:.2f}".format(**locals())

output = """
+-----------------------------------------+
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
+-----------------------------------------+\n"""

sys.stdout.write(output.format(**locals()))
