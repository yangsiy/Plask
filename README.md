#Plask

A simple online questionnaire survey system

##Dependency

Dependencies needed for running the system:

* Flask

* flask-login

* sqlalchemy

* flask-sqlalchemy

* sqlalchemy-migrate

* flask-wtf

##Debugging

For the first time running, empty sqlite database should be generated:

```
$ python db_create.py
```

Start the develpment server for debugging:

```
$ python run.py
```

The system will be running on 
``
http://localhost:5000
``

##License

MIT
