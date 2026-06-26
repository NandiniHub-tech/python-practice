# app.py
# streamlit run c:/Users/Anjal/Desktop/qrcode_bill/dilip_sir_bill.py
import streamlit as st
import pandas as pd
import qrcode
from io import BytesIO
from datetime import datetime

# Page Config
st.set_page_config(page_title="Cafe Billing System", page_icon="☕", layout="wide")

# Session State
if "total_amount" not in st.session_state:
    st.session_state.total_amount = 0

if "bill_items" not in st.session_state:
    st.session_state.bill_items = []

if "final_amount" not in st.session_state:
    st.session_state.final_amount = 0

# Header
st.title("Cafe Billing System")
st.subheader("☕ Anjali Cafe")
st.write("Date & Time:", datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

st.divider()

# Menu Mapping (same menu as original code)
menu_options = {
    "Poha": 1,
    "Idli": 2,
    "Dosa": 3,
    "Cold Coffee": 4,
    "Sandwich": 5
}

col1, col2 = st.columns(2)

with col1:
    item = st.selectbox(
        "Select Item",
        list(menu_options.keys())
    )

with col2:
    qty = st.number_input(
        "Enter Quantity",
        min_value=1,
        step=1
    )

# Add Item Button
if st.button("Add Item"):

    ch = menu_options[item]
    rate = 0

    # ORIGINAL LOGIC PRESERVED
    if ch == 1:
        rate = 20
    elif ch == 2:
        rate = 30
    elif ch == 3:
        rate = 40
    elif ch == 4:
        rate = 50
    elif ch == 5:
        rate = 60

    # ORIGINAL DISCOUNT LOGIC
    if qty >= 10 and qty <= 20:
        rate = rate - 1
        cur_total = rate * qty
        st.session_state.total_amount += cur_total

    elif qty > 20:
        rate = rate - (rate / 100) * 5
        cur_total = rate * qty
        st.session_state.total_amount += cur_total

    else:
        cur_total = rate * qty
        st.session_state.total_amount += cur_total

    st.session_state.bill_items.append({
        "Item Name": item,
        "Quantity": qty,
        "Rate": round(rate, 2),
        "Amount": round(cur_total, 2)
    })

    st.success(f"{item} added successfully!")

st.divider()

# Bill Table
st.subheader("Bill Details")

if st.session_state.bill_items:
    df = pd.DataFrame(st.session_state.bill_items)
    st.table(df)

st.info(f"Running Total Amount: ₹ {st.session_state.total_amount:.2f}")

st.divider()

# Final Bill
if st.button("Generate Final Bill"):

    total_amount = st.session_state.total_amount

    # ORIGINAL EXIT LOGIC PRESERVED
    if total_amount > 2000:
        dis = (total_amount / 100) * 10
        total_amount = total_amount - dis

    r = total_amount % 10

    if r <= 5:
        total_amount = total_amount - r
    else:
        total_amount = (total_amount - r) + 10

    st.session_state.final_amount = total_amount

    st.success(f"Final Amount: ₹ {total_amount:.2f}")

st.divider()

# QR Code Generation
if st.button("Generate QR Code"):

    total_amount = st.session_state.final_amount

    if total_amount == 0:
        st.warning("Please generate final bill first.")
    else:

        upi_id = "9171431426@axl"
        name = "Anjali_pal"

        # ORIGINAL QR LOGIC PRESERVED
        link = f"upi://pay?pa={upi_id}&pn={name}&am={total_amount}&cu=INR"

        qr = qrcode.make(link)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        st.image(
            buffer.getvalue(),
            caption=f"Pay ₹{total_amount:.2f}",
            width=300
        )

        # st.code(link)

st.divider()

# Reset Button
if st.button("Reset Bill"):
    st.session_state.total_amount = 0
    st.session_state.bill_items = []
    st.session_state.final_amount = 0
    st.success("Bill Reset Successfully")

