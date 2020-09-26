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

            is_start_budget = budget.yearMonth == start.strftime("%Y%m")
            is_end_budget = budget.yearMonth == end.strftime("%Y%m")

            if is_start_budget and is_end_budget:
                return round(budget.amount / days_of_budget * (end.day - start.day + 1), 2)

            if is_start_budget:
                amount += round(budget.amount / days_of_budget * (days_of_budget - start.day + 1), 2)

            if begin_month < budget.yearMonth < end_month:
                amount += budget.amount

            if is_end_budget:
                amount += round(budget.amount / days_of_budget * end.day, 2)

        return amount

    def get_budgets(self):
        pass
