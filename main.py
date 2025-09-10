import requests

import tkinter as tk

root = tk.Tk()
root.title("Divar Scraper")


url = "https://api.divar.ir/v8/postlist/w/search"

headers ={
    "accept" : "application/json, text/plain, */*",
    "content-type" : "application/json",
    "x-render-type" : "CSR",
}

payload = {
    "city_ids": ["3"], 
    "pagination_data": {
        "@type": "type.googleapis.com/post_list.PaginationData",
        "page": 1
    },
    "search_data": {
        "form_data": {
            "data": {
                "category": {"str": {"value": "ROOT"}}
            }
        }
    }
}

res = requests.post(url,headers = headers,json=payload)
data = res.json()

print(data)
