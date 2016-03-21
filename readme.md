**expenseallocation** is a small library to calculate a department and/or manager's monthly expense allocation based on the number and types of employees reporting to the manager or contained withtin the department. Default types and allocations can be adjusted in the Employee class.

Default Types/Allocations:
* Manager = 300
* Developer = 1000
* QA Tester = 500

Assumptions:
* Departments must have a department head (manager).
* Employee names are unique within a department.

Example usage:

```python
from expenseallocation import Department


department = Department('Engineering', 'Manager A Name')

department.add_employee('Manager', 'Manager B Name')
department.add_employee('Developer', 'Developer Name')
department.add_employee('QA Tester', 'QA Tester Name')

department.add_report('Manager A Name', 'Manager B Name')
department.add_report('Manager B Name', 'Developer Name')
department.add_report('Manager B Name', 'QA Tester Name')

print(department.allocation_for_manager('Manager B Name'))
# prints 1800

print(department.allocation())
# prints 2100
```

Running Unit Tests: `python test.py -v`