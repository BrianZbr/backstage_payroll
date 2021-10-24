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
|GET|/employee|Show all employee IDs. PII is not displayed.|
|POST, PUT|/employee|Add a new employee to the database. Request body may include `ssn`, `first_name`, `last_name` and/or `user_id`.|
|POST, PUT|/employee/:id|Modify employee data. Request body may include new `ssn`, `first_name`, `last_name` and/or `user_id`. 

### **To Be Implemented**: 
/client, /contract, /workrole, /employee-workrole, /timeworked, /paycheck
