import requests
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Divar Scraper")
root.geometry("400x300")

# فیلد ورودی شهر
label_city = tk.Label(root, text="نام شهر (id):")
label_city.pack(pady=5)

entry_city = tk.Entry(root)
entry_city.pack(pady=5)

# ناحیه نمایش نتایج
text_result = tk.Text(root, height=10, width=40)
text_result.pack(pady=10)

def Scraper():
    city_id = entry_city.get().strip()
    if not city_id.isdigit():
        messagebox.showerror("خطا", "لطفا کد شهر عددی وارد کنید!")
        return

    url = "https://api.divar.ir/v8/postlist/w/search"

    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "x-render-type": "CSR",
    }

    payload = {
        "city_ids": [city_id],
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

    try:
        res = requests.post(url, headers=headers, json=payload)
        data = res.json()
        
        # نمایش داده در Text
        text_result.delete("1.0", tk.END)
        text_result.insert(tk.END, str(data))
    except Exception as e:
        messagebox.showerror("خطا", f"مشکل در دریافت داده:\n{e}")

# دکمه
btn_scrape = tk.Button(root, text="دریافت آگهی‌ها", command=Scraper)
btn_scrape.pack(pady=10)

root.mainloop()
