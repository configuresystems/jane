# User Module API

### Requests

Request | URL Endpoint | Action
------- | ------------ | ------
 POST   | http://12.34.56.78/api/users | POST new user
 GET    | http://12.34.56.78/api/users | GET list of users
 GET    | http://12.34.56.78/api/users/<int:page> | GET page of user list
 GET    | http://12.34.56.78/api/users/<username> | GET specific user information
 PUT    | http://12.34.56.78/api/users/<username> | Update specific user

### User Models

#### Users
* **username:** Unique identifier for users, *String Type*
* **password:** Password to log into the systems for the user, *String Type*
* **shell:** Valid shell for the user to use, *String Type*
* **domain:** Domain they manage, *String Type*
* **sudoer:** Set sudo user, *Boolean Type* 
* **user_details:** Relationship to UserDetails, identified by user, *String Type*

#### UserDetails
* **first** First name of the user, *String Type*
* **last** Last name of the user, *String Type*
* **company** Company name, *String Type*
* **phone** Phone Number, *String Type*
* **email** Email, *String Type*
* **user** Foreign Key of the Users model, Users.username, *String Type*


### Sample POST Request
```bash
$ curl -i -H "Content-Type: application/json" -X POST -d '{"username":"jane","domain":"jane.systems","shell":"/bin/bash","user_details":{"phone":"2105554545","company":"Galaxy Enterprises","last":"doe","email":"jane.doe@jane.systems","first":"Jane"},"sudoer":1,"password":"0ned4y1w1llbeah4sh"}' 12.34.56.78/api/users
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 544
Server: Werkzeug/0.9.6 Python/2.6.6
Date: Wed, 02 Jul 2014 05:22:26 GMT
{
    "user": {
        "domain": "jane.systems",
        "shell": "/bin/bash",
        "created": [
            "2014-07-02",
            "05:22:25"
            ],
        "user_details": {
            "last": "doe",
            "company": "Galaxy Enterprises",
            "phone": "2105554545",
            "user": "jane",
            "email": "jane.doe@jane.systems",
            "first": "jane"
            },
        "sudoer": 1,
        "uri": "http://12.34.56.78/api/users/jane",
        "password": "$6$rounds=100000$xQoZmX8AM.4t4oQ0$WESv4ktw.pOPHA6nCegfD5wsSN0xYbKph6fOt//ChoN.QpNjDMdGZy/q9qZPJQmyMJUrqK0dTJ1mtPQHSfiiS0"
    }
}
```

### Sample GET Request
```bash
$ curl http://23.253.96.98/api/users
{
    "users": [
    {
        "domain": "jane.systems",
        "shell": "/bin/bash",
        "created": [
            "2014-07-02",
            "05:22:25"
            ],
        "user_details": {
            "last": "doe",
            "company": "Galaxy Enterprises",
            "phone": "2105554545",
            "user": "jane",
            "email": "jane.doe@jane.systems",
            "first": "jane"
            },
        "sudoer": true,
        "id": 1,
        "username": "jane",
        "password": "0ned4y1w1llbeah4sh",
    },
    {
        "domain": "bob.systems",
        "shell": "/bin/nologin",
        "created": [
            "2014-07-02",
            "05:22:25"
            ],
        "user_details": {
            "last": "doe",
            "company": "Galaxy Enterprises",
            "phone": "2105554545",
            "user": "bob",
            "email": "bob.doe@bob.systems",
            "first": "bob"
            },
        "sudoer": false,
        "id": 2
        "usernane": "bob",
        "password": "hawt d0gs and h4mbooger$",
        }
    ]
}
```


### Sample GET Request on user
```bash
$ curl http://23.253.96.98/api/users/jane
{
    "user": [
    {
        "domain": "jane.systems",
        "shell": "/bin/bash",
        "created": [
            "2014-07-02",
            "05:22:25"
            ],
        "user_details": {
            "last": "doe",
            "company": "Galaxy Enterprises",
            "phone": "2105554545",
            "user": "jane",
            "email": "jane.doe@jane.systems",
            "first": "jane"
            },
        "sudoer": true,
        "id": 1,
        "username": "jane",
        "password": "0ned4y1w1llbeah4sh",
        },
    ]
}
```
