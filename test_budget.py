import calendar
import unittest
from datetime import datetime

from unittest.mock import patch

from budgetservice import BudgetService


class Budget(object):

    def __init__(self, yearMonth, amount):
        self.yearMonth = yearMonth
        self.amount = amount

    def first_day(self):
        budget_first_day = datetime.strptime(self.yearMonth, "%Y%m")
        return budget_first_day

    def days(self):
        return calendar.monthrange(self.first_day().year, self.first_day().month)[1]

    def last_day(self):
        return self.first_day().replace(day=(self.days()))

    def daily_amount(self):
        return self.amount / self.days()


class BudgetServiceTests(unittest.TestCase):

    def setUp(self):
        self.service = BudgetService()
        budget_repo_patcher = patch('budgetservice.BudgetService.get_budgets')
        self.fake_get_budgets = budget_repo_patcher.start()

    def tearDown(self) -> None:
        patch.stopall()

    def test_invalid_start_end(self):
        self.assertEqual(self.service.query(datetime(2020, 9, 30), datetime(2020, 9, 26)), 0)

    def test_query_whole_month(self):
        self.fake_get_budgets.return_value = [
            Budget('202009', 30),
            Budget('202010', 50),
        ]
        self.assertEqual(self.service.query(datetime(2020, 9, 1), datetime(2020, 9, 30), ), 30)

    def test_query_no_budget(self):
        self.fake_get_budgets.return_value = [
            Budget('202009', 30),
            Budget('202010', 50),
        ]
        self.assertEqual(self.service.query(datetime(2020, 11, 1), datetime(2020, 11, 30), ), 0)

    def test_query_one_day(self):
        self.fake_get_budgets.return_value = [
            Budget('202009', 30),
        ]
        self.assertEqual(self.service.query(datetime(2020, 9, 1), datetime(2020, 9, 1), ), 1)

    def test_over_one_month(self):
        self.fake_get_budgets.return_value = [
            Budget('202009', 30),
            Budget('202010', 310),
        ]
        self.assertEqual(self.service.query(datetime(2020, 9, 30), datetime(2020, 10, 2)), 21)

    def test_over_three_month(self):
        self.fake_get_budgets.return_value = [
            Budget('202009', 30),
            Budget('202010', 310),
            Budget('202011', 3000),
        ]
        self.assertEqual(self.service.query(datetime(2020, 9, 30), datetime(2020, 11, 2)), 511)

    def test_over_year(self):
        self.fake_get_budgets.return_value = [
            Budget('202012', 31),
            Budget('202101', 310),
        ]
        self.assertEqual(self.service.query(datetime(2020, 12, 31), datetime(2021, 1, 2)), 21)


if __name__ == '__main__':
    unittest.main()
