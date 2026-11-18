
import streamlit as st
import pandas as pd
import requests
import json
import os
from datetime import datetime, date, time
from urllib.parse import quote

# =====================================================
# 1. CẤU HÌNH
# =====================================================

st.set_page_config(
    page_title="BBQ HOUSE",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "bbq_data.json"

# =====================================================
# 2. THỰC ĐƠN 20 MÓN
# =====================================================

MENU = [
    {"name": "Ba chỉ bò Mỹ", "category": "Thịt bò", "price": 129000,
     "description": "Ba chỉ bò Mỹ mềm ngon, đậm vị."},

    {"name": "Sườn bò nướng", "category": "Thịt bò", "price": 189000,
     "description": "Sườn bò nướng thơm lừng."},

    {"name": "Lõi vai bò Mỹ", "category": "Thịt bò", "price": 159000,
     "description": "Lõi vai bò Mỹ tươi ngon."},

    {"name": "Bò cuộn nấm", "category": "Thịt bò", "price": 99000,
     "description": "Thịt bò cuộn nấm kim châm."},

    {"name": "Ba chỉ heo nướng", "category": "Thịt heo", "price": 89000,
     "description": "Ba chỉ heo nướng vàng thơm."},

    {"name": "Sườn heo BBQ", "category": "Thịt heo", "price": 129000,
     "description": "Sườn heo nướng sốt BBQ."},

    {"name": "Nạc vai heo", "category": "Thịt heo", "price": 99000,
     "description": "Nạc vai heo tươi dùng để nướng."},

    {"name": "Tôm sú nướng", "category": "Hải sản", "price": 149000,
     "description": "Tôm sú nướng thơm ngon."},

    {"name": "Mực nướng sa tế", "category": "Hải sản", "price": 139000,
     "description": "Mực nướng sa tế cay thơm."},

    {"name": "Bạch tuộc nướng", "category": "Hải sản", "price": 159000,
     "description": "Bạch tuộc nướng thơm ngon."},

    {"name": "Hàu nướng phô mai", "category": "Hải sản", "price": 99000,
     "description": "Hàu nướng phô mai béo thơm."},

    {"name": "Nấm kim châm", "category": "Rau củ", "price": 35000,
     "description": "Nấm kim châm tươi ngon."},

    {"name": "Rau củ tổng hợp", "category": "Rau củ", "price": 45000,
     "description": "Các loại rau củ tươi ngon."},

    {"name": "Kim chi Hàn Quốc", "category": "Rau củ", "price": 30000,
     "description": "Kim chi Hàn Quốc chua cay."},

    {"name": "Lẩu Thái hải sản", "category": "Lẩu & món nóng", "price": 259000,
     "description": "Lẩu Thái chua cay hải sản."},

    {"name": "Lẩu kim chi", "category": "Lẩu & món nóng", "price": 229000,
     "description": "Lẩu kim chi Hàn Quốc nóng hổi."},

    {"name": "Cơm chiên hải sản", "category": "Lẩu & món nóng", "price": 69000,
     "description": "Cơm chiên cùng tôm và hải sản."},

    {"name": "Trà đào cam sả", "category": "Đồ uống", "price": 39000,
     "description": "Trà đào cam sả thanh mát."},

    {"name": "Nước ngọt", "category": "Đồ uống", "price": 25000,
     "description": "Nước giải khát mát lạnh."},

    {"name": "Nước suối", "category": "Đồ uống", "price": 15000,
     "description": "Nước suối đóng chai."}
]

CATEGORIES = [
    "Thịt bò", "Thịt heo", "Hải sản",
    "Rau củ", "Lẩu & món nóng", "Đồ uống"
]

# =====================================================
# 3. ẢNH RIÊNG CHO TỪNG MÓN
# =====================================================

# Mỗi món có từ khóa và mã ảnh riêng.
# Ảnh được tải từ LoremFlickr.

IMAGE_SETTINGS = {
    "Ba chỉ bò Mỹ": ("beef,brisket,grilled,food", 101),
    "Sườn bò nướng": ("grilled,beef,ribs,barbecue", 102),
    "Lõi vai bò Mỹ": ("beef,steak,grilled,food", 103),
    "Bò cuộn nấm": ("beef,mushroom,roll,food", 104),

    "Ba chỉ heo nướng": ("pork,belly,grilled,barbecue", 105),
    "Sườn heo BBQ": ("pork,ribs,barbecue,grilled", 106),
    "Nạc vai heo": ("pork,meat,grilled,food", 107),

    "Tôm sú nướng": ("grilled,shrimp,prawn,food", 108),
    "Mực nướng sa tế": ("grilled,squid,seafood,food", 109),
    "Bạch tuộc nướng": ("grilled,octopus,seafood", 110),
    "Hàu nướng phô mai": ("baked,oyster,cheese,seafood", 111),

    "Nấm kim châm": ("enoki,mushroom,food", 112),
    "Rau củ tổng hợp": ("grilled,vegetable,platter,food", 113),
    "Kim chi Hàn Quốc": ("korean,kimchi,food", 114),

    "Lẩu Thái hải sản": ("thai,seafood,hotpot,soup", 115),
    "Lẩu kim chi": ("korean,kimchi,hotpot,stew", 116),
    "Cơm chiên hải sản": ("seafood,fried,rice,food", 117),

    "Trà đào cam sả": ("peach,iced,tea,drink", 118),
    "Nước ngọt": ("soft,drink,glass,ice", 119),
    "Nước suối": ("bottled,water,drink", 120)
}


@st.cache_data(ttl=3600, show_spinner=False)
def get_food_image(tags, image_lock):
    url = (
        f"https://loremflickr.com/900/650/"
        f"{quote(tags, safe=',')}?lock={image_lock}"
    )

    try:
        response = requests.get(
            url,
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"},
            allow_redirects=True
        )

        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")

        if "image" not in content_type.lower():
            return None

        if len(response.content) < 1000:
            return None

        return response.content

    except requests.RequestException:
        return None


def show_food_image(item):
    settings = IMAGE_SETTINGS.get(item["name"])

    if settings is None:
        st.warning("Chưa có cấu hình ảnh cho món này.")
        return

    tags, image_lock = settings
    image_data = get_food_image(tags, image_lock)

    if image_data:
        st.image(
            image_data,
            use_container_width=True,
            caption=item["name"]
        )
    else:
        st.warning(
            f"Không tải được ảnh minh họa: {item['name']}"
        )


# =====================================================
# 4. DỮ LIỆU VÀ GIỎ HÀNG
# =====================================================

def load_database():
    default_data = {"orders": [], "bookings": []}

    if not os.path.exists(DATA_FILE):
        return default_data

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            return default_data

        data.setdefault("orders", [])
        data.setdefault("bookings", [])
        return data

    except (json.JSONDecodeError, OSError, TypeError):
        return default_data


if "database" not in st.session_state:
    st.session_state.database = load_database()

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "last_invoice" not in st.session_state:
    st.session_state.last_invoice = None


def save_database():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                st.session_state.database,
                file,
                ensure_ascii=False,
                indent=4
            )
        return True

    except (OSError, TypeError) as error:
        st.error(f"Không thể lưu dữ liệu: {error}")
        return False


def money(number):
    return f"{number:,.0f}đ".replace(",", ".")


def add_to_cart(item, quantity):
    if quantity <= 0:
        return

    name = item["name"]

    if name in st.session_state.cart:
        st.session_state.cart[name]["quantity"] += int(quantity)
    else:
        st.session_state.cart[name] = {
            "name": name,
            "price": item["price"],
            "quantity": int(quantity)
        }


def cart_total():
    return sum(
        item["price"] * item["quantity"]
        for item in st.session_state.cart.values()
    )


# =====================================================
# 5. GIAO DIỆN
# =====================================================

st.markdown("""
<style>
.stApp {
    background-color: #111111;
    color: white;
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

div.stButton > button {
    background-color: #e65c16;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    min-height: 38px;
}

div.stButton > button:hover {
    background-color: #ff8533;
    color: white;
}

.food-card {
    background: #202020;
    border: 1px solid #414141;
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 15px;
}

.food-price {
    color: #ff8c32;
    font-size: 21px;
    font-weight: bold;
}

.main-title {
    text-align: center;
    color: #ff8c32;
    font-size: 42px;
    font-weight: bold;
}

.footer {
    text-align: center;
    color: #aaaaaa;
    padding: 25px;
}

div[data-testid="stImage"] img {
    border-radius: 12px;
    object-fit: cover;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# 6. SIDEBAR
# =====================================================

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
        "📋 Quản lý",
        "📊 Doanh thu"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### 🛒 GIỎ HÀNG")
st.sidebar.write("Số loại món:", len(st.session_state.cart))
st.sidebar.markdown(f"**Tổng tiền: {money(cart_total())}**")
st.sidebar.caption("BBQ HOUSE © 2026")


# =====================================================
# 7. TRANG CHỦ
# =====================================================

if page == "🏠 Trang chủ":

    st.markdown(
        "<div class='main-title'>🔥 BBQ HOUSE 🔥</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align:center;color:white !important'>"
        "THƯỞNG THỨC HƯƠNG VỊ NƯỚNG TUYỆT HẢO"
        "</h3>",
        unsafe_allow_html=True
    )

    hero_image = get_food_image(
        "barbecue,grilled,meat,restaurant,food",
        900
    )

    if hero_image:
        st.image(
            hero_image,
            use_container_width=True,
            caption="BBQ HOUSE - Grill • Food • Good Times"
        )
    else:
        st.info("Ảnh banner chưa tải được.")

    st.markdown("## CHÀO MỪNG ĐẾN VỚI BBQ HOUSE")

    st.write(
        "BBQ HOUSE mang đến trải nghiệm ẩm thực nướng hấp dẫn "
        "với thực đơn đa dạng từ thịt bò, thịt heo, hải sản "
        "đến các món lẩu thơm ngon."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Thực đơn", "20 món")
    col2.metric("Nhóm món", "6 nhóm")
    col3.metric("Phong cách", "BBQ")

    st.divider()
    st.markdown("## ⭐ MÓN ĂN NỔI BẬT")

    columns = st.columns(3)

    for column, index in zip(columns, [0, 9, 14]):
        item = MENU[index]

        with column:
            show_food_image(item)
            st.markdown(f"### {item['name']}")
            st.write(item["description"])
            st.markdown(
                f"<div class='food-price'>{money(item['price'])}</div>",
                unsafe_allow_html=True
            )

    st.info("Vào mục Thực đơn để khám phá 20 món ăn của BBQ HOUSE.")


# =====================================================
# 8. THỰC ĐƠN
# =====================================================

elif page == "🍖 Thực đơn":

    st.title("🍖 THỰC ĐƠN BBQ HOUSE")
    st.write("Khám phá các món ăn hấp dẫn tại nhà hàng.")

    selected_category = st.selectbox(
        "Chọn nhóm món ăn",
        ["Tất cả"] + CATEGORIES
    )

    search = st.text_input(
        "🔎 Tìm kiếm món ăn",
        placeholder="Nhập tên món ăn..."
    )

    filtered = MENU.copy()

    if selected_category != "Tất cả":
        filtered = [
            item for item in filtered
            if item["category"] == selected_category
        ]

    if search.strip():
        filtered = [
            item for item in filtered
            if search.strip().lower() in item["name"].lower()
        ]

    st.write(f"Hiển thị {len(filtered)} món ăn.")

    for start in range(0, len(filtered), 3):
        columns = st.columns(3)

        for column, item in zip(columns, filtered[start:start + 3]):
            with column:
                index = MENU.index(item)

                st.markdown(
                    "<div class='food-card'>",
                    unsafe_allow_html=True
                )

                show_food_image(item)

                st.markdown(f"### {item['name']}")
                st.caption(item["category"])
                st.write(item["description"])

                st.markdown(
                    f"<div class='food-price'>{money(item['price'])}</div>",
                    unsafe_allow_html=True
                )

                quantity = st.number_input(
                    "Số lượng",
                    min_value=1,
                    max_value=20,
                    value=1,
                    key=f"menu_qty_{index}"
                )

                if st.button(
                    "➕ THÊM VÀO GIỎ",
                    key=f"menu_add_{index}",
                    use_container_width=True
                ):
                    add_to_cart(item, quantity)
                    st.success(f"Đã thêm {item['name']}!")

                st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# 9. ĐẶT BÀN
# =====================================================

elif page == "📅 Đặt bàn":

    st.title("📅 ĐẶT BÀN")
    st.write("Đặt bàn trước để có trải nghiệm tốt nhất.")

    with st.form("booking_form"):

        name = st.text_input("Họ và tên")
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
            [
                "Bàn 2 người",
                "Bàn 4 người",
                "Bàn 6 người",
                "Bàn gia đình"
            ]
        )

        note = st.text_area("Ghi chú")

        submitted = st.form_submit_button(
            "XÁC NHẬN ĐẶT BÀN",
            use_container_width=True
        )

        if submitted:
            if not name.strip() or not phone.strip():
                st.error("Vui lòng nhập họ tên và số điện thoại.")
            else:
                booking = {
                    "name": name.strip(),
                    "phone": phone.strip(),
                    "date": str(booking_date),
                    "time": str(booking_time),
                    "people": int(people),
                    "table": table_type,
                    "note": note,
                    "status": "Chờ xác nhận"
                }

                st.session_state.database["bookings"].append(booking)

                if save_database():
                    st.success("Đặt bàn thành công!")


# =====================================================
# 10. GỌI MÓN
# =====================================================

elif page == "🛒 Gọi món":

    st.title("🛒 GỌI MÓN")

    st.text_input("Tên khách hàng", key="order_customer")

    table = st.selectbox(
        "Chọn bàn",
        [
            "Bàn 1", "Bàn 2", "Bàn 3",
            "Bàn 4", "Bàn 5", "Bàn 6",
            "Mang về"
        ]
    )

    category = st.selectbox(
        "Chọn nhóm món",
        ["Tất cả"] + CATEGORIES,
        key="order_category"
    )

    available = MENU if category == "Tất cả" else [
        item for item in MENU
        if item["category"] == category
    ]

    st.divider()

    for start in range(0, len(available), 2):
        columns = st.columns(2)

        for column, item in zip(columns, available[start:start + 2]):
            with column:
                index = MENU.index(item)

                show_food_image(item)
                st.markdown(f"### {item['name']}")
                st.write(money(item["price"]))

                quantity = st.number_input(
                    "Số lượng",
                    min_value=0,
                    max_value=20,
                    value=0,
                    key=f"order_qty_{index}"
                )

                if st.button(
                    f"Thêm {item['name']}",
                    key=f"order_add_{index}"
                ):
                    if quantity > 0:
                        add_to_cart(item, quantity)
                        st.success("Đã thêm món!")
                    else:
                        st.warning("Vui lòng chọn số lượng lớn hơn 0.")

    st.divider()
    st.subheader("GIỎ HÀNG")

    if st.session_state.cart:

        for name, item in list(st.session_state.cart.items()):
            col1, col2, col3, col4 = st.columns([3, 1, 2, 1])

            with col1:
                st.write(item["name"])

            with col2:
                st.write(f"x{item['quantity']}")

            with col3:
                st.write(
                    money(item["price"] * item["quantity"])
                )

            with col4:
                if st.button("Xóa", key=f"remove_{name}"):
                    del st.session_state.cart[name]
                    st.rerun()

        st.markdown(f"## Tổng tiền: {money(cart_total())}")

        if st.button("XÓA TOÀN BỘ GIỎ HÀNG"):
            st.session_state.cart = {}
            st.rerun()

    else:
        st.info("Giỏ hàng đang trống.")


# =====================================================
# 11. THANH TOÁN
# =====================================================

elif page == "💳 Thanh toán":

    st.title("💳 THANH TOÁN")

    if st.session_state.cart:

        customer = st.text_input(
            "Tên khách hàng",
            key="payment_customer"
        )

        table = st.text_input(
            "Bàn",
            key="payment_table",
            value="Chưa chọn"
        )

        st.divider()
        st.subheader("CHI TIẾT HÓA ĐƠN")

        rows = []

        for item in st.session_state.cart.values():
            rows.append({
                "Tên món": item["name"],
                "Đơn giá": money(item["price"]),
                "Số lượng": item["quantity"],
                "Thành tiền": money(
                    item["price"] * item["quantity"]
                )
            })

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True
        )

        total = cart_total()

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
                    "customer": customer.strip(),
                    "table": table,
                    "items": [
                        item.copy()
                        for item in st.session_state.cart.values()
                    ],
                    "total": total,
                    "payment": payment_method,
                    "status": "Đã thanh toán",
                    "created_at": datetime.now().strftime(
                        "%d/%m/%Y %H:%M:%S"
                    )
                }

                st.session_state.database["orders"].append(order)

                if save_database():
                    st.session_state.last_invoice = order
                    st.session_state.cart = {}
                    st.success("Thanh toán thành công!")
                    st.rerun()

    else:
        st.info("Giỏ hàng đang trống. Hãy chọn món trước khi thanh toán.")

    if st.session_state.last_invoice:

        order = st.session_state.last_invoice

        st.divider()
        st.subheader("🧾 HÓA ĐƠN BBQ HOUSE")

        st.write(f"Mã hóa đơn: {order['id']}")
        st.write(f"Khách hàng: {order['customer']}")
        st.write(f"Bàn: {order['table']}")
        st.write(f"Thời gian: {order['created_at']}")

        invoice_lines = [
            "========== BBQ HOUSE ==========",
            f"Ma hoa don: {order['id']}",
            f"Khach hang: {order['customer']}",
            f"Ban: {order['table']}",
            f"Thoi gian: {order['created_at']}",
            "-------------------------------"
        ]

        for item in order["items"]:
            line = (
                f"{item['name']} x{item['quantity']} = "
                f"{money(item['price'] * item['quantity'])}"
            )

            st.write(line)
            invoice_lines.append(line)

        st.markdown(f"### Tổng tiền: {money(order['total'])}")
        st.write(f"Thanh toán: {order['payment']}")
        st.success("Đã thanh toán")

        invoice_lines.extend([
            "-------------------------------",
            f"TONG TIEN: {money(order['total'])}",
            f"Thanh toan: {order['payment']}",
            "Cam on quy khach!"
        ])

        st.download_button(
            "⬇️ TẢI HÓA ĐƠN TXT",
            data="\n".join(invoice_lines),
            file_name=f"{order['id']}.txt",
            mime="text/plain",
            use_container_width=True
        )

        csv_data = pd.DataFrame(order["items"]).to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "⬇️ TẢI HÓA ĐƠN CSV",
            data=csv_data,
            file_name=f"{order['id']}.csv",
            mime="text/csv",
            use_container_width=True
        )


# =====================================================
# 12. QUẢN LÝ ĐƠN HÀNG VÀ ĐẶT BÀN
# =====================================================

elif page == "📋 Quản lý":

    st.title("📋 QUẢN LÝ BBQ HOUSE")

    orders = st.session_state.database["orders"]
    bookings = st.session_state.database["bookings"]

    tab1, tab2 = st.tabs(["Đơn hàng", "Đặt bàn"])

    with tab1:

        st.subheader("DANH SÁCH ĐƠN HÀNG")

        if orders:
            for order in reversed(orders):

                with st.expander(
                    f"{order['id']} | {order['customer']} | "
                    f"{money(order['total'])}"
                ):

                    st.write(f"Khách hàng: {order['customer']}")
                    st.write(f"Bàn: {order['table']}")
                    st.write(f"Thời gian: {order['created_at']}")

                    for item in order["items"]:
                        st.write(
                            f"- {item['name']} x{item['quantity']} "
                            f"= {money(item['price'] * item['quantity'])}"
                        )

                    st.write(f"**Tổng: {money(order['total'])}**")
                    st.success(order["status"])

        else:
            st.info("Chưa có đơn hàng.")

    with tab2:

        st.subheader("DANH SÁCH ĐẶT BÀN")

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

                    statuses = [
                        "Chờ xác nhận",
                        "Đã xác nhận",
                        "Đã hủy"
                    ]

                    current_status = booking.get(
                        "status",
                        "Chờ xác nhận"
                    )

                    selected = st.selectbox(
                        "Trạng thái",
                        statuses,
                        index=statuses.index(current_status)
                        if current_status in statuses else 0,
                        key=f"status_{index}"
                    )

                    if selected != current_status:
                        st.session_state.database["bookings"][index]["status"] = selected

                        if save_database():
                            st.success("Đã cập nhật trạng thái.")
                            st.rerun()

        else:
            st.info("Chưa có đặt bàn.")


# =====================================================
# 13. THỐNG KÊ DOANH THU
# =====================================================

elif page == "📊 Doanh thu":

    st.title("📊 THỐNG KÊ DOANH THU")

    orders = [
        order
        for order in st.session_state.database["orders"]
        if order.get("status") == "Đã thanh toán"
    ]

    total_revenue = sum(
        order["total"] for order in orders
    )

    total_orders = len(orders)

    total_items = sum(
        item["quantity"]
        for order in orders
        for item in order["items"]
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Tổng doanh thu", money(total_revenue))
    col2.metric("Đơn thanh toán", total_orders)
    col3.metric("Số món đã bán", total_items)

    st.divider()

    if orders:

        revenue_df = pd.DataFrame([
            {
                "Mã đơn": order["id"],
                "Khách hàng": order["customer"],
                "Thời gian": order["created_at"],
                "Doanh thu": order["total"]
            }
            for order in orders
        ])

        st.subheader("DOANH THU THEO ĐƠN")

        st.dataframe(
            revenue_df,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            revenue_df.set_index("Mã đơn")["Doanh thu"]
        )

        st.download_button(
            "⬇️ XUẤT BÁO CÁO CSV",
            data=revenue_df.to_csv(
                index=False
            ).encode("utf-8-sig"),
            file_name="bao_cao_doanh_thu.csv",
            mime="text/csv"
        )

        st.divider()
        st.subheader("MÓN ĂN BÁN CHẠY")

        sales = {}

        for order in orders:
            for item in order["items"]:
                name = item["name"]
                sales[name] = (
                    sales.get(name, 0) + item["quantity"]
                )

        sales_df = pd.DataFrame(
            list(sales.items()),
            columns=["Tên món", "Số lượng"]
        ).sort_values(
            "Số lượng",
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
            "Doanh thu sẽ được ghi nhận sau khi thanh toán."
        )


# =====================================================
# 14. CHÂN TRANG
# =====================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        <h3>🔥 BBQ HOUSE 🔥</h3>
        <p>GRILL • FOOD • GOOD TIMES</p>
        <p>Cảm ơn quý khách đã lựa chọn BBQ HOUSE!</p>
    </div>
    """,
    unsafe_allow_html=True
)
