class Period(object):
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end


class BudgetService(object):
    def query(self, start, end):
        if start > end:
            return 0

        total_amount = 0
        for budget in self.get_budgets():
            if end < budget.first_day() or start > budget.last_day():
                break

            period = Period(start, end)
            overlapping_days = self.overlapping_days(budget, end, start, period)
            total_amount += round(budget.daily_amount() * overlapping_days, 2)

        return total_amount

    @staticmethod
    def overlapping_days(budget, end, start, period):
        overlapping_end = end if end < budget.last_day() else budget.last_day()
        overlapping_start = start if start > budget.first_day() else budget.first_day()
        overlapping_days = ((overlapping_end - overlapping_start).days + 1)
        return overlapping_days

    def get_budgets(self):
        pass
