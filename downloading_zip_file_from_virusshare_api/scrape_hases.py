import requests
import csv

url = "https://virusshare.com/hashfiles/unpacked_hashes.md5"
print("Getting all the hasheh.........")
response = requests.get(url)
response = response.text
result = []


response = response.split("\n")
for each in response[1:-2]:
    # print(response)
    try:
        result.append(each.split("  ")[1])
    except Exception as error:
        print(error)
        continue

print("Loading into csv...")
with open('hashes.csv', "w") as file:
    writer = csv.writer(file, dialect='excel')
    for each in result:

        writer.writerow([each])

# hashses = response.text

# print(hashses)
