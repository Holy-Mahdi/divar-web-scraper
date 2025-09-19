import requests
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json


# --- Setup main window ---
root = tk.Tk()
root.title("📡 Divar Scraper")
root.geometry("600x500")
root.minsize(500, 400)

# Use ttk style (modern look)
style = ttk.Style()
style.theme_use("clam")  # you can try "vista", "alt", "default" too

# --- Frame for inputs ---
frame_input = ttk.Frame(root, padding=10)
frame_input.pack(fill="x")

label_city = ttk.Label(frame_input, text="نام شهر (ID عددی):", font=("IRANSans", 11))
label_city.grid(row=0, column=0, sticky="w", padx=5)

entry_city = ttk.Entry(frame_input, justify="center", width=20, font=("Consolas", 11))
entry_city.grid(row=0, column=1, padx=5)

btn_scrape = ttk.Button(frame_input, text="🔍 دریافت آگهی‌ها")
btn_scrape.grid(row=0, column=2, padx=10)


# --- Results area ---
frame_result = ttk.LabelFrame(root, text="نتایج", padding=10)
frame_result.pack(fill="both", expand=True, padx=10, pady=10)

text_result = scrolledtext.ScrolledText(
    frame_result,
    wrap="word",
    font=("Consolas", 10),
    state="disabled",
    relief="flat",
    borderwidth=0,
)
text_result.pack(fill="both", expand=True)


# --- Status bar ---
status_var = tk.StringVar(value="آماده ✅")
status_bar = ttk.Label(root, textvariable=status_var, anchor="w", relief="flat")
status_bar.pack(fill="x", side="bottom", padx=5, pady=3)


def scrape(*args):
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
            "form_data": {"data": {"category": {"str": {"value": "ROOT"}}}},
        },
    }

    try:
        # Show status + loading cursor
        status_var.set("در حال دریافت داده‌ها ... ⏳")
        root.config(cursor="watch")
        root.update_idletasks()

        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        formatted = json.dumps(data, ensure_ascii=False, indent=2)

        text_result.config(state="normal")
        text_result.delete("1.0", tk.END)
        text_result.insert(tk.END, formatted)
        text_result.config(state="disabled")

        status_var.set("دریافت شد ✅")

    except requests.exceptions.RequestException as net_err:
        messagebox.showerror("خطای شبکه", f"ارتباط برقرار نشد:\n{net_err}")
        status_var.set("خطای شبکه ❌")
    except ValueError:
        messagebox.showerror("خطا", "فرمت داده دریافتی معتبر نیست.")
        status_var.set("خطا در داده ❌")
    except Exception as e:
        messagebox.showerror("خطا", f"مشکل غیرمنتظره:\n{e}")
        status_var.set("خطای ناشناخته ❌")
    finally:
        root.config(cursor="")  # reset cursor


# --- Bind actions ---
btn_scrape.config(command=scrape)
root.bind("<Return>", scrape)  # Press Enter to search


# --- Run the app ---
root.mainloop()
