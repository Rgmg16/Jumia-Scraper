import requests
# Checking the permission to scrap
# jumia = 'https://www.jumia.co.ke/'

# Check the robots.txt file
# robots_url = jumia + 'robots.txt'
# response = requests.get(robots_url)

# if response.status_code == 200:
#     robots_content = response.text
#     print("robots.txt file found. Content:")
#     print(robots_content)
    
#     # Check if the robots.txt file disallows web scraping
#     if 'User-agent: *' in robots_content and 'Disallow: /' in robots_content:
#         print("Web scraping is not allowed.")
#     else:
#         print("Web scraping is allowed.")
# else:
#     print("robots.txt file not found. Proceed with caution.")

# Web scraping from the anniversaries page
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Jumia anniversary tab (you need to replace this with the actual URL)
jumia = 'https://www.jumia.co.ke/mlp-anniversary/'

# Send a request to fetch the webpage content
response = requests.get(jumia)
response.raise_for_status()  # Check if the request was successful

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the container holding the product items
products = soup.find_all('article', class_='prd _fb col c-prd')

# Lists to hold the data
product_names = []
brand_names = []
prices = []
discounts = []
reviews_count = []
ratings = []

# Loop through each product and extract the required information
for product in products:
    # Extract product name
    product_name = product.find('h3', class_='name').text.strip()
    product_names.append(product_name)

    # Extract brand name
    brand_name = product.find('a', class_='brand').text.strip() if product.find('a', class_='brand') else 'N/A'
    brand_names.append(brand_name)

    # Extract price
    price = product.find('div', class_='prc').text.strip().replace('KSh ', '').replace(',', '')
    prices.append(price)

    # Extract discount
    discount = product.find('div', class_='bdg _dsct _sm').text.strip().replace('%', '') if product.find('div', class_='bdg _dsct _sm') else '0'
    discounts.append(discount)

    # Extract total number of reviews
    reviews = product.find('div', class_='rev').text.strip() if product.find('div', class_='rev') else '0'
    reviews_count.append(reviews)

    # Extract product rating
    rating = product.find('div', class_='stars _s').text.strip() if product.find('div', class_='stars _s') else '0'
    ratings.append(rating)

# Create a DataFrame using the extracted data
data = {
    'Product Name': product_names,
    'Brand Name': brand_names,
    'Price (Ksh)': prices,
    'Discount (%)': discounts,
    'Total Number of Reviews': reviews_count,
    'Product Rating (out of 5)': ratings
}

df = pd.DataFrame(data)

# Print the DataFrame
print(df)

# Optionally, save the DataFrame to a CSV file
df.to_csv('jumia_anniversary_products.csv', index=False)
