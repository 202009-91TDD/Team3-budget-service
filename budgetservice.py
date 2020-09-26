class Period(object):
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end

    def overlapping_days(self, budget):
        another = Period(budget.first_day(), budget.last_day())
        first_day = budget.first_day()
        last_day = budget.last_day()
        if self.start > self.end:
            return 0
        if self.end < first_day or self.start > last_day:
            return 0

        overlapping_end = self.end if self.end < last_day else last_day
        overlapping_start = self.start if self.start > first_day else first_day
        return (overlapping_end - overlapping_start).days + 1


class BudgetService(object):
    def query(self, start, end):
        period = Period(start, end)
        total_amount = 0
        for budget in self.get_budgets():
            total_amount += round(budget.daily_amount() * period.overlapping_days(budget), 2)

        return total_amount

    def get_budgets(self):
        pass
