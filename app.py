
import streamlit as st
import pandas as pd
import requests
import json
import os
from io import BytesIO
from PIL import Image, ImageDraw
from datetime import datetime, date, time
from urllib.parse import quote

# ==================================================
# 1. CẤU HÌNH
# ==================================================

st.set_page_config(
    page_title="BBQ HOUSE",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "bbq_data.json"

# ==================================================
# 2. THỰC ĐƠN 20 MÓN VÀ ẢNH RIÊNG
# ==================================================

MENU = [
    {"name": "Ba chỉ bò Mỹ", "category": "Thịt bò", "price": 129000,
     "description": "Ba chỉ bò Mỹ mềm ngon, đậm vị.",
     "keywords": "beef,bbq,grilled", "emoji": "🥩"},

    {"name": "Sườn bò nướng", "category": "Thịt bò", "price": 189000,
     "description": "Sườn bò nướng thơm lừng.",
     "keywords": "beef,ribs,barbecue", "emoji": "🥩"},

    {"name": "Lõi vai bò Mỹ", "category": "Thịt bò", "price": 159000,
     "description": "Lõi vai bò Mỹ tươi ngon.",
     "keywords": "beef,steak,grilled", "emoji": "🥩"},

    {"name": "Bò cuộn nấm", "category": "Thịt bò", "price": 99000,
     "description": "Thịt bò cuộn nấm kim châm.",
     "keywords": "beef,enoki,mushroom,roll", "emoji": "🥩"},

    {"name": "Ba chỉ heo nướng", "category": "Thịt heo", "price": 89000,
     "description": "Ba chỉ heo nướng vàng thơm.",
     "keywords": "pork,belly,grilled", "emoji": "🥓"},

    {"name": "Sườn heo BBQ", "category": "Thịt heo", "price": 129000,
     "description": "Sườn heo nướng sốt BBQ.",
     "keywords": "pork,ribs,barbecue", "emoji": "🍖"},

    {"name": "Nạc vai heo", "category": "Thịt heo", "price": 99000,
     "description": "Nạc vai heo tươi dùng để nướng.",
     "keywords": "pork,grilled,meat", "emoji": "🥓"},

    {"name": "Tôm sú nướng", "category": "Hải sản", "price": 149000,
     "description": "Tôm sú nướng thơm ngon.",
     "keywords": "grilled,tiger,prawns", "emoji": "🍤"},

    {"name": "Mực nướng sa tế", "category": "Hải sản", "price": 139000,
     "description": "Mực nướng sa tế cay thơm.",
     "keywords": "grilled,squid,seafood", "emoji": "🦑"},

    {"name": "Bạch tuộc nướng", "category": "Hải sản", "price": 159000,
     "description": "Bạch tuộc nướng thơm ngon.",
     "keywords": "grilled,octopus,seafood", "emoji": "🐙"},

    {"name": "Hàu nướng phô mai", "category": "Hải sản", "price": 99000,
     "description": "Hàu nướng phô mai béo thơm.",
     "keywords": "grilled,oysters,cheese", "emoji": "🦪"},

    {"name": "Nấm kim châm", "category": "Rau củ", "price": 35000,
     "description": "Nấm kim châm tươi ngon.",
     "keywords": "enoki,mushrooms", "emoji": "🍄"},

    {"name": "Rau củ tổng hợp", "category": "Rau củ", "price": 45000,
     "description": "Các loại rau củ tươi ngon.",
     "keywords": "grilled,vegetables,platter", "emoji": "🥗"},

    {"name": "Kim chi Hàn Quốc", "category": "Rau củ", "price": 30000,
     "description": "Kim chi Hàn Quốc chua cay.",
     "keywords": "korean,kimchi", "emoji": "🥬"},

    {"name": "Lẩu Thái hải sản", "category": "Lẩu & món nóng", "price": 259000,
     "description": "Lẩu Thái chua cay hải sản.",
     "keywords": "thai,seafood,hotpot", "emoji": "🍲"},

    {"name": "Lẩu kim chi", "category": "Lẩu & món nóng", "price": 229000,
     "description": "Lẩu kim chi Hàn Quốc nóng hổi.",
     "keywords": "korean,kimchi,hotpot", "emoji": "🍲"},

    {"name": "Cơm chiên hải sản", "category": "Lẩu & món nóng", "price": 69000,
     "description": "Cơm chiên cùng tôm và hải sản.",
     "keywords": "seafood,fried,rice", "emoji": "🍚"},

    {"name": "Trà đào cam sả", "category": "Đồ uống", "price": 39000,
     "description": "Trà đào cam sả thanh mát.",
     "keywords": "peach,orange,iced,tea", "emoji": "🍹"},

    {"name": "Nước ngọt", "category": "Đồ uống", "price": 25000,
     "description": "Nước giải khát mát lạnh.",
     "keywords": "cola,soft,drink,glass", "emoji": "🥤"},

    {"name": "Nước suối", "category": "Đồ uống", "price": 15000,
     "description": "Nước suối đóng chai.",
     "keywords": "mineral,water,bottle", "emoji": "💧"},
]

CATEGORIES = [
    "Thịt bò",
    "Thịt heo",
    "Hải sản",
    "Rau củ",
    "Lẩu & món nóng",
    "Đồ uống"
]

# ==================================================
# 3. HÌNH ẢNH
# ==================================================

@st.cache_data(ttl=3600, show_spinner=False)
def get_food_image(keywords, index):
    """
    Tải ảnh theo từ khóa món ăn.
    Nếu không tải được, tạo ảnh dự phòng.
    """

    url = (
        "https://loremflickr.com/800/600/"
        + quote(keywords)
        + "?lock="
        + str(index + 100)
    )

    try:
        response = requests.get(
            url,
            timeout=12,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        image = Image.open(BytesIO(response.content)).convert("RGB")

        if image.width < 100 or image.height < 100:
            raise ValueError("Ảnh không hợp lệ")

        return image

    except Exception:
        image = Image.new("RGB", (800, 600), "#292929")
        draw = ImageDraw.Draw(image)

        draw.text(
            (400, 250),
            "BBQ HOUSE",
            fill="#ff8c32",
            anchor="mm"
        )

        draw.text(
            (400, 320),
            "Food image unavailable",
            fill="white",
            anchor="mm"
        )

        return image


# ==================================================
# 4. DỮ LIỆU VÀ LƯU TRỮ
# ==================================================

def load_database():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

                if "orders" not in data:
                    data["orders"] = []

                if "bookings" not in data:
                    data["bookings"] = []

                return data

        except Exception:
            pass

    return {
        "orders": [],
        "bookings": []
    }


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
    except Exception as error:
        st.error(f"Không thể lưu dữ liệu: {error}")
        return False


def money(number):
    return f"{number:,.0f}đ".replace(",", ".")


def add_to_cart(item, quantity):
    name = item["name"]

    if name in st.session_state.cart:
        st.session_state.cart[name]["quantity"] += quantity
    else:
        st.session_state.cart[name] = {
            "name": name,
            "price": item["price"],
            "quantity": quantity
        }


def cart_total():
    return sum(
        item["price"] * item["quantity"]
        for item in st.session_state.cart.values()
    )


# ==================================================
# 5. GIAO DIỆN
# ==================================================

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
</style>
""", unsafe_allow_html=True)


# ==================================================
# 6. SIDEBAR
# ==================================================

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

st.sidebar.write(
    "Số loại món:",
    len(st.session_state.cart)
)

st.sidebar.markdown(
    f"**Tổng tiền: {money(cart_total())}**"
)

st.sidebar.caption("BBQ HOUSE © 2026")


# ==================================================
# 7. TRANG CHỦ
# ==================================================

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

    try:
        hero = get_food_image("korean,bbq,grill,restaurant", 50)
        st.image(hero, use_container_width=True)
    except Exception:
        st.warning("Không thể tải ảnh banner.")

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

    featured = [MENU[0], MENU[9], MENU[14]]
    columns = st.columns(3)

    for index, (column, item) in enumerate(zip(columns, featured)):
        with column:
            st.image(
                get_food_image(item["keywords"], MENU.index(item)),
                use_container_width=True
            )

            st.markdown(f"### {item['name']}")
            st.write(item["description"])

            st.markdown(
                f"<div class='food-price'>{money(item['price'])}</div>",
                unsafe_allow_html=True
            )

    st.info("Vào mục Thực đơn để khám phá 20 món ăn của BBQ HOUSE.")


# ==================================================
# 8. THỰC ĐƠN
# ==================================================

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

    if search:
        filtered = [
            item for item in filtered
            if search.lower() in item["name"].lower()
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

                st.image(
                    get_food_image(item["keywords"], index),
                    use_container_width=True
                )

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


# ==================================================
# 9. ĐẶT BÀN
# ==================================================

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
                    "name": name,
                    "phone": phone,
                    "date": str(booking_date),
                    "time": str(booking_time),
                    "people": people,
                    "table": table_type,
                    "note": note,
                    "status": "Chờ xác nhận"
                }

                st.session_state.database["bookings"].append(booking)

                if save_database():
                    st.success("Đặt bàn thành công!")


# ==================================================
# 10. GỌI MÓN
# ==================================================

elif page == "🛒 Gọi món":

    st.title("🛒 GỌI MÓN")

    customer = st.text_input(
        "Tên khách hàng",
        key="order_customer"
    )

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

                st.image(
                    get_food_image(item["keywords"], index),
                    use_container_width=True
                )

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
                st.write(money(item["price"] * item["quantity"]))

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


# ==================================================
# 11. THANH TOÁN
# ==================================================

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
                    "customer": customer,
                    "table": table,
                    "items": list(st.session_state.cart.values()),
                    "total": total,
                    "payment": payment_method,
                    "status": "Đã thanh toán",
                    "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                }

                st.session_state.database["orders"].append(order)

                if save_database():

                    st.session_state.last_invoice = order
                    st.session_state.cart = {}

                    st.success("Thanh toán thành công!")
                    st.rerun()

    else:

        st.info("Giỏ hàng đang trống. Hãy chọn món trước khi thanh toán.")

    # HÓA ĐƠN SAU THANH TOÁN

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


# ==================================================
# 12. QUẢN LÝ ĐƠN HÀNG VÀ ĐẶT BÀN
# ==================================================

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

                    selected = st.selectbox(
                        "Trạng thái",
                        statuses,
                        index=statuses.index(booking["status"]),
                        key=f"status_{index}"
                    )

                    if selected != booking["status"]:

                        st.session_state.database["bookings"][index]["status"] = selected
                        save_database()
                        st.success("Đã cập nhật trạng thái.")


# ==================================================
# 13. THỐNG KÊ DOANH THU
# ==================================================

elif page == "📊 Doanh thu":

    st.title("📊 THỐNG KÊ DOANH THU")

    orders = [
        order
        for order in st.session_state.database["orders"]
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


# ==================================================
# 14. CHÂN TRANG
# ==================================================

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
