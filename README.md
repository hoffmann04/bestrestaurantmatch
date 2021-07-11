# Best Match Algorithm

Hello! This algorithm searches for the best restaurant match given the user input.

It uses some pre-defined criteria to know which is the best option and the best match fot that given input.

The input and the output are in JSON, because the algorith was made thinking to be easily adapted to API's.

## How to run the algorithm

To run the algorithm is pretty simple!

You only need to inform the max number of results that you want and a JSON file containing the things that you want to filter

Open the terminal where your source code, csv and JSON files are and type:

python3 bestmatch.py argv1 argv1

Where:
- argv1 are the number of results that you want
- argv2 are the json file with the input that you want to filter

## The JSON input

The JSON input can have all the criterias, some of the criterias or none of them, as the example below:

```
{
	"distance": 2,
	"price": 15
}
```

or

```
{
	
}
```

or

```
{
    "restaurant_name": "deli",
    "customer_rating": 5,
    "distance": 10,
    "price": 50,
    "cuisine": ""
}
```

## The result

The result of your search will come in a JSON file as well.

You will only have a simple message in the terminal to know what happened (error or success).

The JSON with the results will be a empty object if no match were found.

If one or more matched were founded, it will be:

```
[
	{
		"1": {
			"restaurant_name": "Name",
			"customer_rating": 5,
			"distance": 2,
			"price": 15,
			"cuisine": "18"
		},
		"2":{
			and go on...
		}
	}
]
```

#### p.s.: The approach in this algorithm uses lists, but could be done using class/object as well.