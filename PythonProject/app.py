import requests
from bs4 import BeautifulSoup

products_to_track = [
    {
        "product_url": "https://www.amazon.in/Samsung-Galaxy-Ocean-Blue-Storage/dp/B07HGJKDQL?tag=coa_in-21",
        "name": "Samsung M31",
        "target_price": 16000
    },
    {
        "product_url": "https://www.amazon.in/Test-Exclusive-668/dp/B07HGH88GL",
        "name": "Samsung M21 6GB 128RAM",
        "target_price": 16000
    },
    {
        "product_url": "https://www.amazon.in/Test-Exclusive-553/dp/B0784D7NFQ",
        "name": "Redmi Note 9 Pro",
        "target_price": 17000
    },
    {
        "product_url": "https://www.amazon.in/Oneplus-Celadon-Marble-128Gb-Storage/dp/B0CX58MTNN",
        "name": "OnePlus Nord CE4",
        "target_price": 20000
    },
    {
        "product_url": "https://www.amazon.in/Himalayan-Storage-Additional-Exchange-Offers/dp/B07WHPLH6D",
        "name": "vivo Y58 5G",
        "target_price": 17000
    }
]

def give_product_price(URL):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    try:
        page = requests.get(URL, headers=headers, timeout=10)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Try multiple price selectors
        product_price = soup.find(id="priceblock_dealprice")
        if product_price is None:
            product_price = soup.find(id="priceblock_ourprice")
        if product_price is None:
            product_price = soup.find("span", class_="a-price-whole")  # fallback

        if product_price:
            return product_price.get_text(strip=True)
        else:
            return None
    except Exception as e:
        print(f"Failed to get price from URL {URL} due to: {e}")
        return None

# Use 'with' to auto-close the file
with open('my_result_file.txt', 'w', encoding='utf-8') as result_file:
    for product in products_to_track:
        product_price_str = give_product_price(product["product_url"])

        if product_price_str:
            print(f"{product_price_str} - {product['name']}")
            # Remove currency symbols and commas
            price_num = ''.join(filter(str.isdigit, product_price_str))
            try:
                my_product_price = int(price_num)
            except ValueError:
                print(f"Could not convert price '{product_price_str}' to integer.")
                continue

            print(my_product_price)
            if my_product_price < product["target_price"]:
                print("Available at your required price")
                result_file.write(
                    f"{product['name']} - \t Available at Target Price. Current Price - ₹{my_product_price}\n"
                )
            else:
                print("Still at current price")
        else:
            print(f"Could not fetch price for {product['name']}")
