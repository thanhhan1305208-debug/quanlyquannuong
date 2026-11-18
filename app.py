
import streamlit as st
import pandas as pd
import json
import os
import uuid
from pathlib import Path
from datetime import datetime, date
from PIL import Image

# =====================================================
# 1. CẤU HÌNH
# =====================================================

st.set_page_config(
    page_title="BBQ HOUSE | Restaurant",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
IMAGE_DIR = BASE_DIR / "images"
DATA_FILE = BASE_DIR / "bbq_data.json"
COLLAGE_FILE = BASE_DIR / "bbq-house-menu.png"

IMAGE_DIR.mkdir(exist_ok=True)

# =====================================================
# 2. DANH SÁCH HÌNH ẢNH
# =====================================================

IMAGE_NAMES = [
    "ba-chi-bo-my",
    "bo-cuon-nam-kim-cham",
    "de-suon-bo-my",
    "ba-chi-heo",
    "suon-heo-bbq",
    "nac-vai-heo",
    "ga-nuong-mat-ong",
    "muc-nuong-sa-te",
    "tom-nuong-muoi-ot",
    "bach-tuoc-nuong",
    "ca-hoi-nuong",
    "salad-tron",
    "kim-chi",
    "khoai-tay-chien",
    "com-chien-trung",
    "lau-kim-chi",
    "lau-nam",
    "coca-cola",
    "tra-dao",
    "nuoc-suoi"
]


def create_images():
    """
    Tự cắt ảnh thực đơn tổng 5 cột x 4 hàng.
    Ảnh nguồn cần nằm cạnh app.py và tên là
    bbq-house-menu.png.
    """

    missing = [
        name for name in IMAGE_NAMES
        if not (IMAGE_DIR / f"{name}.jpg").exists()
    ]

    if not missing or not COLLAGE_FILE.exists():
        return

    try:
        with Image.open(COLLAGE_FILE) as source:
            source = source.convert("RGB")
            width, height = source.size

            cell_width = width / 5
            cell_height = height / 4

            for index, name in enumerate(IMAGE_NAMES):
                row, col = divmod(index, 5)

                left = round(col * cell_width)
                top = round(row * cell_height)
                right = round((col + 1) * cell_width)
                bottom = round((row + 1) * cell_height)

                # Bỏ đường phân cách giữa các ô
                if col > 0:
                    left += 2
                if row > 0:
                    top += 2
                if col < 4:
                    right -= 2
                if row < 3:
                    bottom -= 2

                image = source.crop(
                    (left, top, right, bottom)
                )

                image.save(
                    IMAGE_DIR / f"{name}.jpg",
                    "JPEG",
                    quality=92
                )

    except Exception as error:
        st.warning(f"Không thể xử lý ảnh thực đơn: {error}")


create_images()


# =====================================================
# 3. THỰC ĐƠN
# =====================================================

MENU = [
    {
        "id": 1,
        "name": "Ba chỉ bò Mỹ",
        "category": "Thịt bò",
        "price": 159000,
        "description": "Ba chỉ bò Mỹ thái lát, mềm và béo.",
        "image": "ba-chi-bo-my"
    },
    {
        "id": 2,
        "name": "Bò cuộn nấm kim châm",
        "category": "Thịt bò",
        "price": 139000,
        "description": "Thịt bò cuộn nấm kim châm tươi.",
        "image": "bo-cuon-nam-kim-cham"
    },
    {
        "id": 3,
        "name": "Dẻ sườn bò Mỹ",
        "category": "Thịt bò",
        "price": 189000,
        "description": "Dẻ sườn bò Mỹ ướp sốt BBQ.",
        "image": "de-suon-bo-my"
    },
    {
        "id": 4,
        "name": "Ba chỉ heo",
        "category": "Thịt heo",
        "price": 109000,
        "description": "Ba chỉ heo tươi, thái lát vừa ăn.",
        "image": "ba-chi-heo"
    },
    {
        "id": 5,
        "name": "Sườn heo BBQ",
        "category": "Thịt heo",
        "price": 149000,
        "description": "Sườn heo nướng sốt BBQ đậm vị.",
        "image": "suon-heo-bbq"
    },
    {
        "id": 6,
        "name": "Nạc vai heo",
        "category": "Thịt heo",
        "price": 99000,
        "description": "Nạc vai heo tươi ngon.",
        "image": "nac-vai-heo"
    },
    {
        "id": 7,
        "name": "Gà nướng mật ong",
        "category": "Thịt gà",
        "price": 119000,
        "description": "Gà nướng phủ sốt mật ong.",
        "image": "ga-nuong-mat-ong"
    },
    {
        "id": 8,
        "name": "Mực nướng sa tế",
        "category": "Hải sản",
        "price": 159000,
        "description": "Mực tươi nướng cùng sa tế.",
        "image": "muc-nuong-sa-te"
    },
    {
        "id": 9,
        "name": "Tôm nướng muối ớt",
        "category": "Hải sản",
        "price": 169000,
        "description": "Tôm nướng muối ớt thơm ngon.",
        "image": "tom-nuong-muoi-ot"
    },
    {
        "id": 10,
        "name": "Bạch tuộc nướng",
        "category": "Hải sản",
        "price": 179000,
        "description": "Bạch tuộc nướng gia vị đặc biệt.",
        "image": "bach-tuoc-nuong"
    },
    {
        "id": 11,
        "name": "Cá hồi nướng",
        "category": "Hải sản",
        "price": 199000,
        "description": "Cá hồi nướng thơm, ăn kèm chanh.",
        "image": "ca-hoi-nuong"
    },
    {
        "id": 12,
        "name": "Salad trộn",
        "category": "Món ăn kèm",
        "price": 59000,
        "description": "Rau xanh, cà chua và sốt salad.",
        "image": "salad-tron"
    },
    {
        "id": 13,
        "name": "Kim chi",
        "category": "Món ăn kèm",
        "price": 39000,
        "description": "Kim chi cải thảo kiểu Hàn Quốc.",
        "image": "kim-chi"
    },
    {
        "id": 14,
        "name": "Khoai tây chiên",
        "category": "Món ăn kèm",
        "price": 49000,
        "description": "Khoai tây chiên giòn.",
        "image": "khoai-tay-chien"
    },
    {
        "id": 15,
        "name": "Cơm chiên trứng",
        "category": "Món ăn kèm",
        "price": 59000,
        "description": "Cơm chiên trứng nóng hổi.",
        "image": "com-chien-trung"
    },
    {
        "id": 16,
        "name": "Lẩu kim chi",
        "category": "Lẩu",
        "price": 259000,
        "description": "Lẩu kim chi chua cay kiểu Hàn.",
        "image": "lau-kim-chi"
    },
    {
        "id": 17,
        "name": "Lẩu nấm",
        "category": "Lẩu",
        "price": 239000,
        "description": "Lẩu nấm thanh ngọt với nhiều loại nấm.",
        "image": "lau-nam"
    },
    {
        "id": 18,
        "name": "Coca-Cola",
        "category": "Đồ uống",
        "price": 25000,
        "description": "Nước giải khát Coca-Cola.",
        "image": "coca-cola"
    },
    {
        "id": 19,
        "name": "Trà đào",
        "category": "Đồ uống",
        "price": 35000,
        "description": "Trà đào mát lạnh.",
        "image": "tra-dao"
    },
    {
        "id": 20,
        "name": "Nước suối",
        "category": "Đồ uống",
        "price": 15000,
        "description": "Nước suối đóng chai.",
        "image": "nuoc-suoi"
    }
]


# =====================================================
# 4. DỮ LIỆU VÀ LƯU TRỮ
# =====================================================

def load_data():
    default = {
        "orders": [],
        "reservations": []
    }

    if not DATA_FILE.exists():
        return default

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        data.setdefault("orders", [])
        data.setdefault("reservations", [])
        return data

    except (json.JSONDecodeError, OSError):
        return default


def save_data():
    temp_file = DATA_FILE.with_suffix(".tmp")

    with open(temp_file, "w", encoding="utf-8") as file:
        json.dump(
            st.session_state.database,
            file,
            ensure_ascii=False,
            indent=4
        )

    os.replace(temp_file, DATA_FILE)


if "database" not in st.session_state:
    st.session_state.database = load_data()

if "cart" not in st.session_state:
    st.session_state.cart = []

if "customer_name" not in st.session_state:
    st.session_state.customer_name = ""

if "table_number" not in st.session_state:
    st.session_state.table_number = "Bàn 01"

if "last_order_id" not in st.session_state:
    st.session_state.last_order_id = None


# =====================================================
# 5. HÀM HỖ TRỢ
# =====================================================

def money(value):
    return f"{int(value):,}".replace(",", ".") + " đ"


def get_image_path(item):
    path = IMAGE_DIR / f"{item['image']}.jpg"

    if path.exists():
        return str(path)

    return None


def get_item(item_id):
    for item in MENU:
        if item["id"] == item_id:
            return item

    return None


def cart_total():
    return sum(
        item["price"] * item["quantity"]
        for item in st.session_state.cart
    )


def add_to_cart(item, quantity, note):
    if quantity < 1:
        return

    st.session_state.cart.append({
        "id": item["id"],
        "name": item["name"],
        "price": item["price"],
        "quantity": quantity,
        "note": note.strip()
    })


def clear_cart():
    st.session_state.cart = []


def create_order():
    if not st.session_state.cart:
        return None

    order_id = "BBQ-" + uuid.uuid4().hex[:8].upper()

    order = {
        "id": order_id,
        "customer": st.session_state.customer_name.strip(),
        "table": st.session_state.table_number,
        "items": st.session_state.cart.copy(),
        "total": cart_total(),
        "status": "Chưa thanh toán",
        "payment_method": "",
        "created_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    st.session_state.database["orders"].append(order)
    st.session_state.last_order_id = order_id

    clear_cart()
    save_data()

    return order_id


def find_order(order_id):
    for order in st.session_state.database["orders"]:
        if order["id"] == order_id:
            return order

    return None


def show_food_image(item):
    image_path = get_image_path(item)

    if image_path:
        st.image(
            image_path,
            use_container_width=True
        )
    else:
        st.markdown(
            """
            <div style="
                height:170px;
                background:#252525;
                border-radius:12px;
                display:flex;
                align-items:center;
                justify-content:center;
                color:#aaa;
                font-size:14px;">
                Chưa có hình ảnh
            </div>
            """,
            unsafe_allow_html=True
        )


# =====================================================
# 6. GIAO DIỆN
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

.stApp {
    background-color: #101010;
    color: #ffffff;
}

section[data-testid="stSidebar"] {
    background-color: #191919;
    border-right: 1px solid #343434;
}

h1, h2, h3 {
    color: #ffffff;
}

p, label, span {
    color: #eeeeee;
}

.brand {
    font-size: 34px;
    font-weight: 800;
    color: #ff7029;
    letter-spacing: 1px;
}

.subtitle {
    color: #bbbbbb;
    font-size: 14px;
}

.hero {
    background: linear-gradient(120deg, #28120b, #5c1b0b, #1c1010);
    padding: 45px 35px;
    border-radius: 18px;
    border: 1px solid #71351d;
    margin-bottom: 25px;
}

.hero h1 {
    color: #ff762e;
    font-size: 43px;
    font-weight: 800;
}

.hero p {
    color: #f0d4c4;
    font-size: 16px;
}

.food-card {
    background: #1c1c1c;
    padding: 12px;
    border-radius: 14px;
    border: 1px solid #333333;
    margin-bottom: 12px;
}

.price {
    color: #ff762e;
    font-size: 18px;
    font-weight: 800;
}

.orange-text {
    color: #ff762e;
}

div.stButton > button {
    background: #f15b24;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
    min-height: 40px;
}

div.stButton > button:hover {
    background: #ff7a38;
    color: white;
}

div[data-testid="stMetric"] {
    background: #202020;
    border: 1px solid #383838;
    padding: 18px;
    border-radius: 12px;
}

hr {
    border-color: #333333;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 7. THANH ĐIỀU HƯỚNG
# =====================================================

with st.sidebar:
    st.markdown(
        '<div class="brand">🔥 BBQ HOUSE</div>',
        unsafe_allow_html=True
    )

    st.caption("GRILL • HOTPOT • ENJOY")

    st.divider()

    page = st.radio(
        "MENU CHÍNH",
        [
            "Trang chủ",
            "Thực đơn",
            "Đặt bàn",
            "Gọi món",
            "Thanh toán",
            "Quản lý đơn hàng",
            "Doanh thu"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### 🛒 Giỏ hàng")
    st.write(f"Đang có **{len(st.session_state.cart)}** món")

    st.markdown(
        f'<div class="price">{money(cart_total())}</div>',
        unsafe_allow_html=True
    )

    st.caption("BBQ HOUSE © 2026")


# =====================================================
# 8. TRANG CHỦ
# =====================================================

if page == "Trang chủ":

    st.markdown("""
    <div class="hero">
        <h1>BBQ HOUSE 🔥</h1>
        <h2>THƯỞNG THỨC TIỆC NƯỚNG ĐÚNG ĐIỆU</h2>
        <p>
            Thịt nướng hấp dẫn • Hải sản tươi ngon • Lẩu nóng hổi
        </p>
        <p>Không gian ấm cúng - Hương vị khó quên</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔥 Món ăn nổi bật")

    featured = [MENU[0], MENU[7], MENU[15], MENU[16]]

    cols = st.columns(4)

    for col, item in zip(cols, featured):
        with col:
            show_food_image(item)
            st.markdown(f"**{item['name']}**")
            st.markdown(
                f'<div class="price">{money(item["price"])}</div>',
                unsafe_allow_html=True
            )

    st.divider()

    a, b, c = st.columns(3)

    with a:
        st.markdown("### 🥩")
        st.markdown("**Thịt nướng**")
        st.caption("Đa dạng các loại thịt tươi ngon.")

    with b:
        st.markdown("### 🦐")
        st.markdown("**Hải sản**")
        st.caption("Nhiều lựa chọn hấp dẫn.")

    with c:
        st.markdown("### 🍲")
        st.markdown("**Lẩu nóng**")
        st.caption("Thưởng thức cùng bạn bè và gia đình.")

    st.divider()

    st.markdown("### 📍 Chào mừng đến với BBQ HOUSE")
    st.write(
        "BBQ HOUSE mang đến trải nghiệm thưởng thức món nướng "
        "và lẩu với thực đơn đa dạng."
    )

    st.caption(
        "Thông tin liên hệ và địa chỉ nhà hàng có thể được bổ sung "
        "theo thông tin thực tế."
    )


# =====================================================
# 9. TRANG THỰC ĐƠN
# =====================================================

elif page == "Thực đơn":

    st.title("🍽️ THỰC ĐƠN BBQ HOUSE")
    st.caption("Khám phá những món ăn hấp dẫn của chúng tôi.")

    search = st.text_input(
        "🔍 Tìm món ăn",
        placeholder="Nhập tên món ăn..."
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

    category = st.selectbox(
        "Danh mục món ăn",
        categories
    )

    filtered = MENU.copy()

    if category != "Tất cả":
        filtered = [
            item for item in filtered
            if item["category"] == category
        ]

    if search.strip():
        filtered = [
            item for item in filtered
            if search.lower() in item["name"].lower()
        ]

    st.write(f"Tìm thấy **{len(filtered)}** món ăn")

    cols = st.columns(3)

    for index, item in enumerate(filtered):
        with cols[index % 3]:
            st.markdown('<div class="food-card">', unsafe_allow_html=True)

            show_food_image(item)

            st.markdown(f"### {item['name']}")
            st.caption(item["description"])

            st.markdown(
                f'<div class="price">{money(item["price"])}</div>',
                unsafe_allow_html=True
            )

            st.caption(item["category"])

            quantity = st.number_input(
                "Số lượng",
                min_value=1,
                max_value=50,
                value=1,
                step=1,
                key=f"menu_quantity_{item['id']}"
            )

            note = st.text_input(
                "Ghi chú món",
                placeholder="Ví dụ: Không cay",
                key=f"menu_note_{item['id']}"
            )

            if st.button(
                "＋ Thêm vào giỏ",
                key=f"add_menu_{item['id']}",
                use_container_width=True
            ):
                add_to_cart(item, quantity, note)
                st.success(f"Đã thêm {item['name']} vào giỏ hàng!")

            st.markdown("</div>", unsafe_allow_html=True)


# =====================================================
# 10. TRANG ĐẶT BÀN
# =====================================================

elif page == "Đặt bàn":

    st.title("📅 ĐẶT BÀN BBQ HOUSE")
    st.write("Điền thông tin để đặt bàn tại nhà hàng.")

    with st.form("booking_form"):

        name = st.text_input("Họ và tên khách hàng")
        phone = st.text_input("Số điện thoại")

        col1, col2 = st.columns(2)

        with col1:
            booking_date = st.date_input(
                "Ngày đặt bàn",
                value=date.today(),
                min_value=date.today()
            )

        with col2:
            booking_time = st.time_input(
                "Giờ đặt bàn"
            )

        people = st.selectbox(
            "Số lượng khách",
            list(range(1, 21))
        )

        table_type = st.selectbox(
            "Loại bàn",
            [
                "Bàn thường",
                "Bàn gia đình",
                "Bàn nhóm"
            ]
        )

        note = st.text_area("Ghi chú thêm")

        submitted = st.form_submit_button(
            "XÁC NHẬN ĐẶT BÀN",
            use_container_width=True
        )

        if submitted:

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
                    "note": note.strip(),
                    "created_at": datetime.now().strftime(
                        "%d/%m/%Y %H:%M:%S"
                    )
                }

                st.session_state.database[
                    "reservations"
                ].append(reservation)

                save_data()

                st.success("Đặt bàn thành công!")
                st.json(reservation)


# =====================================================
# 11. TRANG GỌI MÓN
# =====================================================

elif page == "Gọi món":

    st.title("🛒 GỌI MÓN TẠI BÀN")

    st.text_input(
        "Tên khách hàng",
        key="customer_name"
    )

    st.selectbox(
        "Chọn bàn",
        [f"Bàn {i:02d}" for i in range(1, 21)],
        key="table_number"
    )

    st.divider()

    st.subheader("Giỏ món của bạn")

    if st.session_state.cart:

        for index, item in enumerate(st.session_state.cart):

            col1, col2, col3 = st.columns([4, 2, 1])

            with col1:
                st.write(f"**{item['name']}**")
                st.caption(item["note"] or "Không có ghi chú")

            with col2:
                st.write(
                    f"{item['quantity']} × {money(item['price'])}"
                )

            with col3:
                if st.button(
                    "Xóa",
                    key=f"remove_cart_{index}"
                ):
                    st.session_state.cart.pop(index)
                    st.rerun()

        st.divider()

        st.markdown(
            f"### Tổng cộng: <span class='price'>{money(cart_total())}</span>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "XÓA TOÀN BỘ GIỎ HÀNG",
                use_container_width=True
            ):
                clear_cart()
                st.rerun()

        with col2:
            if st.button(
                "XÁC NHẬN GỌI MÓN",
                use_container_width=True
            ):

                if not st.session_state.customer_name.strip():
                    st.error("Vui lòng nhập tên khách hàng.")

                else:
                    order_id = create_order()

                    if order_id:
                        st.success(
                            f"Đã tạo đơn hàng {order_id} thành công!"
                        )
                        st.info(
                            "Vào trang Thanh toán để xem và thanh toán hóa đơn."
                        )

    else:
        st.info("Giỏ hàng đang trống. Hãy vào Thực đơn để chọn món.")


# =====================================================
# 12. TRANG THANH TOÁN
# =====================================================

elif page == "Thanh toán":

    st.title("💳 THANH TOÁN HÓA ĐƠN")

    orders = st.session_state.database["orders"]

    if not orders:
        st.info("Chưa có đơn hàng nào.")
    else:

        unpaid = [
            order for order in orders
            if order["status"] == "Chưa thanh toán"
        ]

        if unpaid:

            order_options = {
                f"{order['id']} | {order['customer']} | {money(order['total'])}":
                order["id"]
                for order in unpaid
            }

            selected_label = st.selectbox(
                "Chọn hóa đơn cần thanh toán",
                list(order_options.keys())
            )

            order = find_order(order_options[selected_label])

            if order:

                st.subheader("BBQ HOUSE")
                st.caption("HÓA ĐƠN THANH TOÁN")

                st.write(f"**Mã hóa đơn:** {order['id']}")
                st.write(f"**Khách hàng:** {order['customer']}")
                st.write(f"**Bàn:** {order['table']}")
                st.write(f"**Thời gian:** {order['created_at']}")

                st.divider()

                bill_data = []

                for item in order["items"]:
                    bill_data.append({
                        "Món ăn": item["name"],
                        "Đơn giá": money(item["price"]),
                        "Số lượng": item["quantity"],
                        "Thành tiền": money(
                            item["price"] * item["quantity"]
                        ),
                        "Ghi chú": item.get("note", "")
                    })

                st.dataframe(
                    pd.DataFrame(bill_data),
                    use_container_width=True,
                    hide_index=True
                )

                st.markdown(
                    f"## Tổng thanh toán: <span class='price'>{money(order['total'])}</span>",
                    unsafe_allow_html=True
                )

                payment_method = st.radio(
                    "Phương thức thanh toán",
                    [
                        "Tiền mặt",
                        "Chuyển khoản",
                        "Thẻ ngân hàng"
                    ],
                    horizontal=True
                )

                if st.button(
                    "XÁC NHẬN ĐÃ THANH TOÁN",
                    use_container_width=True
                ):

                    order["status"] = "Đã thanh toán"
                    order["payment_method"] = payment_method
                    order["paid_at"] = datetime.now().strftime(
                        "%d/%m/%Y %H:%M:%S"
                    )

                    save_data()

                    st.success("Thanh toán thành công!")
                    st.rerun()

        else:
            st.success("Không có hóa đơn nào đang chờ thanh toán.")

        st.divider()

        st.subheader("🧾 Xuất hóa đơn")

        paid_orders = [
            order for order in orders
            if order["status"] == "Đã thanh toán"
        ]

        if paid_orders:

            invoice_labels = {
                f"{order['id']} | {order['customer']}":
                order["id"]
                for order in paid_orders
            }

            selected_invoice = st.selectbox(
                "Chọn hóa đơn đã thanh toán",
                list(invoice_labels.keys()),
                key="invoice_select"
            )

            invoice = find_order(
                invoice_labels[selected_invoice]
            )

            if invoice:

                lines = [
                    "BBQ HOUSE",
                    "HOA DON THANH TOAN",
                    "--------------------------------",
                    f"Ma hoa don: {invoice['id']}",
                    f"Khach hang: {invoice['customer']}",
                    f"Ban: {invoice['table']}",
                    f"Thoi gian: {invoice['created_at']}",
                    "--------------------------------",
                ]

                for item in invoice["items"]:
                    lines.append(
                        f"{item['name']} x {item['quantity']}"
                    )
                    lines.append(
                        f"Thanh tien: {money(item['price'] * item['quantity'])}"
                    )

                lines.extend([
                    "--------------------------------",
                    f"TONG CONG: {money(invoice['total'])}",
                    f"Phuong thuc: {invoice['payment_method']}",
                    "TRANG THAI: DA THANH TOAN",
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


# =====================================================
# 13. QUẢN LÝ ĐƠN HÀNG
# =====================================================

elif page == "Quản lý đơn hàng":

    st.title("📋 QUẢN LÝ NHÀ HÀNG")

    tab1, tab2 = st.tabs([
        "Đơn hàng",
        "Đặt bàn"
    ])

    with tab1:

        orders = st.session_state.database["orders"]

        st.subheader("Danh sách đơn hàng")

        if orders:

            for order in reversed(orders):

                with st.expander(
                    f"{order['id']} | {order['customer']} | {money(order['total'])}"
                ):

                    st.write(f"**Bàn:** {order['table']}")
                    st.write(f"**Thời gian:** {order['created_at']}")
                    st.write(f"**Trạng thái:** {order['status']}")

                    if order.get("payment_method"):
                        st.write(
                            f"**Thanh toán:** {order['payment_method']}"
                        )

                    for item in order["items"]:
                        st.write(
                            f"- {item['name']} x {item['quantity']} "
                            f"= {money(item['price'] * item['quantity'])}"
                        )

                    st.markdown(
                        f"**Tổng tiền: {money(order['total'])}**"
                    )

        else:
            st.info("Chưa có đơn hàng.")

    with tab2:

        reservations = st.session_state.database["reservations"]

        st.subheader("Danh sách đặt bàn")

        if reservations:

            for reservation in reversed(reservations):

                with st.expander(
                    f"{reservation['name']} | {reservation['date']} | {reservation['time']}"
                ):

                    st.write(f"**Mã đặt bàn:** {reservation['id']}")
                    st.write(f"**Điện thoại:** {reservation['phone']}")
                    st.write(f"**Số khách:** {reservation['people']}")
                    st.write(f"**Loại bàn:** {reservation['table_type']}")
                    st.write(f"**Ghi chú:** {reservation['note']}")

        else:
            st.info("Chưa có lượt đặt bàn.")


# =====================================================
# 14. TRANG DOANH THU
# =====================================================

elif page == "Doanh thu":

    st.title("📊 THỐNG KÊ DOANH THU")

    orders = st.session_state.database["orders"]

    paid_orders = [
        order for order in orders
        if order["status"] == "Đã thanh toán"
    ]

    today_string = date.today().strftime("%d/%m/%Y")

    period = st.selectbox(
        "Thời gian thống kê",
        [
            "Tất cả",
            "Hôm nay",
            "7 ngày gần nhất",
            "30 ngày gần nhất"
        ]
    )

    def parse_datetime(order):
        try:
            return datetime.strptime(
                order["paid_at"],
                "%d/%m/%Y %H:%M:%S"
            )
        except (KeyError, ValueError):
            return None

    filtered_orders = []

    for order in paid_orders:

        paid_date = parse_datetime(order)

        if not paid_date:
            continue

        days = (date.today() - paid_date.date()).days

        if period == "Tất cả":
            filtered_orders.append(order)

        elif period == "Hôm nay" and days == 0:
            filtered_orders.append(order)

        elif period == "7 ngày gần nhất" and 0 <= days < 7:
            filtered_orders.append(order)

        elif period == "30 ngày gần nhất" and 0 <= days < 30:
            filtered_orders.append(order)

    total_revenue = sum(
        order["total"] for order in filtered_orders
    )

    total_orders = len(filtered_orders)

    total_items = sum(
        item["quantity"]
        for order in filtered_orders
        for item in order["items"]
    )

    average = (
        total_revenue / total_orders
        if total_orders else 0
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "💰 Tổng doanh thu",
            money(total_revenue)
        )

    with col2:
        st.metric(
            "🧾 Số đơn đã thanh toán",
            total_orders
        )

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "🍽️ Số món đã bán",
            total_items
        )

    with col4:
        st.metric(
            "📈 Giá trị đơn trung bình",
            money(average)
        )

    st.divider()

    st.subheader("🏆 Món bán chạy")

    sold_items = {}

    for order in filtered_orders:
        for item in order["items"]:
            sold_items[item["name"]] = (
                sold_items.get(item["name"], 0)
                + item["quantity"]
            )

    if sold_items:

        best_sellers = pd.DataFrame(
            [
                {
                    "Tên món": name,
                    "Số lượng bán": quantity
                }
                for name, quantity in sold_items.items()
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
        st.info("Chưa có dữ liệu bán hàng trong khoảng thời gian này.")

    st.divider()

    st.subheader("📄 Chi tiết giao dịch")

    if filtered_orders:

        revenue_data = []

        for order in filtered_orders:
            revenue_data.append({
                "Mã đơn": order["id"],
                "Khách hàng": order["customer"],
                "Bàn": order["table"],
                "Ngày thanh toán": order.get("paid_at", ""),
                "Phương thức": order.get("payment_method", ""),
                "Tổng tiền": order["total"]
            })

        revenue_df = pd.DataFrame(revenue_data)

        st.dataframe(
            revenue_df,
            use_container_width=True,
            hide_index=True
        )

        csv_data = revenue_df.to_csv(
            index=False
        ).encode("utf-8-sig")

        st.download_button(
            "⬇️ XUẤT BÁO CÁO DOANH THU CSV",
            data=csv_data,
            file_name="bao_cao_doanh_thu.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:
        st.info("Chưa có giao dịch thanh toán trong khoảng thời gian này.")


# =====================================================
# 15. CHÂN TRANG
# =====================================================

st.divider()

st.markdown("""
<div style="
    text-align:center;
    padding:20px;
    color:#999999;
">
    <h3 style="color:#ff7029;">🔥 BBQ HOUSE</h3>
    <p>GRILL • HOTPOT • ENJOY</p>
    <p>Trải nghiệm ẩm thực - Kết nối mọi khoảnh khắc</p>
    <small>© 2026 BBQ HOUSE. All rights reserved.</small>
</div>
""", unsafe_allow_html=True)
