### NYU-DevOps Orders Squad
[![codecov](https://codecov.io/gh/devops-orders/orders/branch/master/graph/badge.svg)](https://codecov.io/gh/devops-orders/orders)
[![Build Status](https://travis-ci.org/devops-orders/orders.svg?branch=master)](https://travis-ci.org/devops-orders/orders)

README for the orders squad.

#### API calls
URL | Operation | Description
-- | -- | --
`GET /orders` | READ | List all available routes
`POST /orders` | CREATE | Create new order
`GET /orders/:id` | READ | Fetch information for particular order
`PUT /orders/:id` | UPDATE | Update particular order
`DELETE /orders/:id` | DELETE | Delete particular order
`GET /orders/products/:product_id` | READ | Fetch orders for given product
`PUT /orders/:id/cancel` | PUT | Cancel order for given order id
`GET /orders/customers/:customer_id` | GET | Fetch orders for a given customer

#### Run and Test
- Clone the repository using: `git clone git@github.com:devops-orders/orders.git`
- Start the Vagrant VM using : `vagrant up`
- After the VM has been provisioned ssh into it using: `vagrant ssh`
- cd into `/vagrant` using `cd /vagrant` and start the server using `FLASK_APP=service:app flask run -h 0.0.0.0`
- Inside `/vagrant` run `nosetests`
