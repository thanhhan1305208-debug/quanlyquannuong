

import streamlit as st
import pandas as pd
from datetime import datetime
from html import escape

st.set_page_config(
    page_title="BBQ HOUSE - Nhà hàng nướng",
    page_icon="🔥",
    layout="wide"
)

# =========================
# 1. GIAO DIỆN
# =========================

st.markdown("""
<style>
.stApp {
    background-color: #171717;
    color: white;
}
header {visibility: hidden;}
h1, h2, h3, p, label {
    color: white !important;
}
.hero {
    background: linear-gradient(120deg, #48120e, #171717);
    padding: 35px 25px;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 25px;
    border: 1px solid #713126;
}
.hero h1 {
    color: #ff8b35 !important;
    font-size: 42px;
}
.hero p {
    color: #eeeeee !important;
}
.food-card {
    background: #292929;
    border-radius: 15px;
    padding: 12px;
    border: 1px solid #444;
    margin-bottom: 8px;
}
.price {
    color: #ff9b45;
    font-size: 20px;
    font-weight: bold;
}
div.stButton > button {
    background: #d94127;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: bold;
}
div.stButton > button:hover {
    background: #ff653d;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 2. DỮ LIỆU MÓN ĂN
# =========================

MENU = [
    {
        "name": "Ba chỉ bò Mỹ",
        "category": "Thịt bò",
        "price": 129000,
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947",
        "description": "Thịt bò Mỹ mềm, thơm ngon."
    },
    {
        "name": "Bò cuộn nấm",
        "category": "Thịt bò",
        "price": 99000,
        "image": "https://images.unsplash.com/photo-1558030006-450675393462",
        "description": "Bò cuộn nấm tươi."
    },
    {
        "name": "Ba chỉ heo",
        "category": "Thịt heo",
        "price": 89000,
        "image": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f",
        "description": "Ba chỉ heo tươi ngon."
    },
    {
        "name": "Sườn heo nướng",
        "category": "Thịt heo",
        "price": 109000,
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947",
        "description": "Sườn heo đậm vị BBQ."
    },
    {
        "name": "Đùi gà nướng",
        "category": "Thịt gà",
        "price": 79000,
        "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435",
        "description": "Gà nướng thơm lừng."
    },
    {
        "name": "Tôm nướng",
        "category": "Hải sản",
        "price": 139000,
        "image": "https://images.unsplash.com/photo-1559737558-2f5a35f4523b",
        "description": "Tôm tươi nướng thơm."
    },
    {
        "name": "Mực nướng",
        "category": "Hải sản",
        "price": 129000,
        "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0",
        "description": "Mực nướng hấp dẫn."
    },
    {
        "name": "Nấm kim châm",
        "category": "Rau củ",
        "price": 35000,
        "image": "https://images.unsplash.com/photo-1504545102780-26774c1bb073",
        "description": "Nấm tươi ăn kèm."
    },
    {
        "name": "Rau củ tổng hợp",
        "category": "Rau củ",
        "price": 45000,
        "image": "https://images.unsplash.com/photo-1540420773420-3366772f4999",
        "description": "Rau xanh tươi ngon."
    }
]

SIZE_EXTRA = {
    "Nhỏ": 0,
    "Vừa": 20000,
    "Lớn": 40000
}

SAUCES = [
    "Không",
    "Sốt BBQ",
    "Muối ớt xanh",
    "Sốt tiêu đen",
    "Kim chi",
    "Salad"
]

# =========================
# 3. KHỞI TẠO GIỎ HÀNG
# =========================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None

if "customer" not in st.session_state:
    st.session_state.customer = ""

# =========================
# 4. HEADER
# =========================

st.markdown("""
<div class="hero">
    <h1>🔥 BBQ HOUSE</h1>
    <h3>RESTAURANT & GRILL</h3>
    <p>Thưởng thức hương vị nướng tuyệt hảo</p>
    <p>Fresh Food - Great Taste - Happy Moments</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 🍽️ KHÁM PHÁ THỰC ĐƠN")

# =========================
# 5. THÔNG TIN KHÁCH HÀNG
# =========================

with st.expander("👤 THÔNG TIN KHÁCH HÀNG", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        customer = st.text_input(
            "Tên khách hàng",
            key="customer"
        )

    with col2:
        table = st.number_input(
            "Số bàn",
            min_value=1,
            step=1,
            key="table"
        )

# =========================
# 6. LỌC DANH MỤC
# =========================

categories = [
    "Tất cả",
    "Thịt bò",
    "Thịt heo",
    "Thịt gà",
    "Hải sản",
    "Rau củ"
]

selected_category = st.selectbox(
    "Chọn danh mục món ăn",
    categories
)

filtered_menu = [
    item for item in MENU
    if selected_category == "Tất cả"
    or item["category"] == selected_category
]

# =========================
# 7. HIỂN THỊ MÓN ĂN
# =========================

st.markdown("### 🔥 MENU NHÀ HÀNG")

for i in range(0, len(filtered_menu), 2):
    cols = st.columns(2)

    for col, item in zip(cols, filtered_menu[i:i+2]):
        with col:
            st.markdown('<div class="food-card">', unsafe_allow_html=True)

            st.image(
                item["image"],
                use_container_width=True
            )

            st.markdown(
                f"### {item['name']}"
            )

            st.caption(item["description"])

            st.markdown(
                f'<p class="price">{item["price"]:,.0f} VNĐ</p>',
                unsafe_allow_html=True
            )

            size = st.selectbox(
                "Khẩu phần",
                list(SIZE_EXTRA.keys()),
                key=f"size_{item['name']}"
            )

            sauce = st.selectbox(
                "Nước chấm / Món kèm",
                SAUCES,
                key=f"sauce_{item['name']}"
            )

            qty = st.number_input(
                "Số lượng",
                min_value=1,
                value=1,
                step=1,
                key=f"qty_{item['name']}"
            )

            note = st.text_input(
                "Ghi chú món",
                key=f"note_{item['name']}",
                placeholder="Ví dụ: Không cay..."
            )

            unit_price = item["price"] + SIZE_EXTRA[size]

            if st.button(
                "➕ THÊM VÀO GIỎ",
                key=f"add_{item['name']}",
                use_container_width=True
            ):
                st.session_state.cart.append({
                    "Tên món": item["name"],
                    "Danh mục": item["category"],
                    "Khẩu phần": size,
                    "Nước chấm": sauce,
                    "Số lượng": qty,
                    "Đơn giá": unit_price,
                    "Thành tiền": unit_price * qty,
                    "Ghi chú": note
                })

                st.session_state.invoice = None
                st.success(f"Đã thêm {item['name']}!")

            st.markdown('</div>', unsafe_allow_html=True)

# =========================
# 8. GIỎ HÀNG
# =========================

st.divider()
st.markdown("## 🛒 GIỎ HÀNG CỦA BẠN")

if st.session_state.cart:

    for index, item in enumerate(st.session_state.cart):
        with st.container(border=True):
            col1, col2, col3 = st.columns([4, 2, 1])

            with col1:
                st.markdown(f"**{item['Tên món']}**")
                st.caption(
                    f"{item['Khẩu phần']} | "
                    f"{item['Nước chấm']} | "
                    f"{item['Số lượng']} phần"
                )
                if item["Ghi chú"]:
                    st.caption("Ghi chú: " + item["Ghi chú"])

            with col2:
                st.write(f"{item['Thành tiền']:,.0f} đ")

            with col3:
                if st.button("❌", key=f"remove_{index}"):
                    st.session_state.cart.pop(index)
                    st.session_state.invoice = None
                    st.rerun()

    total = sum(
        item["Thành tiền"]
        for item in st.session_state.cart
    )

    st.markdown(
        f"## 💰 TỔNG CỘNG: {total:,.0f} VNĐ"
    )

    if st.button(
        "💳 THANH TOÁN",
        use_container_width=True
    ):
        if not customer.strip():
            st.error("Vui lòng nhập tên khách hàng!")
        else:
            st.session_state.invoice = {
                "customer": customer,
                "table": table,
                "items": list(st.session_state.cart),
                "total": total,
                "time": datetime.now().strftime(
                    "%d/%m/%Y %H:%M:%S"
                )
            }

else:
    st.info("Giỏ hàng đang trống. Hãy chọn món ăn nhé!")

# =========================
# 9. HÓA ĐƠN
# =========================

if st.session_state.invoice:

    inv = st.session_state.invoice

    st.divider()
    st.markdown("## 🧾 HÓA ĐƠN THANH TOÁN")

    st.markdown("### 🔥 BBQ HOUSE")

    st.write("Khách hàng:", inv["customer"])
    st.write("Số bàn:", inv["table"])
    st.write("Thời gian:", inv["time"])

    bill_df = pd.DataFrame(inv["items"])

    st.dataframe(
        bill_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        f"## TỔNG THANH TOÁN: {inv['total']:,.0f} VNĐ"
    )

    bill_text = f"""
================================
             BBQ HOUSE
          HÓA ĐƠN THANH TOÁN
================================

Khách hàng: {inv['customer']}
Số bàn: {inv['table']}
Thời gian: {inv['time']}

{bill_df.to_string(index=False)}

--------------------------------
TỔNG TIỀN: {inv['total']:,.0f} VNĐ
--------------------------------

       CẢM ƠN QUÝ KHÁCH!
================================
"""

    st.download_button(
        "📥 TẢI HÓA ĐƠN",
        data=bill_text,
        file_name="hoa_don_BBQ_HOUSE.txt",
        mime="text/plain",
        use_container_width=True
    )

    if st.button(
        "🆕 TẠO HÓA ĐƠN MỚI",
        use_container_width=True
    ):
        st.session_state.cart = []
        st.session_state.invoice = None
        st.rerun()

# =========================
# 10. FOOTER
# =========================

st.divider()

st.markdown("""
<div style="text-align:center; padding:20px;">
    <h3 style="color:#ff8b35;">🔥 BBQ HOUSE</h3>
    <p>Thank you for choosing us!</p>
    <p>© 2026 BBQ HOUSE Restaurant</p>
</div>
""", unsafe_allow_html=True)
