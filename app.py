
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Quản lý quán nướng",
    page_icon="🔥",
    layout="wide"
)

st.title("🔥 QUẢN LÝ QUÁN NƯỚNG")
st.subheader("Ứng dụng gọi món và thanh toán hóa đơn")

MENU = {
    "Thịt bò": {
        "Ba chỉ bò Mỹ": 129000,
        "Bò cuộn nấm": 99000,
        "Bắp bò": 119000
    },
    "Thịt heo": {
        "Ba chỉ heo": 89000,
        "Sườn heo": 109000,
        "Nạc vai heo": 95000
    },
    "Thịt gà": {
        "Đùi gà": 79000,
        "Cánh gà": 85000
    },
    "Hải sản": {
        "Tôm nướng": 139000,
        "Mực nướng": 129000,
        "Bạch tuộc": 119000
    },
    "Rau củ": {
        "Nấm kim châm": 35000,
        "Đậu bắp": 30000,
        "Bắp Mỹ": 35000
    }
}

SIZE_PRICE = {
    "Nhỏ": 0,
    "Vừa": 20000,
    "Lớn": 40000
}

if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None

st.header("1. Thông tin khách hàng")

col1, col2 = st.columns(2)

with col1:
    customer = st.text_input("Tên khách hàng")

with col2:
    table_number = st.number_input(
        "Số bàn", min_value=1, step=1
    )

st.divider()
st.header("2. Chọn món ăn")

category = st.selectbox(
    "Loại món nướng",
    list(MENU.keys())
)

food = st.selectbox(
    "Tên món ăn",
    list(MENU[category].keys())
)

col1, col2 = st.columns(2)

with col1:
    size = st.selectbox(
        "Khẩu phần",
        list(SIZE_PRICE.keys())
    )

with col2:
    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        value=1,
        step=1
    )

sauce = st.selectbox(
    "Nước chấm / Món ăn kèm",
    ["Không", "Sốt BBQ", "Muối ớt xanh",
     "Kim chi", "Salad", "Rau ăn kèm"]
)

note = st.text_input("Ghi chú riêng cho món")

unit_price = MENU[category][food] + SIZE_PRICE[size]
total_item = unit_price * quantity

st.info(
    f"Đơn giá: {unit_price:,.0f} VNĐ | "
    f"Thành tiền: {total_item:,.0f} VNĐ"
)

if st.button("➕ Thêm món vào hóa đơn"):
    st.session_state.cart.append({
        "Tên món": food,
        "Danh mục": category,
        "Khẩu phần": size,
        "Món kèm": sauce,
        "Số lượng": quantity,
        "Đơn giá": unit_price,
        "Thành tiền": total_item,
        "Ghi chú": note
    })
    st.session_state.invoice = None
    st.success("Đã thêm món thành công!")

st.divider()
st.header("3. Danh sách món đã chọn")

if st.session_state.cart:
    df = pd.DataFrame(st.session_state.cart)
    st.dataframe(df, use_container_width=True)

    total = sum(
        item["Thành tiền"]
        for item in st.session_state.cart
    )

    st.subheader(f"Tổng tiền: {total:,.0f} VNĐ")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ Xóa toàn bộ món"):
            st.session_state.cart = []
            st.session_state.invoice = None
            st.rerun()

    with col2:
        if st.button("💳 THANH TOÁN"):
            if not customer.strip():
                st.error("Vui lòng nhập tên khách hàng!")
            else:
                st.session_state.invoice = {
                    "customer": customer,
                    "table": table_number,
                    "items": list(st.session_state.cart),
                    "total": total,
                    "time": datetime.now().strftime(
                        "%d/%m/%Y %H:%M:%S"
                    )
                }

else:
    st.info("Chưa có món ăn nào được chọn.")

if st.session_state.invoice:
    inv = st.session_state.invoice

    st.divider()
    st.header("🧾 HÓA ĐƠN THANH TOÁN")

    st.write(f"Khách hàng: {inv['customer']}")
    st.write(f"Số bàn: {inv['table']}")
    st.write(f"Thời gian: {inv['time']}")

    bill = pd.DataFrame(inv["items"])
    st.dataframe(bill, use_container_width=True)

    st.subheader(f"TỔNG THANH TOÁN: {inv['total']:,.0f} VNĐ")

    bill_text = f"""
QUÁN NƯỚNG
HÓA ĐƠN THANH TOÁN
Khách hàng: {inv['customer']}
Số bàn: {inv['table']}
Thời gian: {inv['time']}

{bill.to_string(index=False)}

TỔNG TIỀN: {inv['total']:,.0f} VNĐ
Cảm ơn quý khách!
"""

    st.download_button(
        "📥 TẢI HÓA ĐƠN",
        data=bill_text,
        file_name="hoa_don_quan_nuong.txt",
        mime="text/plain"
    )

