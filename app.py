
import streamlit as st
from datetime import datetime
import pandas as pd

# =========================
# CẤU HÌNH WEBSITE
# =========================
st.set_page_config(
    page_title="BBQ HOUSE | Nhà hàng nướng",
    page_icon="🔥",
    layout="wide"
)

# =========================
# GIAO DIỆN CSS
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #111111;
    color: white;
}

header[data-testid="stHeader"] {
    background-color: #111111;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

.hero {
    background: linear-gradient(120deg, #310909, #8f1d0d, #e34b16);
    padding: 38px 25px;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 42px;
    font-weight: 900;
    margin-bottom: 8px;
}

.hero p {
    color: #ffe0d0;
    font-size: 17px;
}

.section-title {
    color: #ff6536;
    font-size: 25px;
    font-weight: 800;
    margin-top: 18px;
    margin-bottom: 12px;
}

.food-card {
    background: #202020;
    border: 1px solid #383838;
    border-radius: 15px;
    padding: 12px;
    margin-bottom: 12px;
}

.food-name {
    color: white;
    font-size: 18px;
    font-weight: 800;
}

.food-desc {
    color: #bbbbbb;
    font-size: 13px;
    min-height: 35px;
}

.food-price {
    color: #ff7043;
    font-size: 19px;
    font-weight: 900;
}

div.stButton > button {
    background: linear-gradient(90deg, #e63e20, #ff7135);
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: bold;
    min-height: 40px;
}

div.stButton > button:hover {
    background: #ff8a50;
    color: white;
    border: none;
}

.cart-box {
    background: #202020;
    border: 1px solid #444444;
    border-radius: 14px;
    padding: 18px;
}

.total-price {
    color: #ff7043;
    font-size: 28px;
    font-weight: 900;
}

.footer {
    text-align: center;
    color: #999999;
    padding: 30px 0 10px 0;
    border-top: 1px solid #333333;
    margin-top: 40px;
}

div[data-testid="stImage"] img {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# DANH SÁCH THỰC ĐƠN
# Giá tính theo một phần
# =========================
menu = [
    # THỊT BÒ
    {
        "name": "Ba chỉ bò Mỹ",
        "category": "Thịt bò",
        "price": 129000,
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947",
        "description": "Ba chỉ bò mềm, thơm ngon."
    },
    {
        "name": "Sườn bò nướng",
        "category": "Thịt bò",
        "price": 189000,
        "image": "https://images.unsplash.com/photo-1558030006-450675393462",
        "description": "Sườn bò đậm vị sốt BBQ."
    },
    {
        "name": "Lõi vai bò Mỹ",
        "category": "Thịt bò",
        "price": 159000,
        "image": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f",
        "description": "Thịt bò mềm, nhiều hương vị."
    },
    {
        "name": "Bò cuộn nấm",
        "category": "Thịt bò",
        "price": 99000,
        "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435",
        "description": "Bò cuộn nấm kim châm."
    },

    # THỊT HEO
    {
        "name": "Ba chỉ heo nướng",
        "category": "Thịt heo",
        "price": 89000,
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947",
        "description": "Ba chỉ heo tươi, nướng thơm."
    },
    {
        "name": "Sườn heo BBQ",
        "category": "Thịt heo",
        "price": 129000,
        "image": "https://images.unsplash.com/photo-1558030006-450675393462",
        "description": "Sườn heo ướp sốt đặc biệt."
    },
    {
        "name": "Nạc vai heo",
        "category": "Thịt heo",
        "price": 99000,
        "image": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f",
        "description": "Nạc vai mềm, đậm đà."
    },

    # HẢI SẢN
    {
        "name": "Tôm sú nướng",
        "category": "Hải sản",
        "price": 149000,
        "image": "https://images.unsplash.com/photo-1559737558-2f5a35f4523b",
        "description": "Tôm sú tươi nướng muối ớt."
    },
    {
        "name": "Mực nướng sa tế",
        "category": "Hải sản",
        "price": 139000,
        "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0",
        "description": "Mực giòn, cay nhẹ sa tế."
    },
    {
        "name": "Bạch tuộc nướng",
        "category": "Hải sản",
        "price": 159000,
        "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435",
        "description": "Bạch tuộc tươi nướng BBQ."
    },
    {
        "name": "Hàu nướng phô mai",
        "category": "Hải sản",
        "price": 99000,
        "image": "https://images.unsplash.com/photo-1559737558-2f5a35f4523b",
        "description": "Hàu nướng béo ngậy."
    },

    # RAU CỦ
    {
        "name": "Nấm kim châm",
        "category": "Rau củ",
        "price": 35000,
        "image": "https://images.unsplash.com/photo-1504545102780-26774c1bb073",
        "description": "Nấm tươi dùng để nướng."
    },
    {
        "name": "Rau củ tổng hợp",
        "category": "Rau củ",
        "price": 45000,
        "image": "https://images.unsplash.com/photo-1540420773420-3366772f4999",
        "description": "Rau củ tươi theo mùa."
    },
    {
        "name": "Kim chi Hàn Quốc",
        "category": "Rau củ",
        "price": 30000,
        "image": "https://images.unsplash.com/photo-1540420773420-3366772f4999",
        "description": "Kim chi chua cay hấp dẫn."
    },

    # LẨU VÀ MÓN NÓNG
    {
        "name": "Lẩu Thái hải sản",
        "category": "Lẩu & món nóng",
        "price": 259000,
        "image": "https://images.unsplash.com/photo-1547592180-85f173990554",
        "description": "Lẩu chua cay, hải sản tươi."
    },
    {
        "name": "Lẩu kim chi",
        "category": "Lẩu & món nóng",
        "price": 229000,
        "image": "https://images.unsplash.com/photo-1547592180-85f173990554",
        "description": "Lẩu kim chi đậm vị Hàn Quốc."
    },
    {
        "name": "Cơm chiên hải sản",
        "category": "Lẩu & món nóng",
        "price": 69000,
        "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19",
        "description": "Cơm chiên nóng, nhiều topping."
    },

    # ĐỒ UỐNG
    {
        "name": "Trà đào cam sả",
        "category": "Đồ uống",
        "price": 39000,
        "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc",
        "description": "Trà đào thơm mát."
    },
    {
        "name": "Nước ngọt",
        "category": "Đồ uống",
        "price": 25000,
        "image": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97",
        "description": "Nước ngọt có gas."
    },
    {
        "name": "Nước suối",
        "category": "Đồ uống",
        "price": 15000,
        "image": "https://images.unsplash.com/photo-1523362628745-0c100150b504",
        "description": "Nước suối đóng chai."
    }
]


# =========================
# KHỞI TẠO DỮ LIỆU
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None

if "customer" not in st.session_state:
    st.session_state.customer = ""

if "table" not in st.session_state:
    st.session_state.table = "1"


def format_money(value):
    return f"{int(value):,}".replace(",", ".") + "đ"


def add_to_cart(item, quantity):
    if quantity <= 0:
        return

    found = False

    for cart_item in st.session_state.cart:
        if cart_item["name"] == item["name"]:
            cart_item["quantity"] += quantity
            found = True
            break

    if not found:
        st.session_state.cart.append({
            "name": item["name"],
            "price": item["price"],
            "quantity": quantity
        })


# =========================
# HEADER
# =========================
st.markdown("""
<div class="hero">
    <h1>🔥 BBQ HOUSE 🔥</h1>
    <p>THE TASTE OF REAL BBQ</p>
    <p>Thưởng thức hương vị nướng tuyệt hảo cùng bạn bè và gia đình</p>
</div>
""", unsafe_allow_html=True)


# =========================
# THÔNG TIN KHÁCH HÀNG
# =========================
st.markdown('<div class="section-title">📋 THÔNG TIN ĐẶT MÓN</div>',
            unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    customer = st.text_input(
        "Tên khách hàng",
        value=st.session_state.customer,
        placeholder="Nhập tên khách hàng"
    )
    st.session_state.customer = customer

with col2:
    table = st.selectbox(
        "Số bàn",
        [str(i) for i in range(1, 21)],
        index=int(st.session_state.table) - 1
    )
    st.session_state.table = table


# =========================
# TÌM KIẾM VÀ LỌC MÓN
# =========================
st.markdown('<div class="section-title">🍖 THỰC ĐƠN BBQ HOUSE</div>',
            unsafe_allow_html=True)

search = st.text_input(
    "🔍 Tìm món ăn",
    placeholder="Nhập tên món bạn muốn tìm..."
)

categories = [
    "Tất cả",
    "Thịt bò",
    "Thịt heo",
    "Hải sản",
    "Rau củ",
    "Lẩu & món nóng",
    "Đồ uống"
]

category = st.selectbox("Chọn danh mục", categories)

filtered_menu = []

for item in menu:
    match_category = (
        category == "Tất cả" or item["category"] == category
    )
    match_search = search.lower() in item["name"].lower()

    if match_category and match_search:
        filtered_menu.append(item)

st.caption(f"Hiện có {len(filtered_menu)} món phù hợp.")

# =========================
# HIỂN THỊ MÓN ĂN
# =========================
if not filtered_menu:
    st.warning("Không tìm thấy món ăn phù hợp.")
else:
    for start in range(0, len(filtered_menu), 2):
        cols = st.columns(2)

        for col, item in zip(cols, filtered_menu[start:start+2]):
            with col:
                st.markdown('<div class="food-card">',
                            unsafe_allow_html=True)

                try:
                    st.image(item["image"], use_container_width=True)
                except Exception:
                    st.info("Hình ảnh món ăn đang được cập nhật.")

                st.markdown(
                    f'<div class="food-name">{item["name"]}</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="food-desc">{item["description"]}</div>',
                    unsafe_allow_html=True
                )

                st.markdown(
                    f'<div class="food-price">{format_money(item["price"])}</div>',
                    unsafe_allow_html=True
                )

                quantity = st.number_input(
                    "Số lượng",
                    min_value=1,
                    max_value=50,
                    value=1,
                    step=1,
                    key="qty_" + item["name"]
                )

                if st.button(
                    "➕ THÊM VÀO GIỎ",
                    key="add_" + item["name"],
                    use_container_width=True
                ):
                    add_to_cart(item, quantity)
                    st.success(f"Đã thêm {item['name']} vào giỏ hàng!")

                st.markdown('</div>', unsafe_allow_html=True)


# =========================
# GIỎ HÀNG
# =========================
st.divider()

st.markdown('<div class="section-title">🛒 GIỎ HÀNG CỦA BẠN</div>',
            unsafe_allow_html=True)

if len(st.session_state.cart) == 0:
    st.info("Giỏ hàng đang trống. Hãy chọn món ăn nhé!")

else:
    total = 0

    for index, item in enumerate(st.session_state.cart):
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

        with col1:
            st.write(f"**{item['name']}**")

        with col2:
            st.write(format_money(item["price"]))

        with col3:
            st.write(f"x {item['quantity']}")

        with col4:
            if st.button("🗑️", key=f"remove_{index}"):
                st.session_state.cart.pop(index)
                st.rerun()

        subtotal = item["price"] * item["quantity"]
        total += subtotal

    st.divider()

    st.markdown(
        f'<div class="total-price">TỔNG TIỀN: {format_money(total)}</div>',
        unsafe_allow_html=True
    )

    if st.button("🧹 XÓA TOÀN BỘ GIỎ HÀNG"):
        st.session_state.cart = []
        st.rerun()

    # =========================
    # THANH TOÁN
    # =========================
    st.markdown('<div class="section-title">💳 THANH TOÁN</div>',
                unsafe_allow_html=True)

    if st.button("✅ XÁC NHẬN THANH TOÁN", use_container_width=True):

        if not customer.strip():
            st.warning("Vui lòng nhập tên khách hàng trước khi thanh toán.")

        elif len(st.session_state.cart) == 0:
            st.warning("Giỏ hàng đang trống.")

        else:
            invoice_total = sum(
                x["price"] * x["quantity"]
                for x in st.session_state.cart
            )

            st.session_state.invoice = {
                "customer": customer,
                "table": table,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "items": [x.copy() for x in st.session_state.cart],
                "total": invoice_total
            }

            st.session_state.cart = []
            st.success("Thanh toán thành công! Hóa đơn đã được tạo.")


# =========================
# HIỂN THỊ HÓA ĐƠN
# =========================
if st.session_state.invoice is not None:

    invoice = st.session_state.invoice

    st.divider()

    st.markdown('<div class="section-title">🧾 HÓA ĐƠN THANH TOÁN</div>',
                unsafe_allow_html=True)

    st.markdown("## 🔥 BBQ HOUSE")
    st.write("Địa chỉ: Nhà hàng BBQ HOUSE")
    st.write("Điện thoại: 0123 456 789")
    st.write(f"Khách hàng: **{invoice['customer']}**")
    st.write(f"Số bàn: **{invoice['table']}**")
    st.write(f"Thời gian: {invoice['date']}")

    invoice_rows = []

    for item in invoice["items"]:
        invoice_rows.append({
            "Tên món": item["name"],
            "Đơn giá": format

