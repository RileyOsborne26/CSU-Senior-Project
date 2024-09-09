import requests
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta
import sys
import csv
import subprocess  #needed since we are using WSL

# ToC
### User input & URL manipulation - Line 142
### Web Scraping - Line 285
### Card Pricing Functionality - Line 357

##### TESTING BLOCK for new code (up at the beginning of the program)


#####


# source URL: brightdata.com/blog/how-tos/how-to-scrape-ebay-in-python
# Author: Riley Osborne

# list of product sets currently supported in the web scraping script
SUPPORTED_SETS = ["Donruss", "Donruss Optic", "Prizm", "Panini Prizm", "Score", "Mosaic", "Chronicles", "Panini Chronicles",
                   "Phoenix", "Torque", "Panini Torque", "Contenders", "Panini Contenders"]

# list of sports currently supported
SUPPORTED_SPORTS = ["Baseball", "Basketball", "Football", "Nascar"]
 
# The grading companies array and url string have been replaced by the superior "&Grade"" url piece
#######                   
## list of card grading companies. List will be used for narrowing seaches excluding graded cards and searches including specific grading companies
## Even though there is a Graded bit in the URL, this will be used for exclusion because it isn't perfect
GRADING_COMPANIES = ["CSG", "PSA", "BGS", "SGC", "HGA"]               
#######
    

# functions
# print the supported sets
def print_set_products():
    print("\nSupported sets: ")
    for i in SUPPORTED_SETS:
        print(i + ", ")

# prints a menu of the sports for the user to choose
def print_sports_list():
    print("\nSports Menu:")
    count = 0
    for i in SUPPORTED_SPORTS:
        print("[" + str(count) + "] " + i)
        count += 1

# get parallel colors list for the given SET + SPORT + YEAR in hopes of narrowing down search
def get_parallel_colors_list(set_name, sport_index, year):
    print(set_name)
    print(sport_index)
    print(year)
    # check the options
    if (set_name == "Donruss" and sport_index == 2 and year == "2018"):
        return ["blue", "green", "red", "silver", "gold", "black"]
    else:
        # return empty list if set+sport+year is not supported
        print("We are sorry, your card does not yet have a parallel colors list")
        return []
    

# get parallel types list for the given SET + SPORT + YEAR in hopes of narrowing down search
def get_parallel_types_list(set_name, sport_index, year):
    # check the options
    if (set_name == "Donruss" and sport_index == 2 and year == "2018"):
        return ["studio series", "prime", "nfl shield", "nfl player's logo", "brand logo", "aqueous test", "stat line", "jersey number", "press proof", "press proof die-cut", "holo"]
    else:
        # return empty list if set+sport+year is not supported
        print("We are sorry, your card does not yet have a parallel types list")
        return []

# print the parallel colors list
def print_parallel_colors(parallel_colors):
    # print the list passed to the function
    count = 0
    print("\nParallel Colors List:")
    for i in parallel_colors:
        print("[" + str(count) + "] " + i)
        count += 1

# print the parallel types list
def print_parallel_types(parallel_types):
    # print the list passed to the function
    count = 0
    print("\nParallel Types List:")
    for i in parallel_types:
        print("[" + str(count) + "] " + i)
        count += 1

# trims the price data going into the results
def format_price(main_price):
    return float( main_price.strip("$") )    #cast to float after making it all numbers

# trims the shipping data going into the results
def format_shipping(ship_price):
    # special case for free shipping listings
    if ship_price == "Free shipping":
        return float( '0' )
    else:
        # make shipping price a number ONLY string and then cast to float precision 2
        return float( ship_price.strip('+$ shipping') )
    
# trims the date and puts it in the preferred format
def format_selling_date(sold_date_string):
    # Remove "Sold " from the string result by using substrings 
    sold_date_string = sold_date_string[6:]
    print("TROUBLESHOOT (2): " + sold_date_string)

    # remove the comma from the date to ensure fluidity in converting to date object
    sold_date_string = sold_date_string.replace(',', '')
    print("TROUBLESHOOT (3): " + sold_date_string)

    # convert string to date object format
    sold_date = datetime.datetime.strptime(sold_date_string, '%b %d %Y').date()
    sold_date_string = datetime.datetime.strftime(sold_date, '%m-%d-%Y')     # converting back to a string with desired date form
    sold_date = datetime.datetime.strptime(sold_date_string, '%m-%d-%Y').date()     # converting back to date object with desired date form

    # turn string into the date object
    return sold_date
    
# combines the shipping and price for a total listing price    
def get_listing_price(main_price, ship_price):
    return round((main_price + ship_price), 2)

# get the oldest completed selling date for a card
def get_oldest_sold_date(sold_dates, index):
    return sold_dates[index - 1]

# get the most recent completed selling date for a card
def get_newest_sold_date():
    return sold_dates[0]

# scrapes the sold listings, I will pass all the arrays and the soup as arguments
def scrape_page(sold_dates, titles, prices, shipping, total_prices, search_results, listings_num):
    # all the sold listings contain the unique "data-viewport" attribute, which is used to scrape them all.
    search_results = soup.find('ul', class_='srp-results srp-list clearfix').find_all('li', attrs={'data-viewport': True})

    # iterate only for the amount of search results returned
    for i in range(listings_num):
        print(i)
        item_title = search_results[i].find('div').find(class_='s-item__info clearfix').find('a').find('div').find('span').text
        titles.append(item_title)
        
        # temp prices is used here to hold the price, type of listing (# of bids, best offer, or buy it now), and the shipping cost
        # this is because the html is not different enough to ignore the type of listing unless there are tools out there that I am missing. This gets the job done though
        temp_prices = search_results[i].find('div').find(class_='s-item__info clearfix').find(class_='s-item__details clearfix').find_all('div', class_='s-item__detail s-item__detail--primary')
        
        # get the item sold date
        sold_date_string = search_results[i].find('div').find(class_='s-item__info clearfix').find(class_='s-item__caption').find('div').find('span').text
        print("TROUBLESHOOT (1): " + sold_date_string)

        # using a for loop through the temp_prices to ensure I get the correct span for shipping!!!
        for price in temp_prices:
            shipping_span = price.find('span', class_='s-item__shipping s-item__logisticsCost')
            if shipping_span:
                ship_price = shipping_span.text
                break
        
        main_price = temp_prices[0].find('span').find('span').text

        # format date AND price AND shipping
        sold_date = format_selling_date(sold_date_string)
        main_price = format_price(main_price)
        ship_price = format_shipping(ship_price)

        # get the total price for the listing
        total_price = get_listing_price(main_price, ship_price)

        # add the results to their arrays
        sold_dates.append(sold_date)
        prices.append(main_price)
        shipping.append(ship_price)
        total_prices.append(total_price)

# passes the results_csvformat array and all five arrays of info for output in dictionary form
# This was originally done in scrape_page() but was moved to help sort the results first with selection_sort_scraped_results()
def scrape_results_to_csv(results_csvformat, sold_dates, titles, prices, shipping, total_prices):
    # check that the arrays are the same length
    if len(sold_dates) != len(sold_dates) != len(titles) != len(prices) != len(shipping) != len(total_prices):
        print("ERROR: You are missing data from your ebay scraping results. The arrays are not all the same length.")
        exit(1)   #exit program with the error message

    # create a dictionary to combine all the array results into one place. MAKE SURE EVERYTHING IS SORTED!!!
    for i in range(len(sold_dates)):
        # get all the data for the dictionary in one place
        sold_date = sold_dates[i]
        item_title = titles[i]
        main_price = prices[i]
        ship_price = shipping[i]
        total_price = total_prices[i]

        # put it into the csv dictionary form
        results_csvformat.append(
            {
                'date': sold_date,
                'name': item_title,
                'main price': main_price,
                'shipping price': ship_price,
                'listing price' : total_price
            }
        )

    # This csv file will be used to check the results of the web scraping
    # create a "results.csv" if not present
    output_file_dir = "results/"
    output_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_name = output_name + ".csv"    # add the file extension
    output_file = output_file_dir + output_name
    csv_file = open(output_file, 'w', encoding='utf-8', newline='')

    # initializing the writer object to insert data
    # in the CSV file
    writer = csv.writer(csv_file)

    # writing the header of the CSV file
    writer.writerow(['Sold Date', 'Name', 'Main Price', 'Shipping Cost', 'Listing Total'])

    # writing each row of the CSV
    for result in results_csvformat:
        writer.writerow(result.values())

    # add the link and search info to the end of the file for reference
    writer.writerow([url])
    full_name = first_name + last_name
    writer.writerow(['Year', 'Product', 'Player Name'])
    writer.writerow([year, product_set, full_name])

    # terminating the operation and releasing the resources
    csv_file.close()

    print("SUCCESS: web scraping to CSV function")


# This is a sort to fix Ebay's poor job of sorting listings by date with their "ended recently" filter
# This function ensures the appropriate changes are made to all the arrays & not just the sold dates array.
# the first parameter is the main array getting selection sorted, with the other arrays being parallel.
def selection_sort_scraped_results(sold_dates, titles, prices, shipping, total_prices):
    # sort variables
    sort = 0
    idx = 0
    primary_size = len(sold_dates)
    temp_sold = 0
    temp_title = ""
    temp_price = 0
    temp_ship = 0
    temp_total = 0

    # start sorting, if array is length 10, 10th item is 9th index
    for sort in range(primary_size - 1):
        newest_idx = sort

        for idx in range(sort + 1, primary_size):
            if sold_dates[idx] > sold_dates[newest_idx]:
                newest_idx = idx
        
        # start swapping with the primary array 
        temp_sold = sold_dates[sort]
        sold_dates[sort] = sold_dates[newest_idx]
        sold_dates[newest_idx] = temp_sold

        # swap for the parallel arrays as well
        temp_title = titles[sort]
        temp_price = prices[sort]
        temp_ship = shipping[sort]
        temp_total = total_prices[sort]
        titles[sort] = titles[newest_idx]
        titles[newest_idx] = temp_title
        prices[sort] = prices[newest_idx]
        prices[newest_idx] = temp_price
        shipping[sort] = shipping[newest_idx]
        shipping[newest_idx] = temp_ship
        total_prices[sort] = total_prices[newest_idx]
        total_prices[newest_idx] = temp_total


    print("**COMPLETE: Ebay sold listings were sorted by date.")

# return the number of sold listings for the x amount of past days
# the first parameter is the dates sold list, second being the days you want to count into the past. Third parameter is current date.
# the function assumes the array is sorted
def sold_in_range(sold_dates, num_days, current_date):
    # variable for counting listings number
    listing_count = 0
    idx = 0
    
    # current date - the date in the array gives a number of days for the gap. Make sure it is in range of num_days.
    while (current_date - sold_dates[idx]).days <= num_days:
        # if the date is valid, increase listing count and index
        listing_count += 1
        idx += 1

    return listing_count

    
###
# get the current year for user input validation
currentYear = datetime.datetime.now().year

# get the sport of the card from the user and validate input
print_sports_list()
invalid = True

while invalid: 
    sport = input("Enter your card's sport name from the list: ")
    count = 0
    for i in SUPPORTED_SPORTS:
        if i == sport:
            sport_index = count
            invalid = False
        else:
            count += 1

# keep the number of arguments
argCount = len(sys.argv)

# start of user interaction
### get card year from arguments list or from the user
if (argCount < 2):
    year = input("Enter in the year your card was manufactured: ")
else:
    year = sys.argv[1]
    # check that the input is not a string
    if (year.isdigit() == 0):
        print('ERROR: you either forgot to give a year for' + 
              'an argument or you did not enter a number. Please ensure your run command contains the correct parameters.')
        isFinished = input("Please press any key to continue or 0 to exit.")
        # ask the user if they want to continue
        if(isFinished == 0):
            sys.exit(2)
        else:
            year = input("Enter in the year your card was manufactured: ")

# validate year input
while(int(year) < 1860 or int(year) > currentYear):
    print("Invalid year. Please try again.")
    year = input("Enter in the year your card was manufactured: ")

### get product set name
if(argCount < 3):
    print_set_products()
    product_set = input("Enter in the card product set name: ")
else:
    product_set = sys.argv[2]

# validate product set name input
while(product_set not in SUPPORTED_SETS):
    print("Invalid or unsupported product set name. Please try again.")
    product_set = input("Enter in the card product set name: ")

### get first name
if(argCount < 4):
    first_name = input("\nEnter the athlete's first name: ")
else:
    first_name = sys.argv[3]

### get last name
if(argCount < 5):
    last_name = input("\nEnter the athlete's last name: ")
else:
    last_name = sys.argv[4]

### get rookie keyword if it exists
if(argCount == 6):
    isRookie = "rookie"
else:
    isRookie = "0"
    
# ask if the card is graded
isGraded = input("\nIs the card graded (y/n): ")

# validate user input
while(isGraded != "y" and isGraded != "n"):
    print("Invalid input. Please try again.")
    isGraded = input("Is the card graded (y/n): ")

# create the url bit based on the user answer
if isGraded == "y":
    gradeNum = input("Please enter a card grade number (1-10): ")
    while(int(gradeNum) < 1 or int(gradeNum) > 10):
        print("Invalid number. Please try again.")
        gradeNum = input("Please enter a card grade number (1-10): ")
    # translate result into url part
    gradedUrlBit = "=" + gradeNum
else:
    gradedUrlBit = "d=No"

    ## add the url part that excludes listings with the name of the grading company in the title
    ## string to be used for search queries excluding graded cards
    gradersString = ""

    ## create final version of gradersString for URL
    for i in GRADING_COMPANIES:
        gradersString = gradersString + "-" + i + "+"

    # take off the extra "+" at the end of the string    
    gradersString = gradersString[0:-1]


# other detailed variables to implement later
isAuto = "0"
isParallel = "0"
parallelColor = "0"
parallelType = "0"
isNumbered = "0"
printRun = "0"

# ask if the card is a parallel
isParallel = input("\nIs the card a parallel (y/n): ")

# validate user input
while(isParallel != "y" and isParallel != "n"):
    print("Invalid input. Please try again.")
    isParallel = input("Is the card a parallel (y/n): ")

# get the card's parallel color and type if user input is yes, if not then the set information is still gathered
set_parallel_colors = []
set_parallel_types = []

# get the array of parallel options for the given card
# this was moved outside of the if statement for URL term excluding
set_parallel_colors = get_parallel_colors_list(product_set, sport_index, year)
set_parallel_types = get_parallel_types_list(product_set, sport_index, year)

# handle when the user says the card has a parallel
if isParallel == "y":
    # a variable to ensure that if isParallel is set to yes that at least one parallel attribute is assigned (color or type)
    invalid_isParallel = True

    # ask user if they want to input a parallel type
    print_parallel_types(set_parallel_types)
    parallelType = input("\nAssign card a parallel type from list? (y/n): ")

    # validate user input
    while(parallelType != "y" and parallelType != "n"):
        print("Invalid input. Please try again.")
        parallelType = input("Assign card a parallel type from list? (y/n): ")

    # take input to determine how to handle parallelType
    if parallelType == "y":
        # parallel attribute will be set, so isParallel is set correctly
        invalid_isParallel = False

        # get parallel type from user and validate input
        while(parallelType not in set_parallel_types):
            parallelType = input("Enter in a card parallel type from the list: ")
    # no else bc subtracting types from the search query not always wise will reset to zero before creating url

    # ask user if they want to input a parallel color
    print_parallel_colors(set_parallel_colors)
    parallelColor = input("\nAssign card a parallel color from list? (y/n): ")

    # validate user input
    while(parallelColor != "y" and parallelColor != "n"):
        print("Invalid input. Please try again.")
        parallelColor = input("Assign card a parallel color from list? (y/n): ")

    # check that a parallel attribute was or will be actually set, or isParallel will change to "n"
    if parallelColor == "n" and invalid_isParallel == True:
        isParallel = "n"


# take input to determine how to handle parallelColor
# had to bump it out of the conditional so I can use the excluded terms despite the value of "isParallel"
if parallelColor == "y":
    # parallel attribute will be set, so isParallel is set correctly
    invalid_isParallel = False

    # get parallel color from user and validate input
    while(parallelColor not in set_parallel_colors):
        parallelColor = input("Enter in a card parallel color from the list: ")

    ### TO DO: exclude color terms that were NOT set to be parallelColor
    ###
else:
    # since no, create the url part that will exclude listings with color names in the title
    ## string to be used for search queries excluding parallelColor
    colorsString = ""

    ## create final version of colorsString for URL
    for i in set_parallel_colors:
        # check for spaces and alternate URL format accordingly if found
        if i.find(" ") != -1:
            temp_i = i.replace(" ", "+")
            colorsString = colorsString + "-\"" + temp_i + "\"+"
        else:
            colorsString = colorsString + "-" + i + "+"

    # take off the extra "+" at the end of the string    
    colorsString = colorsString[0:-1]


# if no then add colors to exclude from the url


# if there are no CLI parameters
if len(sys.argv) < 1:
    print('Item ID argument missing!')
### sys.exit(2)

# read the item ID from a CLI argument
###item_id = sys.argv[1]

# build the URL of the target product page
# it is for one product
###url_one_item = f'https://www.ebay.com/itm/{item_id}'

# display all the details for the user to approve
print("\n" + "Your search keywords (0 = not set):")
print("Year = " + year + "\n" + "Product set = " + product_set
      + "\n" + "First name = " + first_name + "\n" + "Last name = " + last_name)
print("Rookie card = " + isRookie + "\n" + "Autographed = " + isAuto + "\n"
      + "Parallel = " + isParallel + "\n" + "Parallel color = " + parallelColor + "\n"
      + "Numbered = " + isNumbered + "\n" + "Print run = " + printRun + "\n")

# ask user if they want to add parameters to search
confirm = "n"

while (confirm == "n" or confirm == "N"):
    userAdditions = input("If you want to add any search parameters then list them all here with a space between each one: ")
    # confirm user selections
    confirm = input("Confirm your search parameter? (y/n): ")

#### variable format tweaking section for url manipulation
# reconstruct user parameters for URL
userAdditions = userAdditions.replace(" ", "+")

# tweak the product set variable for the url because the input is validified
product_set = product_set.replace(" ", "+")

# tweak the parallel COLOR and TYPE variables for the url because the input is validified
parallelColor = parallelColor.replace(" ", "+")
parallelType = parallelType.replace(" ", "+")

# Change isParallel to "-parallel" if == n. Search results are worse for "+parallel"
if isParallel == "n":
    isParallel = "-parallel"
else:
    isParallel = "0"

# Change isGraded to "0" if yes so it will reset, or to a string of excluded grading companies if no.
if isGraded == "n":
    isGraded = gradersString
else:
    isGraded = "0"

# Change parallelColor to exclude the colors if it is still == "n" or if we found a list of colors to exclude
colors_length = len(set_parallel_colors)

if parallelColor == "n" or parallelColor == "0":
    parallelColor = colorsString

# Change parallelColor back to "0" if == "n"
if parallelType == "n":
    parallelType = "0"


###TO DO: change isAuto to "auto" if == y, else switch back to "0"
###

# SPECIAL CHECK: add a "-optic" and "-elite" component to the product_set variable to improve search results.
# it differentiates the "Donruss" search results from the "Donruss Optic" search results.
if(product_set == "Donruss"):
    product_set = "Donruss+-optic+-elite+-clearly"

# set to 0 if the user did not add to the parameters
if (len(userAdditions) < 1):
    userAdditions = 0

# building the url for ebay sold data
url = f'https://www.ebay.com/sch/i.html?_nkw={year}+{product_set}+{first_name}+{last_name}+{userAdditions}+{isGraded}+{isRookie}+{isAuto}+{isParallel}+{parallelType}+{parallelColor}+{isNumbered}+{printRun}&Grade{gradedUrlBit}&_sacat=0&type=s&_dcat=261328&LH_Complete=1&LH_Sold=1&_ipg=240'

# take out all unset values
url = url.replace("+0", "")
print(url)

# open the web url, used some help from ChatGPT. It is harder because the environment is WSL. That is why subprocess was chosen.
subprocess.run(['powershell.exe', 'Start-Process', f'"{url}"'])

# request to download the webpage from the url we made
page = requests.get(url)

# parse the HTML document with bs4
# If this isn't working then a User-Agent header is probably needed
soup = BeautifulSoup(page.text, 'html.parser')

# scraping logic
print('scraping logic')

# arrays to hold the date, titles, and prices. search results holds all the returned listings
sold_dates = []
search_results = []
titles = []
prices = []
shipping = []
total_prices = []

# used to input results into a csv for checking
results_csvformat = []

#####
# there are 4 cases:
# 1. there are enough results that it is less than 240 returned and enough to keep ebay from searching and returning from beyond our parameters
# 2. there are more than 240 results returned and we would want the date for the last result on the first page
# 3. there are not many results so ebay tries finding other results. After a divider, the returned results unfortunately use the same class.
# 4. there are no results
#####

# get the number of search results!!!
results_num = soup.find('div', 'srp-controls__control srp-controls__count').find_next('span', class_='BOLD').text
results_num = int(results_num)    # make it an integer
print(results_num)

# this variable will be used to eliminate a magic number and for some array indexing during card pricing
adjusted_results_num = results_num

# scrape the page depending on the number of results gotten
if results_num > 0 and results_num <= 240:
    scrape_page(sold_dates, titles, prices, shipping, total_prices, search_results, results_num)
elif results_num > 240:
    adjusted_results_num = 240
    scrape_page(sold_dates, titles, prices, shipping, total_prices, search_results, adjusted_results_num)
else:
    print("ERROR: we could not find any sold data for your card, so pricing is not yet supported.")
    exit(1)   # exit if there are no results for the card


### TO-DO: sort your results arrays before outputing to CSV file and pricing below!!!
selection_sort_scraped_results(sold_dates, titles, prices, shipping, total_prices)

# create csv file and add results to it
scrape_results_to_csv(results_csvformat, sold_dates, titles, prices, shipping, total_prices)

# add all the listings minus the last one on the pages into the results array
#search_results = soup.find('div', id='srp-river-results').find('ul', class_='srp-results srp-list clearfix')####.find_all('li', class_='s-item s-item__before-answer s-item__pl-on-bottom')
#soup.find_next('li', attrs={'data-viewport': True})


#### Card Pricing Functionality ####
# date variables for pricing and date object operations
current_date = datetime.date.today()

year_interval = current_date - relativedelta(years=1)
six_month_interval = current_date - relativedelta(months=6)
three_month_interval = current_date - relativedelta(months=3)
month_interval = current_date - relativedelta(months=1)
week_interval = current_date - relativedelta(days=7)
day_interval = current_date - relativedelta(days=1)

# most important intervals
thirty_days_interval = current_date - relativedelta(days=30)
sixty_days_interval = current_date - relativedelta(days=60)

# variable to hold the current price
current_value = 0

# TESTING date format and relative accuracy
print(datetime.datetime.strftime(current_date, '%m-%d-%Y') + " - today")
print(datetime.datetime.strftime(day_interval, '%m-%d-%Y') + " - day ago")
print(datetime.datetime.strftime(week_interval, '%m-%d-%Y') + " - week ago")
print(datetime.datetime.strftime(month_interval, '%m-%d-%Y') + " - month ago")
print(datetime.datetime.strftime(three_month_interval, '%m-%d-%Y') + " - 3 months ago")
print(datetime.datetime.strftime(six_month_interval, '%m-%d-%Y') + " - 6 months ago")
print(datetime.datetime.strftime(year_interval, '%m-%d-%Y') + " - year ago")

# get the endpoints of the range of sold card data gathered (oldest and most recent)
last_sold_date = get_newest_sold_date()
oldest_sold_date = get_oldest_sold_date(sold_dates, adjusted_results_num)

print("sold data range endpoints: ")
print(str(last_sold_date) + " " + str(total_prices[adjusted_results_num - 1]))
print(str(oldest_sold_date) + " " + str(total_prices[0]))

### testing out prices
total_prices_sum = 0

for i in total_prices:
    total_prices_sum += float( i )

# calculate the total average price
total_prices_average = total_prices_sum / adjusted_results_num

# if there are more than 9 items sold then get average price for oldest and newest 5 items sold
if adjusted_results_num > 9:
    temp_adj = adjusted_results_num - 5
    first_five = total_prices[temp_adj:adjusted_results_num]
    last_five = total_prices[0:5]

first_five_sum = 0
for i in first_five:
    first_five_sum += i
    print(i)

first_five_avg = first_five_sum / 5

print("gap")

last_five_sum = 0
for i in last_five:
    last_five_sum += i
    print(i)

last_five_avg = last_five_sum / 5

print("newest five average: " + str(last_five_avg))
print("oldest five average: " + str(first_five_avg))
print("Average total: " + str(total_prices_average))

# my pricing strategy will be to calculate the price based off what I can figure out about the
# sold dates. In order not to bog down the system, I will look at the sold dates data as analytically
# as possible without getting in depth with the details, and figure out where to go with price calculation
# based off what I was able to deduce on the sold dates data.
oldest_sold_date = sold_dates[(len(sold_dates) - 1)]    # get the oldest sold date of an item
newest_sold_date = sold_dates[0]
dt_current_from_oldest = current_date - oldest_sold_date    # timedelta of the amount of days since the oldest sold date

# convert timedelta to integer
current_from_oldest = dt_current_from_oldest.days

print("Oldest sold date: " + str( oldest_sold_date ))
print("Newest sold date: " + str( newest_sold_date ))
print("Days since oldest sold date: " + str( current_from_oldest ))

# counting variables for determining what time intervals the sold items fall into
newest_count = 0
middle_count = 0
oldest_count = 0

# counting variables for the amount of cards sold within a certain amount of days

# count what range the sold items fall into
for i in sold_dates:
    #
    if i >= thirty_days_interval:
        newest_count += 1
    elif i < thirty_days_interval and i >= sixty_days_interval:
        middle_count += 1
    else:
        oldest_count += 1

print("New count: " + str( newest_count ))
print("Mid count: " + str( middle_count ))
print("Old count: " + str( oldest_count ))

# get the average number of cards sold per day
# LIKELY to get skewed from results over 90 days. Not essential to project atm.
avg_sold_per_day = len(sold_dates) / current_from_oldest
print("avg sold per day: " + str( avg_sold_per_day ))

# get the average number of cards sold last 30 days (convert datetime.date to int)
avg_sold_last_thirty = newest_count / (current_date - thirty_days_interval).days
print("avg num sold per day in the last 30 days: " + str( avg_sold_last_thirty ))

# handle pricing differently according to the avg_sold_newest first. The if statements use ratio = (cards sold/every 7 days)
# note, IF the current pricing is underperforming, then next build can use EMA and dig deeper into some of the data
if avg_sold_last_thirty < (1/7):    # 1/7 is one sale a week
    current_value = total_prices[0]
elif avg_sold_last_thirty >= (1/7) and avg_sold_last_thirty <= (3/7):  # interval for 5-12 avg sold in last 30 days
    current_value_sum = total_prices[0] + total_prices[1]

    # using last x amount sold method
    current_value = round((current_value_sum / 2), 2)
elif avg_sold_last_thirty > (3/7) and avg_sold_last_thirty <= (4/7):   # interval for 13-17 avg sold in last 30 days
    current_value_sum = total_prices[0] + total_prices[1] + total_prices[2]

    # using last x amount sold method
    current_value = round((current_value_sum / 3), 2)
elif avg_sold_last_thirty > (4/7) and avg_sold_last_thirty <= (6/7):   # interval for 18-25 avg sold in last 30 days    
    current_value_sum = total_prices[0] + total_prices[1] + total_prices[2] + total_prices[3]

    # using last x amount sold method
    current_value = round((current_value_sum / 4), 2)
elif avg_sold_last_thirty > (6/7) and avg_sold_last_thirty <= (8/7):   # interval for 26-34 avg sold in last 30 days
    current_value_sum = total_prices[0] + total_prices[1] + total_prices[2] + total_prices[3] + total_prices[4]
    
    # using last x amount sold method
    current_value = round((current_value_sum / 5), 2)
elif avg_sold_last_thirty > (8/7) and avg_sold_last_thirty <= (11/7):   # interval for 35-47 avg sold in last 30 days
    # use the last 4 days of sales method
    current_value_sum = 0
    sold_count = sold_in_range(sold_dates, 4, current_date)    # get the number of sold listings
    print("days count for interval: 4 days & " + str(sold_count) + " results")

    # add the values together
    for idx in range(sold_count):
        current_value_sum += total_prices[idx]
    
    current_value = round((current_value_sum / sold_count), 2)
elif avg_sold_last_thirty > (11/7) and avg_sold_last_thirty <= (15/7):   # interval for 48-64 avg sold in last 30 days
    # use the last 3 days of sales method
    current_value_sum = 0
    sold_count = sold_in_range(sold_dates, 3, current_date)    # get the number of sold listings
    print("days count for interval: 3 days & " + str(sold_count) + " results")

    # add the values together
    for idx in range(sold_count):
        current_value_sum += total_prices[idx]
    
    current_value = round((current_value_sum / sold_count), 2)
elif avg_sold_last_thirty > (15/7) and avg_sold_last_thirty * 3 <= 80:   # interval for 65-80 avg sold in last 30 days
    # use the last 2 days of sales method
    current_value_sum = 0
    sold_count = sold_in_range(sold_dates, 2, current_date)    # get the number of sold listings
    print("days count for interval: 2 days & " + str(sold_count) + " results")

    # add the values together
    for idx in range(sold_count):
        current_value_sum += total_prices[idx]
    
    current_value = round((current_value_sum / sold_count), 2)
else:
    # use the last day of sales method
    current_value_sum = 0
    sold_count = sold_in_range(sold_dates, 1, current_date)    # get the number of sold listings
    print("days count for interval: 1 day(s) & " + str(sold_count) + " results")

    # add the values together
    for idx in range(sold_count):
        current_value_sum += total_prices[idx]
    
    current_value = round((current_value_sum / sold_count), 2)

print("Current value: " + str( current_value ))