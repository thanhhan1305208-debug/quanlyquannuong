
import streamlit as st
import pandas as pd
import json
import os
import uuid
from pathlib import Path
from datetime import datetime, date
from PIL import Image
from io import BytesIO

# ==================================================
# 1. CẤU HÌNH
# ==================================================

st.set_page_config(
    page_title="BBQ HOUSE",
    page_icon="🔥",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
IMAGE_FILE = BASE_DIR / "Thực đơn BBQ hấp dẫn.webp"
DATA_FILE = BASE_DIR / "bbq_data.json"
IMAGE_DIR = BASE_DIR / "images"

IMAGE_DIR.mkdir(exist_ok=True)

# ==================================================
# 2. CẮT ẢNH TỔNG THÀNH 20 ẢNH RIÊNG
# ==================================================

@st.cache_data
def crop_food_images(image_path, modified_time):
    if not os.path.exists(image_path):
        return []

    with Image.open(image_path) as original:
        original = original.convert("RGB")
        width, height = original.size

        columns = 5
        rows = 4

        cell_width = width / columns
        cell_height = height / rows

        images = []

        for index in range(20):
            row, col = divmod(index, columns)

            left = round(col * cell_width)
            top = round(row * cell_height)
            right = round((col + 1) * cell_width)
            bottom = round((row + 1) * cell_height)

            food_image = original.crop(
                (left, top, right, bottom)
            )

            buffer = BytesIO()
            food_image.save(buffer, format="JPEG", quality=92)
            images.append(buffer.getvalue())

        return images


food_images = []

if IMAGE_FILE.exists():
    food_images = crop_food_images(
        str(IMAGE_FILE),
        IMAGE_FILE.stat().st_mtime
    )

# ==================================================
# 3. THỰC ĐƠN 20 MÓN
# Thứ tự ảnh tương ứng thứ tự món trong danh sách
# ==================================================

MENU = [
    {
        "id": 1,
        "name": "Ba chỉ bò Mỹ",
        "category": "Thịt bò",
        "price": 159000,
        "description": "Ba chỉ bò Mỹ tươi ngon."
    },
    {
        "id": 2,
        "name": "Bò cuộn nấm kim châm",
        "category": "Thịt bò",
        "price": 139000,
        "description": "Bò cuộn nấm kim châm."
    },
    {
        "id": 3,
        "name": "Dẻ sườn bò Mỹ",
        "category": "Thịt bò",
        "price": 189000,
        "description": "Dẻ sườn bò Mỹ nướng."
    },
    {
        "id": 4,
        "name": "Ba chỉ heo",
        "category": "Thịt heo",
        "price": 109000,
        "description": "Ba chỉ heo tươi thái lát."
    },
    {
        "id": 5,
        "name": "Sườn heo BBQ",
        "category": "Thịt heo",
        "price": 149000,
        "description": "Sườn heo sốt BBQ."
    },
    {
        "id": 6,
        "name": "Nạc vai heo",
        "category": "Thịt heo",
        "price": 99000,
        "description": "Nạc vai heo nướng."
    },
    {
        "id": 7,
        "name": "Gà nướng mật ong",
        "category": "Thịt gà",
        "price": 119000,
        "description": "Gà nướng sốt mật ong."
    },
    {
        "id": 8,
        "name": "Mực nướng sa tế",
        "category": "Hải sản",
        "price": 159000,
        "description": "Mực nướng sa tế cay thơm."
    },
    {
        "id": 9,
        "name": "Tôm nướng muối ớt",
        "category": "Hải sản",
        "price": 169000,
        "description": "Tôm nướng muối ớt."
    },
    {
        "id": 10,
        "name": "Bạch tuộc nướng",
        "category": "Hải sản",
        "price": 179000,
        "description": "Bạch tuộc nướng thơm ngon."
    },
    {
        "id": 11,
        "name": "Cá hồi nướng",
        "category": "Hải sản",
        "price": 199000,
        "description": "Cá hồi nướng."
    },
    {
        "id": 12,
        "name": "Salad trộn",
        "category": "Món ăn kèm",
        "price": 59000,
        "description": "Salad rau củ tươi."
    },
    {
        "id": 13,
        "name": "Kim chi",
        "category": "Món ăn kèm",
        "price": 39000,
        "description": "Kim chi cải thảo."
    },
    {
        "id": 14,
        "name": "Khoai tây chiên",
        "category": "Món ăn kèm",
        "price": 49000,
        "description": "Khoai tây chiên giòn."
    },
    {
        "id": 15,
        "name": "Cơm chiên trứng",
        "category": "Món ăn kèm",
        "price": 59000,
        "description": "Cơm chiên trứng nóng."
    },
    {
        "id": 16,
        "name": "Lẩu kim chi",
        "category": "Lẩu",
        "price": 259000,
        "description": "Lẩu kim chi chua cay."
    },
    {
        "id": 17,
        "name": "Lẩu nấm",
        "category": "Lẩu",
        "price": 239000,
        "description": "Lẩu nấm thanh ngọt."
    },
    {
        "id": 18,
        "name": "Coca-Cola",
        "category": "Đồ uống",
        "price": 25000,
        "description": "Nước giải khát."
    },
    {
        "id": 19,
        "name": "Trà đào",
        "category": "Đồ uống",
        "price": 35000,
        "description": "Trà đào mát lạnh."
    },
    {
        "id": 20,
        "name": "Nước suối",
        "category": "Đồ uống",
        "price": 15000,
        "description": "Nước suối đóng chai."
    }
]

# ==================================================
# 4. LƯU DỮ LIỆU
# ==================================================

def load_database():
    default = {
        "orders": [],
        "reservations": []
    }

    if not DATA_FILE.exists():
        return default

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        data.setdefault("orders", [])
        data.setdefault("reservations", [])
        return data

    except (OSError, json.JSONDecodeError):
        return default


def save_database():
    temp = DATA_FILE.with_suffix(".tmp")

    with open(temp, "w", encoding="utf-8") as f:
        json.dump(
            st.session_state.database,
            f,
            ensure_ascii=False,
            indent=4
        )

    os.replace(temp, DATA_FILE)


if "database" not in st.session_state:
    st.session_state.database = load_database()

if "cart" not in st.session_state:
    st.session_state.cart = []

if "customer" not in st.session_state:
    st.session_state.customer = ""

if "table" not in st.session_state:
    st.session_state.table = "Bàn 01"

# ==================================================
# 5. HÀM HỖ TRỢ
# ==================================================

def money(number):
    return f"{int(number):,}".replace(",", ".") + " đ"


def get_total():
    return sum(
        item["price"] * item["quantity"]
        for item in st.session_state.cart
    )


def add_item(item, quantity, note):
    for cart_item in st.session_state.cart:
        if (
            cart_item["id"] == item["id"]
            and cart_item["note"] == note.strip()
        ):
            cart_item["quantity"] += quantity
            return

    st.session_state.cart.append({
        "id": item["id"],
        "name": item["name"],
        "price": item["price"],
        "quantity": quantity,
        "note": note.strip()
    })


def get_order(order_id):
    for order in st.session_state.database["orders"]:
        if order["id"] == order_id:
            return order
    return None


def create_order():
    if not st.session_state.cart:
        return None

    order_id = "BBQ-" + uuid.uuid4().hex[:8].upper()

    order = {
        "id": order_id,
        "customer": st.session_state.customer.strip(),
        "table": st.session_state.table,
        "items": [
            dict(item) for item in st.session_state.cart
        ],
        "total": get_total(),
        "status": "Chưa thanh toán",
        "payment_method": "",
        "created_at": datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )
    }

    st.session_state.database["orders"].append(order)
    st.session_state.cart = []
    save_database()

    return order_id


# ==================================================
# 6. GIAO DIỆN
# ==================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

.stApp {
    background: #101010;
    color: white;
}

section[data-testid="stSidebar"] {
    background: #191919;
    border-right: 1px solid #383838;
}

h1, h2, h3 {
    color: white;
}

p, label {
    color: #eeeeee;
}

.brand {
    color: #ff542b;
    font-size: 34px;
    font-weight: 800;
}

.hero {
    background: linear-gradient(120deg, #24100b, #681c10, #171111);
    border: 1px solid #80331e;
    border-radius: 18px;
    padding: 35px;
    margin-bottom: 25px;
}

.hero h1 {
    color: #ff642e;
    font-size: 42px;
    font-weight: 800;
}

.hero p {
    color: #f3d7c9;
}

.food-card {
    background: #1d1d1d;
    border: 1px solid #383838;
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 15px;
}

.price {
    color: #ff5935;
    font-size: 19px;
    font-weight: 800;
}

div.stButton > button {
    background: #e93625;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    min-height: 40px;
}

div.stButton > button:hover {
    background: #ff5a35;
    color: white;
}

div[data-testid="stMetric"] {
    background: #202020;
    border: 1px solid #383838;
    padding: 15px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# 7. THANH ĐIỀU HƯỚNG
# ==================================================

with st.sidebar:
    st.markdown(
        '<div class="brand">🔥 BBQ HOUSE</div>',
        unsafe_allow_html=True
    )

    st.caption("GRILL • HOTPOT • ENJOY")
    st.divider()

    page = st.radio(
        "DANH MỤC",
        [
            "Trang chủ",
            "Thực đơn",
            "Đặt bàn",
            "Gọi món",
            "Thanh toán",
            "Quản lý đơn hàng",
            "Doanh thu"
        ]
    )

    st.divider()
    st.markdown("### 🛒 Giỏ hàng")
    st.write(f"{len(st.session_state.cart)} món")
    st.markdown(
        f'<div class="price">{money(get_total())}</div>',
        unsafe_allow_html=True
    )

    st.caption("BBQ HOUSE © 2026")

# ==================================================
# 8. TRANG CHỦ
# ==================================================

if page == "Trang chủ":

    st.markdown("""
    <div class="hero">
        <h1>🔥 BBQ HOUSE</h1>
        <h2>THIÊN ĐƯỜNG ẨM THỰC NƯỚNG</h2>
        <p>Thịt nướng • Hải sản • Lẩu nóng</p>
        <p>Thưởng thức hương vị tuyệt vời cùng gia đình và bạn bè.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔥 Món ăn nổi bật")

    featured = [MENU[0], MENU[7], MENU[9], MENU[15]]
    cols = st.columns(4)

    for col, item in zip(cols, featured):
        with col:
            index = item["id"] - 1

            if index < len(food_images):
                st.image(food_images[index], use_container_width=True)
            else:
                st.info("Chưa có ảnh")

            st.markdown(f"**{item['name']}**")
            st.markdown(
                f'<div class="price">{money(item["price"])}</div>',
                unsafe_allow_html=True
            )

    st.divider()
    st.subheader("Chào mừng đến với BBQ HOUSE")
    st.write(
        "Khám phá thực đơn phong phú với nhiều món nướng, "
        "hải sản, món ăn kèm và lẩu hấp dẫn."
    )

# ==================================================
# 9. THỰC ĐƠN
# ==================================================

elif page == "Thực đơn":

    st.title("🍽️ THỰC ĐƠN BBQ HOUSE")

    search = st.text_input(
        "🔍 Tìm món ăn",
        placeholder="Nhập tên món..."
    )

    categories = [
        "Tất cả",
        "Thịt bò",
        "Thịt heo",
        "Thịt gà",
        "Hải sản",
        "Món ăn kèm",
        "Lẩu",
        "Đồ uống"
    ]

    category = st.selectbox("Danh mục", categories)

    filtered = MENU.copy()

    if category != "Tất cả":
        filtered = [
            x for x in filtered
            if x["category"] == category
        ]

    if search.strip():
        filtered = [
            x for x in filtered
            if search.lower() in x["name"].lower()
        ]

    st.caption(f"Có {len(filtered)} món ăn")

    cols = st.columns(3)

    for index, item in enumerate(filtered):
        with cols[index % 3]:

            st.markdown(
                '<div class="food-card">',
                unsafe_allow_html=True
            )

            image_index = item["id"] - 1

            if image_index < len(food_images):
                st.image(
                    food_images[image_index],
                    use_container_width=True
                )
            else:
                st.warning(
                    "Chưa tìm thấy ảnh món ăn."
                )

            st.markdown(f"### {item['name']}")
            st.caption(item["description"])

            st.markdown(
                f'<div class="price">{money(item["price"])}</div>',
                unsafe_allow_html=True
            )

            quantity = st.number_input(
                "Số lượng",
                min_value=1,
                max_value=50,
                value=1,
                key=f"quantity_{item['id']}"
            )

            note = st.text_input(
                "Ghi chú",
                placeholder="Ví dụ: Không cay",
                key=f"note_{item['id']}"
            )

            if st.button(
                "＋ Thêm vào giỏ",
                key=f"add_{item['id']}",
                use_container_width=True
            ):
                add_item(item, quantity, note)
                st.success("Đã thêm vào giỏ hàng!")

            st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# 10. ĐẶT BÀN
# ==================================================

elif page == "Đặt bàn":

    st.title("📅 ĐẶT BÀN BBQ HOUSE")

    with st.form("booking_form"):

        name = st.text_input("Họ và tên")
        phone = st.text_input("Số điện thoại")

        col1, col2 = st.columns(2)

        with col1:
            booking_date = st.date_input(
                "Ngày đặt",
                min_value=date.today()
            )

        with col2:
            booking_time = st.time_input("Giờ đặt")

        people = st.number_input(
            "Số lượng khách",
            min_value=1,
            max_value=50,
            value=2
        )

        table_type = st.selectbox(
            "Loại bàn",
            ["Bàn thường", "Bàn gia đình", "Bàn nhóm"]
        )

        note = st.text_area("Ghi chú")

        submit = st.form_submit_button(
            "XÁC NHẬN ĐẶT BÀN",
            use_container_width=True
        )

        if submit:

            if not name.strip() or not phone.strip():
                st.error("Vui lòng nhập họ tên và số điện thoại.")

            elif not phone.strip().replace(" ", "").isdigit():
                st.error("Số điện thoại không hợp lệ.")

            else:
                reservation = {
                    "id": "RES-" + uuid.uuid4().hex[:8].upper(),
                    "name": name.strip(),
                    "phone": phone.strip(),
                    "date": booking_date.strftime("%d/%m/%Y"),
                    "time": booking_time.strftime("%H:%M"),
                    "people": people,
                    "table_type": table_type,
                    "note": note.strip()
                }

                st.session_state.database[
                    "reservations"
                ].append(reservation)

                save_database()
                st.success("Đặt bàn thành công!")
                st.json(reservation)

# ==================================================
# 11. GỌI MÓN
# ==================================================

elif page == "Gọi món":

    st.title("🛒 GỌI MÓN")

    st.text_input("Tên khách hàng", key="customer")

    st.selectbox(
        "Chọn bàn",
        [f"Bàn {i:02d}" for i in range(1, 21)],
        key="table"
    )

    st.divider()
    st.subheader("Giỏ hàng")

    if st.session_state.cart:

        for index, item in enumerate(st.session_state.cart):

            col1, col2, col3 = st.columns([4, 2, 1])

            with col1:
                st.write(f"**{item['name']}**")
                st.caption(item["note"] or "Không có ghi chú")

            with col2:
                st.write(f"{item['quantity']} × {money(item['price'])}")

            with col3:
                if st.button("Xóa", key=f"delete_{index}"):
                    st.session_state.cart.pop(index)
                    st.rerun()

        st.divider()

        st.markdown(
            f"### Tổng cộng: <span class='price'>{money(get_total())}</span>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("XÓA GIỎ HÀNG", use_container_width=True):
                st.session_state.cart = []
                st.rerun()

        with col2:
            if st.button("XÁC NHẬN GỌI MÓN", use_container_width=True):

                if not st.session_state.customer.strip():
                    st.error("Vui lòng nhập tên khách hàng.")

                else:
                    order_id = create_order()

                    if order_id:
                        st.success(
                            f"Đã tạo đơn hàng {order_id}!"
                        )
                        st.info("Vào Thanh toán để xử lý hóa đơn.")

    else:
        st.info("Giỏ hàng đang trống. Hãy chọn món trong Thực đơn.")

# ==================================================
# 12. THANH TOÁN
# ==================================================

elif page == "Thanh toán":

    st.title("💳 THANH TOÁN")

    orders = st.session_state.database["orders"]

    unpaid = [
        x for x in orders
        if x["status"] == "Chưa thanh toán"
    ]

    if unpaid:

        options = {
            f"{x['id']} | {x['customer']} | {money(x['total'])}": x["id"]
            for x in unpaid
        }

        selected = st.selectbox(
            "Chọn hóa đơn",
            list(options.keys())
        )

        order = get_order(options[selected])

        st.subheader("BBQ HOUSE - HÓA ĐƠN")

        st.write(f"**Mã đơn:** {order['id']}")
        st.write(f"**Khách hàng:** {order['customer']}")
        st.write(f"**Bàn:** {order['table']}")
        st.write(f"**Thời gian:** {order['created_at']}")

        bill = []

        for item in order["items"]:
            bill.append({
                "Tên món": item["name"],
                "Đơn giá": money(item["price"]),
                "Số lượng": item["quantity"],
                "Thành tiền": money(
                    item["price"] * item["quantity"]
                ),
                "Ghi chú": item.get("note", "")
            })

        st.dataframe(
            pd.DataFrame(bill),
            use_container_width=True,
            hide_index=True
        )

        st.markdown(
            f"## Tổng tiền: <span class='price'>{money(order['total'])}</span>",
            unsafe_allow_html=True
        )

        method = st.radio(
            "Phương thức thanh toán",
            ["Tiền mặt", "Chuyển khoản", "Thẻ ngân hàng"],
            horizontal=True
        )

        if st.button(
            "XÁC NHẬN ĐÃ THANH TOÁN",
            use_container_width=True
        ):
            order["status"] = "Đã thanh toán"
            order["payment_method"] = method
            order["paid_at"] = datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )

            save_database()
            st.success("Thanh toán thành công!")
            st.rerun()

    else:
        st.info("Không có hóa đơn chờ thanh toán.")

    st.divider()
    st.subheader("🧾 Xuất hóa đơn")

    paid = [
        x for x in orders
        if x["status"] == "Đã thanh toán"
    ]

    if paid:

        invoice_options = {
            f"{x['id']} | {x['customer']}": x["id"]
            for x in paid
        }

        selected_invoice = st.selectbox(
            "Chọn hóa đơn đã thanh toán",
            list(invoice_options.keys())
        )

        invoice = get_order(invoice_options[selected_invoice])

        lines = [
            "BBQ HOUSE",
            "HOA DON THANH TOAN",
            "-------------------------",
            f"Ma don: {invoice['id']}",
            f"Khach hang: {invoice['customer']}",
            f"Ban: {invoice['table']}",
            f"Thoi gian: {invoice['created_at']}",
            "-------------------------"
        ]

        for item in invoice["items"]:
            lines.append(
                f"{item['name']} x {item['quantity']}"
            )
            lines.append(
                money(item["price"] * item["quantity"])
            )

        lines.extend([
            "-------------------------",
            f"TONG TIEN: {money(invoice['total'])}",
            f"Phuong thuc: {invoice['payment_method']}",
            "DA THANH TOAN",
            "Cam on quy khach!"
        ])

        invoice_text = "\n".join(lines)

        st.code(invoice_text)

        st.download_button(
            "⬇️ TẢI HÓA ĐƠN TXT",
            data=invoice_text,
            file_name=f"{invoice['id']}.txt",
            mime="text/plain",
            use_container_width=True
        )

    else:
        st.info("Chưa có hóa đơn đã thanh toán.")

# ==================================================
# 13. QUẢN LÝ ĐƠN HÀNG
# ==================================================

elif page == "Quản lý đơn hàng":

    st.title("📋 QUẢN LÝ NHÀ HÀNG")

    tab1, tab2 = st.tabs(["Đơn hàng", "Đặt bàn"])

    with tab1:

        orders = st.session_state.database["orders"]

        if orders:

            for order in reversed(orders):

                with st.expander(
                    f"{order['id']} | {order['customer']} | {money(order['total'])}"
                ):

                    st.write(f"Bàn: {order['table']}")
                    st.write(f"Thời gian: {order['created_at']}")
                    st.write(f"Trạng thái: {order['status']}")

                    for item in order["items"]:
                        st.write(
                            f"- {item['name']} x {item['quantity']} "
                            f"= {money(item['price'] * item['quantity'])}"
                        )

                    st.write(f"**Tổng: {money(order['total'])}**")

        else:
            st.info("Chưa có đơn hàng.")

    with tab2:

        reservations = st.session_state.database["reservations"]

        if reservations:

            for reservation in reversed(reservations):

                with st.expander(
                    f"{reservation['name']} | {reservation['date']} | {reservation['time']}"
                ):

                    st.write(f"Mã đặt bàn: {reservation['id']}")
                    st.write(f"Số điện thoại: {reservation['phone']}")
                    st.write(f"Số khách: {reservation['people']}")
                    st.write(f"Loại bàn: {reservation['table_type']}")
                    st.write(f"Ghi chú: {reservation['note']}")

        else:
            st.info("Chưa có lượt đặt bàn.")

# ==================================================
# 14. DOANH THU
# ==================================================

elif page == "Doanh thu":

    st.title("📊 THỐNG KÊ DOANH THU")

    paid_orders = [
        x for x in st.session_state.database["orders"]
        if x["status"] == "Đã thanh toán"
    ]

    period = st.selectbox(
        "Khoảng thời gian",
        ["Tất cả", "Hôm nay", "7 ngày gần nhất", "30 ngày gần nhất"]
    )

    filtered = []

    for order in paid_orders:

        try:
            paid_date = datetime.strptime(
                order["paid_at"],
                "%d/%m/%Y %H:%M:%S"
            ).date()
        except (KeyError, ValueError):
            continue

        days = (date.today() - paid_date).days

        if period == "Tất cả":
            filtered.append(order)
        elif period == "Hôm nay" and days == 0:
            filtered.append(order)
        elif period == "7 ngày gần nhất" and 0 <= days < 7:
            filtered.append(order)
        elif period == "30 ngày gần nhất" and 0 <= days < 30:
            filtered.append(order)

    revenue = sum(x["total"] for x in filtered)
    order_count = len(filtered)

    item_count = sum(
        item["quantity"]
        for order in filtered
        for item in order["items"]
    )

    average = revenue / order_count if order_count else 0

    c1, c2 = st.columns(2)

    c1.metric("💰 Tổng doanh thu", money(revenue))
    c2.metric("🧾 Đơn đã thanh toán", order_count)

    c3, c4 = st.columns(2)

    c3.metric("🍽️ Số món đã bán", item_count)
    c4.metric("📈 Trung bình mỗi đơn", money(average))

    st.divider()
    st.subheader("🏆 Món bán chạy")

    sold = {}

    for order in filtered:
        for item in order["items"]:
            sold[item["name"]] = (
                sold.get(item["name"], 0) + item["quantity"]
            )

    if sold:

        best_sellers = pd.DataFrame([
            {"Tên món": name, "Số lượng": quantity}
            for name, quantity in sold.items()
        ]).sort_values("Số lượng", ascending=False)

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
    st.subheader("📄 Chi tiết giao dịch")

    if filtered:

        report = pd.DataFrame([
            {
                "Mã đơn": x["id"],
                "Khách hàng": x["customer"],
                "Bàn": x["table"],
                "Ngày thanh toán": x.get("paid_at", ""),
                "Phương thức": x.get("payment_method", ""),
                "Tổng tiền": x["total"]
            }
            for x in filtered
        ])

        st.dataframe(
            report,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇️ TẢI BÁO CÁO CSV",
            data=report.to_csv(index=False).encode("utf-8-sig"),
            file_name="bao_cao_doanh_thu.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:
        st.info("Chưa có giao dịch trong khoảng thời gian này.")

# ==================================================
# 15. KIỂM TRA ẢNH VÀ CHÂN TRANG
# ==================================================

if not IMAGE_FILE.exists():

    st.error(
        "Không tìm thấy file ảnh 'Thực đơn BBQ hấp dẫn.webp'. "
        "Hãy kiểm tra file có nằm cùng cấp với app.py trên GitHub không."
    )

elif len(food_images) != 20:

    st.warning(
        "Không đọc đủ 20 ảnh. Hãy kiểm tra ảnh nguồn có bố cục "
        "5 cột × 4 hàng hay không."
    )

st.divider()

st.markdown("""
<div style="text-align:center; padding:20px; color:#999;">
    <h3 style="color:#ff5935;">🔥 BBQ HOUSE</h3>
    <p>GRILL • HOTPOT • ENJOY</p>
    <p>Thưởng thức ẩm thực - Kết nối mọi khoảnh khắc</p>
    <small>© 2026 BBQ HOUSE</small>
</div>
""", unsafe_allow_html=True)
