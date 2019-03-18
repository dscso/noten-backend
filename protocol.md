# Loginrequest
    /login [POST]

### Parameter:
```JS
{
    username: (mail)
    password: (password)
}
```

### Response: 200/401
```JS
{
    tocken: "token valid for 30 days",
    expiration: "UNIX timestamp in seconds",
    firstname: "The first name",
    surname: "The family name",
    uid: "the user id in the database used to make requests",
    type: "1 SEKI, 2 SekII, 3 teacher, 4 admin",
}
```
The token will be saved as a cookie (called *token*) and will be send with every further request
# Userinfo
    /user/<userid> [GET]
    /profile

### Parameter [login required]
None
### Response 200/403/403
```JS
{
    firsname: "The first name",
    surname: "The family name",
    uid: "the user id in the database used to make requests",
    type: "1 SEKI, 2 SekII, 3 teacher, 4 admin",
}
```

This request returns general userinfo used by the webiterface

# Teacher get courses
    /teacher/<teacherid>/courses [GET]
### Parameter [login required]
None
### Response 200/403/404
```JS
{
    courses: [{
        subject: "the kind of the course (math, physics etc.)",
        cid: "the id",
        generation: "SEKI/SEKII"
    }{
        ...
    }]
}
```

This will be fetched when the teacher is logging in and the client shows all courses the teacher teaches. **classes he teaches like ma-4 etc.**

# get Students of course
    /courses/<courseid>/students [GET]
### Parameter [login_required]
None
### Repsonse 200/403/404
```JS
{
    subject: "...",
    cid: "...",
    generation: "",
    students: [{
        firsname: "The first name",
        surname: "The family name",
        uid: "the id of the student"
    },{
        ...
    }]
}
```
This is used to render the colums of the table with the grades
# Create new MarkMeta for course
    /courses/<courseid>/markmetas [POST,PUT,DELETE]
### Paramerters [login_required] 
    name, valance
### Response 200/403
```JS
{
    "success":true
}
```

# Error message

```JS
{
    error: 401/404,
    msg: "Humanreadable Message",
}
```
# Authentification
Using authetification headers (like oauth)
`Authorization` get set to `Bearer <token>`
Example:
```YML
Accept: application/json
Authorization: Bearer K3nnpiMFi8nEHnk0VK1RNR94a2PmOYC0
Origin: http://localhost:8080
Referer: http://localhost:8080/
...
```
