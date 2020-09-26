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
            budget_first_day = datetime.strptime(budget.yearMonth, "%Y%m")
            days_of_budget = calendar.monthrange(budget_first_day.year, budget_first_day.month)[1]
            budget_last_day = budget_first_day.replace(day=days_of_budget)

            is_start_budget = budget.yearMonth == start.strftime("%Y%m")
            is_end_budget = budget.yearMonth == end.strftime("%Y%m")

            daily_amount = budget.amount / days_of_budget
            overlapping_end = end
            overlapping_start = start
            amount = 0

            if is_start_budget and is_end_budget:
                overlapping_end = end
                overlapping_start = start
                amount = round(daily_amount * (overlapping_end - overlapping_start).days + 1, 2)
                # amount += round(daily_amount * (overlapping_end - overlapping_start).days + 1, 2)

            elif is_start_budget:
                overlapping_end = budget_last_day
                overlapping_start = start
                amount = round(daily_amount * ((overlapping_end - overlapping_start).days + 1), 2)
                # amount += round(daily_amount * ((overlapping_end - overlapping_start).days + 1), 2)

            elif begin_month < budget.yearMonth < end_month:
                overlapping_end = budget_last_day
                overlapping_start = budget_first_day
                amount = round(daily_amount * ((overlapping_end - overlapping_start).days + 1), 2)
                # amount += round(daily_amount * ((overlapping_end - overlapping_start).days + 1), 2)

            elif is_end_budget:
                overlapping_end = end
                overlapping_start = budget_first_day
                amount = round(daily_amount * ((overlapping_end - overlapping_start).days + 1), 2)
                # amount += round(daily_amount * ((overlapping_end - overlapping_start).days + 1), 2)
            total_amount += amount
        return total_amount

    def get_budgets(self):
        pass
