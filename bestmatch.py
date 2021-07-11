import csv
import sys
import json
from operator import itemgetter
import random


#########################
#                       #
# Auxiliary functions!  #
#                       #
#########################


def get_args(error_list):
    """Get the args from the command line."""
    n = len(sys.argv)
    args = []
    if n < 3:
        #print("Error: Missing args")
        error_list.append("Error: Missing args")
        return 0, error_list
    elif n > 3:
        #print("Error: Too many args")
        error_list.append("Error: Too many args")
        return 0, error_list
    else:
        for i in range(1,n):
            args.append(sys.argv[i])
        return args, error_list


def open_input_file(my_input):
    """Open the JSON contaiting the user input."""
    with open(my_input) as f:
        my_data = json.load(f)
    return my_data


def get_cuisines():
    """Get the cuisines from the csv file."""
    cuisines_file = open('cuisines.csv')
    cuisines_csv = csv.reader(cuisines_file)

    cuisines_list = []
    for row in cuisines_csv:
        cuisines_list.append(row)

    cuisines_list.pop(0)
    return cuisines_list


def get_restaurants():
    """Get the restaurants from the csv file."""
    restaurants_file = open('restaurants.csv')
    restaurants_csv = csv.reader(restaurants_file)

    restaurants_list = []
    for row in restaurants_csv:
        restaurants_list.append(row)

    restaurants_list.pop(0)
    return restaurants_list


def filter_restaurant(name, restaurant_list, error_list):
    """Filter the restaurant name based on the user input."""
    if name != "":
        aux_list = []
        for restaurant in restaurant_list:
            if (name.lower() in restaurant[0].lower()) == True:
                aux_list.append(restaurant)
        return aux_list, error_list
    else:
        return restaurant_list, error_list

def filter_customer_rating(rating, restaurant_list, error_list):
    """Filter the customer rating based on the user input."""
    if rating != "" and rating > 0 and rating <= 5:
        aux_list = []
        for restaurant in restaurant_list:
            if int(restaurant[1]) >= rating:
                aux_list.append(restaurant)
        return aux_list, error_list
    else:
        error_list.append("The customer rating needs to be between 1 and 5")
        return restaurant_list, error_list

def filter_distance(distance, restaurant_list, error_list):
    """Filter the distance based on the user input."""
    if distance != "" and distance > 0 and distance <= 10:
        aux_list = []
        for restaurant in restaurant_list:
            if int(restaurant[2]) <= distance:
                aux_list.append(restaurant)
        return aux_list, error_list
    else:
        error_list.append("The distance needs to be between 1 and 10")
        return restaurant_list, error_list

def filter_price(price, restaurant_list, error_list):
    """Filter the price based on the user input."""
    if price != "" and price >= 10 and price <= 50:
        aux_list = []
        for restaurant in restaurant_list:
            if int(restaurant[3]) <= price:
                aux_list.append(restaurant)
        return aux_list, error_list
    else:
        error_list.append("The price needs to be between 10 and 50")
        return restaurant_list, error_list

def filter_cuisine(cuisine, restaurant_list, cuisine_list, error_list):
    """Filter the cuisine type based on the user input."""
    if cuisine != "":
        cuisine_ids = []
        for cuisine_obj in cuisine_list:
            if (cuisine.lower() in cuisine_obj[1].lower()) == True:
                cuisine_ids.append(cuisine_obj[0])
        aux_list = []
        for restaurant in restaurant_list:
            if restaurant[4] in cuisine_ids:
                aux_list.append(restaurant)
        return aux_list, error_list
    else:
        return restaurant_list, error_list


def initialize_data(args, error_list):
    """Initialize the data, filtering the restaurants with the user input."""
    # Get the cuisines from the csv
    cuisines_list = get_cuisines()

    # Get the restaurants from the csv
    restaurants_list = get_restaurants()

    # Get the number of results that the user wants
    number_of_results = int(args[0])

    # Get the user input
    my_data = open_input_file(args[1])

    # Variable that will receive the filtered data
    filtered_list = restaurants_list.copy()

    # Filter the list with the user input
    for item in my_data:
        if item == "restaurant_name":
            filtered_list, error_list = filter_restaurant(my_data[item], filtered_list, error_list)
        elif item == "customer_rating":
            filtered_list, error_list = filter_customer_rating(my_data[item], filtered_list, error_list)
        elif item == "distance":
            filtered_list, error_list = filter_distance(my_data[item], filtered_list, error_list)  
        elif item == "price":
            filtered_list, error_list = filter_price(my_data[item], filtered_list, error_list)
        elif item == "cuisine":
            filtered_list, error_list = filter_cuisine(my_data[item], filtered_list, cuisines_list, error_list)

    return filtered_list, number_of_results, error_list


def check_tie(sorted_list, level, matched, original_size):
    """Check if there are tie or if there is a match."""
    list_size = len(sorted_list)

    if level == 1: # We are testing the distance
        criteria = 2
    elif level == 2: # We are testing the rating
        criteria = 1
        # Sort by the ratings in the descending order
        sorted_list = sorted(sorted_list, key = itemgetter(1), reverse=True)
    elif level == 3: # We are testing the price
        criteria = 3
        # Sort by the price
        sorted_list = sorted(sorted_list, key = itemgetter(3))
    else: # We are choosing randomly
        # Get the random number to decide which one to choose
        random_number = random.randint(0,list_size-1)

        return ["match", sorted_list[random_number]]

    # Get the param to compare with the other ones
    if list_size == original_size: # If we are dealing with the full list
        param = sorted_list[matched][criteria] # We will get the next one that are not matched
        param_for = matched+1 # Start comparing by the second one that are not matched
    else:
        param = sorted_list[0][criteria] # The param that we need to compare the others with
        param_for = 1 # We will start comparing by the next one

    # Aux variable to see how much equals we have in this round
    equals = 0

    for item in sorted_list[param_for:]:
        if item[criteria] == param: # We found an equal one
            equals = equals + 1
    
    if equals == 0: # We have a best option!
        if len(sorted_list) == original_size: # If we found the best in the first round
            return ["match", sorted_list[matched]] # We need to exclude the already matched ones
        else: # We found in another round
            return ["match", sorted_list[0]] # Its the first one
    else: # We still have a tie
        return ["tie", sorted_list, equals+1]


def prepare_the_results(final_list):
    """Prepare the JSON output containing the result."""
    final_data = []
    final_obj = {}
    message = ""
    if len(filtered_list) != 0:
        for i,item in enumerate(final_list):
            obj = {}
            obj["restaurant_name"] = item[0]
            obj["customer_rating"] = item[1]
            obj["distance"] = item[2]
            obj["price"] = item[3]
            obj["cuisine"] = item[4]
            final_obj[i+1] = obj
        message = "Your results are in the json file."
    else:
        message = "Sorry we dont have any recommendation"
    
    final_data.append(final_obj)
    
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    
    print(message)


#########################
#                       #
# Start of the program! #
#                       #
#########################

error_list = []

# Get the args from the command line
args, error_list = get_args(error_list)

# We have problem with the arguments
if args == 0:
    for item in error_list:
        print(item)
else:
    # Receive the filtered list using the user input that we will work on
    # and also the number os results that we want and a error list in case of any error occur
    filtered_list, number_of_results, error_list = initialize_data(args, error_list)

    if len(filtered_list) == 0: # There ae no matches
        prepare_the_results(filtered_list)
    elif len(filtered_list) == 1: # There are only one match
        print("We have just one recommendation:")
        prepare_the_results(filtered_list)
    else: # We have a lot of results, so lets filter the best ones
        
        # Cast the str's to int's
        for item in filtered_list:
            item[1] = int(item[1])
            item[2] = int(item[2])
            item[3] = int(item[3])

        # Sort the items by the distance
        sorted_distance_list = sorted(filtered_list, key = itemgetter(2))
        
        # Total items in the list
        total_items = len(sorted_distance_list)

        # If the results are bigger than 5, then cut the unnecessary ones
        if len(sorted_distance_list) > number_of_results:
            # Get the max distance based on the number of results wanted
            max_distance = sorted_distance_list[number_of_results-1][2]

            short_distance_count = 0
            equal_distance_count = 0
            
            # Cut the unnecessary items in the list
            for index, item in enumerate(sorted_distance_list):
                # If distance is shorter
                if item[2] < max_distance:
                    short_distance_count = short_distance_count + 1
                # If distance is equal
                elif item[2] == max_distance:
                    equal_distance_count = equal_distance_count + 1
                # If distance if bigger, then delete the rest of the itens from the list
                elif item[2] > max_distance:
                    aux_index = short_distance_count + equal_distance_count
                    del sorted_distance_list[aux_index:]
                    break
            
            # Total items that remained in the list
            total_items = short_distance_count + equal_distance_count

        # Aux variables
        finished = False
        matched = 0
        equals = 0
        level = 1 # start comparing the distances
        original_size = len(sorted_distance_list)
        aux_list = sorted_distance_list
        final_list = []

        while finished != True:

            # See if its tied
            result = check_tie(aux_list, level, matched, original_size)
            
            if result[0] == "match": # If we have a match

                # Search the index inside the list
                my_index = sorted_distance_list.index(result[1])
                
                # Remove from that index
                sorted_distance_list.pop(my_index)

                # Put in the right ranked position in the list
                sorted_distance_list.insert(matched, result[1])
                
                # Update the matched ones
                matched = matched + 1
                
                # Return the level to the start
                level = 1

                # Put the matched one in the final list
                final_list.append(result[1])

                # Update the aux list with the complete sorted list again, to the next round of tests
                aux_list = sorted_distance_list

                # If we reached the end of our matching process
                if matched == number_of_results or matched == len(sorted_distance_list):
                    finished = True
            elif result[0] == "tie": # We are tied
                
                # Get how much equals we have in this round of tests
                equals = result[2]

                # Update the level of the test
                level = level + 1

                # Get the sorted list that will be used in the new round of tests
                sorted_list = result[1]

                # If we are testing other than distance (remember that the level was recently updated)
                if level > 2:
                    aux_list = sorted_list[0:equals]
                else: # If we are testing the distance, we need to exclude the already matched ones
                    aux_list = sorted_list[matched:matched+equals]

        prepare_the_results(final_list)