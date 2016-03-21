#!/usr/bin/env python
#
# Copyright 2016 Brandon Regard
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import unittest

from expenseallocation import *
from exception import *


class EmployeeTests(unittest.TestCase):
    """Unit tests for the employee class."""

    def test_employee_kind(self):
        """Assert exception creating invalid kinds of employees."""
        self.assertRaises(EAEmployeeError, Employee, 'President', 'President')

    def test_kind_allocation(self):
        """Assert that the allocations for kinds of employees are correct."""
        manager = Employee('Manager', 'Manager')
        developer = Employee('Developer', 'Developer')
        qa_tester = Employee('QA Tester', 'QA Tester')

        self.assertEqual(manager.allocation, 300)
        self.assertEqual(developer.allocation, 1000)
        self.assertEqual(qa_tester.allocation, 500)


class ReportTests(unittest.TestCase):
    """Unit tests for the report class."""

    def test_report_to_self(self):
        """Assert exception when employee reports to him/her self."""
        employee = Employee('Manager', 'Manager')

        self.assertRaises(EAReportError, Report, employee, employee)

    def test_report_to_non_manager(self):
        """Assert exception when employee report to a non manager."""
        developer = Employee('Developer', 'Developer')
        qa_tester = Employee('QA Tester', 'QA Tester')

        self.assertRaises(EAReportError, Report, developer, qa_tester)


class DepartmentTests(unittest.TestCase):
    """Unit tests for the Department class."""

    def setUp(self):
        """Setup for our Department test cases."""
        self.d = Department('Engineering', 'Tom')

        mike = Employee('Manager', 'Mike')
        kelby = Employee('Developer', 'Kelby')
        tyler = Employee('Developer', 'Tyler')
        self.brandon = Employee('Manager', 'Brandon')
        andrew = Employee('Developer', 'Andrew')
        steve = Employee('Developer', 'Steve')
        joe = Employee('QA Tester', 'Joe')

        self.d.add_employee(mike)
        self.d.add_employee(kelby)
        self.d.add_employee(tyler)
        self.d.add_employee(self.brandon)
        self.d.add_employee(andrew)
        self.d.add_employee(steve)
        self.d.add_employee(joe)

        self.d.add_report(Report(self.d.department_head, mike))
        self.d.add_report(Report(self.d.department_head, kelby))
        self.d.add_report(Report(mike, tyler))
        self.d.add_report(Report(self.d.department_head, self.brandon))
        self.d.add_report(Report(self.brandon, andrew))
        self.d.add_report(Report(self.brandon, steve))
        self.d.add_report(Report(self.brandon, joe))

        self.d2 = Department('CL', 'Manager A')

        manager_b = Employee('Manager', 'Manager B')
        developer = Employee('Developer', 'Developer')
        qa_tester = Employee('QA Tester', 'QA Tester')

        self.d2.add_employee(manager_b)
        self.d2.add_employee(developer)
        self.d2.add_employee(qa_tester)

        self.d2.add_report(Report(self.d2.department_head, manager_b))
        self.d2.add_report(Report(manager_b, developer))
        self.d2.add_report(Report(manager_b, qa_tester))

        self.d3 = Department('CL', 'Manager A')

        manager_b = Employee('Manager', 'Manager B')
        developer = Employee('Developer', 'Developer')
        qa_tester = Employee('QA Tester', 'QA Tester')

        self.d3.add_employee(manager_b)
        self.d3.add_employee(developer)
        self.d3.add_employee(qa_tester)

        self.d3.add_report(Report(manager_b, developer))
        self.d3.add_report(Report(manager_b, qa_tester))

    def test_single_manager(self):
        """Assert exception when employee reports to more than one manager."""
        manager = Employee('Manager', 'Manager')
        developer = Employee('Developer', 'Developer')

        self.d.add_employee(manager)
        self.d.add_employee(developer)

        self.d.add_report(Report(self.d.department_head, developer))
        bad_report = Report(manager, developer)

        self.assertRaises(EADepartmentError, self.d.add_report, bad_report)

    def test_manager_allocation(self):
        """Assert manager allocations at different levels."""
        self.assertEqual(self.d.allocation_for_manager(self.brandon, 0), 300)
        self.assertEqual(self.d.allocation_for_manager(self.brandon, 1), 2800)
        self.assertEqual(self.d.allocation_for_manager(self.brandon, -1), 300)
        self.assertEqual(self.d.allocation_for_manager(self.brandon, 100), 2800)
        self.assertEqual(self.d.allocation_for_manager(self.brandon), 2800)

        self.assertEqual(
            self.d2.allocation_for_manager(self.d2.department_head), 2100)

        self.assertEqual(self.d2.allocation(0), 300)
        self.assertEqual(self.d2.allocation(1), 600)
        self.assertEqual(self.d2.allocation(), 2100)

    def test_department_allocation_with_no_head(self):
        """Assert exception when evaluating headless department allocation."""
        self.assertRaises(EADepartmentError, self.d3.allocation)


if __name__ == '__main__':
    unittest.main()
