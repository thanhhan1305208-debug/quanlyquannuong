
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date, time
from urllib.parse import quote

# ==========================================
# 1. CẤU HÌNH
# ==========================================

st.set_page_config(
    page_title="BBQ HOUSE",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "bbq_data.json"

# ==========================================
# 2. DỮ LIỆU THỰC ĐƠN VÀ ẢNH
# ==========================================

MENU = [
    {
        "name": "Ba chỉ bò Mỹ",
        "category": "Thịt bò",
        "price": 129000,
        "description": "Ba chỉ bò Mỹ tươi ngon, mềm và đậm vị",
        "keywords": "korean bbq beef belly grilled beef",
        "emoji": "🥩"
    },
    {
        "name": "Sườn bò nướng",
        "category": "Thịt bò",
        "price": 189000,
        "description": "Sườn bò nướng thơm ngon, đậm đà",
        "keywords": "grilled beef ribs bbq",
        "emoji": "🥩"
    },
    {
        "name": "Lõi vai bò Mỹ",
        "category": "Thịt bò",
        "price": 159000,
        "description": "Lõi vai bò Mỹ mềm ngọt, thích hợp nướng",
        "keywords": "grilled beef steak",
        "emoji": "🥩"
    },
    {
        "name": "Bò cuộn nấm",
        "category": "Thịt bò",
        "price": 99000,
        "description": "Thịt bò cuộn nấm kim châm",
        "keywords": "beef enoki mushroom rolls",
        "emoji": "🥩"
    },
    {
        "name": "Ba chỉ heo nướng",
        "category": "Thịt heo",
        "price": 89000,
        "description": "Ba chỉ heo nướng vàng thơm",
        "keywords": "grilled pork belly bbq",
        "emoji": "🥓"
    },
    {
        "name": "Sườn heo BBQ",
        "category": "Thịt heo",
        "price": 129000,
        "description": "Sườn heo phủ sốt BBQ",
        "keywords": "barbecue pork ribs",
        "emoji": "🍖"
    },
    {
        "name": "Nạc vai heo",
        "category": "Thịt heo",
        "price": 99000,
        "description": "Nạc vai heo tươi ngon dùng để nướng",
        "keywords": "grilled pork shoulder",
        "emoji": "🥓"
    },
    {
        "name": "Tôm sú nướng",
        "category": "Hải sản",
        "price": 149000,
        "description": "Tôm sú nướng thơm ngon",
        "keywords": "grilled tiger prawns",
        "emoji": "🍤"
    },
    {
        "name": "Mực nướng sa tế",
        "category": "Hải sản",
        "price": 139000,
        "description": "Mực nướng phủ sa tế cay thơm",
        "keywords": "grilled squid spicy sauce",
        "emoji": "🦑"
    },
    {
        "name": "Bạch tuộc nướng",
        "category": "Hải sản",
        "price": 159000,
        "description": "Bạch tuộc nướng thơm ngon",
        "keywords": "grilled octopus",
        "emoji": "🐙"
    },
    {
        "name": "Hàu nướng phô mai",
        "category": "Hải sản",
        "price": 99000,
        "description": "Hàu nướng phủ phô mai béo thơm",
        "keywords": "grilled oysters cheese",
        "emoji": "🦪"
    },
    {
        "name": "Nấm kim châm",
        "category": "Rau củ",
        "price": 35000,
        "description": "Nấm kim châm tươi ngon",
        "keywords": "enoki mushrooms",
        "emoji": "🍄"
    },
    {
        "name": "Rau củ tổng hợp",
        "category": "Rau củ",
        "price": 45000,
        "description": "Các loại rau củ tươi dùng để nướng",
        "keywords": "grilled vegetables platter",
        "emoji": "🥗"
    },
    {
        "name": "Kim chi Hàn Quốc",
        "category": "Rau củ",
        "price": 30000,
        "description": "Kim chi Hàn Quốc chua cay",
        "keywords": "korean kimchi",
        "emoji": "🥬"
    },
    {
        "name": "Lẩu Thái hải sản",
        "category": "Lẩu & món nóng",
        "price": 259000,
        "description": "Lẩu Thái chua cay với hải sản",
        "keywords": "thai seafood hot pot",
        "emoji": "🍲"
    },
    {
        "name": "Lẩu kim chi",
        "category": "Lẩu & món nóng",
        "price": 229000,
        "description": "Lẩu kim chi Hàn Quốc nóng hổi",
        "keywords": "korean kimchi hot pot",
        "emoji": "🍲"
    },
    {
        "name": "Cơm chiên hải sản",
        "category": "Lẩu & món nóng",
        "price": 69000,
        "description": "Cơm chiên cùng tôm và hải sản",
        "keywords": "seafood fried rice",
        "emoji": "🍚"
    },
    {
        "name": "Trà đào cam sả",
        "category": "Đồ uống",
        "price": 39000,
        "description": "Trà đào cam sả thanh mát",
        "keywords": "peach orange lemongrass tea",
        "emoji": "🍹"
    },
    {
        "name": "Nước ngọt",
        "category": "Đồ uống",
        "price": 25000,
        "description": "Nước giải khát",
        "keywords": "soft drink cola glass",
        "emoji": "🥤"
    },
    {
        "name": "Nước suối",
        "category": "Đồ uống",
        "price": 15000,
        "description": "Nước suối đóng chai",
        "keywords": "bottled mineral water",
        "emoji": "💧"
    }
]

# ==========================================
# 3. LƯU VÀ ĐỌC DỮ LIỆU
# ==========================================

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return {
        "orders": [],
        "bookings": []
    }


if "database" not in st.session_state:
    st.session_state.database = load_data()

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "customer" not in st.session_state:
    st.session_state.customer = ""

if "table" not in st.session_state:
    st.session_state.table = "Chưa chọn"


def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(
                st.session_state.database,
                f,
                ensure_ascii=False,
                indent=4
            )
    except Exception:
        st.error("Không thể lưu dữ liệu.")


def money(value):
    return f"{value:,.0f}đ".replace(",", ".")


def get_image_url(item):
    keyword = quote(item["keywords"])
    return (
        f"https://loremflickr.com/800/600/{keyword}"
        f"?lock={MENU.index(item) + 101}"
    )


# ==========================================
# 4. GIAO DIỆN
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #111111;
    color: #ffffff;
}
section[data-testid="stSidebar"] {
    background-color: #1b1b1b;
}
h1, h2, h3 {
    color: #ff8c32 !important;
}
p, label, span {
    color: #eeeeee;
}
.menu-card {
    background: #202020;
    border: 1px solid #393939;
    border-radius: 13px;
    padding: 14px;
    margin-bottom: 12px;
}
.price {
    color: #ff8c32;
    font-size: 20px;
    font-weight: bold;
}
.small-text {
    color: #bbbbbb;
    font-size: 13px;
}
div.stButton > button {
    background-color: #e65c16;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: bold;
}
div.stButton > button:hover {
    background-color: #ff8533;
    color: white;
}
hr {
    border-color: #444444;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 5. THANH MENU
# ==========================================

st.sidebar.markdown("# 🔥 BBQ HOUSE")
st.sidebar.caption("GRILL • FOOD • GOOD TIMES")
st.sidebar.divider()

page = st.sidebar.radio(
    "DANH MỤC",
    [
        "🏠 Trang chủ",
        "🍖 Thực đơn",
        "📅 Đặt bàn",
        "🛒 Gọi món",
        "💳 Thanh toán",
        "📋 Quản lý đơn hàng",
        "📊 Thống kê doanh thu"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### 🛒 Giỏ hàng")
st.sidebar.write(f"Số loại món: {len(st.session_state.cart)}")

cart_total = sum(
    item["price"] * item["quantity"]
    for item in st.session_state.cart.values()
)

st.sidebar.markdown(
    f"**Tổng tiền: {money(cart_total)}**"
)

st.sidebar.caption("BBQ HOUSE © 2026")


# ==========================================
# 6. TRANG CHỦ
# ==========================================

if page == "🏠 Trang chủ":

    st.markdown(
        "<h1 style='text-align:center'>🔥 BBQ HOUSE 🔥</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align:center;color:white !important'>"
        "THƯỞNG THỨC HƯƠNG VỊ NƯỚNG TUYỆT HẢO"
        "</h3>",
        unsafe_allow_html=True
    )

    st.image(
        "https://loremflickr.com/1600/650/korean,bbq,grill",
        use_container_width=True
    )

    st.markdown("## Chào mừng đến với BBQ HOUSE")

    st.write(
        "Không gian ẩm thực nướng hấp dẫn, "
        "thực đơn đa dạng với thịt bò, thịt heo, "
        "hải sản và các món lẩu thơm ngon."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Thực đơn", "20 món")

    with col2:
        st.metric("Nhóm món", "6 nhóm")

    with col3:
        st.metric("Phong cách", "BBQ")

    st.divider()

    st.markdown("## ⭐ Món ăn nổi bật")

    featured = [
        MENU[0],
        MENU[9],
        MENU[14]
    ]

    cols = st.columns(3)

    for col, item in zip(cols, featured):
        with col:
            try:
                st.image(get_image_url(item), use_container_width=True)
            except Exception:
                st.markdown(f"# {item['emoji']}")

            st.markdown(f"**{item['name']}**")
            st.markdown(
                f"<div class='price'>{money(item['price'])}</div>",
                unsafe_allow_html=True
            )

    st.info("Hãy vào mục Thực đơn để khám phá tất cả món ăn!")


# ==========================================
# 7. TRANG THỰC ĐƠN
# ==========================================

elif page == "🍖 Thực đơn":

    st.title("🍖 THỰC ĐƠN BBQ HOUSE")
    st.write("Khám phá những món ăn hấp dẫn của chúng tôi.")

    categories = ["Tất cả"] + list(dict.fromkeys(
        item["category"] for item in MENU
    ))

    selected_category = st.selectbox(
        "Chọn nhóm món ăn",
        categories
    )

    search = st.text_input(
        "🔎 Tìm kiếm món ăn",
        placeholder="Nhập tên món..."
    )

    filtered = MENU

    if selected_category != "Tất cả":
        filtered = [
            item for item in filtered
            if item["category"] == selected_category
        ]

    if search:
        filtered = [
            item for item in filtered
            if search.lower() in item["name"].lower()
        ]

    st.write(f"Tìm thấy {len(filtered)} món ăn")

    for start in range(0, len(filtered), 3):
        cols = st.columns(3)

        for col, item in zip(cols, filtered[start:start + 3]):
            with col:
                st.markdown("<div class='menu-card'>",
                            unsafe_allow_html=True)

                try:
                    st.image(
                        get_image_url(item),
                        use_container_width=True
                    )
                except Exception:
                    st.markdown(f"# {item['emoji']}")

                st.markdown(f"### {item['name']}")
                st.caption(item["category"])
                st.write(item["description"])

                st.markdown(
                    f"<div class='price'>{money(item['price'])}</div>",
                    unsafe_allow_html=True
                )

                quantity = st.number_input(
                    "Số lượng",
                    min_value=1,
                    max_value=20,
                    value=1,
                    key=f"menu_qty_{item['name']}"
                )

                if st.button(
                    "➕ Thêm vào giỏ",
                    key=f"menu_add_{item['name']}",
                    use_container_width=True
                ):
                    name = item["name"]

                    if name in st.session_state.cart:
                        st.session_state.cart[name]["quantity"] += quantity
                    else:
                        st.session_state.cart[name] = {
                            "name": name,
                            "price": item["price"],
                            "quantity": quantity
                        }

                    st.success(f"Đã thêm {name} vào giỏ hàng!")

                st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# 8. TRANG ĐẶT BÀN
# ==========================================

elif page == "📅 Đặt bàn":

    st.title("📅 ĐẶT BÀN")
    st.write("Vui lòng điền thông tin để đặt bàn tại BBQ HOUSE.")

    with st.form("booking_form"):

        customer_name = st.text_input("Họ và tên khách hàng")
        phone = st.text_input("Số điện thoại")

        booking_date = st.date_input(
            "Ngày đặt bàn",
            min_value=date.today()
        )

        booking_time = st.time_input(
            "Giờ đặt bàn",
            value=time(18, 0)
        )

        people = st.number_input(
            "Số lượng khách",
            min_value=1,
            max_value=30,
            value=2
        )

        table_type = st.selectbox(
            "Loại bàn",
            ["Bàn 2 người", "Bàn 4 người", "Bàn 6 người", "Bàn gia đình"]
        )

        note = st.text_area("Ghi chú thêm")

        submitted = st.form_submit_button(
            "XÁC NHẬN ĐẶT BÀN",
            use_container_width=True
        )

        if submitted:
            if not customer_name.strip() or not phone.strip():
                st.error("Vui lòng nhập họ tên và số điện thoại.")
            else:
                booking = {
                    "name": customer_name,
                    "phone": phone,
                    "date": str(booking_date),
                    "time": str(booking_time),
                    "people": people,
                    "table": table_type,
                    "note": note,
                    "status": "Chờ xác nhận"
                }

                st.session_state.database["bookings"].append(booking)
                save_data()

                st.success("Đã ghi nhận thông tin đặt bàn!")


# ==========================================
# 9. TRANG GỌI MÓN
# ==========================================

elif page == "🛒 Gọi món":

    st.title("🛒 GỌI MÓN")

    customer = st.text_input(
        "Tên khách hàng",
        value=st.session_state.customer
    )

    table = st.selectbox(
        "Chọn bàn",
        ["Bàn 1", "Bàn 2", "Bàn 3", "Bàn 4",
         "Bàn 5", "Bàn 6", "Mang về"]
    )

    st.session_state.customer = customer
    st.session_state.table = table

    st.divider()

    st.subheader("Chọn món ăn")

    category = st.selectbox(
        "Nhóm món",
        ["Tất cả"] + list(dict.fromkeys(
            item["category"] for item in MENU
        )),
        key="order_category"
    )

    available = MENU if category == "Tất cả" else [
        item for item in MENU
        if item["category"] == category
    ]

    cols = st.columns(2)

    for index, item in enumerate(available):
        with cols[index % 2]:
            st.markdown(f"**{item['name']}**")
            st.caption(money(item["price"]))

            qty = st.number_input(
                f"Số lượng - {item['name']}",
                min_value=0,
                max_value=20,
                value=0,
                key=f"order_{item['name']}"
            )

            if st.button(
                f"Thêm {item['name']}",
                key=f"add_order_{item['name']}"
            ):
                if qty > 0:
                    name = item["name"]

                    if name in st.session_state.cart:
                        st.session_state.cart[name]["quantity"] += qty
                    else:
                        st.session_state.cart[name] = {
                            "name": name,
                            "price": item["price"],
                            "quantity": qty
                        }

                    st.success("Đã thêm món vào giỏ!")

    st.divider()

    st.subheader("Giỏ hàng hiện tại")

    if st.session_state.cart:

        for name, item in list(st.session_state.cart.items()):
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.write(item["name"])

            with col2:
                st.write(f"x{item['quantity']}")

            with col3:
                st.write(money(
                    item["price"] * item["quantity"]
                ))

        st.markdown(
            f"### Tổng cộng: {money(cart_total)}"
        )

        if st.button("🗑️ Xóa toàn bộ giỏ hàng"):
            st.session_state.cart = {}
            st.rerun()

    else:
        st.info("Giỏ hàng đang trống.")


# ==========================================
# 10. TRANG THANH TOÁN
# ==========================================

elif page == "💳 Thanh toán":

    st.title("💳 THANH TOÁN")
    st.write("Kiểm tra hóa đơn trước khi thanh toán.")

    if not st.session_state.cart:
        st.warning("Chưa có món ăn trong giỏ hàng.")
    else:

        customer = st.text_input(
            "Tên khách hàng",
            value=st.session_state.customer
        )

        table = st.text_input(
            "Bàn",
            value=st.session_state.table
        )

        st.divider()

        st.subheader("CHI TIẾT HÓA ĐƠN")

        invoice_data = []

        for item in st.session_state.cart.values():
            subtotal = item["price"] * item["quantity"]

            invoice_data.append({
                "Tên món": item["name"],
                "Đơn giá": item["price"],
                "Số lượng": item["quantity"],
                "Thành tiền": subtotal
            })

        df = pd.DataFrame(invoice_data)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        total = sum(
            item["price"] * item["quantity"]
            for item in st.session_state.cart.values()
        )

        st.markdown(
            f"<h2 style='text-align:right;color:#ff8c32'>"
            f"TỔNG TIỀN: {money(total)}</h2>",
            unsafe_allow_html=True
        )

        payment_method = st.selectbox(
            "Phương thức thanh toán",
            ["Tiền mặt", "Chuyển khoản", "Thẻ ngân hàng"]
        )

        if st.button(
            "XÁC NHẬN THANH TOÁN",
            use_container_width=True
        ):

            if not customer.strip():
                st.error("Vui lòng nhập tên khách hàng.")
            else:
                order = {
                    "id": "BBQ" + datetime.now().strftime("%Y%m%d%H%M%S"),
                    "customer": customer,
                    "table": table,
                    "items": list(st.session_state.cart.values()),
                    "total": total,
                    "payment": payment_method,
                    "status": "Đã thanh toán",
                    "created_at": datetime.now().strftime(
                        "%d/%m/%Y %H:%M:%S"
                    )
                }

                st.session_state.database["orders"].append(order)
                save_data()

                st.session_state.last_invoice = order
                st.session_state.cart = {}
                st.session_state.customer = customer
                st.session_state.table = table

                st.success("Thanh toán thành công!")
                st.rerun()

    # Hiển thị hóa đơn vừa thanh toán
    if "last_invoice" in st.session_state:
        order = st.session_state.last_invoice

        st.divider()
        st.subheader("🧾 HÓA ĐƠN ĐÃ THANH TOÁN")

        st.write("**BBQ HOUSE**")
        st.write(f"Mã hóa đơn: {order['id']}")
        st.write(f"Khách hàng: {order['customer']}")
        st.write(f"Bàn: {order['table']}")
        st.write(f"Thời gian: {order['created_at']}")

        invoice_text = [
            "========== BBQ HOUSE ==========",
            f"Ma hoa don: {order['id']}",
            f"Khach hang: {order['customer']}",
            f"Ban: {order['table']}",
            f"Thoi gian: {order['created_at']}",
            "--------------------------------"
        ]

        for item in order["items"]:
            line = (
                f"{item['name']} x{item['quantity']} "
                f"- {money(item['price'] * item['quantity'])}"
            )
            st.write(line)
            invoice_text.append(line)

        st.markdown(f"### Tổng tiền: {money(order['total'])}")
        st.write(f"Thanh toán: {order['payment']}")
        st.success("Trạng thái: Đã thanh toán")

        invoice_text.extend([
            "--------------------------------",
            f"TONG TIEN: {money(order['total'])}",
            f"Thanh toan: {order['payment']}",
            "Cam on quy khach!"
        ])

        st.download_button(
            "⬇️ TẢI HÓA ĐƠN TXT",
            data="\n".join(invoice_text),
            file_name=f"{order['id']}.txt",
            mime="text/plain",
            use_container_width=True
        )

        csv_data = pd.DataFrame(order["items"]).to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "⬇️ XUẤT CHI TIẾT HÓA ĐƠN CSV",
            data=csv_data,
            file_name=f"{order['id']}.csv",
            mime="text/csv",
            use_container_width=True
        )


# ==========================================
# 11. QUẢN LÝ ĐƠN HÀNG VÀ ĐẶT BÀN
# ==========================================

elif page == "📋 Quản lý đơn hàng":

    st.title("📋 QUẢN LÝ ĐƠN HÀNG")

    orders = st.session_state.database["orders"]

    st.subheader("Danh sách đơn hàng")

    if orders:
        for order in reversed(orders):
            with st.expander(
                f"{order['id']} | {order['customer']} | "
                f"{money(order['total'])}"
            ):
                st.write(f"Khách hàng: {order['customer']}")
                st.write(f"Bàn: {order['table']}")
                st.write(f"Thời gian: {order['created_at']}")
                st.write(f"Thanh toán: {order['payment']}")

                for item in order["items"]:
                    st.write(
                        f"- {item['name']} x{item['quantity']} "
                        f"= {money(item['price'] * item['quantity'])}"
                    )

                st.write(f"**Tổng: {money(order['total'])}**")
                st.success(order["status"])

    else:
        st.info("Chưa có đơn hàng.")

    st.divider()

    st.subheader("Danh sách đặt bàn")

    bookings = st.session_state.database["bookings"]

    if bookings:
        for index, booking in enumerate(bookings):
            with st.expander(
                f"{booking['name']} | {booking['date']} | "
                f"{booking['time']}"
            ):
                st.write(f"Số điện thoại: {booking['phone']}")
                st.write(f"Số khách: {booking['people']}")
                st.write(f"Loại bàn: {booking['table']}")
                st.write(f"Ghi chú: {booking['note']}")

                status = st.selectbox(
                    "Trạng thái đặt bàn",
                    ["Chờ xác nhận", "Đã xác nhận", "Đã hủy"],
                    index=[
                        "Chờ xác nhận",
                        "Đã xác nhận",
                        "Đã hủy"
                    ].index(booking["status"]),
                    key=f"booking_status_{index}"
                )

                if status != booking["status"]:
                    st.session_state.database["bookings"][index]["status"] = status
                    save_data()
                    st.success("Đã cập nhật trạng thái.")
    else:
        st.info("Chưa có thông tin đặt bàn.")


# ==========================================
# 12. THỐNG KÊ DOANH THU
# ==========================================

elif page == "📊 Thống kê doanh thu":

    st.title("📊 THỐNG KÊ DOANH THU")

    orders = [
        order for order in st.session_state.database["orders"]
        if order["status"] == "Đã thanh toán"
    ]

    total_revenue = sum(order["total"] for order in orders)
    total_orders = len(orders)

    total_items = sum(
        item["quantity"]
        for order in orders
        for item in order["items"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Tổng doanh thu", money(total_revenue))
    col2.metric("Đơn đã thanh toán", total_orders)
    col3.metric("Tổng món đã bán", total_items)

    st.divider()

    st.subheader("Doanh thu theo đơn hàng")

    if orders:
        revenue_df = pd.DataFrame([
            {
                "Mã đơn": order["id"],
                "Khách hàng": order["customer"],
                "Ngày": order["created_at"],
                "Doanh thu": order["total"]
            }
            for order in orders
        ])

        st.dataframe(
            revenue_df,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            revenue_df.set_index("Mã đơn")["Doanh thu"]
        )

        st.download_button(
            "⬇️ Xuất báo cáo doanh thu CSV",
            data=revenue_df.to_csv(
                index=False
            ).encode("utf-8-sig"),
            file_name="bao_cao_doanh_thu.csv",
            mime="text/csv"
        )

        st.divider()

        st.subheader("Món ăn bán chạy")

        sales = {}

        for order in orders:
            for item in order["items"]:
                name = item["name"]
                sales[name] = (
                    sales.get(name, 0) + item["quantity"]
                )

        if sales:
            sales_df = pd.DataFrame(
                list(sales.items()),
                columns=["Tên món", "Số lượng đã bán"]
            ).sort_values(
                by="Số lượng đã bán",
                ascending=False
            )

            st.dataframe(
                sales_df,
                use_container_width=True,
                hide_index=True
            )

            st.bar_chart(
                sales_df.set_index("Tên món")
            )

    else:
        st.info(
            "Chưa có dữ liệu doanh thu. "
            "Doanh thu sẽ xuất hiện sau khi có đơn thanh toán."
        )


# ==========================================
# 13. CHÂN TRANG
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        <h3>🔥 BBQ HOUSE 🔥</h3>
        <p>GRILL • FOOD • GOOD TIMES</p>
        <p style="color:#999999;">
            Cảm ơn quý khách đã lựa chọn BBQ HOUSE!
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
