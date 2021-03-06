# Backstage Payroll

This project (a work in progress) represents a simple payroll database/API for managing contract-based work, built on Postgres and Flask. It is designed with theater, movie and television stagehands in mind but should be flexible enough to use for other fields where work is paid at different rates to multiple employees by contract or "gig". It will keep records of employees, contract assignments, hours worked, paychecks and more. It is NOT secure or production ready and should not be used to store real data.

## API endpoints reference
### **User** 

|Method|Route|Description|
|------|-----|-----------|
|GET|/user|Show all user accounts. Password hashes are not displayed.|
|POST, PUT|/user|Add a new user account. Request body must include `username` and `password`, can optionally include `email` address.|
|DELETE|/user/:id|Delete user account.|
|POST, PUT|/user/:id|Modify user account. Request body may include new `email`, `username` and/or `password`.| 

### **Employee**

|Method|Route|Description|
|------|-----|-----------|
|GET|/employee|Show all employee IDs, including any assigned workroles. PII is not displayed.|
|POST, PUT|/employee|Add a new employee to the database. Request body may include `ssn`, `first_name`, `last_name` and/or `user_id`.|
|POST, PUT|/employee/:id|Modify employee data. Request body may include new `ssn`, `first_name`, `last_name` and/or `user_id`. 

### **Client**
|Method|Route|Description|
|------|-----|-----------|
|GET|/client|Show all client company names.|
|POST, PUT|/client|Add a new client to the database. Request body must consist of `company_name`.|
|POST, PUT|/client/:id|Modify client name. Request body must consist of `company_name`. 

### **Contract**
|Method|Route|Description|
|------|-----|-----------|
|GET|/contract|Show all contracts.|
|POST, PUT|/contract|Add a new contract to the database. Request body must include `client_id`. It may include `start_date`, `end_date`, and/or `contract_description`. |
|POST, PUT|/contract/:id|Modify contract. Request body may include `start_date`, `end_date`, and/or `contract_description`. 

### **Workrole**
|Method|Route|Description|
|------|-----|-----------|
|GET|/workrole|Show all workroles, including IDs of any assigned employees.|
|POST, PUT|/workrole|Add a new workrole to the database. Request body must include `contract_id`. It may include `workrole_description`, `hour_budget`, `hourly_pay`, `hourly_deduction`. |
|POST, PUT|/workrole/:id|Modify contract. Request body may include `workrole_description`, `hour_budget`, `hourly_pay`, `hourly_deduction`. 

### **Employee-Workrole**
|Method|Route|Description|
|------|-----|-----------|
|POST, PUT|/employee-workrole|Assign employees to workroles. Request must include a list of at least one `employee_ids` and a list of at least one `workrole_ids`. All listed employees will be added to all workroles (E.g. If `employee_ids` is `[1, 2]"` and `workrole_ids` `[3, 4]` then both employees will be added to both workroles.) Returns a dictionary with updated records of relevant employees and workroles.|
|DELETE|/employee-workrole/| Delete employees from workroles. Request must include a list of at least one `employee_ids` and a list of at least one `workrole_ids`. All listed employees will be added to all workroles (E.g. If `employee_ids` is `[1, 2]"` and `workrole_ids` `[3, 4]` then both employees will be deleted from both workroles if present. Returns a dictionary with updated records of relevant employees and workroles.)

### **To Be Implemented**: 
/timeworked, /paycheck
