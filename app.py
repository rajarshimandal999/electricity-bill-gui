import streamlit as st
import math

st.set_page_config(page_title="Electricity Bill Splitter", layout="centered")

slabs = [(102, 6), (78, 7), (120, 8), (float("inf"), 9)]

def calculate_bill(units):
    original_units = units
    total = 0
    breakdown = []
    for limit, rate in slabs:
        consume = min(units, limit)
        cost = consume * rate
        breakdown.append((consume, rate, cost))
        total += cost
        units -= consume
        if units <= 0:
            break
    return math.ceil(total), breakdown

st.title("🔌 Electricity Bill Calculator & Splitter")

total_units = st.number_input("Enter Total Units Consumed", min_value=0.0, step=0.1, format="%.2f")

with st.form("bill_form"):
    st.subheader("Tenant & Owner Usage Details")

    t1_name = st.text_input("Tenant 1 Name", "Tenant 1")
    t1_units = st.number_input(f"{t1_name} Units Used", min_value=0.0, step=0.1, format="%.2f")

    t2_name = st.text_input("Tenant 2 Name", "Tenant 2")
    t2_units = st.number_input(f"{t2_name} Units Used", min_value=0.0, step=0.1, format="%.2f")

    o_name = st.text_input("Owner Name", "Owner")
    o_units = st.number_input(f"{o_name} Units Used", min_value=0.0, step=0.1, format="%.2f")

    submitted = st.form_submit_button("Calculate Bill")

if submitted:
    used_total = t1_units + t2_units + o_units
    if round(used_total, 2) != round(total_units, 2):
        st.error("⚠️ Total individual usage doesn't match the total consumption. Please correct it.")
    else:
        st.success("✅ Units matched. Here's the breakdown:")
        total_bill = 0
        results = [(t1_name, t1_units), (t2_name, t2_units), (o_name, o_units)]

        for name, units in results:
            total, details = calculate_bill(units)
            st.markdown(f"### {name} — {units:.2f} units")
            for i, (u, r, c) in enumerate(details):
                st.write(f"  Slab {i+1}: {u:.2f} × ₹{r} = ₹{c:.2f}")
            st.write(f"**Total Payable: ₹{total}**")
            st.markdown("---")
            total_bill += total

        st.markdown(f"### 💰 Total Bill (All Members): ₹{total_bill}")
        if o_name.lower() == "you" or st.checkbox("Show Owner Profit Analysis"):
            cost_price, _ = calculate_bill(total_units)
            profit = total_bill - cost_price
            if profit >= 0:
                st.success(f"🎉 Owner Profit: ₹{profit}")
            else:
                st.warning(f"📉 Owner Loss: ₹{-profit}")
