import requests
from bs4 import BeautifulSoup
from datetime import datetime
import sys

# source URL: brightdata.com/blog/how-tos/how-to-scrape-ebay-in-python
# Author: Riley Osborne

# list of product sets currently supported in the web scraping script
SUPPORTED_SETS = ["Donruss", "Donruss Optic", "Prizm", "Panini Prizm", "Score", "Mosaic", "Chronicles", "Panini Chronicles",
                   "Phoenix", "Torque", "Panini Torque", "Contenders", "Panini Contenders"]
 
# The grading companies array and url string have been replaced by the superior "&Grade"" url piece
#######                   
## list of card grading companies. List will be used for narrowing seaches excluding graded cards and searches including specific grading companies
#GRADING_COMPANIES = ["CSG", "PSA", "BGS", "SGC", "HGA"]               

## string to be used for search queries excluding graded cards
#gradersString = ""

## create final version of gradersString for URL
#for i in GRADING_COMPANIES:
# gradersString = gradersString + "-" + i + "+"

## take off the extra "+" at the end of the string    
#gradersString = gradersString[0:-1]
#######
    

# functions
# print the supported sets
def print_set_products():
    print("\nSupported sets: ")
    for i in SUPPORTED_SETS:
        print(i + ", ")

# get the current year for user input validation
currentYear = datetime.now().year

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

# tweak the product set variable for the url once the input is validified
product_set = product_set.replace(" ", "+")

# SPECIAL CHECK: add a "-optic" and "-elite" component to the product_set variable to improve search results.
# it differentiates the "Donruss" search results from the "Donruss Optic" search results.
if(product_set == "Donruss"):
    product_set = "Donruss+-optic+-elite"

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



# other detailed variables to implement later
isAuto = "0"
isParallel = "0"
parallelColor = "0"
isNumbered = "0"
printRun = "0"

# ask if the card is a parallel


# get the card's parallel color and type if user input is yes


# if no then add colors to exclude from the url


# verify all information before scraping???

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

# reconstruct user parameters for URL
userAdditions = userAdditions.replace(" ", "+")

# set to 0 if the user did not add to the parameters
if (len(userAdditions) < 1):
    userAdditions = 0

# building the url for ebay sold data
url = f'https://www.ebay.com/sch/i.html?_nkw={year}+{product_set}+{first_name}+{last_name}+{userAdditions}+{isRookie}+{isAuto}+{isParallel}+{parallelColor}+{isNumbered}+{printRun}&Grade{gradedUrlBit}&_sacat=0&type=s&_dcat=261328&LH_Complete=1&LH_Sold=1&_ipg=240'

# take out all unset values
url = url.replace("+0", "")
print(url)


# request to download the webpage from the url we made
page = requests.get(url)

# parse the HTML document with bs4
# If this isn't working then a User-Agent header is probably needed
soup = BeautifulSoup(page.text, 'html.parser')

# scraping logic
print('scraping logic')

# arrays to hold the titles and prices. search results holds all the returned listings
search_results = []
titles = []
prices = []

#####
# there are 4 cases:
# 1. there are enough results that it is less than 240 returned and enough to keep ebay from searching and returning from beyond our parameters
# 2. there are more than 240 results returned and we would want the date for the last result on the first page
# 3. there are not many results so ebay tries finding other results. After a divider, the returned results unfortunately use the same class.
# 4. there are no results
#####

# get the number of search results!!!
results_num = soup.find('div', 'srp-controls__control srp-controls__count').find_next('span', class_='BOLD').text
print(results_num)

if results_num > 0 and results_num <= 240:
    search_results = soup.find('ul', class_='srp-results srp-list clearfix').find_all('li')
    #for 
# add all the listings minus the last one on the pages into the results array
#search_results = soup.find('div', id='srp-river-results').find('ul', class_='srp-results srp-list clearfix')####.find_all('li', class_='s-item s-item__before-answer s-item__pl-on-bottom')
soup.find_next('li', attrs={'data-viewport': True})

# this line gets the last listing on the page