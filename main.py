import requests
import customtkinter as ctk
from tkinter import messagebox


# --- Setup ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("📡 دیوار - جستجوگر آگهی‌ها")
app.geometry("800x650")


# --- Input Section ---
frame_input = ctk.CTkFrame(app, corner_radius=15)
frame_input.pack(pady=15, padx=15, fill="x")

label_city = ctk.CTkLabel(frame_input, text="🔑 کد شهر:", font=("Tahoma", 14), anchor="e")
label_city.pack(side="right", padx=10, pady=10)

entry_city = ctk.CTkEntry(frame_input, placeholder_text="مثلاً 1", width=100, justify="right")
entry_city.pack(side="right", padx=10, pady=10)

label_query = ctk.CTkLabel(frame_input, text="🔍 عبارت جستجو:", font=("Tahoma", 14), anchor="e")
label_query.pack(side="right", padx=10, pady=10)

entry_query = ctk.CTkEntry(frame_input, placeholder_text="مثلاً مانتو، مبل، لپ‌تاپ ...", width=200, justify="right")
entry_query.pack(side="right", padx=10, pady=10)

btn_scrape = ctk.CTkButton(frame_input, text="📥 جستجو")
btn_scrape.pack(side="left", padx=10, pady=10)


# --- Results Section (scrollable frame) ---
canvas = ctk.CTkCanvas(app, bg="#1a1a1a", highlightthickness=0)
scrollbar = ctk.CTkScrollbar(app, orientation="vertical", command=canvas.yview)
scroll_frame = ctk.CTkFrame(canvas)

scroll_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=10)
scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=10)


# --- Status Bar ---
status_var = ctk.StringVar(value="آماده ✅")
status_bar = ctk.CTkLabel(app, textvariable=status_var, anchor="e", font=("Tahoma", 12))
status_bar.pack(fill="x", padx=15, pady=(0, 10))


def display_posts(data, query=""):
    """Show posts as nice cards in scroll_frame with RTL."""
    for widget in scroll_frame.winfo_children():
        widget.destroy()

    posts = [w["data"] for w in data.get("list_widgets", []) if w["widget_type"] == "POST_ROW"]

    # --- Filtering ---
    if query:
        query = query.strip()
        posts = [p for p in posts if query in p.get("title", "") or query in p.get("middle_description_text", "")]

    if not posts:
        ctk.CTkLabel(scroll_frame, text="❌ هیچ آگهی‌ای یافت نشد", font=("Tahoma", 13)).pack(pady=20)
        return

    for post in posts:
        title = post.get("title", "بدون عنوان")
        price = post.get("middle_description_text", "نامشخص")
        location = post.get("action", {}).get("payload", {}).get("web_info", {}).get("district_persian", "")
        city = post.get("action", {}).get("payload", {}).get("web_info", {}).get("city_persian", "")
        desc_top = post.get("top_description_text", "")
        desc_bottom = post.get("bottom_description_text", "")

        card = ctk.CTkFrame(scroll_frame, corner_radius=12, fg_color="#2a2a2a")
        card.pack(fill="x", pady=6, padx=10)

        lbl_title = ctk.CTkLabel(card, text=f"🛒 {title}", font=("Tahoma", 13, "bold"), anchor="e")
        lbl_title.pack(fill="x", padx=10, pady=(8, 0))

        lbl_price = ctk.CTkLabel(card, text=f"💵 {price}", font=("Tahoma", 12), anchor="e", text_color="#00ff99")
        lbl_price.pack(fill="x", padx=10)

        lbl_location = ctk.CTkLabel(card, text=f"📍 {city} - {location}", font=("Tahoma", 11), anchor="e")
        lbl_location.pack(fill="x", padx=10)

        if desc_top:
            lbl_top = ctk.CTkLabel(card, text=f"📌 {desc_top}", font=("Tahoma", 11), anchor="e", text_color="#ffcc00")
            lbl_top.pack(fill="x", padx=10)

        if desc_bottom:
            lbl_bottom = ctk.CTkLabel(card, text=f"⏰ {desc_bottom}", font=("Tahoma", 10), anchor="e", text_color="#cccccc")
            lbl_bottom.pack(fill="x", padx=10, pady=(0, 8))


def scrape(event=None):
    city_id = entry_city.get().strip()
    query = entry_query.get().strip()

    if not city_id.isdigit():
        messagebox.showerror("خطا", "کد شهر باید عددی باشد.")
        return

    url = "https://api.divar.ir/v8/postlist/w/search"
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "x-render-type": "CSR",
    }
    payload = {
        "city_ids": [city_id],
        "pagination_data": {"@type": "type.googleapis.com/post_list.PaginationData", "page": 1},
        "search_data": {"form_data": {"data": {"category": {"str": {"value": "ROOT"}}}}},
    }

    try:
        status_var.set("⏳ در حال دریافت ...")
        app.update_idletasks()

        res = requests.post(url, headers=headers, json=payload, timeout=10)
        res.raise_for_status()
        data = res.json()

        display_posts(data, query)
        status_var.set("✅ دریافت شد")

    except Exception as e:
        messagebox.showerror("خطا", f"مشکل:\n{e}")
        status_var.set("❌ خطا")


btn_scrape.configure(command=scrape)
app.bind("<Return>", scrape)

app.mainloop()
