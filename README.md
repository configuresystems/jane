## TO DO List
* - [ ] Create Common Usage API
  * - [X] Create Basic API 
* - [X] Log each action into the database
* - [ ] Base Modules
  * - [ ] User
    * - [X] Create 
    * - [X] Modify
    * - [X] Ansible Support
    * - [X] API Support
    * - [ ] Web Support
    * - [X] Overview
    * - [X] Logging
      * - [X] Create
      * - [X] Update
      * - [X] Error
    * - [ ] Validation
      * - [ ] Username
      * - [ ] Passwd
      * - [ ] Shell
  * - [ ] Domain
    * - [X] Create 
    * - [ ] Modify
    * - [ ] Ansible Support
    * - [X] API Support
    * - [ ] Web Support
    * - [X] Overview
    * - [X] Logging
      * - [X] Create
      * - [ ] Update
      * - [X] Error
    * - [ ] Validation
      * - [ ] Domain
  * - [ ] Database
    * - [ ] Create 
    * - [ ] Modify
    * - [ ] Ansible Support
    * - [ ] API Support
    * - [ ] Web Support
    * - [ ] Overview
    * - [ ] Logging
      * - [ ] Create
      * - [ ] Update
      * - [ ] Error
    * - [ ] Validation
      * - [ ] Domain
* - [ ] Core Modules 
  * - [ ] Ansible
    * - [X] Deploy
    * - [ ] Parse Output
    * - [ ] Sort in database
    * - [ ] Determine Status
  * - [X] Database
  * - [X] Logging
  * - [ ] Install
  * - [ ] Server Details


## Directory Structure

    ├── app
    │   ├── core
    │   │   ├── ansible
    │   │   │   ├── __init__.py
    │   │   │   └── playbooks
    │   │   │       ├── group_vars
    │   │   │       │   └── all
    │   │   │       ├── inventory
    │   │   │       │   └── hosts
    │   │   │       ├── roles
    │   │   │       │   └── useradd
    │   │   │       │       ├── handlers
    │   │   │       │       ├── tasks
    │   │   │       │       │   └── main.yml
    │   │   │       │       ├── templates
    │   │   │       │       └── vars
    │   │   │       └── useradd.yml
    │   │   ├── api_views
    │   │   │   └── __init__.py
    │   │   ├── __init__.py
    │   │   ├── logging
    │   │   │   ├── __init__.py
    │   │   ├── models
    │   │   │   ├── __init__.py
    │   │   │   ├── jane.db
    │   │   │   └── jane_repository
    │   │   │       ├── __init__.py
    │   │   │       ├── manage.py
    │   │   │       ├── migrate.cfg
    │   │   │       ├── README
    │   │   │       └── versions
    │   │   │           └── __init__.py
    │   │   └── web_views
    │   ├── __init__.py
    │   ├── modules
    │   │   ├── domains
    │   │   │   ├── forms
    │   │   │   ├── inc
    │   │   │   └── views
    │   │   ├── __init__.py
    │   │   ├── overview
    │   │   │   ├── forms
    │   │   │   ├── inc
    │   │   │   └── views
    │   │   └── users
    │   │       ├── forms
    │   │       ├── inc
    │   │       │   └── __init__.py
    │   │       ├── __init__.py
    │   │       └── views
    │   │           ├── __init__.py
    │   │           └── main.py
    │   └── themes
    │       └── framework
    ├── bootstrap.sh
    ├── config.py
    ├── db_create.py
    ├── db_downgrade.py
    ├── db_migrate.py
    ├── db_upgrade.py
    ├── README.md
    ├── requirements.txt
    ├── run.py
    ├── tmp
    │   ├── error.log
    │   └── jane.log
    └── virtualenv.py

47 directories, 56 files
