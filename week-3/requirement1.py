import json
import urllib.request as request
import csv

src = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"
with request.urlopen(src) as response:
    dataset = json.load(response)
    dataset = dataset["result"]["results"]

with open("data.csv", mode="w") as file:
    # get csv writer
    writer = csv.writer(file)
    
    # access every data, and save data's attribute.
    # Finally, use writerrow() to write data.
    for data in dataset:
        stitle = data["stitle"]
        address = data["address"][5:8]
        longitude = data["longitude"]
        latitude = data["latitude"]
        file = data["file"].lower().split(".jpg")[0] + ".jpg"  # for get first url.
        writer.writerow([stitle, address, longitude, latitude, file])
