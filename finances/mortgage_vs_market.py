"""
Find what is the difference between paying your mortgage early or investing in the market instead

My loans are for 20 years.
    144 000 at 1.45% (monthly 691,56 EUR)
    16 000 at 0% (monthly 66,67 EUR)
equivalent to one loan with
    160000 at 1.3187% (monthly 758.23 EUR)
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize


def sample_function(func, x_bounds):
    x1, x2 = x_bounds
    x = np.linspace(x1, x2, 10000)
    y = func(x)

    fig, ax = plt.subplots(figsize=(10, 7.5))
    ax.plot(x, y)
    ax.xaxis.grid(True, which='minor', color='#000000', linestyle=':')
    ax.yaxis.grid(True, which='minor', color='#000000', linestyle=':')
    ax.xaxis.grid(True, which='major', color='#000000', linestyle='--')
    ax.yaxis.grid(True, which='major', color='#000000', linestyle='--')

    return fig


def get_periodic_interest(interest):
    """
    From the yearly interest rate, compute the monthly interest rate

    :param float interest: yearly interest rate in percentage
    :return: monthly interest rate as a decimal (e.g. 0.03 is 3 percent)
    :rtype: float
    """

    return (1 + 0.01 * interest) ** (1/12) - 1


def get_interest(montly_interest):
    """
    From the monthly interest, get the yearly interest rate in percentage

    :param float montly_interest: in decimal (0.03 means 3%)
    :return: yearly interest rate in percentage
    """

    return ((1+montly_interest)**12 - 1) * 100


def get_monthly_payment(total, duration, interest):
    """

    :param float total: in euros
    :param int duration: number of months
    :param float interest: in percentage, yearly interest
    :return:
    """

    # directly decimal, not in percentage
    montly_interest = get_periodic_interest(interest)

    # source: https://www.inc-conso.fr/content/comment-sont-calculees-les-mensualites-de-votre-emprunt
    payment = total * montly_interest * (1 + montly_interest)**duration / \
              ((1 + montly_interest)**duration - 1)

    return payment


def get_average_interest(total, duration, payment):
    """
    Get the interest rate based on the total amount and the monthly payment.
    This is to average multiple mortgage for instance and get the average interest rate on all of them

    :param float total: in euros
    :param int duration: number of months
    :param float payment: monthly payment
    :return:
    """

    def func(montly_interest):

        return total * montly_interest * (1 + montly_interest) ** duration / \
               ((1 + montly_interest) ** duration - 1) - payment

    x0 = get_periodic_interest(15)
    result = optimize.root_scalar(func, bracket=(1e-4, x0))

    num_month = result.root
    num_year = get_interest(num_month)
    print(f"Numerical solution: Average month interest rate = {num_month * 100:.4f}% ; "
          f"average year interest rate = {num_year:.4f}%")

    return num_year


def get_interest_on_regular_investment(start, monthly_contribution, interest, duration):
    """

    :param float start: initial sum
    :param float monthly_contribution:
    :param float interest: interest rate in percentage per year
    :param int duration: Duration, in years, of this investment
    :return:
    """

    total = start
    for i in range(duration):
        total += (monthly_contribution * 12)
        total *= 1 + interest/100

    return total

mortgage_total = 144000  # euros
mortgage_interest = 1.45  # percent per year

early_repay = 10
normal_repay = 20

# market_interest = 7  # percent per year

# Average for both loans
total = 160000
duration = 240
payment = 758.230


average_interest_rate = get_average_interest(total, duration, payment)
print(f"Average interest rate: {average_interest_rate:.4f}%")

monthly_normal = get_monthly_payment(total, normal_repay*12, average_interest_rate)
monthly_early = get_monthly_payment(total, early_repay*12, average_interest_rate)
print(f"Repay your loan in {normal_repay} years with: {monthly_normal:.2f}€/month")
print(f"Repay your loan in {early_repay} years with: {monthly_early:.2f}€/month")

# Sum at your disposal each month if you pay your mortgage for 20 years rather than 10 years
monthly_delta = monthly_early - monthly_normal
print(f"Difference to invest each month: {monthly_delta:.2f}€")

# Check how the market return influence this balance
market_interests = np.linspace(1, 10, 500)
normal_benefits = []
early_benefits = []
for interest in market_interests:
    normal_benefits.append(get_interest_on_regular_investment(0, monthly_delta, interest, normal_repay))
    early_benefits.append(get_interest_on_regular_investment(0, monthly_early, interest, normal_repay - early_repay))

fig, ax = plt.subplots(figsize=(10, 7.5))
ax.plot(market_interests, normal_benefits, label=f"Invest leftovers for {normal_repay} years")
ax.plot(market_interests, early_benefits, label=f"Pay loan in {early_repay} years, then invest for {normal_repay-early_repay} years")
ax.set_xlabel("Average market interest rate [%]")
ax.set_ylabel(f"Sum at your disposal after {normal_repay} years [€]")
ax.legend()
ax.xaxis.grid(True, which='minor', color='#000000', linestyle=':')
ax.yaxis.grid(True, which='minor', color='#000000', linestyle=':')
ax.xaxis.grid(True, which='major', color='#000000', linestyle='--')
ax.yaxis.grid(True, which='major', color='#000000', linestyle='--')
fig.suptitle(f"Loan for {normal_repay} years vs paid early in {early_repay} years.")

# normal_benefits = get_interest_on_regular_investment(monthly_delta, 7, 20)
# fast_loan_benefits = get_interest_on_regular_investment(monthly_early, 7, 10)
# print(f"Reimburse your loan normally, and invest the left for 20 years gets you : {normal_benefits:.2f} €")
# print(f"Reimburse your loan early, then invest for 10 years gets you: {fast_loan_benefits:.2f} €")

# Check if average interest is correct
# print(get_monthly_payment(160000, mortgage_duration*12, 1.3187))

# compare taking a loan at CASDEN for 21500€ over 7 years then repaying 279.08€ per month for 7 years
loan_benefits = get_interest_on_regular_investment(21500, 0, 7, 7) - 23472.26 + 21500
normal_benefits = get_interest_on_regular_investment(0, 279.08, 7, 7)

print(f"If you take the 21500€ loan, you get after 7 years: {loan_benefits:.2f}€")
print(f"If you invest normally 279.08€ for 7 years: {normal_benefits:.2f}€")

plt.show()
