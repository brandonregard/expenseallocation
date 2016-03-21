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

"""expenseallocation is a small library to calculate a department and/or
manager's monthly expense allocation based on the number and types of
employees reporting to the manager or contained withtin the department.
"""

from exception import *


class Employee(object):
    """The class defining an employee."""

    KIND_ALLOCATION = {
        'Manager': 300,
        'Developer': 1000,
        'QA Tester': 500
    }

    def __init__(self, kind, name):
        """Construct an employee.

        Arguments:
        kind -- the kind of employee (must be a valid key to KIND_ALLOCATION)
        """
        if kind in self.KIND_ALLOCATION:
            self._kind = kind
        else:
            raise EAEmployeeError('Creating an invalid kind of employee.')
        self._name = name
        if kind == 'Manager':
            self._is_manager = True
        else:
            self._is_manager = False
        self._allocation = self.KIND_ALLOCATION[kind]

    @property
    def kind(self):
        return self._kind

    @property
    def name(self):
        return self._name
    
    @property
    def is_manager(self):
        return self._is_manager

    @property
    def allocation(self):
        return self._allocation

    def __eq__(self, other):
        return self._name == other.name

    def __hash__(self):
        return hash(self._name)

    def __str__(self):
        return '{} {}'.format(self._kind, self._name)


class Report(object):
    """The class defining a report. A report is the relationship between an
    employee and their manager.
    """

    def __init__(self, manager, employee):
        """Construct a report.

        Arguments:
        manager - an employee of kind manager that employee reports to
        employee - an employee
        """
        if manager == employee:
            raise EAReportError('Employee cannot report to him/her self.')
        if not manager.is_manager:
            raise EAReportError('Employees can only report to Managers.')
        self._employee = employee
        self._manager = manager

    @property
    def manager(self):
        return self._manager

    @property
    def employee(self):
        return self._employee

    def __str__(self):
        return '{}->{}'.format(self._manager, self._employee)
    

class Department(object):
    """The class defining a department. A department is really a simple
    n-ary tree of employees(nodes) and reports(edges). An adjacency list
    (in this case a dictionary or hash table) is used to store which employees
    report to which managers.
    """

    def __init__(self, name, department_head):
        """Construct a department.

        Arguments:
        name - the name of the department
        department_head - the name of an employee that acts as the head of
        the department
        """
        self._employees = []
        self._reports = {}
        self._name = name
        self._department_head = Employee('Manager', department_head)
        self.add_employee(self._department_head)

    @property
    def name(self):
        return self._name

    @property
    def department_head(self):
        return self._department_head
    
    @property
    def employees(self):
        return self._employees

    @property
    def reports(self):
        return self._reports

    def add_employee(self, employee):
        """Add an employee to the department."""
        if employee in self._employees:
            raise EADepartmentError('Employee already exists.')
        self._employees.append(employee)
        self._reports[employee] = []

    def add_report(self, report):
        """Add a report to the department."""
        if not(report.manager in self._employees
            and report.employee in self._employees):
            raise EADepartmentError('Employee missing from department.')
        for reports in self._reports.values():
            if report.employee in reports:
                raise EADepartmentError('Employee already has a direct report.')
        self._reports[report.manager].append(report.employee)

    def allocation_for_manager(self, manager, level=None):
        """Calculates the total allocation for a manager and all reports to
        the level specified.

        Arguments:
        manager - manager to calculate allocation for
        level - how deep in the report hierarchy to calculate to (level >= 0,
        level == None will calculate all the way down)
        """
        result = 0
        if level is None or level > 0:
            if level is not None:
                level -= 1
            for employee in self._reports[manager]:
                result += self.allocation_for_manager(employee, level)
        result += manager.allocation
        return result

    def allocation(self, level=None):
        """Calculates the total allocation for this department to the level
        specified.

        Arguments:
        level - how deep in the report hierarchy to calculate to (level >= 0,
        level == None will calculate all the way down)
        """
        if len(self._reports[self._department_head]) == 0:
            raise EADepartmentError('No employees report to the department head.')
        return self.allocation_for_manager(self._department_head, level)

    def __hash__(self):
        return hash(self._name)

    def __str__(self):
        result = ''
        for key in self._reports:
            for report in self._reports[key]:
                result = '{}{}->{}\n'.format(result, str(key), str(report))
        return result[:-1]

