class BudgetService(object):
    def query(self, start, end):
        if start > end:
            return 0

        total_amount = 0
        for budget in self.get_budgets():
            if end < budget.first_day() or start > budget.last_day():
                break

            overlapping_end = end if end < budget.last_day() else budget.last_day()
            overlapping_start = start if start > budget.first_day() else budget.first_day()
            overlapping_days = ((overlapping_end - overlapping_start).days + 1)
            total_amount += round(budget.daily_amount() * overlapping_days, 2)

        return total_amount

    def get_budgets(self):
        pass
