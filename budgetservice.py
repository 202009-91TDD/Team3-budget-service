from datetime import datetime
import calendar
from time import strftime


class BudgetService(object):
    def query(self, start, end):
        if start > end:
            return 0

        begin_month = datetime.strftime(start, "%Y%m")
        end_month = datetime.strftime(end, "%Y%m")

        budgetsList = self.get_budgets()

        amount = 0
        for budget in budgetsList:
            budget_first_day = datetime.strptime(budget.yearMonth, "%Y%m")
            days_of_budget = calendar.monthrange(budget_first_day.year, budget_first_day.month)[1]
            budget_last_day = budget_first_day.replace(day=days_of_budget)

            is_start_budget = budget.yearMonth == start.strftime("%Y%m")
            is_end_budget = budget.yearMonth == end.strftime("%Y%m")

            daily_amount = budget.amount / days_of_budget
            if is_start_budget and is_end_budget:
                return round(daily_amount * (end.day - start.day + 1), 2)

            if is_start_budget:
                amount += round(daily_amount * (days_of_budget - start.day + 1), 2)

            if begin_month < budget.yearMonth < end_month:
                amount += round(daily_amount * ((budget_last_day - budget_first_day).days + 1), 2)
                # amount += budget.amount

            if is_end_budget:
                amount += round(daily_amount * end.day, 2)

        return amount

    def get_budgets(self):
        pass
