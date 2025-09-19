import requests
import customtkinter as ctk
from tkinter import messagebox
import json


# --- App Setup ---
ctk.set_appearance_mode("dark")   # "light" or "system"
ctk.set_default_color_theme("blue")  # themes: "blue", "green", "dark-blue"

app = ctk.CTk()
app.title("📡 Divar Scraper")
app.geometry("700x500")


# --- Input Frame ---
frame_input = ctk.CTkFrame(app, corner_radius=15)
frame_input.pack(pady=15, padx=15, fill="x")

label_city = ctk.CTkLabel(frame_input, text="🔑 کد شهر (ID):", font=("IRANSans", 14))
label_city.pack(side="left", padx=10, pady=10)

entry_city = ctk.CTkEntry(frame_input, placeholder_text="مثلاً 1", width=120, font=("Consolas", 13))
entry_city.pack(side="left", padx=10, pady=10)

btn_scrape = ctk.CTkButton(frame_input, text="📥 دریافت آگهی‌ها")
btn_scrape.pack(side="right", padx=10, pady=10)


# --- Results Box ---
text_result = ctk.CTkTextbox(app, wrap="word", font=("Consolas", 12))
text_result.pack(padx=15, pady=10, fill="both", expand=True)


# --- Status Bar ---
status_var = ctk.StringVar(value="آماده ✅")
status_bar = ctk.CTkLabel(app, textvariable=status_var, anchor="w", font=("IRANSans", 12))
status_bar.pack(fill="x", padx=10, pady=(0, 10))


def scrape(event=None):
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
        status_var.set("در حال دریافت... ⏳")
        app.update_idletasks()

        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        formatted = json.dumps(data, ensure_ascii=False, indent=2)

        text_result.delete("1.0", "end")
        text_result.insert("end", formatted)

        status_var.set("دریافت شد ✅")

    except Exception as e:
        messagebox.showerror("خطا", f"مشکل:\n{e}")
        status_var.set("❌ خطا")


# --- Bind & Run ---
btn_scrape.configure(command=scrape)
app.bind("<Return>", scrape)

app.mainloop()
