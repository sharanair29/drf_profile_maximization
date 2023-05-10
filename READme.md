
# Section 1 : Steps to run the project with Docker (skip if manual install is preferred)

Install docker desktop and run your daemon : 

https://www.docker.com/products/docker-desktop/

Set `DB_HOST=db` in `.env`.

Enter `docker compose build`

Enter `docker compose up -d`

Enter `docker-compose exec qrt python3 manage.py migrate`

Refer to `Input Payload` Section 3.

To stop run enter `docker compose down`


# Section 2 : Steps to run the project manually on (skip if docker install is preferred)

Make sure you have postgres installed.

Set `DB_HOST=localhost` in `.env`. 

Add your local DB connection parameters in `.env` for postgres.


`python3 -m venv ./venv`

`source ./venv/bin/activate`

`pip install -r requirements.txt`

`python manage.py migrate`

`python manage.py collectstatic`

`python manage.py runserver`

Refer to `Input Payload` Section 3.

To stop run enter `Ctrl + C`


# Section 3 : Input Payload


You can run the payload.py file in the root directory to test the payload input and output.

Enter `python payload.py`


# Section 4 : Project Description

This is an API utilizing Django Rest Framework to process input payloads with a list of contracts with details on their start, duration and price. The expected output is the optimum number of contracts to be taken with maximum profit without overlapping time periods from start to end.

For the purpose of this project time intervals are calculated as such:

`start = start`


`end = start + duration`

Profit per contract is calculated as:

`profit = price * duration`

# Section 5 : API 

The method chosen to build the API has been using a synchronous function based view that is wrapped with the `@api_view['POST']` decorator to explicitly state that this is an API view that takes in `POST` methods only. This view can be found in `api/views.py`.

A `Contracts` model was built in `api/models.py` within a postgres database to describe the standard SQL data structure (schema) of each Contract record object. 

After this, `ContractsSerializers` were built in `api/serializers.py` to describe the serializers used to validate the incoming json data against the `Contracts` Model defined in our `api/models.py` file.

This allows control of incoming data to make sure it adheres to the data structure we described and if it is valid we will go ahead with applying our profit maximization algorithm on the incoming contract data. Otherwise, we will return serializer errors stating what is missing in the input payload.

Since our input payload is a list of dictionaries of Contracts. We will need to validate the data using our serializers with the parameter `many=True` as follows `serializer = ContractsSerializer(data=python_data, many=True)`.

If valid against our Contracts Model we will save these serializers and generate a list of ids of all of the Contracts saved called `res_id`. This list of ids will allow us to filter the saved Contracts and map the contract details later on.

Next based on the list of ids called `res_id` we created from the validated serializer, we filter the contracts out and store it in `contracts`. As such:

`contracts = Contracts.objects.filter(pk__in=res_id)`


These filtered contracts queryset will be looped through to generate a list input called `contracts_list` that our Profit Maximization Algorithm takes in.

So we would have something like this `output = findMaxProfitContracts(contracts_list)` within our API view.

The function `findMaxProfitContracts` returns a list of ids of the Contract combination that returns the most profit with non overlapping intervals. This list will be stored in the variable `output` as stated above.

We can then further filter the previously filtered Contracts in `contracts` to return contracts with the `pk__in` the list `output`. This is done to prevent redundant SQL querying of the database all over again. By doing this we are limiting the number of queries processed by the server.

And there we have the list of contracts that will return maximum profit with non-overlapping time intervals and we can parse through this queryset to return `income` and `path` for the contract names as required.



# Section 6 : Profit Maximization Algorithm

The algorithm that is calculating the maximum profit possible with non-overlapping time intervals from the input contracts can be found in `api/algorithm.py`. The final function that will be called is `findMaxProfitContracts` and this will be imported into our `api/views.py` to process the json input payload and return a list of ids of the contracts that provide max profit.

The binary search on the contracts are documented in detail in the `api/algorithms.py`.

# Section 7 : Super user with docker

You may view the application running on docker at: 

`localhost:8080/spaceship/optimize`

If you wish to create a superuser to login to view the admin page at `localhost:8080/admin`:

Create a superuser with : `docker-compose exec qrt python3 manage.py createsuperuser`

# Section 8 : Super user with manual install

If you wish to create a superuser to login to view the admin page at `localhost:8080/admin`:

Create a superuser with : `python manage.py createsuperuser`