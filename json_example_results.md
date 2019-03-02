# Login
## Successful Login:
```json
{
  "expiration": "1551566875429.159", 
  "firstname": "Jürgen", 
  "surname": "Schulz", 
  "token": "ZLXz8RA8pJ4ziYyoSUKkgxEzBkzgSqDJPerKyi6nSQpUdkB1QVi3F2Bntd4xe112DqkMz5Llt1zUL0naNKUinVhUtVQfZBIWLCYgTxM9zZKWHFA9XXmBBezrxkyhiswo", 
  "type": 3, 
  "uid": 1
}
```

## Error-Response:
```json
{
  "error": 401, 
  "msg": "Login Failed"
}
```

# Teacher
## Get all Courses of a Teacher:
```
/teachers/<id>/courses
```
```json
[
  {
    "cid": 1, 
    "classid": 4, 
    "ctype": 3, 
    "short": "de", 
    "subid": 8, 
    "subject": "Deutsch", 
    "teacherid": 2
  }, 
  {
    "cid": 3, 
    "classid": 4, 
    "ctype": 3, 
    "short": "bio", 
    "subid": 1, 
    "subject": "Biologie", 
    "teacherid": 2
  }
]
```

# Student
## Get all Courses of a Student:
```
/students/<id>/courses
```
```json
[
  {
    "cid": 1, 
    "classid": 4, 
    "ctype": 3, 
    "short": "de", 
    "subid": 8, 
    "subject": "Deutsch", 
    "teacherid": 2
  }, 
  {
    "cid": 3, 
    "classid": 4, 
    "ctype": 3, 
    "short": "bio", 
    "subid": 1, 
    "subject": "Biologie", 
    "teacherid": 2
  }
]
```

# Class
## Get all Students of a Class:
```
/classes/<id>/students
```
```json
[
  {
    "classid": 4, 
    "courses": [
      {
        "cid": 1, 
        "classid": 4, 
        "ctype": 3, 
        "short": "de", 
        "subid": 8, 
        "subject": "Deutsch", 
        "teacherid": 2
      }, 
      {
        "cid": 2, 
        "classid": 4, 
        "ctype": 3, 
        "short": "ma", 
        "subid": 5, 
        "subject": "Mathematik", 
        "teacherid": 1
      }
    ], 
    "firstname": "Hugh", 
    "mail": "hugh@plg", 
    "name": "Mungus", 
    "uid": 3
  }, 
  {
    "classid": 4, 
    "courses": [
      {
        "cid": 1, 
        "classid": 4, 
        "ctype": 3, 
        "short": "de", 
        "subid": 8, 
        "subject": "Deutsch", 
        "teacherid": 2
      }, 
      {
        "cid": 3, 
        "classid": 4, 
        "ctype": 3, 
        "short": "bio", 
        "subid": 1, 
        "subject": "Biologie", 
        "teacherid": 2
      }
    ], 
    "firstname": "Big", 
    "mail": "big@plg", 
    "name": "Chungus", 
    "uid": 4
  }
]
```
