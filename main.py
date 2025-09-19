import requests
import tkinter as tk
from tkinter import messagebox, scrolledtext
import json

# --- Setup main window ---
root = tk.Tk()
root.title("Divar Scraper")
root.geometry("500x400")

# --- City input field ---
label_city = tk.Label(root, text="نام شهر (ID عددی):")
label_city.pack(pady=5)

entry_city = tk.Entry(root, justify="center")
entry_city.pack(pady=5)

# --- Results display (scrollable, read-only) ---
text_result = scrolledtext.ScrolledText(root, height=15, width=60, state="disabled")
text_result.pack(pady=10)


def scrape():
    """Fetch ads data from Divar API based on city ID."""
    city_id = entry_city.get().strip()

    if not city_id.isdigit():
        messagebox.showerror("خطا", "لطفاً کد شهر را به‌صورت عددی وارد کنید.")
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
            "page": 1,
        },
        "search_data": {
            "form_data": {
                "data": {
                    "category": {"str": {"value": "ROOT"}}
                }
            }
        },
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Pretty-print JSON result
        formatted = json.dumps(data, ensure_ascii=False, indent=2)

        # Update result box
        text_result.config(state="normal")
        text_result.delete("1.0", tk.END)
        text_result.insert(tk.END, formatted)
        text_result.config(state="disabled")

    except requests.exceptions.RequestException as net_err:
        messagebox.showerror("خطای شبکه", f"ارتباط برقرار نشد:\n{net_err}")
    except ValueError:
        messagebox.showerror("خطا", "فرمت داده دریافتی معتبر نیست.")
    except Exception as e:
        messagebox.showerror("خطا", f"مشکل غیرمنتظره:\n{e}")


# --- Button ---
btn_scrape = tk.Button(root, text="دریافت آگهی‌ها", command=scrape)
btn_scrape.pack(pady=10)

# --- Run the app ---
root.mainloop()
