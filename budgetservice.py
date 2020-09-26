class Period(object):
    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end

    def overlapping_days(self, another):
        if self.start > self.end:
            return 0
        if self.end < another.start or self.start > another.end:
            return 0

        overlapping_end = self.end if self.end < another.end else another.end
        overlapping_start = self.start if self.start > another.start else another.start
        return (overlapping_end - overlapping_start).days + 1


class BudgetService(object):
    def query(self, start, end):
        period = Period(start, end)
        total_amount = 0
        for budget in self.get_budgets():
            another = self.create_period(budget)
            total_amount += round(budget.daily_amount() * period.overlapping_days(another), 2)

        return total_amount

    @staticmethod
    def create_period(budget):
        return Period(budget.first_day(), budget.last_day())

    def get_budgets(self):
        pass
