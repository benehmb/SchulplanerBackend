# Schulplaner REST API

## Homework

```JSON:
{
    "group_id": int,     (over path)
    "id": int,          (Oprional for PUT, over path)
    "date": int,
    "subject": String,
    "homework": String
}
```

### GET /groups/{group_id}/homework

 Return all homework for {group_id}
 
  - 200 -> Ok
  - 204 -> No homework to return
  - 400 -> Bad request (Group_id is String or something else)
  - 404 -> Group not found
  
### POST /groups/{group_id}/homework

  Create and return a new homework according to the request body
  
  - 201 -> Created
  - 401 -> Unauthorized: missing or wrong password
  - 400 -> Bad request (Group_id is String or something else)
  - 404 -> Group not found
 
### DELETE /groups/{group_id}/homework/{homework_id}

  Delete {homework_id} under {group_id}
  
  - 204 -> No content anymore, homework successfully deleted
  - 400 -> Bad request (Group_id is String or Something else)
  - 401 -> Unauthorized: missing or wrong password
  - 404 -> Group or homework not found
  - 410 -> Gone, homework is already deleted
  
### PUT /groups/{group_id}/homework/{homework_id}

  Update {homework_id} under {group_id} according to request body
  
  - 200 -> Ok
  - 400 -> Bad request (Group_id is String or Something else)
  - 401 -> Unauthorized: missing or wrong password
  - 404 -> Group or homework not found
  - 410 -> Gone, homework was deleted
  
  
## Exams

```JSON:
{
    "group_id": int,     (over path)
    "id": int,          (Oprional for PUT, over path)
    "date": int,
    "subject": String,
    "exam": String
}
```

### GET /groups/{group_id}/exams

  Return all exams for {group_id}
  
  - 200 -> Ok
  - 204 -> No exam to return
  - 400 -> Bad request (Group_id is String or Something else)
  - 404 -> Group not found

### POST /groups/{group_id}/exams

  Create and return a new exam according to the request body
  
  - 201 -> Created
  - 400 -> Bad request (Group_id is String or Something else)
  - 401 -> Unauthorized: missing or wrong password
  - 404 -> Group not found

### DELETE /groups/{group_id}/exams/{exam_id}

  Delete {exam_id} under {group_id}
  
  - 204 -> No content anymore, exam successfully deleted
  - 400 -> Bad request (Group_id is String or Something else)
  - 401 -> Unauthorized: missing or wrong password
  - 404 -> Group or exam not found
  - 410 -> Gone, exam is already deleted

### PUT /groups/{group_id}/exams/{exam_id}

  Update {exam_id} under {group_id} according to request body
  
  - 200 -> Ok
  - 400 -> Bad request (Group_id is String or Something else)
  - 401 -> Unauthorized: missing or wrong password
  - 404 -> Group or exam not found
  - 410 -> Gone, exam was deleted
  

## Groups

```JSON:
{
    "id": int       (over path)
    "name": String
}
```

### GET /groups/{group_id}

  Return info for {group_id}
  
  - 200 -> Ok
  - 400 -> Bad request (Group_id is String or Something else)
  - 404 -> Group not found
  Additional: If Password is in get, returns 200 or 401 to check if Password is correct
  - 401 -> Unauthorized: wrong password

### POST /groups

  Create and return group according to the request body
  
  - 201 -> Created
  - 400 -> Bad request (Group_id is String or Something else)

### DELETE /groups/{group_id}

  Delete {group_id}
  
  - 204 -> No content anymore, group successfully deleted
  - 400 -> Bad request (Group_id is String or Something else)
  - 401 -> Unauthorized: missing or wrong password
  - 404 -> Group not found
  - 410 -> Gone, group is already deleted

### PUT /groups/{group_id}

  Update {group_id} according to request body (without body, returns new Password, with body, sets new name)
  
  - 200 -> Ok
  - 400 -> Bad request (Group_id is String or Something else)
  - 401 -> Unauthorized: missing or wrong password
  - 404 -> Group not found
  - 410 -> Gone, group was deleted
  
## Database methods

### General

  - ```__init__()```
  - ```connect():mysql.connection```
  - ```init()```

### Groups

  - ```get_group_name(group_id):{boolean(worked), integer(statuscode), string(name; only returned if worked=true)}```
  - ```create_group(name):{boolean(worked), integer(statuscode), {"group_id": group_id, "password": password}}```
  - ```change_group_pass(group_id, old_password):{boolean(worled), integer(statuscode), string(Password; only returned if worked=true)}```
  - ```delete_group(group_id, password):{boolean(worked), integer(statuscode)}```
  - ```change_group_name(group_id, name, password):{boolean(worked), integer(statuscode)}```
  - ```check_group_pass(group_id, password):{boolean(worked), integer(statuscode)}```

### Homework

  - ```get_homework(group_id):{boolean(worked), integer(statuscode), String-array(homework; only returned if worked=true)}```
  - ```add_homework(group_id, date, subject, homework, password):{boolean(worked), integer(statuscode)}```
  - ```delete_homework(homework_id, group_id, password):{boolean(worked), integer(statuscode)}```
  - ```edit_homework(homework_id, group_id, date, subject, homework, password):{boolean(worked), integer(statuscode)}```

### Exams

  - ```get_exams(group_id):{boolean(worked), integer(statuscode), String-array(exams; only returned if worked=true)}```
  - ```add_exam(group_id, date, subject, exam, password):{boolean(worked), integer(statuscode)}```
  - ```delete_exam(exam_id, group_id, password):{boolean(worked), integer(statuscode)}```
  - ```edit_exam(exam_id, group_id, date, subject, exam, password):{boolean(worked), integer(statuscode)}```
