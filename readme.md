expenseallocation is a small library to calculate a department and/or manager's monthly expense allocation based on the number and types of employees reporting to the manager or contained withtin the department. Default types and allocations can be adjusted in the Employee class.

Manager = 300
Developer = 1000
QA Tester = 500

Example usage:

```python
from expenseallocation import Department, Employee, Report


department = Department('Engineering', 'Manager A')

manager_b = Employee('Manager', 'Manager B Name')
developer = Employee('Developer', 'Developer Name')
qa_tester = Employee('QA Tester', 'QA Tester Name')

department.add_employee(manager_b)
department.add_employee(developer)
department.add_employee(qa_tester)

department.add_report(Report(department.department_head, manager_b))
department.add_report(Report(manager_b, developer))
department.add_report(Report(manager_b, qa_tester))

print(department.allocation_for_manager(manager_b))
# prints 1800

print(department.allocation())
# prints 2100
```