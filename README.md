# Greenprint

## Paths:
------
`GET /accounts` | Returns a list all of the accounts
`GET /accounts/{id}` | Returns the account with a given id number
`POST /accounts `| creates a new account record in the database
`PUT /accounts/{id}` | updates an account record in the database
`DELETE /accounts/{id}` | deletes an account record in the database
`GET /accounts/{owner}` | Returns the accounts with a given owner
`GET /accounts/{account_id}` | Returns the accounts with a given account id number
`GET /accounts/{account_type}` | Returns the accounts with a given account type
`GET /accounts/{institution_id}` | Returns the accounts with a given institution id number
`GET /accounts/{balance}` | Returns the accounts with a given balance
"""


## Prerequisite Installation using Vagrant VM

The easiest way to use this lab is with **Vagrant** and **VirtualBox**. if you don't have this software the first step is down download and install it.

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

Then all you have to do is clone this repo and invoke vagrant:

```bash
    git clone https://github.com/nyu-devops/lab-flask-rest.git
    cd lab-flask-rest
    vagrant up
    vagrant ssh
    cd /vagrant
    FLASK_APP=service:app flask run -h 0.0.0.0
    honcho start 2>&1 > /dev/null &
```


When you are done, you can exit and shut down the vm with:

```bash
    exit
    vagrant halt
```

If the VM is no longer needed you can remove it with:

```bash
    vagrant destroy
```
