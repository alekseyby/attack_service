# Cloud attack service

Service provides 4 urls to
* Attack (`/api/v1/attack/`) to perform analysis of possible accessed machined by vm_id
* Stats (`/api/v1/stats/`) to get stat of API usage

### API documentation
#### Attack endpoint
url: `/api/v1/attack/`
method: GET

permissions: Allow any

Query pararms

| Field name | Field type | Limitations                                         |
|------------|------------|-----------------------------------------------------|
| vm_id      | char       | required                                            |

Example with curl
```
curl -i 'http://localhost:8000/api/v1/attack/?vm_id=vm-2987241'
```

Response example
```
["vm-ab51cba10"]
```


#### Stats endpoint
url: `/api/v1/stats/`
method: GET

permissions: Allow any

Example with curl
```
curl -i 'http://localhost:8000/api/v1/stats/'
```

Response example
```
{
    "vm_count":11,
    "request_count":2,
    "average_request_time":0.5187334
}
```



### Make commands

* `make test` - run tests
* `make build` - build service
* `make up` - launch service
* `make linter` - launch linter
* `make load_infra FILE=${relative_path_to_json_data_input}`
  * example: ` make load_infra FILE=data_inputs/input-4.json`
* `make overwrite_infra FILE=${relative_path_to_json_data_input}` (DELETES OLD INFRASTRUCTURE BEFORE LOADING)
  * example: ` make load_infra FILE=data_inputs/input-4.json`



How to run step-by-step:

1. `docker-compose up` 
2. `make load_infra FILE=data_inputs/input-4.json` (it's important to use relative path to data_inputs directory)
3. make requests to endpoints
