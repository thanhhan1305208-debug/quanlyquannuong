
import streamlit as st
import pandas as pd
import json
import os
import uuid
from datetime import datetime, date, timedelta

# =====================================================
# 1. CẤU HÌNH
# =====================================================

st.set_page_config(
    page_title="BBQ HOUSE | Nhà hàng nướng",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "bbq_data.json"

# =====================================================
# 2. GIAO DIỆN DARK MODE
# =====================================================

st.markdown("""
<style>
.stApp {
    background-color: #101010;
    color: #ffffff;
}
[data-testid="stSidebar"] {
    background-color: #191919;
}
[data-testid="stHeader"] {
    background-color: #101010;
}
h1, h2, h3, h4 {
    color: #ff8c32 !important;
}
p, label, span {
    color: #eeeeee;
}
div.stButton > button {
    background-color: #ff7b22;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: bold;
    min-height: 42px;
}
div.stButton > button:hover {
    background-color: #e65f00;
    color: white;
}
.menu-card {
    background: #202020;
    border: 1px solid #383838;
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 12px;
}
.hero {
    background: linear-gradient(120deg, #301408, #171717);
    padding: 45px 25px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #66320e;
}
.hero h1 {
    font-size: 48px;
    margin-bottom: 8px;
}
.price {
    color: #ff9b45;
    font-size: 21px;
    font-weight: bold;
}
.small-note {
    color: #aaaaaa;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. THỰC ĐƠN VÀ HÌNH ẢNH
# =====================================================

MENU = [
    {"name": "Ba chỉ bò Mỹ", "category": "Thịt bò", "price": 129000,
     "desc": "Ba chỉ bò Mỹ thái lát, mềm và thơm.",
     "image": "https://loremflickr.com/800/600/beef,thin,sliced"},

    {"name": "Bò cuộn nấm kim châm", "category": "Thịt bò", "price": 119000,
     "desc": "Thịt bò cuộn nấm kim châm tươi.",
     "image": "https://loremflickr.com/800/600/beef,enoki,mushroom"},

    {"name": "Dẻ sườn bò Mỹ", "category": "Thịt bò", "price": 159000,
     "desc": "Dẻ sườn bò Mỹ đậm vị BBQ.",
     "image": "https://loremflickr.com/800/600/grilled,beef,ribs"},

    {"name": "Ba chỉ heo", "category": "Thịt heo", "price": 85000,
     "desc": "Ba chỉ heo thái lát dùng để nướng.",
     "image": "https://loremflickr.com/800/600/pork,belly,sliced"},

    {"name": "Sườn heo BBQ", "category": "Thịt heo", "price": 139000,
     "desc": "Sườn heo nướng sốt BBQ.",
     "image": "https://loremflickr.com/800/600/barbecue,pork,ribs"},

    {"name": "Nạc vai heo", "category": "Thịt heo", "price": 89000,
     "desc": "Nạc vai heo tươi ngon.",
     "image": "https://loremflickr.com/800/600/pork,shoulder,grilled"},

    {"name": "Gà nướng mật ong", "category": "Món nướng", "price": 99000,
     "desc": "Gà nướng phủ sốt mật ong.",
     "image": "https://loremflickr.com/800/600/honey,glazed,grilled,chicken"},

    {"name": "Mực nướng sa tế", "category": "Hải sản", "price": 129000,
     "desc": "Mực nướng sa tế cay thơm.",
     "image": "https://loremflickr.com/800/600/grilled,squid"},

    {"name": "Tôm nướng muối ớt", "category": "Hải sản", "price": 139000,
     "desc": "Tôm nướng muối ớt đậm đà.",
     "image": "https://loremflickr.com/800/600/grilled,shrimp"},

    {"name": "Bạch tuộc nướng", "category": "Hải sản", "price": 149000,
     "desc": "Bạch tuộc nướng thơm ngon.",
     "image": "https://loremflickr.com/800/600/grilled,octopus"},

    {"name": "Cá hồi nướng", "category": "Hải sản", "price": 169000,
     "desc": "Cá hồi nướng thơm béo.",
     "image": "https://loremflickr.com/800/600/grilled,salmon,fish"},

    {"name": "Salad trộn", "category": "Món ăn kèm", "price": 45000,
     "desc": "Salad rau củ tươi trộn sốt.",
     "image": "https://loremflickr.com/800/600/fresh,vegetable,salad"},

    {"name": "Kim chi", "category": "Món ăn kèm", "price": 25000,
     "desc": "Kim chi cải thảo Hàn Quốc.",
     "image": "https://loremflickr.com/800/600/korean,kimchi"},

    {"name": "Khoai tây chiên", "category": "Món ăn kèm", "price": 35000,
     "desc": "Khoai tây chiên giòn.",
     "image": "https://loremflickr.com/800/600/french,fries"},

    {"name": "Cơm chiên trứng", "category": "Món ăn kèm", "price": 45000,
     "desc": "Cơm chiên trứng nóng hổi.",
     "image": "https://loremflickr.com/800/600/egg,fried,rice"},

    {"name": "Lẩu kim chi", "category": "Lẩu", "price": 229000,
     "desc": "Lẩu kim chi Hàn Quốc chua cay.",
     "image": "https://loremflickr.com/800/600/korean,kimchi,hotpot"},

    {"name": "Lẩu nấm", "category": "Lẩu", "price": 219000,
     "desc": "Lẩu nấm thanh ngọt với nhiều loại nấm.",
     "image": "https://loremflickr.com/800/600/mushroom,hotpot"},

    {"name": "Coca-Cola", "category": "Đồ uống", "price": 18000,
     "desc": "Nước ngọt Coca-Cola.",
     "image": "https://loremflickr.com/800/600/coca,cola,drink"},

    {"name": "Trà đào", "category": "Đồ uống", "price": 30000,
     "desc": "Trà đào thơm mát.",
     "image": "https://loremflickr.com/800/600/peach,iced,tea"},

    {"name": "Nước suối", "category": "Đồ uống", "price": 12000,
     "desc": "Nước suối đóng chai.",
     "image": "https://loremflickr.com/800/600/bottled,water"}
]

# =====================================================
# 4. LƯU VÀ ĐỌC DỮ LIỆU
# =====================================================

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return (
                    data.get("orders", []),
                    data.get("reservations", [])
                )
        except (json.JSONDecodeError, OSError, TypeError):
            pass
    return [], []


def save_data():
    data = {
        "orders": st.session_state.order_history,
        "reservations": st.session_state.reservations
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# =====================================================
# 5. KHỞI TẠO SESSION STATE
# =====================================================

if "order_history" not in st.session_state:
    orders, reservations = load_data()
    st.session_state.order_history = orders
    st.session_state.reservations = reservations

if "reservations" not in st.session_state:
    st.session_state.reservations = []

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "current_order" not in st.session_state:
    st.session_state.current_order = None

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

if "table_number" not in st.session_state:
    st.session_state.table_number = "Bàn 01"


# =====================================================
# 6. HÀM HỖ TRỢ
# =====================================================

def money(value):
    return f"{int(value):,} VNĐ".replace(",", ".")


def total_cart():
    return sum(
        item["price"] * item["qty"]
        for item in st.session_state.cart.values()
    )


def get_menu_item(name):
    for item in MENU:
        if item["name"] == name:
            return item
    return None


def add_to_cart(item, quantity):
    key = item["name"]

    if key not in st.session_state.cart:
        st.session_state.cart[key] = {
            "name": item["name"],
            "price": item["price"],
            "qty": 0,
            "note": ""
        }

    st.session_state.cart[key]["qty"] += int(quantity)


def make_order():
    if not st.session_state.cart:
        return None

    order_items = [
        {
            "name": item["name"],
            "price": item["price"],
            "qty": item["qty"],
            "note": item.get("note", "")
        }
        for item in st.session_state.cart.values()
    ]

    return {
        "id": str(uuid.uuid4())[:8].upper(),
        "customer": st.session_state.customer_name,
        "table": st.session_state.table_number,
        "items": order_items,
        "total": total_cart(),
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "created_date": date.today().isoformat(),
        "paid": False,
        "payment_method": ""
    }


# =====================================================
# 7. THANH ĐIỀU HƯỚNG
# =====================================================

st.sidebar.markdown("# 🔥 BBQ HOUSE")
st.sidebar.caption("Hương vị nướng tuyệt vời")

page = st.sidebar.radio(
    "MENU CHÍNH",
    [
        "🏠 Trang chủ",
        "🍖 Thực đơn",
        "📅 Đặt bàn",
        "🛒 Order món",
        "💳 Thanh toán",
        "📋 Quản lý",
        "📊 Doanh thu"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### 🕒 Giờ hoạt động")
st.sidebar.write("10:00 - 22:00")
st.sidebar.markdown("### 📞 Liên hệ")
st.sidebar.write("Hotline: 0900 000 000")
st.sidebar.caption("© BBQ HOUSE")


# =====================================================
# 8. TRANG CHỦ
# =====================================================

if page == "🏠 Trang chủ":

    st.markdown("""
    <div class="hero">
        <h1>🔥 BBQ HOUSE 🔥</h1>
        <h3>THE TASTE OF KOREAN BBQ</h3>
        <p>Thưởng thức tinh hoa ẩm thực nướng trong không gian ấm cúng</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🍖 Số món ăn", len(MENU))

    with col2:
        st.metric("📅 Lượt đặt bàn", len(st.session_state.reservations))

    with col3:
        paid_orders = [
            o for o in st.session_state.order_history
            if o.get("paid")
        ]
        st.metric("🧾 Đơn đã thanh toán", len(paid_orders))

    st.divider()
    st.subheader("⭐ MÓN ĂN NỔI BẬT")

    featured = [
        "Ba chỉ bò Mỹ",
        "Bạch tuộc nướng",
        "Lẩu kim chi",
        "Lẩu nấm"
    ]

    cols = st.columns(4)

    for i, name in enumerate(featured):
        item = get_menu_item(name)
        with cols[i]:
            st.image(item["image"], use_container_width=True)
            st.markdown(f"**{item['name']}**")
            st.markdown(
                f"<p class='price'>{money(item['price'])}</p>",
                unsafe_allow_html=True
            )

    st.divider()
    st.subheader("❤️ Vì sao chọn BBQ HOUSE?")
    c1, c2, c3 = st.columns(3)

    c1.markdown("### 🥩")
    c1.write("Nguyên liệu tươi ngon")

    c2.markdown("### 🔥")
    c2.write("Hương vị nướng hấp dẫn")

    c3.markdown("### 🍲")
    c3.write("Thực đơn đa dạng")


# =====================================================
# 9. TRANG THỰC ĐƠN
# =====================================================

elif page == "🍖 Thực đơn":

    st.title("🍖 THỰC ĐƠN BBQ HOUSE")
    st.write("Khám phá các món ăn hấp dẫn của chúng tôi.")

    categories = ["Tất cả"] + sorted(set(
        item["category"] for item in MENU
    ))

    selected_category = st.selectbox(
        "Chọn danh mục",
        categories
    )

    keyword = st.text_input(
        "🔍 Tìm món ăn",
        placeholder="Nhập tên món..."
    )

    filtered = MENU

    if selected_category != "Tất cả":
        filtered = [
            x for x in filtered
            if x["category"] == selected_category
        ]

    if keyword:
        filtered = [
            x for x in filtered
            if keyword.lower() in x["name"].lower()
        ]

    if not filtered:
        st.warning("Không tìm thấy món ăn phù hợp.")

    cols = st.columns(3)

    for index, item in enumerate(filtered):
        with cols[index % 3]:
            with st.container(border=True):
                try:
                    st.image(item["image"], use_container_width=True)
                except Exception:
                    st.markdown("🍽️")

                st.markdown(f"### {item['name']}")
                st.caption(item["category"])
                st.write(item["desc"])
                st.markdown(
                    f"<p class='price'>{money(item['price'])}</p>",
                    unsafe_allow_html=True
                )


# =====================================================
# 10. TRANG ĐẶT BÀN
# =====================================================

elif page == "📅 Đặt bàn":

    st.title("📅 ĐẶT BÀN BBQ HOUSE")
    st.write("Vui lòng điền thông tin để đặt bàn.")

    with st.form("booking_form"):

        name = st.text_input("Tên khách hàng")
        phone = st.text_input("Số điện thoại")

        col1, col2 = st.columns(2)

        with col1:
            booking_date = st.date_input(
                "Ngày đặt bàn",
                min_value=date.today()
            )

        with col2:
            booking_time = st.time_input(
                "Giờ đến"
            )

        people = st.number_input(
            "Số lượng khách",
            min_value=1,
            max_value=30,
            value=2
        )

        table_type = st.selectbox(
            "Loại bàn",
            ["Bàn thường", "Bàn gia đình", "Bàn VIP"]
        )

        note = st.text_area("Ghi chú")

        submit = st.form_submit_button(
            "XÁC NHẬN ĐẶT BÀN",
            use_container_width=True
        )

        if submit:
            if not name.strip() or not phone.strip():
                st.error("Vui lòng nhập tên và số điện thoại.")
            else:
                reservation = {
                    "id": str(uuid.uuid4())[:8].upper(),
                    "name": name.strip(),
                    "phone": phone.strip(),
                    "date": booking_date.isoformat(),
                    "time": booking_time.strftime("%H:%M"),
                    "people": int(people),
                    "table_type": table_type,
                    "note": note,
                    "created_at": datetime.now().strftime(
                        "%d/%m/%Y %H:%M"
                    )
                }

                st.session_state.reservations.append(reservation)
                save_data()

                st.success("Đặt bàn thành công!")
                st.info(f"Mã đặt bàn: {reservation['id']}")


# =====================================================
# 11. TRANG ORDER MÓN
# =====================================================

elif page == "🛒 Order món":

    st.title("🛒 ORDER MÓN ĂN")
    st.write("Chọn món ăn cho khách hàng.")

    col1, col2 = st.columns(2)

    with col1:
        st.session_state.customer_name = st.text_input(
            "Tên khách hàng",
            value=st.session_state.customer_name
        )

    with col2:
        st.session_state.table_number = st.selectbox(
            "Chọn bàn",
            [f"Bàn {i:02d}" for i in range(1, 21)],
            index=(
                int(st.session_state.table_number[-2:]) - 1
                if st.session_state.table_number[-2:].isdigit()
                else 0
            )
        )

    st.divider()

    category = st.selectbox(
        "Danh mục món",
        ["Tất cả"] + sorted(set(
            x["category"] for x in MENU
        ))
    )

    available_items = MENU

    if category != "Tất cả":
        available_items = [
            x for x in MENU
            if x["category"] == category
        ]

    cols = st.columns(2)

    for index, item in enumerate(available_items):

        with cols[index % 2]:
            with st.container(border=True):

                c1, c2 = st.columns([1, 1.5])

                with c1:
                    try:
                        st.image(
                            item["image"],
                            use_container_width=True
                        )
                    except Exception:
                        st.markdown("🍽️")

                with c2:
                    st.markdown(f"### {item['name']}")
                    st.markdown(
                        f"<p class='price'>{money(item['price'])}</p>",
                        unsafe_allow_html=True
                    )

                    qty = st.number_input(
                        "Số lượng",
                        min_value=1,
                        max_value=50,
                        value=1,
                        key=f"qty_{item['name']}"
                    )

                    if st.button(
                        "➕ THÊM MÓN",
                        key=f"add_{item['name']}",
                        use_container_width=True
                    ):
                        add_to_cart(item, qty)
                        st.success(
                            f"Đã thêm {item['name']} vào giỏ hàng!"
                        )

    st.divider()
    st.subheader("🛒 GIỎ HÀNG")

    if st.session_state.cart:

        for key in list(st.session_state.cart.keys()):

            item = st.session_state.cart[key]

            with st.container(border=True):
                c1, c2, c3 = st.columns([2, 1, 1])

                with c1:
                    st.write(f"**{item['name']}**")
                    st.caption(money(item["price"]))

                with c2:
                    new_qty = st.number_input(
                        "Số lượng",
                        min_value=1,
                        max_value=100,
                        value=int(item["qty"]),
                        key=f"cart_qty_{key}"
                    )
                    st.session_state.cart[key]["qty"] = new_qty

                with c3:
                    st.write(
                        money(item["price"] * item["qty"])
                    )

                    if st.button(
                        "🗑️ Xóa",
                        key=f"delete_{key}"
                    ):
                        del st.session_state.cart[key]
                        st.rerun()

                note = st.text_input(
                    "Ghi chú món",
                    value=item.get("note", ""),
                    key=f"note_{key}"
                )
                st.session_state.cart[key]["note"] = note

        st.markdown(
            f"## Tổng cộng: {money(total_cart())}"
        )

        if st.button(
            "XÁC NHẬN ĐƠN HÀNG",
            use_container_width=True
        ):

            if not st.session_state.customer_name.strip():
                st.error("Vui lòng nhập tên khách hàng.")
            else:
                st.session_state.current_order = make_order()

                st.session_state.cart = {}

                st.success("Đã tạo đơn hàng!")
                st.info(
                    f"Mã đơn hàng: "
                    f"{st.session_state.current_order['id']}"
                )
                st.write("Chuyển sang mục Thanh toán để hoàn tất.")

    else:
        st.info("Giỏ hàng hiện chưa có món nào.")


# =====================================================
# 12. TRANG THANH TOÁN
# =====================================================

elif page == "💳 Thanh toán":

    st.title("💳 THANH TOÁN")

    order = st.session_state.current_order

    if order is None:
        st.warning("Chưa có đơn hàng chờ thanh toán.")

    else:

        st.subheader("THÔNG TIN ĐƠN HÀNG")

        st.write(f"**Mã đơn:** {order['id']}")
        st.write(f"**Khách hàng:** {order['customer']}")
        st.write(f"**Bàn:** {order['table']}")
        st.write(f"**Thời gian:** {order['created_at']}")

        st.divider()

        rows = []

        for item in order["items"]:
            rows.append({
                "Tên món": item["name"],
                "Đơn giá": money(item["price"]),
                "Số lượng": item["qty"],
                "Thành tiền": money(
                    item["price"] * item["qty"]
                ),
                "Ghi chú": item.get("note", "")
            })

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

        st.markdown(
            f"# TỔNG THANH TOÁN: {money(order['total'])}"
        )

        method = st.selectbox(
            "Phương thức thanh toán",
            ["Tiền mặt", "Chuyển khoản", "Thẻ ngân hàng"]
        )

        if st.button(
            "XÁC NHẬN ĐÃ THANH TOÁN",
            use_container_width=True
        ):

            order["paid"] = True
            order["payment_method"] = method
            order["paid_at"] = datetime.now().strftime(
                "%d/%m/%Y %H:%M"
            )

            st.session_state.order_history.append(order.copy())

            save_data()

            st.session_state.current_order = None

            st.success("Thanh toán thành công!")
            st.balloons()

        invoice_text = f"""
BBQ HOUSE
HÓA ĐƠN THANH TOÁN

Mã đơn: {order['id']}
Khách hàng: {order['customer']}
Bàn: {order['table']}
Thời gian: {order['created_at']}

CHI TIẾT:
"""

        for item in order["items"]:
            invoice_text += (
                f"\n{item['name']} x {item['qty']}"
                f" = {money(item['price'] * item['qty'])}"
            )

        invoice_text += (
            f"\n\nTỔNG CỘNG: {money(order['total'])}"
        )

        st.download_button(
            "📥 TẢI HÓA ĐƠN TXT",
            data=invoice_text,
            file_name=f"hoadon_{order['id']}.txt",
            mime="text/plain"
        )


# =====================================================
# 13. TRANG QUẢN LÝ
# =====================================================

elif page == "📋 Quản lý":

    st.title("📋 QUẢN LÝ NHÀ HÀNG")

    tab1, tab2 = st.tabs([
        "🧾 Đơn hàng",
        "📅 Đặt bàn"
    ])

    with tab1:

        st.subheader("DANH SÁCH ĐƠN HÀNG")

        if st.session_state.order_history:

            for order in reversed(
                st.session_state.order_history
            ):

                status = (
                    "Đã thanh toán"
                    if order.get("paid")
                    else "Chưa thanh toán"
                )

                with st.expander(
                    f"Đơn {order['id']} | "
                    f"{order['customer']} | "
                    f"{status}"
                ):

                    st.write(f"Bàn: {order['table']}")
                    st.write(f"Ngày: {order['created_at']}")

                    for item in order["items"]:
                        st.write(
                            f"- {item['name']} x {item['qty']}"
                        )

                    st.write(
                        f"**Tổng tiền: {money(order['total'])}**"
                    )

                    if order.get("paid"):
                        st.success(
                            f"Thanh toán: "
                            f"{order.get('payment_method', '')}"
                        )
                    else:
                        st.warning("Đang chờ thanh toán.")

        else:
            st.info("Chưa có đơn hàng.")

    with tab2:

        st.subheader("DANH SÁCH ĐẶT BÀN")

        if st.session_state.reservations:

            df = pd.DataFrame(
                st.session_state.reservations
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("Chưa có thông tin đặt bàn.")


# =====================================================
# 14. TRANG DOANH THU
# =====================================================

elif page == "📊 Doanh thu":

    st.title("📊 THỐNG KÊ DOANH THU")

    paid_orders = [
        order for order in st.session_state.order_history
        if order.get("paid") is True
    ]

    period = st.selectbox(
        "Chọn khoảng thời gian",
        [
            "Hôm nay",
            "7 ngày gần nhất",
            "Tháng này",
            "Năm nay",
            "Tất cả"
        ]
    )

    today = date.today()

    if period == "Hôm nay":
        start_date = today
    elif period == "7 ngày gần nhất":
        start_date = today - timedelta(days=6)
    elif period == "Tháng này":
        start_date = today.replace(day=1)
    elif period == "Năm nay":
        start_date = today.replace(month=1, day=1)
    else:
        start_date = date.min

    filtered_orders = []

    for order in paid_orders:
        try:
            order_date = date.fromisoformat(
                order["created_date"]
            )

            if start_date <= order_date <= today:
                filtered_orders.append(order)

        except (KeyError, ValueError):
            continue

    revenue = sum(
        order["total"] for order in filtered_orders
    )

    number_orders = len(filtered_orders)

    total_items = sum(
        item["qty"]
        for order in filtered_orders
        for item in order["items"]
    )

    average = (
        revenue / number_orders
        if number_orders > 0
        else 0
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric("💰 Tổng doanh thu", money(revenue))
        st.metric("🧾 Số đơn đã thanh toán", number_orders)

    with c2:
        st.metric("🍖 Tổng số món bán ra", total_items)
        st.metric("📈 Giá trị trung bình/đơn", money(average))

    st.divider()
    st.subheader("🔥 MÓN ĂN BÁN CHẠY")

    sold = {}

    for order in filtered_orders:
        for item in order["items"]:
            name = item["name"]
            sold[name] = sold.get(name, 0) + item["qty"]

    if sold:

        best_sellers = pd.DataFrame(
            [
                {"Tên món": name, "Số lượng bán": qty}
                for name, qty in sold.items()
            ]
        ).sort_values(
            "Số lượng bán",
            ascending=False
        )

        st.bar_chart(
            best_sellers.set_index("Tên món")
        )

        st.dataframe(
            best_sellers,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Chưa có dữ liệu bán hàng trong thời gian này.")

    st.divider()
    st.subheader("📋 CHI TIẾT GIAO DỊCH")

    if filtered_orders:

        transaction_rows = []

        for order in filtered_orders:
            transaction_rows.append({
                "Mã đơn": order["id"],
                "Khách hàng": order["customer"],
                "Bàn": order["table"],
                "Ngày": order["created_at"],
                "Tổng tiền": order["total"],
                "Thanh toán": order.get("payment_method", "")
            })

        transaction_df = pd.DataFrame(transaction_rows)

        st.dataframe(
            transaction_df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = transaction_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "📥 XUẤT BÁO CÁO DOANH THU CSV",
            data=csv_data,
            file_name="bao_cao_doanh_thu.csv",
            mime="text/csv"
        )

    else:
        st.info("Không có giao dịch phù hợp.")


# =====================================================
# 15. FOOTER
# =====================================================

st.divider()

st.markdown("""
<div style="text-align:center; padding:20px;">
    <h3>🔥 BBQ HOUSE 🔥</h3>
    <p>Thank you for choosing us!</p>
    <p style="color:#999999;">
        © 2026 BBQ HOUSE - All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)
