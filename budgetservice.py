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

        total_amount = 0
        for budget in budgetsList:
            budget_first_day = self.first_day(budget)
            days_of_budget = calendar.monthrange(budget_first_day.year, budget_first_day.month)[1]
            budget_last_day = budget_first_day.replace(day=days_of_budget)

            daily_amount = budget.amount / days_of_budget

            if end < budget_first_day or start > budget_last_day:
                break

            overlapping_end = end if end < budget_last_day else budget_last_day
            overlapping_start = start if start > budget_first_day else budget_first_day
            overlapping_days = ((overlapping_end - overlapping_start).days + 1)
            total_amount += round(daily_amount * overlapping_days, 2)

        return total_amount

    @staticmethod
    def first_day(budget):
        budget_first_day = datetime.strptime(budget.yearMonth, "%Y%m")
        return budget_first_day

    def get_budgets(self):
        pass
