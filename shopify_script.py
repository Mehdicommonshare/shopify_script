import pandas as pd
import os, requests, time
from json import JSONDecodeError


def scrape_price(url):
    if "fr135.net" in url:
        url = url
    else:    
        url = url.split("?")[0]

    print(url + ".json")
    while True:
        r = requests.get(url + ".json")
        if "Page temporarily unavailable" in r.text:
            print("Page temporarily unavailable")
            time.sleep(2)
            continue
        break

    try:
        data = r.json()
    except JSONDecodeError:
        print(r.text)
        print("Not Found")
        return "", ""
    
    original_price = data["product"]["variants"][0]["price"]
    discount_price = data["product"]["variants"][0]["compare_at_price"]
    return original_price, discount_price


def main():
    shopify_excel = pd.read_csv('shopify_list.csv')
    shopify_excel = shopify_excel.fillna("")
    data_shopify = shopify_excel.to_dict('records')

    for item in data_shopify:
        new_list = []
        new_dict = item
        orig_price, disc_price = scrape_price(item["Visit URL"])
        if orig_price:
            new_dict["Original Price"] = item["Currency"]  + " " +str(orig_price)
        else:
            new_dict["Original Price"] = ""
        
        if disc_price:
            new_dict["Discount Price"] = item["Currency"]  + " " +str(disc_price)
        else:
            new_dict["Discount Price"] = ""
        new_list.append(new_dict)

        df = pd.DataFrame(new_list)
        if os.path.exists("shopify_results.xlsx"):
            df1 = pd.read_excel("shopify_results.xlsx")
            df2 = pd.concat([df1, df], ignore_index=True)
            df2.to_excel("shopify_results.xlsx", index=False)
        else:
            df.to_excel("shopify_results.xlsx", index=False)

        time.sleep(1)


if __name__ == "__main__":
    print("Program Started\n")
    main()
    print("\nProgram Ended")