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

from expenseallocation import Department, _Employee, _Report
from exception import *


class EmployeeTests(unittest.TestCase):
    """Unit tests for the employee class."""

    def test_employee_kind(self):
        """Assert exception creating invalid kinds of employees."""
        self.assertRaises(EAEmployeeError, _Employee, 'President', 'President')

    def test_kind_allocation(self):
        """Assert that the allocations for kinds of employees are correct."""
        manager = _Employee('Manager', 'Manager')
        developer = _Employee('Developer', 'Developer')
        qa_tester = _Employee('QA Tester', 'QA Tester')

        self.assertEqual(manager.allocation, 300)
        self.assertEqual(developer.allocation, 1000)
        self.assertEqual(qa_tester.allocation, 500)


class ReportTests(unittest.TestCase):
    """Unit tests for the report class."""

    def test_report_to_self(self):
        """Assert exception when employee reports to him/her self."""
        employee = _Employee('Manager', 'Manager')

        self.assertRaises(EAReportError, _Report, employee, employee)

    def test_report_to_non_manager(self):
        """Assert exception when employee report to a non manager."""
        developer = _Employee('Developer', 'Developer')
        qa_tester = _Employee('QA Tester', 'QA Tester')

        self.assertRaises(EAReportError, _Report, developer, qa_tester)


class DepartmentTests(unittest.TestCase):
    """Unit tests for the Department class."""

    def setUp(self):
        """Setup for our Department test cases."""
        self.d = Department('D1', 'Tom')

        self.d.add_employee('Manager', 'Mike')
        self.d.add_employee('Developer', 'Kelby')
        self.d.add_employee('Developer', 'Tyler')
        self.d.add_employee('Manager', 'Brandon')
        self.d.add_employee('Developer', 'Andrew')
        self.d.add_employee('Developer', 'Steve')
        self.d.add_employee('QA Tester', 'Joe')

        self.d.add_report('Tom', 'Mike')
        self.d.add_report('Tom', 'Kelby')
        self.d.add_report('Mike', 'Tyler')
        self.d.add_report('Tom', 'Brandon')
        self.d.add_report('Brandon', 'Andrew')
        self.d.add_report('Brandon', 'Steve')
        self.d.add_report('Brandon', 'Joe')

        # Test data from requirements document
        self.d2 = Department('D2', 'Manager A')

        self.d2.add_employee('Manager', 'Manager B')
        self.d2.add_employee('Developer', 'Developer')
        self.d2.add_employee('QA Tester', 'QA Tester')

        self.d2.add_report('Manager A', 'Manager B')
        self.d2.add_report('Manager B', 'Developer')
        self.d2.add_report('Manager B', 'QA Tester')

        # Department with no direct reports to department head
        self.d3 = Department('D3', 'Manager A')

        self.d3.add_employee('Manager', 'Manager B')
        self.d3.add_employee('Developer', 'Developer')
        self.d3.add_employee('QA Tester', 'QA Tester')

        self.d3.add_report('Manager B', 'Developer')
        self.d3.add_report('Manager B', 'QA Tester')

    def test_single_manager(self):
        """Assert exception when employee reports to more than one manager."""
        self.d.add_employee('Manager', 'Manager')
        self.d.add_employee('Developer', 'Developer')

        self.d.add_report('Tom', 'Developer')

        self.assertRaises(
            EADepartmentError, self.d.add_report, 'Manager', 'Developer')

    def test_manager_allocation(self):
        """Assert manager allocations at different levels."""
        self.assertEqual(self.d.allocation_for_manager('Brandon', 0), 300)
        self.assertEqual(self.d.allocation_for_manager('Brandon', 1), 2800)
        self.assertEqual(self.d.allocation_for_manager('Brandon', -1), 300)
        self.assertEqual(self.d.allocation_for_manager('Brandon', 100), 2800)
        self.assertEqual(self.d.allocation_for_manager('Brandon'), 2800)

        self.assertEqual(self.d2.allocation_for_manager('Manager A'), 2100)

        self.assertEqual(self.d2.allocation(0), 300)
        self.assertEqual(self.d2.allocation(1), 600)
        self.assertEqual(self.d2.allocation(), 2100)

    def test_department_allocation_with_no_head(self):
        """Assert exception when evaluating headless department allocation."""
        self.assertRaises(EADepartmentError, self.d3.allocation)

    def test_get_unknown_employee(self):
        """Assert unknown employee is None."""
        self.assertEqual(self.d.get_employee('XYZ'), None)

    def test_allocation_for_unknown_manager(self):
        """Assert allocation for unknown manager is None."""
        self.assertEqual(self.d.allocation_for_manager('XYZ'), None)

    def test_report_for_unknown_employee(self):
        """Assert exception on report for unknown employee."""
        self.assertRaises(EADepartmentError, self.d.add_report, 'Tom', 'XYZ')
        self.assertRaises(EADepartmentError, self.d.add_report, 'ABC', 'XYZ')


if __name__ == '__main__':
    unittest.main()
