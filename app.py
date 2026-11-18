
import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from urllib.parse import quote

# =========================================================
# BBQ HOUSE - APP QUAN LY GOI MON VA THANH TOAN
# =========================================================

st.set_page_config(
    page_title="BBQ HOUSE | Nhà hàng nướng",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ========================= GIAO DIEN ======================

st.markdown("""
<style>
.stApp {
    background: #101713;
    color: #f5f0e7;
}
header[data-testid="stHeader"] {
    background: rgba(16, 23, 19, 0.95);
}
h1, h2, h3, h4, p, label, .stMarkdown {
    color: #f5f0e7;
}
section[data-testid="stSidebar"] {
    background: #192820;
}
div[data-testid="stMetric"] {
    background: #1b2a21;
    border: 1px solid #34483a;
    padding: 12px;
    border-radius: 12px;
}
div[data-testid="stMetric"] label {
    color: #d7cbbb !important;
}
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #ffb36b !important;
}
.food-card {
    background: #1b2921;
    border: 1px solid #34483a;
    border-radius: 16px;
    padding: 12px;
    min-height: 100px;
}
.price {
    color: #ffb36b;
    font-size: 21px;
    font-weight: 800;
}
.hero {
    background: linear-gradient(115deg, #173d2d, #315b43);
    border: 1px solid #52745d;
    border-radius: 20px;
    padding: 36px 18px;
    text-align: center;
}
.hero h1 {
    color: #ffd09b !important;
    font-size: clamp(36px, 6vw, 58px);
    letter-spacing: 2px;
}
.hero p {
    color: #fff5e8 !important;
}
.section-note {
    color: #cbbda9;
}
.footer-box {
    background: #173b2d;
    border: 1px solid #365a45;
    border-radius: 18px;
    padding: 28px;
}
div.stButton > button {
    background: #d85b35;
    color: #ffffff;
    border: 0;
    border-radius: 10px;
    font-weight: 700;
    min-height: 42px;
}
div.stButton > button:hover {
    background: #f0784e;
    color: #ffffff;
}
a {
    color: #ffd09b !important;
}
hr {
    border-color: #3b5143;
}
</style>
""", unsafe_allow_html=True)


# ========================= HINH ANH =======================

def food_image(keyword):
    return f"https://loremflickr.com/900/650/{quote(keyword)}"


# ========================= THUC DON =======================

MENU = [
    {
        "name": "Ba chỉ bò Mỹ",
        "category": "Thịt bò",
        "price": 129000,
        "desc": "Ba chỉ bò Mỹ thái lát mỏng, mềm thơm.",
        "image": food_image("raw beef belly slices korean bbq")
    },
    {
        "name": "Bò cuộn nấm kim châm",
        "category": "Thịt bò",
        "price": 119000,
        "desc": "Thịt bò cuộn nấm kim châm tươi.",
        "image": food_image("beef enoki mushroom rolls")
    },
    {
        "name": "Dẻ sườn bò Mỹ",
        "category": "Thịt bò",
        "price": 159000,
        "desc": "Dẻ sườn bò tẩm sốt BBQ đậm đà.",
        "image": food_image("grilled beef short ribs barbecue")
    },
    {
        "name": "Ba chỉ heo",
        "category": "Thịt heo",
        "price": 85000,
        "desc": "Ba chỉ heo thái lát dùng để nướng.",
        "image": food_image("pork belly slices korean barbecue")
    },
    {
        "name": "Sườn heo BBQ",
        "category": "Thịt heo",
        "price": 139000,
        "desc": "Sườn heo nướng phủ sốt BBQ.",
        "image": food_image("barbecue pork ribs glazed")
    },
    {
        "name": "Nạc vai heo",
        "category": "Thịt heo",
        "price": 89000,
        "desc": "Nạc vai heo tươi, ướp gia vị.",
        "image": food_image("grilled pork shoulder slices")
    },
    {
        "name": "Gà nướng mật ong",
        "category": "Thịt gà",
        "price": 99000,
        "desc": "Gà nướng vàng óng với sốt mật ong.",
        "image": food_image("honey glazed grilled chicken")
    },
    {
        "name": "Mực nướng sa tế",
        "category": "Hải sản",
        "price": 129000,
        "desc": "Mực nướng phủ sa tế đỏ, cay thơm.",
        "image": food_image("grilled squid spicy chili sauce")
    },
    {
        "name": "Tôm nướng muối ớt",
        "category": "Hải sản",
        "price": 139000,
        "desc": "Tôm nướng muối ớt thơm cay.",
        "image": food_image("grilled prawns chili salt")
    },
    {
        "name": "Bạch tuộc nướng",
        "category": "Hải sản",
        "price": 149000,
        "desc": "Bạch tuộc nướng thơm, dai giòn.",
        "image": food_image("grilled octopus tentacles")
    },
    {
        "name": "Cá hồi nướng",
        "category": "Hải sản",
        "price": 169000,
        "desc": "Cá hồi nướng sốt bơ chanh.",
        "image": food_image("grilled salmon fillet lemon")
    },
    {
        "name": "Salad trộn",
        "category": "Món ăn kèm",
        "price": 45000,
        "desc": "Xà lách, cà chua bi, dưa leo và sốt salad.",
        "image": food_image("fresh mixed garden salad bowl")
    },
    {
        "name": "Kim chi",
        "category": "Món ăn kèm",
        "price": 25000,
        "desc": "Kim chi cải thảo chua cay.",
        "image": food_image("korean napa cabbage kimchi")
    },
    {
        "name": "Khoai tây chiên",
        "category": "Món ăn kèm",
        "price": 35000,
        "desc": "Khoai tây chiên vàng giòn.",
        "image": food_image("golden french fries in bowl")
    },
    {
        "name": "Cơm chiên trứng",
        "category": "Món ăn kèm",
        "price": 45000,
        "desc": "Cơm chiên trứng nóng hổi.",
        "image": food_image("egg fried rice bowl")
    },
    {
        "name": "Lẩu kim chi",
        "category": "Lẩu",
        "price": 229000,
        "desc": "Lẩu kim chi chua cay, phù hợp 2-3 người.",
        "image": food_image("korean kimchi hot pot stew")
    },
    {
        "name": "Lẩu nấm",
        "category": "Lẩu",
        "price": 219000,
        "desc": "Nước lẩu nấm thanh ngọt.",
        "image": food_image("mushroom hot pot soup")
    },
    {
        "name": "Coca-Cola",
        "category": "Đồ uống",
        "price": 18000,
        "desc": "Nước ngọt có gas ướp lạnh.",
        "image": food_image("cola soda glass ice")
    },
    {
        "name": "Trà đào",
        "category": "Đồ uống",
        "price": 30000,
        "desc": "Trà đào mát lạnh.",
        "image": food_image("peach iced tea glass")
    },
    {
        "name": "Nước suối",
        "category": "Đồ uống",
        "price": 12000,
        "desc": "Nước suối đóng chai.",
        "image": food_image("bottled mineral water")
    },
]


# ========================= HAM HO TRO =====================

def money(value):
    return f"{int(value):,}".replace(",", ".") + "đ"


def get_subtotal(items):
    return sum(
        item["price"] * item["qty"]
        for item in items
    )


# ========================= SESSION ========================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None

if "booking_message" not in st.session_state:
    st.session_state.booking_message = ""


# ========================= HEADER =========================

st.markdown("""
<div class="hero">
    <h1>🔥 BBQ HOUSE</h1>
    <p style="font-size:18px; letter-spacing:3px;">
        THE ART OF BBQ
    </p>
    <p>
        Nướng ngon chuẩn vị · Không gian ấm cúng · Trọn vẹn cuộc vui
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

nav = st.columns(5)

nav_labels = [
    ("🏠 Trang chủ", "#trang-chu"),
    ("🌿 Về chúng tôi", "#ve-bbq-house"),
    ("🍖 Thực đơn", "#menu"),
    ("📅 Đặt bàn", "#dat-ban"),
    ("☎ Liên hệ", "#lien-he"),
]

for col, (label, anchor) in zip(nav, nav_labels):
    with col:
        st.markdown(f"[{label}]({anchor})")

st.divider()


# ========================= GIOI THIEU ======================

st.markdown(
    '<div id="trang-chu"></div>',
    unsafe_allow_html=True
)

st.markdown("## CHÀO MỪNG ĐẾN VỚI BBQ HOUSE")

st.markdown("""
Tận hưởng những món nướng hấp dẫn, nguyên liệu được chuẩn bị
chu đáo và những khoảnh khắc vui vẻ bên gia đình, bạn bè.
""")

st.markdown(
    '<div id="ve-bbq-house"></div>',
    unsafe_allow_html=True
)

feature_cols = st.columns(3)

features = [
    (
        "🔥",
        "MÓN NƯỚNG HẤP DẪN",
        "Thực đơn đa dạng từ thịt bò, thịt heo đến hải sản."
    ),
    (
        "🥗",
        "MÓN ĂN ĐI KÈM",
        "Salad, món ăn kèm và đồ uống cho bữa ăn trọn vị."
    ),
    (
        "🥢",
        "TRẢI NGHIỆM ẤM CÚNG",
        "Phù hợp cho những buổi gặp gỡ và sum họp."
    ),
]

for col, (emoji, title, desc) in zip(feature_cols, features):
    with col:
        st.markdown(f"### {emoji} {title}")
        st.caption(desc)

st.divider()


# ========================= DAT BAN ========================

st.markdown(
    '<div id="dat-ban"></div>',
    unsafe_allow_html=True
)

st.header("📅 ĐẶT BÀN")

st.caption(
    "Điền thông tin để gửi yêu cầu đặt bàn. "
    "Đây là biểu mẫu demo, chưa kết nối hệ thống đặt bàn thật."
)

with st.form("booking_form"):

    b1, b2 = st.columns(2)

    with b1:
        booking_name = st.text_input("Họ và tên")
        booking_phone = st.text_input("Số điện thoại")

    with b2:
        booking_date = st.date_input(
            "Ngày đến",
            min_value=date.today()
        )
        booking_time = st.time_input(
            "Giờ đến",
            value=time(18, 30)
        )

    booking_guests = st.number_input(
        "Số lượng khách",
        min_value=1,
        max_value=30,
        value=2
    )

    booking_note = st.text_area(
        "Ghi chú",
        placeholder="Ví dụ: cần ghế trẻ em, sinh nhật..."
    )

    booking_submit = st.form_submit_button(
        "GỬI YÊU CẦU ĐẶT BÀN",
        use_container_width=True
    )

if booking_submit:

    if not booking_name.strip() or not booking_phone.strip():
        st.warning("Vui lòng nhập họ tên và số điện thoại.")

    else:
        st.session_state.booking_message = (
            f"Đã ghi nhận yêu cầu của {booking_name}, "
            f"{booking_guests} khách, ngày "
            f"{booking_date.strftime('%d/%m/%Y')} "
            f"lúc {booking_time.strftime('%H:%M')}. "
            "Đây là bản demo, nhà hàng cần xác nhận riêng."
        )

        st.success(st.session_state.booking_message)

st.divider()


# ========================= THUC DON =======================

st.markdown(
    '<div id="menu"></div>',
    unsafe_allow_html=True
)

st.header("🍖 THỰC ĐƠN BBQ HOUSE")

st.caption(
    "Giá trong ứng dụng là giá tham khảo và có thể chỉnh sửa "
    "trong danh sách MENU của code."
)

categories = ["Tất cả"] + list(
    dict.fromkeys(x["category"] for x in MENU)
)

filter_col, search_col = st.columns([1, 2])

with filter_col:
    selected_category = st.selectbox(
        "Chọn danh mục",
        categories
    )

with search_col:
    keyword = st.text_input(
        "Tìm món ăn",
        placeholder="Nhập tên món cần tìm..."
    )

filtered_menu = [
    item for item in MENU
    if (
        selected_category == "Tất cả"
        or item["category"] == selected_category
    )
    and keyword.lower() in item["name"].lower()
]

if not filtered_menu:
    st.info("Không tìm thấy món ăn phù hợp.")


# ========================= THE HIEN MON ===================

for start in range(0, len(filtered_menu), 3):

    card_cols = st.columns(3)

    for col, item in zip(
        card_cols,
        filtered_menu[start:start + 3]
    ):

        with col:

            st.markdown(
                '<div class="food-card">',
                unsafe_allow_html=True
            )

            try:
                st.image(
                    item["image"],
                    use_container_width=True
                )
            except Exception:
                st.markdown("## 🍽️")

            st.markdown(f"### {item['name']}")
            st.caption(item["desc"])

            st.markdown(
                f'<div class="price">{money(item["price"])}</div>',
                unsafe_allow_html=True
            )

            qty = st.number_input(
                "Số lượng",
                min_value=1,
                max_value=50,
                value=1,
                step=1,
                key=f"qty_{item['name']}"
            )

            if st.button(
                "＋ THÊM VÀO GIỎ",
                key=f"add_{item['name']}",
                use_container_width=True
            ):

                existing = next(
                    (
                        x for x in st.session_state.cart
                        if x["name"] == item["name"]
                    ),
                    None
                )

                if existing:
                    existing["qty"] += int(qty)

                else:
                    st.session_state.cart.append({
                        "name": item["name"],
                        "price": item["price"],
                        "qty": int(qty),
                    })

                st.toast(
                    f"Đã thêm {item['name']} vào giỏ hàng"
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

            st.write("")


# ========================= THONG TIN HOA DON ==============

st.markdown("#### Thông tin khách hàng cho hóa đơn")

customer_name_for_order = st.text_input(
    "Tên khách hàng trên hóa đơn",
    key="invoice_customer",
    placeholder="Nhập tên khách hàng"
)

table_for_order = st.text_input(
    "Số bàn (nếu có)",
    key="invoice_table",
    placeholder="Ví dụ: Bàn 05"
)


# ========================= GIO HANG =======================

st.divider()
st.header("🛒 GIỎ HÀNG")

if st.session_state.cart:

    for index, item in enumerate(st.session_state.cart):

        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])

        c1.write(item["name"])
        c2.write(f"x {item['qty']}")
        c3.write(
            money(item["price"] * item["qty"])
        )

        if c4.button(
            "Xóa",
            key=f"delete_{index}"
        ):
            st.session_state.cart.pop(index)
            st.rerun()

    subtotal = get_subtotal(st.session_state.cart)

    tax = round(subtotal * 0.08)
    total = subtotal + tax

    m1, m2, m3 = st.columns(3)

    m1.metric("Tạm tính", money(subtotal))
    m2.metric("VAT 8% (tham khảo)", money(tax))
    m3.metric("Tổng thanh toán", money(total))

    clear_col, pay_col = st.columns(2)

    with clear_col:

        if st.button(
            "🧹 XÓA TOÀN BỘ GIỎ",
            use_container_width=True
        ):
            st.session_state.cart = []
            st.rerun()

    with pay_col:

        if st.button(
            "💳 XÁC NHẬN THANH TOÁN",
            type="primary",
            use_container_width=True
        ):

            if not customer_name_for_order.strip():

                st.warning(
                    "Vui lòng nhập tên khách hàng "
                    "trước khi thanh toán."
                )

            else:

                st.session_state.invoice = {
                    "code": "BBQ" + datetime.now().strftime(
                        "%Y%m%d%H%M%S"
                    ),
                    "date": datetime.now().strftime(
                        "%d/%m/%Y %H:%M:%S"
                    ),
                    "customer": customer_name_for_order.strip(),
                    "table": table_for_order.strip() or "Chưa chọn",
                    "items": [
                        dict(x)
                        for x in st.session_state.cart
                    ],
                    "subtotal": subtotal,
                    "tax": tax,
                    "total": total,
                }

                st.session_state.cart = []
                st.rerun()

else:

    st.info(
        "Giỏ hàng đang trống. Hãy chọn món trong thực đơn."
    )


# ========================= HOA DON ========================

if st.session_state.invoice:

    invoice = st.session_state.invoice

    st.divider()
    st.header("🧾 HÓA ĐƠN THANH TOÁN")

    st.markdown("## 🔥 BBQ HOUSE")

    st.write(f"**Mã hóa đơn:** {invoice['code']}")
    st.write(f"**Thời gian:** {invoice['date']}")
    st.write(f"**Khách hàng:** {invoice['customer']}")
    st.write(f"**Số bàn:** {invoice['table']}")

    invoice_rows = []

    for item in invoice["items"]:

        invoice_rows.append({
            "Tên món": item["name"],
            "Đơn giá": money(item["price"]),
            "Số lượng": item["qty"],
            "Thành tiền": money(
                item["price"] * item["qty"]
            ),
        })

    st.dataframe(
        pd.DataFrame(invoice_rows),
        use_container_width=True,
        hide_index=True
    )

    st.write(
        f"**Tạm tính:** {money(invoice['subtotal'])}"
    )

    st.write(
        f"**VAT 8%:** {money(invoice['tax'])}"
    )

    st.markdown(
        f"## Tổng cộng: {money(invoice['total'])}"
    )

    invoice_text = (
        "BBQ HOUSE\n"
        f"Ma hoa don: {invoice['code']}\n"
        f"Thoi gian: {invoice['date']}\n"
        f"Khach hang: {invoice['customer']}\n"
        f"So ban: {invoice['table']}\n\n"
        + "\n".join(
            f"{x['name']} x{x['qty']} = "
            f"{money(x['price'] * x['qty'])}"
            for x in invoice["items"]
        )
        + f"\n\nTam tinh: {money(invoice['subtotal'])}"
        + f"\nVAT 8%: {money(invoice['tax'])}"
        + f"\nTONG CONG: {money(invoice['total'])}"
        + "\nCam on quy khach!"
    )

    st.download_button(
        "⬇️ TẢI HÓA ĐƠN TXT",
        data=invoice_text,
        file_name=f"{invoice['code']}.txt",
        mime="text/plain",
        use_container_width=True,
    )

    csv_data = pd.DataFrame(invoice_rows).to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "⬇️ TẢI CHI TIẾT HÓA ĐƠN CSV",
        data=csv_data,
        file_name=f"{invoice['code']}.csv",
        mime="text/csv",
        use_container_width=True,
    )

    if st.button("TẠO HÓA ĐƠN MỚI"):

        st.session_state.invoice = None
        st.rerun()


# ========================= CUOI TRANG =====================

st.divider()

st.markdown(
    '<div id="lien-he"></div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="footer-box">

<h2 style="color:#ffbd79">🔥 BBQ HOUSE</h2>

<p>THE ART OF BBQ</p>

<p>
Nướng ngon chuẩn vị - Trọn vẹn từng khoảnh khắc.
</p>

<hr>

<h3 style="color:#ffbd79">KHÁM PHÁ BBQ HOUSE</h3>

<p>01　TRANG CHỦ</p>
<p>02　VỀ BBQ HOUSE</p>
<p>03　THỰC ĐƠN</p>
<p>04　ĐẶT BÀN</p>
<p>05　ƯU ĐÃI - SỰ KIỆN</p>
<p>06　TUYỂN DỤNG</p>

<hr>

<h3 style="color:#ffbd79">LIÊN HỆ</h3>

<p>Hotline: [Cập nhật số điện thoại nhà hàng]</p>
<p>Email: [Cập nhật email nhà hàng]</p>

<hr>

<h3 style="color:#ffbd79">KẾT NỐI VỚI CHÚNG TÔI</h3>

<p>
<a href="https://facebook.com">Facebook</a>　|　
<a href="https://instagram.com">Instagram</a>　|　
<a href="https://tiktok.com">TikTok</a>
</p>

<hr>

<p style="text-align:center">
© 2026 BBQ HOUSE. ALL RIGHTS RESERVED.
</p>

</div>
""", unsafe_allow_html=True)

st.caption(
    "BBQ HOUSE • Website demo quản lý gọi món và lập hóa đơn."
)
