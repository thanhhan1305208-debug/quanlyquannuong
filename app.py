
import streamlit as st
import pandas as pd
import json
import os
import uuid
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime, date, timedelta

# ======================================================
# 1. CẤU HÌNH WEBSITE
# ======================================================

st.set_page_config(
    page_title="BBQ HOUSE",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "bbq_data.json"

# ======================================================
# 2. GIAO DIỆN
# ======================================================

st.markdown("""
<style>
.stApp {
    background: #101010;
    color: #ffffff;
}
[data-testid="stSidebar"] {
    background: #1b1b1b;
}
[data-testid="stHeader"] {
    background: #101010;
}
h1, h2, h3, h4 {
    color: #ff8735 !important;
}
p, label, span {
    color: #eeeeee;
}
div.stButton > button {
    background: #f47721;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: bold;
    min-height: 42px;
}
div.stButton > button:hover {
    background: #d95e0b;
    color: white;
}
.hero {
    background: linear-gradient(120deg,#481c08,#171717);
    padding: 55px 20px;
    text-align: center;
    border-radius: 18px;
    border: 1px solid #8d461c;
}
.hero h1 {
    font-size: 48px;
    color: #ff913d !important;
}
.hero p {
    font-size: 17px;
}
.price {
    color: #ff9a45;
    font-size: 21px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# ======================================================
# 3. THỰC ĐƠN 20 MÓN
# ======================================================

MENU = [
    {
        "name": "Ba chỉ bò Mỹ",
        "category": "Thịt bò",
        "price": 129000,
        "desc": "Ba chỉ bò Mỹ thái lát mềm ngon.",
        "image": "https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=900"
    },
    {
        "name": "Bò cuộn nấm kim châm",
        "category": "Thịt bò",
        "price": 119000,
        "desc": "Thịt bò cuộn nấm kim châm.",
        "image": "https://images.unsplash.com/photo-1547592180-85f173990554?w=900"
    },
    {
        "name": "Dẻ sườn bò Mỹ",
        "category": "Thịt bò",
        "price": 159000,
        "desc": "Dẻ sườn bò nướng đậm vị.",
        "image": "https://images.unsplash.com/photo-1558030006-450675393462?w=900"
    },
    {
        "name": "Ba chỉ heo",
        "category": "Thịt heo",
        "price": 85000,
        "desc": "Ba chỉ heo tươi dùng để nướng.",
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947?w=900"
    },
    {
        "name": "Sườn heo BBQ",
        "category": "Thịt heo",
        "price": 139000,
        "desc": "Sườn heo nướng sốt BBQ.",
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947?w=900"
    },
    {
        "name": "Nạc vai heo",
        "category": "Thịt heo",
        "price": 89000,
        "desc": "Nạc vai heo nướng thơm ngon.",
        "image": "https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=900"
    },
    {
        "name": "Gà nướng mật ong",
        "category": "Món nướng",
        "price": 99000,
        "desc": "Gà nướng phủ sốt mật ong.",
        "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=900"
    },
    {
        "name": "Mực nướng sa tế",
        "category": "Hải sản",
        "price": 129000,
        "desc": "Mực nướng sa tế cay thơm.",
        "image": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=900"
    },
    {
        "name": "Tôm nướng muối ớt",
        "category": "Hải sản",
        "price": 139000,
        "desc": "Tôm nướng muối ớt.",
        "image": "https://images.unsplash.com/photo-1559737558-2f5a35f4523b?w=900"
    },
    {
        "name": "Bạch tuộc nướng",
        "category": "Hải sản",
        "price": 149000,
        "desc": "Bạch tuộc nướng thơm ngon.",
        "image": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=900"
    },
    {
        "name": "Cá hồi nướng",
        "category": "Hải sản",
        "price": 169000,
        "desc": "Cá hồi nướng thơm béo.",
        "image": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=900"
    },
    {
        "name": "Salad trộn",
        "category": "Món ăn kèm",
        "price": 45000,
        "desc": "Salad rau củ tươi trộn sốt.",
        "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=900"
    },
    {
        "name": "Kim chi",
        "category": "Món ăn kèm",
        "price": 25000,
        "desc": "Kim chi cải thảo Hàn Quốc.",
        "image": "https://images.unsplash.com/photo-1583224994016-7f4e9b1c6c7a?w=900"
    },
    {
        "name": "Khoai tây chiên",
        "category": "Món ăn kèm",
        "price": 35000,
        "desc": "Khoai tây chiên giòn.",
        "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=900"
    },
    {
        "name": "Cơm chiên trứng",
        "category": "Món ăn kèm",
        "price": 45000,
        "desc": "Cơm chiên trứng nóng hổi.",
        "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=900"
    },
    {
        "name": "Lẩu kim chi",
        "category": "Lẩu",
        "price": 229000,
        "desc": "Lẩu kim chi Hàn Quốc chua cay.",
        "image": "https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43?w=900"
    },
    {
        "name": "Lẩu nấm",
        "category": "Lẩu",
        "price": 219000,
        "desc": "Lẩu nấm thanh ngọt với nhiều loại nấm.",
        "image": "https://images.unsplash.com/photo-1547592180-85f173990554?w=900"
    },
    {
        "name": "Coca-Cola",
        "category": "Đồ uống",
        "price": 18000,
        "desc": "Nước ngọt Coca-Cola.",
        "image": "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=900"
    },
    {
        "name": "Trà đào",
        "category": "Đồ uống",
        "price": 30000,
        "desc": "Trà đào thơm mát.",
        "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=900"
    },
    {
        "name": "Nước suối",
        "category": "Đồ uống",
        "price": 12000,
        "desc": "Nước suối đóng chai.",
        "image": "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=900"
    }
]


# ======================================================
# 4. HÀM TẢI VÀ HIỂN THỊ ẢNH
# ======================================================

@st.cache_data(ttl=3600, show_spinner=False)
def download_image(url):
    response = requests.get(
        url,
        timeout=12,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    response.raise_for_status()

    image = Image.open(BytesIO(response.content))
    image.verify()

    return response.content


def show_food_image(item):
    try:
        image_bytes = download_image(item["image"])
        image = Image.open(BytesIO(image_bytes))
        st.image(
            image,
            caption=item["name"],
            use_container_width=True
        )
    except Exception:
        st.markdown(
            f"""
            <div style="
                background:#252525;
                height:180px;
                display:flex;
                flex-direction:column;
                justify-content:center;
                align-items:center;
                border-radius:12px;
                border:1px solid #444;
                text-align:center;
            ">
                <div style="font-size:45px">🍽️</div>
                <div style="color:#ff913d;font-weight:bold">
                    {item['name']}
                </div>
                <div style="color:#aaaaaa;font-size:12px">
                    Ảnh chưa tải được
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ======================================================
# 5. DỮ LIỆU
# ======================================================

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                return (
                    data.get("orders", []),
                    data.get("reservations", [])
                )
        except (OSError, ValueError, TypeError):
            pass

    return [], []


def save_data():
    data = {
        "orders": st.session_state.order_history,
        "reservations": st.session_state.reservations
    }

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# ======================================================
# 6. KHỞI TẠO SESSION
# ======================================================

if "order_history" not in st.session_state:
    old_orders, old_reservations = load_data()
    st.session_state.order_history = old_orders
    st.session_state.reservations = old_reservations

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


# ======================================================
# 7. HÀM HỖ TRỢ
# ======================================================

def money(value):
    return f"{int(value):,}".replace(",", ".") + " VNĐ"


def get_item(name):
    return next(
        (item for item in MENU if item["name"] == name),
        None
    )


def cart_total():
    return sum(
        item["price"] * item["qty"]
        for item in st.session_state.cart.values()
    )


def add_to_cart(item, qty):
    key = item["name"]

    if key not in st.session_state.cart:
        st.session_state.cart[key] = {
            "name": item["name"],
            "price": item["price"],
            "qty": 0,
            "note": ""
        }

    st.session_state.cart[key]["qty"] += int(qty)


def create_order():
    if not st.session_state.cart:
        return None

    items = [
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
        "items": items,
        "total": cart_total(),
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "created_date": date.today().isoformat(),
        "paid": False,
        "payment_method": ""
    }


# ======================================================
# 8. THANH ĐIỀU HƯỚNG
# ======================================================

st.sidebar.markdown("# 🔥 BBQ HOUSE")
st.sidebar.caption("THE TASTE OF KOREAN BBQ")
st.sidebar.divider()

page = st.sidebar.radio(
    "DANH MỤC",
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
st.sidebar.write("🕒 10:00 - 22:00")
st.sidebar.write("📞 0900 000 000")
st.sidebar.caption("© 2026 BBQ HOUSE")


# ======================================================
# 9. TRANG CHỦ
# ======================================================

if page == "🏠 Trang chủ":

    st.markdown("""
    <div class="hero">
        <h1>🔥 BBQ HOUSE 🔥</h1>
        <h3>THE TASTE OF KOREAN BBQ</h3>
        <p>Thưởng thức tinh hoa ẩm thực nướng</p>
        <p>Không gian ấm cúng - Món ăn hấp dẫn</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    paid_orders = [
        o for o in st.session_state.order_history
        if o.get("paid") is True
    ]

    c1, c2, c3 = st.columns(3)

    c1.metric("🍖 Tổng số món", len(MENU))
    c2.metric("📅 Đặt bàn", len(st.session_state.reservations))
    c3.metric("🧾 Đơn đã thanh toán", len(paid_orders))

    st.divider()
    st.subheader("⭐ MÓN ĂN NỔI BẬT")

    featured_names = [
        "Ba chỉ bò Mỹ",
        "Bạch tuộc nướng",
        "Lẩu kim chi",
        "Lẩu nấm"
    ]

    cols = st.columns(4)

    for i, name in enumerate(featured_names):
        item = get_item(name)

        with cols[i]:
            show_food_image(item)
            st.markdown(f"**{item['name']}**")
            st.markdown(
                f"<div class='price'>{money(item['price'])}</div>",
                unsafe_allow_html=True
            )

    st.divider()
    st.subheader("❤️ TRẢI NGHIỆM BBQ HOUSE")

    a, b, c = st.columns(3)

    a.markdown("### 🥩")
    a.write("Nguyên liệu tươi ngon")

    b.markdown("### 🔥")
    b.write("Hương vị nướng hấp dẫn")

    c.markdown("### 🍲")
    c.write("Thực đơn đa dạng")


# ======================================================
# 10. TRANG THỰC ĐƠN
# ======================================================

elif page == "🍖 Thực đơn":

    st.title("🍖 THỰC ĐƠN BBQ HOUSE")
    st.write("Khám phá những món ăn hấp dẫn.")

    categories = ["Tất cả"] + sorted(
        set(item["category"] for item in MENU)
    )

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
        st.warning("Không tìm thấy món ăn.")

    cols = st.columns(3)

    for i, item in enumerate(filtered):

        with cols[i % 3]:
            with st.container(border=True):

                show_food_image(item)

                st.markdown(f"### {item['name']}")
                st.caption(item["category"])
                st.write(item["desc"])

                st.markdown(
                    f"<div class='price'>{money(item['price'])}</div>",
                    unsafe_allow_html=True
                )


# ======================================================
# 11. TRANG ĐẶT BÀN
# ======================================================

elif page == "📅 Đặt bàn":

    st.title("📅 ĐẶT BÀN BBQ HOUSE")
    st.write("Điền thông tin để đặt bàn.")

    with st.form("booking_form"):

        name = st.text_input("Tên khách hàng")
        phone = st.text_input("Số điện thoại")

        c1, c2 = st.columns(2)

        with c1:
            booking_date = st.date_input(
                "Ngày đặt bàn",
                min_value=date.today()
            )

        with c2:
            booking_time = st.time_input("Giờ đến")

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

                st.success("ĐẶT BÀN THÀNH CÔNG!")
                st.write("Mã đặt bàn:", reservation["id"])


# ======================================================
# 12. TRANG ORDER MÓN
# ======================================================

elif page == "🛒 Order món":

    st.title("🛒 ORDER MÓN ĂN")

    c1, c2 = st.columns(2)

    with c1:
        st.session_state.customer_name = st.text_input(
            "Tên khách hàng",
            value=st.session_state.customer_name
        )

    with c2:
        table_options = [
            f"Bàn {i:02d}" for i in range(1, 21)
        ]

        current_index = (
            table_options.index(st.session_state.table_number)
            if st.session_state.table_number in table_options
            else 0
        )

        st.session_state.table_number = st.selectbox(
            "Chọn bàn",
            table_options,
            index=current_index
        )

    st.divider()

    category = st.selectbox(
        "Danh mục món",
        ["Tất cả"] + sorted(
            set(x["category"] for x in MENU)
        ),
        key="order_category"
    )

    available = MENU

    if category != "Tất cả":
        available = [
            x for x in MENU
            if x["category"] == category
        ]

    cols = st.columns(2)

    for i, item in enumerate(available):

        with cols[i % 2]:

            with st.container(border=True):

                show_food_image(item)

                st.markdown(f"### {item['name']}")

                st.markdown(
                    f"<div class='price'>{money(item['price'])}</div>",
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
                    "➕ THÊM VÀO GIỎ",
                    key=f"add_{item['name']}",
                    use_container_width=True
                ):
                    add_to_cart(item, qty)
                    st.success("Đã thêm món vào giỏ hàng!")
                    st.rerun()

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
            f"## TỔNG CỘNG: {money(cart_total())}"
        )

        if st.button(
            "XÁC NHẬN ĐƠN HÀNG",
            use_container_width=True
        ):

            if not st.session_state.customer_name.strip():
                st.error("Vui lòng nhập tên khách hàng.")

            elif st.session_state.current_order is not None:
                st.warning(
                    "Bạn còn đơn hàng chờ thanh toán. "
                    "Hãy thanh toán đơn cũ trước."
                )

            else:
                st.session_state.current_order = create_order()
                st.session_state.cart = {}

                st.success("TẠO ĐƠN HÀNG THÀNH CÔNG!")
                st.info(
                    "Mã đơn: " +
                    st.session_state.current_order["id"]
                )
                st.info("Vào mục Thanh toán để hoàn tất.")

    else:
        st.info("Giỏ hàng đang trống.")


# ======================================================
# 13. TRANG THANH TOÁN
# ======================================================

elif page == "💳 Thanh toán":

    st.title("💳 THANH TOÁN")

    order = st.session_state.current_order

    if order is None:

        st.warning("Chưa có đơn hàng chờ thanh toán.")

    else:

        st.subheader("THÔNG TIN HÓA ĐƠN")

        st.write("Mã đơn:", order["id"])
        st.write("Khách hàng:", order["customer"])
        st.write("Bàn:", order["table"])
        st.write("Thời gian:", order["created_at"])

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
            f"# TỔNG TIỀN: {money(order['total'])}"
        )

        method = st.selectbox(
            "Phương thức thanh toán",
            ["Tiền mặt", "Chuyển khoản", "Thẻ ngân hàng"]
        )

        invoice = f"""
BBQ HOUSE
HÓA ĐƠN THANH TOÁN

Mã đơn: {order['id']}
Khách hàng: {order['customer']}
Bàn: {order['table']}
Thời gian: {order['created_at']}

CHI TIẾT MÓN:
"""

        for item in order["items"]:
            invoice += (
                f"\n{item['name']} x {item['qty']}"
                f" = {money(item['price'] * item['qty'])}"
            )

        invoice += f"\n\nTỔNG CỘNG: {money(order['total'])}"

        st.download_button(
            "📥 TẢI HÓA ĐƠN",
            data=invoice,
            file_name=f"hoadon_{order['id']}.txt",
            mime="text/plain"
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

            st.session_state.order_history.append(
                order.copy()
            )

            save_data()

            st.session_state.current_order = None

            st.success("THANH TOÁN THÀNH CÔNG!")
            st.balloons()
            st.rerun()


# ======================================================
# 14. TRANG QUẢN LÝ
# ======================================================

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
                    f"{order['id']} | {order['customer']} | {status}"
                ):

                    st.write("Bàn:", order["table"])
                    st.write("Thời gian:", order["created_at"])

                    for item in order["items"]:
                        st.write(
                            f"- {item['name']} x {item['qty']}"
                        )

                    st.write(
                        "Tổng tiền:",
                        money(order["total"])
                    )

                    if order.get("paid"):
                        st.success(
                            order.get("payment_method", "")
                        )
                    else:
                        st.warning("Chưa thanh toán.")

        else:
            st.info("Chưa có đơn hàng.")

    with tab2:

        st.subheader("DANH SÁCH ĐẶT BÀN")

        if st.session_state.reservations:

            reservation_df = pd.DataFrame(
                st.session_state.reservations
            )

            st.dataframe(
                reservation_df,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info("Chưa có thông tin đặt bàn.")


# ======================================================
# 15. TRANG DOANH THU
# ======================================================

elif page == "📊 Doanh thu":

    st.title("📊 THỐNG KÊ DOANH THU")

    paid_orders = [
        order for order in st.session_state.order_history
        if order.get("paid") is True
    ]

    period = st.selectbox(
        "Chọn thời gian",
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
        order["total"]
        for order in filtered_orders
    )

    order_count = len(filtered_orders)

    item_count = sum(
        item["qty"]
        for order in filtered_orders
        for item in order["items"]
    )

    average = (
        revenue / order_count
        if order_count
        else 0
    )

    c1, c2 = st.columns(2)

    c1.metric("💰 Tổng doanh thu", money(revenue))
    c1.metric("🧾 Đơn đã thanh toán", order_count)

    c2.metric("🍖 Số món bán ra", item_count)
    c2.metric("📈 Trung bình mỗi đơn", money(average))

    st.divider()
    st.subheader("🔥 MÓN ĂN BÁN CHẠY")

    sold = {}

    for order in filtered_orders:
        for item in order["items"]:
            name = item["name"]
            sold[name] = sold.get(name, 0) + item["qty"]

    if sold:

        best_sellers = pd.DataFrame([
            {
                "Tên món": name,
                "Số lượng bán": quantity
            }
            for name, quantity in sold.items()
        ])

        best_sellers = best_sellers.sort_values(
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
        st.info("Chưa có dữ liệu bán hàng.")

    st.divider()
    st.subheader("📋 CHI TIẾT GIAO DỊCH")

    if filtered_orders:

        transactions = []

        for order in filtered_orders:

            transactions.append({
                "Mã đơn": order["id"],
                "Khách hàng": order["customer"],
                "Bàn": order["table"],
                "Thời gian": order["created_at"],
                "Tổng tiền": order["total"],
                "Thanh toán": order.get(
                    "payment_method", ""
                )
            })

        transaction_df = pd.DataFrame(transactions)

        st.dataframe(
            transaction_df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = transaction_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "📥 XUẤT BÁO CÁO CSV",
            data=csv_data,
            file_name="bao_cao_doanh_thu.csv",
            mime="text/csv"
        )

    else:
        st.info("Không có giao dịch trong thời gian này.")


# ======================================================
# 16. FOOTER
# ======================================================

st.divider()

st.markdown("""
<div style="text-align:center;padding:20px">
    <h3>🔥 BBQ HOUSE 🔥</h3>
    <p>THE TASTE OF KOREAN BBQ</p>
    <p style="color:#999">
        Thank you for choosing us!
    </p>
    <p style="color:#777;font-size:12px">
        © 2026 BBQ HOUSE - All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)
