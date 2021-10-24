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

## Project Discussion
1. Design process

I received a lot of feedback on my initial entity relationship diagram, and did my best to address these suggestions by doing a thorough revision, which is included here. I feel like I learned a lot from doing so, but have a long way to go. I don't feel like I will have a good grasp on how to design databases well until I have experience interacting with them in practical use. I have been constantly rethinking my design as I implement it, and so while it was helpful to have a diagram as a starting point, I did not find it practical to keep updating. I did keep track of some changes by updating the `ddl.sql` file here in place of a diagram but it no longer accurately reflects every detail of `models.py`.   

To fully work out this design, I feel that I need realistic data to work with. I have spent a lot of time trying to adapt the original `seed.py` we were given to populate my database with, but would need to continue working on this to test all my tables. This isn't something we covered in any detail in the course so it's been slow going and this has been one of the reasons I've not implemented many endpoints compared to what I had planned.

2. ORM vs raw SQL

My feeling is that raw SQL inside of Python should be avoided unless it is a simple project that will only be interacting with the database in limited ways with a few basic queries. Putting static SQL in Python just doesn't seem practical for doing anything much more complex then that, for much the same reason that it is difficult to keep an ERD updated as the code evolves. I can understand from working on this project why ORMs like SQL Alchemy are widely used in production. They simplify what would otherwise be very complicated to manage. 

3. Future improvements

In order to make this project into something that would be practical to use, a lot more work would need to be done. Many more endpoints need to be implemented. A frontend is necessary for users to interact with. In the near term, I wonder if it may be more practical to create a CLI and use this database that way instead of actually implementing it as a web API. I would also need to learn how to securely authenticate and control who has access to the sensitive data this database would contain if it were to be a web-based application.