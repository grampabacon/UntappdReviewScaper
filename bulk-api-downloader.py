import requests
import csv
from dateutil import parser
from openpyxl import Workbook
from openpyxl.styles import numbers
import json

client_id = "E509DDCF2ECEBE5E94B0068489C8BFC08767170C"
client_secret = "14601DE3986759204D16392431DCBC6628EE30E9"


# Bits to change per beer
# beer_id = 3734186
# product_handle = "not-huck-the-fazed-double-ipa-8-abv-440ml"
# product_id = "4808167522439"
# product_title = "Accidental - NOT Huck the FazeD - Double IPA - 8% ABV 440ml"

def generate_file(worksheet, product_handle, product_title, untappd_id, product_id):
    beer = requests.get("https://api.untappd.com/v4/beer/checkins/{}?client_id=E509DDCF2ECEBE5E94B0068489C8BFC08767170C&client_secret=14601DE3986759204D16392431DCBC6628EE30E9".format(str(untappd_id)))

    beer_data = beer.json()
    response = beer_data["response"]
    # print(json.dumps(response))
    print(untappd_id)
    checkins = response["checkins"]

    items = checkins["items"]

    # Required rows are: product_handle, state, rating, title, author, email, body, and created_at.
    for item in items:
        if item["rating_score"] == 0:
            continue
        if round(item["rating_score"]) == 0:
            rating = 1

        user = item["user"]

        media = item["media"]
        media_items = media["items"]
        photo_link = ""
        if len(media_items) > 0:
            photos = media_items[0]["photo"]
            photo_link = photos["photo_img_sm"]

        rating = round(item["rating_score"])
        dt_date = parser.parse(item["created_at"])
        date = dt_date.strftime('%Y-%m-%d %H:%M:%S')

        worksheet.append([str(product_id),
                          product_handle,
                          product_title,
                          str(1),
                          str(rating),
                          "Review from Untappd.com",
                          user["first_name"] + " " + user["last_name"],
                          "{}@example.com".format(item["checkin_id"]),
                          str(user["location"]),
                          "Untappd user: {}  - ".format(str(user["user_name"])) + "Rating: {}/5 - ".format(item["rating_score"]) + "Comment: {}".format(item["checkin_comment"]),
                          str(photo_link),
                          str(photo_link),
                          "",
                          str(date),
                          ""])


with open('input.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    line_count = 0

    wb = Workbook()
    ws = wb.active

    ws.append(["product_id",
               "product_handle",
               "product_title",
               "state",
               "rating",
               "title",
               "author",
               "email",
               "location",
               "body",
               "product_image",
               "image",
               "reply",
               "created_at",
               "replied_at"])

    # for row in range(2, 100, 1):
    #     cell = ws.cell(row=row, column=1)
    #     cell.style =

    for row in spamreader:
        if line_count == 0:
            line_count += 1
            continue
        if row[0] == "":
            break
        generate_file(ws, row[0], row[1], row[2], row[3])
        line_count += 1
    wb.save("out/{}.xlsx".format(str("bulk reviews")))
