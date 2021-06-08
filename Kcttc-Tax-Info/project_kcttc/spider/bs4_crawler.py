import requests
import csv
from bs4 import BeautifulSoup
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--tax_number')
    
    args = parser.parse_args()
    result = []
    tax_no_to_search = args.tax_number
    url = "https://www.kcttc.co.kern.ca.us/Payment/ATNSummary.aspx?NUMBER="+str(tax_no_to_search)+"&NUM_TYPE=AT"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table", {"id":"ContentPlaceHolder1_dlSearchResults"})
    anchors = table.find_all("a")
    hrefs = anchors.get("@href")
    for each in hrefs:
        new_link = "https://www.kcttc.co.kern.ca.us/Payment/"+each
        new_page= requests.get(new_link)
        new_soup = BeautifulSoup(new_page.content, 'html.parser')
        total_due = new_soup.find("span",{"id":"ContentPlaceHolder1_lblTotalAmtDue"})
        
        total_amount_due =total_due.get_text() 
        

        result = {
            "number":tax_no_to_search,
            "total_amount_due":total_amount_due


        }
    csv_columns = ["number","total_amount_due"]
    result.append(result)
    csv_file = "tax_information.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in result:
                writer.writerow(data) 
    except IOError:
        print("I/O error")









