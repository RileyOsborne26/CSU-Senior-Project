####################
# by Riley Osborne #
####################
Instructions for the web scraper script:
To run, use the command
    python scraper.py
in order to skip some of the user interaction use these optional command line arguments as outlined below:
    python scraper.py [year] [product_set] [first_name] [last_name] [is_rookie]

[year]: replace with the year the card was manufactured. It is usually on the back of the card around the bottom.
[product_set]: replace with the name of the product set. Please enclose the product set name within double quotation marks " ".
    Additionally, if the entire product_set's name is not capitalized or spelled correctly then it will not be recognized.
[first_name]: enter the athlete's first name
[last_name]: enter the athlete's last name
[is_rookie]: if the card is a rookie card then enter "rookie" for this arguments

example command with arguments: 
    python scraper.py 2017 "Panini Prizm" Patrick Mahomes rookie
