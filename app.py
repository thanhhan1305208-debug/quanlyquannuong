
import streamlit as st
import pandas as pd
import json
import os
from datetime import date, time, datetime, timedelta

# =====================================================
# 1. CẤU HÌNH
# =====================================================

st.set_page_config(
    page_title="BBQ HOUSE",
    page_icon="🔥",
    layout="wide"
)

DATA_FILE = "bbq_data.json"

# =====================================================
# 2. LƯU DỮ LIỆU
# =====================================================

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"orders": [], "reservations": []}


def save_data():
    data = {
        "orders": st.session_state.order_history,
        "reservations": st.session_state.reservations
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


saved_data = load_data()

if "order_history" not in st.session_state:
    st.session_state.order_history = saved_data["orders"]

if "reservations" not in st.session_state:
    st.session_state.reservations = saved_data["reservations"]

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "current_order" not in st.session_state:
    st.session_state.current_order = None


# =====================================================
# 3. GIAO DIỆN
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Be Vietnam Pro', sans-serif;
}

.stApp {
    background: #111111;
    color: white;
}

section[data-testid="stSidebar"] {
    background: #191919;
    border-right: 1px solid #333;
}

.hero {
    background: linear-gradient(120deg,#351707,#111);
    padding: 35px;
    border-radius: 18px;
    border: 1px solid #80401d;
}

.hero h1 {
    color: #ff852e;
    font-size: 42px;
    font-weight: 800;
}

.section-title {
    color: #ff852e;
    font-size: 26px;
    font-weight: 800;
}

.food-card {
    background: #202020;
    border: 1px solid #393939;
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 15px;
}

.food-name {
    color: white;
    font-weight: 700;
    font-size: 17px;
}

.food-price {
    color: #ff852e;
    font-weight: 800;
    font-size: 19px;
}

.total-box {
    background: #28170f;
    border: 1px solid #a64d1b;
    padding: 20px;
    border-radius: 13px;
}

div.stButton > button {
    background: #e66b20;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: 700;
}

div.stButton > button:hover {
    background: #ff852e;
    color: white;
}

div[data-testid="stMetric"] {
    background: #202020;
    border: 1px solid #393939;
    border-radius: 12px;
    padding: 15px;
}

.footer {
    text-align: center;
    padding: 25px;
    color: #888;
    border-top: 1px solid #333;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# 4. THỰC ĐƠN
# =====================================================

IMG = {
    "Ba chỉ bò Mỹ": "https://images.unsplash.com/photo-1544025162-d76694265947?w=900",
    "Bò cuộn nấm kim châm": "https://images.unsplash.com/photo-1558030006-450675393462?w=900",
    "Dẻ sườn bò Mỹ": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=900",
    "Ba chỉ heo": "https://images.unsplash.com/photo-1602470520998-f4a52199a3d6?w=900",
    "Sườn heo BBQ": "https://images.unsplash.com/photo-1544025162-d76694265947?w=900",
    "Nạc vai heo": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=900",
    "Gà nướng mật ong": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=900",
    "Mực nướng sa tế": "https://mrbarker.sg/cdn/shop/files/hex8703_grilled_squid_sambal_squid_BBQ_professional_photography_9132e3db-f974-4283-a16e-1fb735fc8f1f.png?v=1727772355",
    "Tôm nướng muối ớt": "https://images.unsplash.com/photo-1559737558-2f5a35f4523b?w=900",
    "Bạch tuộc nướng": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=900",
    "Cá hồi nướng": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=900",
    "Salad trộn": "https://d1w7312wesee68.cloudfront.net/C5l584AzlzC7Foc6mlHEuFKEimRHKHCIXrnBWrrMsEE/resize%3Afit%3A720%3A720/plain/s3%3A/toasttab/restaurants/restaurant-18174000000000000/menu/items/4/item-400000000001664564_1770408980.png",
    "Kim chi": "https://images.unsplash.com/photo-1583224994255-5f1a1e0b7c5e?w=900",
    "Khoai tây chiên": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=900",
    "Cơm chiên trứng": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=900",
    "Lẩu kim chi": "https://images.unsplash.com/photo-1547592180-85f173990554?w=900",
    "Lẩu nấm": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=900",
    "Coca-Cola": "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=900",
    "Trà đào": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=900",
    "Nước suối": "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=900"
}

MENU = [
    {"name":"Ba chỉ bò Mỹ","category":"Thịt bò","price":129000,"desc":"Ba chỉ bò Mỹ mềm, thơm"},
    {"name":"Bò cuộn nấm kim châm","category":"Thịt bò","price":119000,"desc":"Bò cuộn nấm tươi"},
    {"name":"Dẻ sườn bò Mỹ","category":"Thịt bò","price":159000,"desc":"Dẻ sườn bò đậm vị"},
    {"name":"Ba chỉ heo","category":"Thịt heo","price":85000,"desc":"Ba chỉ heo tươi ngon"},
    {"name":"Sườn heo BBQ","category":"Thịt heo","price":139000,"desc":"Sườn heo sốt BBQ"},
    {"name":"Nạc vai heo","category":"Thịt heo","price":89000,"desc":"Nạc vai thái lát"},
    {"name":"Gà nướng mật ong","category":"Hải sản & Gà","price":99000,"desc":"Gà ướp mật ong"},
    {"name":"Mực nướng sa tế","category":"Hải sản & Gà","price":129000,"desc":"Mực tươi nướng sa tế"},
    {"name":"Tôm nướng muối ớt","category":"Hải sản & Gà","price":139000,"desc":"Tôm nướng muối ớt"},
    {"name":"Bạch tuộc nướng","category":"Hải sản & Gà","price":149000,"desc":"Bạch tuộc nướng"},
    {"name":"Cá hồi nướng","category":"Hải sản & Gà","price":169000,"desc":"Cá hồi nướng"},
    {"name":"Salad trộn","category":"Món ăn kèm","price":45000,"desc":"Rau xanh và sốt salad"},
    {"name":"Kim chi","category":"Món ăn kèm","price":25000,"desc":"Kim chi Hàn Quốc"},
    {"name":"Khoai tây chiên","category":"Món ăn kèm","price":35000,"desc":"Khoai tây chiên giòn"},
    {"name":"Cơm chiên trứng","category":"Món ăn kèm","price":45000,"desc":"Cơm chiên trứng nóng"},
    {"name":"Lẩu kim chi","category":"Lẩu","price":229000,"desc":"Lẩu kim chi cay thơm"},
    {"name":"Lẩu nấm","category":"Lẩu","price":219000,"desc":"Lẩu nấm thanh ngọt"},
    {"name":"Coca-Cola","category":"Đồ uống","price":18000,"desc":"Nước ngọt có gas"},
    {"name":"Trà đào","category":"Đồ uống","price":30000,"desc":"Trà đào thơm mát"},
    {"name":"Nước suối","category":"Đồ uống","price":12000,"desc":"Nước suối đóng chai"}
]


# =====================================================
# 5. HÀM HỖ TRỢ
# =====================================================

def money(n):
    return f"{n:,.0f}đ".replace(",", ".")


def cart_total(cart):
    return sum(x["price"] * x["qty"] for x in cart.values())


def order_date(order):
    try:
        return datetime.strptime(order["time"], "%d/%m/%Y %H:%M").date()
    except Exception:
        return date.today()


def revenue_data():
    return [
        x for x in st.session_state.order_history
        if x.get("paid") is True
    ]


# =====================================================
# 6. MENU ĐIỀU HƯỚNG
# =====================================================

with st.sidebar:
    st.markdown("# 🔥 BBQ HOUSE")
    st.caption("RESTAURANT MANAGEMENT")
    page = st.radio(
        "MENU",
        [
            "🏠 Trang chủ",
            "📖 Thực đơn",
            "📅 Đặt bàn",
            "🛒 Order món",
            "💳 Thanh toán",
            "📋 Quản lý đơn",
            "📊 Doanh thu"
        ]
    )
    st.divider()
    st.caption("Hotline: 0900 123 456")
    st.caption("10:00 - 22:00")


# =====================================================
# 7. TRANG CHỦ
# =====================================================

if page == "🏠 Trang chủ":

    st.markdown("""
    <div class="hero">
        <h1>🔥 BBQ HOUSE</h1>
        <h2>THE TASTE OF GREAT BBQ</h2>
        <p>Thưởng thức hương vị BBQ tuyệt vời cùng những món ăn hấp dẫn.</p>
        <p>Không gian ấm cúng – Thực đơn phong phú – Phục vụ tận tâm.</p>
    </div>
    """, unsafe_allow_html=True)

    a, b, c = st.columns(3)
    a.metric("Số món ăn", "20+")
    b.metric("Danh mục", "6")
    c.metric("Phong cách", "Korean BBQ")

    st.markdown("## ⭐ MÓN ĂN NỔI BẬT")

    cols = st.columns(3)

    for col, name in zip(cols, ["Ba chỉ bò Mỹ","Mực nướng sa tế","Sườn heo BBQ"]):
        item = next(x for x in MENU if x["name"] == name)
        with col:
            st.image(IMG[name], use_container_width=True)
            st.write(f"**{name}**")
            st.markdown(f"<h3 style='color:#ff852e'>{money(item['price'])}</h3>", unsafe_allow_html=True)


# =====================================================
# 8. THỰC ĐƠN
# =====================================================

elif page == "📖 Thực đơn":

    st.markdown('<div class="section-title">📖 THỰC ĐƠN BBQ HOUSE</div>', unsafe_allow_html=True)

    categories = ["Tất cả"] + list(dict.fromkeys(x["category"] for x in MENU))
    category = st.selectbox("Danh mục", categories)
    keyword = st.text_input("🔍 Tìm món ăn")

    filtered = [
        x for x in MENU
        if (category == "Tất cả" or x["category"] == category)
        and keyword.lower() in x["name"].lower()
    ]

    cols = st.columns(3)

    for i, item in enumerate(filtered):
        with cols[i % 3]:
            st.markdown('<div class="food-card">', unsafe_allow_html=True)
            try:
                st.image(IMG[item["name"]], use_container_width=True)
            except Exception:
                st.caption("Ảnh chưa tải được.")
            st.markdown(f'<div class="food-name">{item["name"]}</div>', unsafe_allow_html=True)
            st.caption(item["desc"])
            st.markdown(f'<div class="food-price">{money(item["price"])}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


# =====================================================
# 9. ĐẶT BÀN
# =====================================================

elif page == "📅 Đặt bàn":

    st.markdown('<div class="section-title">📅 ĐẶT BÀN</div>', unsafe_allow_html=True)

    with st.form("booking"):

        name = st.text_input("Tên khách hàng")
        phone = st.text_input("Số điện thoại")

        c1, c2 = st.columns(2)

        with c1:
            booking_date = st.date_input("Ngày đặt", min_value=date.today())

        with c2:
            booking_time = st.time_input("Giờ đến", value=time(18, 0))

        people = st.selectbox("Số lượng khách", range(1, 21))
        table_type = st.selectbox("Loại bàn", ["Bàn thường","Bàn gia đình","Bàn nhóm"])
        note = st.text_area("Ghi chú")

        submit = st.form_submit_button("XÁC NHẬN ĐẶT BÀN", use_container_width=True)

        if submit:
            if not name.strip() or not phone.strip():
                st.error("Vui lòng nhập tên và số điện thoại.")
            else:
                st.session_state.reservations.append({
                    "name":name,
                    "phone":phone,
                    "date":str(booking_date),
                    "time":str(booking_time),
                    "people":people,
                    "table_type":table_type,
                    "note":note
                })
                save_data()
                st.success("Đặt bàn thành công!")


# =====================================================
# 10. ORDER MÓN
# =====================================================

elif page == "🛒 Order món":

    st.markdown('<div class="section-title">🛒 ORDER MÓN ĂN</div>', unsafe_allow_html=True)

    if st.session_state.current_order is not None:
        st.warning("Đang có đơn hàng chưa thanh toán. Vui lòng thanh toán trước.")
    else:
        c1, c2 = st.columns(2)

        with c1:
            customer = st.text_input("Tên khách hàng", key="customer")

        with c2:
            table = st.selectbox("Chọn bàn", [f"Bàn {i}" for i in range(1,21)])

        categories = ["Tất cả"] + list(dict.fromkeys(x["category"] for x in MENU))
        category = st.selectbox("Danh mục", categories, key="order_category")
        keyword = st.text_input("Tìm món", key="order_keyword")

        filtered = [
            x for x in MENU
            if (category == "Tất cả" or x["category"] == category)
            and keyword.lower() in x["name"].lower()
        ]

        cols = st.columns(3)

        for i, item in enumerate(filtered):
            with cols[i % 3]:
                st.markdown('<div class="food-card">', unsafe_allow_html=True)
                try:
                    st.image(IMG[item["name"]], use_container_width=True)
                except Exception:
                    st.caption("Ảnh chưa tải được.")
                st.markdown(f'<div class="food-name">{item["name"]}</div>', unsafe_allow_html=True)
                st.caption(item["desc"])
                st.markdown(f'<div class="food-price">{money(item["price"])}</div>', unsafe_allow_html=True)

                qty = st.number_input("Số lượng", 1, 50, 1, key=f"qty_{item['name']}")

                if st.button("➕ THÊM MÓN", key=f"add_{item['name']}", use_container_width=True):
                    key = item["name"]
                    if key in st.session_state.cart:
                        st.session_state.cart[key]["qty"] += qty
                    else:
                        st.session_state.cart[key] = {
                            "name":key,
                            "price":item["price"],
                            "qty":qty,
                            "note":""
                        }
                    st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("## 🧺 GIỎ HÀNG")

        if st.session_state.cart:
            for key in list(st.session_state.cart.keys()):
                item = st.session_state.cart[key]

                with st.container(border=True):
                    c1, c2, c3 = st.columns([3,1,1])
                    c1.write(f"**{key}**")
                    c1.caption(money(item["price"]))

                    new_qty = c2.number_input(
                        "SL",
                        1,50,
                        item["qty"],
                        key=f"cart_{key}"
                    )

                    st.session_state.cart[key]["qty"] = new_qty
                    c3.write(money(item["price"] * new_qty))

                    note = st.text_input("Ghi chú", value=item["note"], key=f"note_{key}")
                    st.session_state.cart[key]["note"] = note

                    if st.button("🗑️ Xóa món", key=f"delete_{key}"):
                        del st.session_state.cart[key]
                        st.rerun()

            total = cart_total(st.session_state.cart)

            st.markdown(
                f'<div class="total-box"><h3>TỔNG ĐƠN HÀNG</h3><h1 style="color:#ff852e">{money(total)}</h1></div>',
                unsafe_allow_html=True
            )

            if st.button("🔥 XÁC NHẬN GỬI ORDER", use_container_width=True):
                if not customer.strip():
                    st.error("Vui lòng nhập tên khách hàng.")
                else:
                    st.session_state.current_order = {
                        "customer":customer,
                        "table":table,
                        "items":{k:v.copy() for k,v in st.session_state.cart.items()},
                        "total":total,
                        "time":datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "paid":False,
                        "payment_method":""
                    }
                    st.session_state.cart = {}
                    st.success("Đã gửi order!")
                    st.rerun()
        else:
            st.info("Giỏ hàng đang trống.")


# =====================================================
# 11. THANH TOÁN
# =====================================================

elif page == "💳 Thanh toán":

    st.markdown('<div class="section-title">💳 THANH TOÁN HÓA ĐƠN</div>', unsafe_allow_html=True)

    order = st.session_state.current_order

    if order is None:
        st.info("Chưa có đơn hàng cần thanh toán.")
    else:
        st.write("**Khách hàng:**", order["customer"])
        st.write("**Bàn:**", order["table"])
        st.write("**Thời gian:**", order["time"])

        rows = []
        for item in order["items"].values():
            rows.append({
                "Tên món":item["name"],
                "Đơn giá":money(item["price"]),
                "Số lượng":item["qty"],
                "Thành tiền":money(item["price"] * item["qty"]),
                "Ghi chú":item["note"]
            })

        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.markdown(
            f'<div class="total-box"><h3>TỔNG THANH TOÁN</h3><h1 style="color:#ff852e">{money(order["total"])}</h1></div>',
            unsafe_allow_html=True
        )

        if not order["paid"]:
            method = st.radio(
                "Phương thức thanh toán",
                ["Tiền mặt","Chuyển khoản","Thẻ ngân hàng"],
                horizontal=True
            )

            if st.button("✅ XÁC NHẬN THANH TOÁN", use_container_width=True):
                order["paid"] = True
                order["payment_method"] = method
                st.session_state.order_history.append(order.copy())
                save_data()
                st.success("Thanh toán thành công!")
                st.rerun()

        else:
            st.success("Đơn hàng đã thanh toán.")
            st.write("Phương thức:", order["payment_method"])

            invoice = f"BBQ HOUSE\nHÓA ĐƠN THANH TOÁN\nKhách hàng: {order['customer']}\nBàn: {order['table']}\nThời gian: {order['time']}\n"

            for item in order["items"].values():
                invoice += f"\n{item['name']} x {item['qty']} = {money(item['price']*item['qty'])}"

            invoice += f"\n\nTỔNG TIỀN: {money(order['total'])}\nPhương thức: {order['payment_method']}\nCảm ơn quý khách!"

            st.download_button(
                "📥 TẢI HÓA ĐƠN",
                invoice.encode("utf-8"),
                "hoa_don_BBQ_HOUSE.txt",
                mime="text/plain",
                use_container_width=True
            )

            if st.button("➕ TẠO ĐƠN MỚI"):
                st.session_state.current_order = None
                st.rerun()


# =====================================================
# 12. QUẢN LÝ ĐƠN
# =====================================================

elif page == "📋 Quản lý đơn":

    st.markdown('<div class="section-title">📋 QUẢN LÝ ĐƠN HÀNG</div>', unsafe_allow_html=True)

    st.markdown("### Đặt bàn")

    if st.session_state.reservations:
        st.dataframe(pd.DataFrame(st.session_state.reservations), use_container_width=True, hide_index=True)
    else:
        st.info("Chưa có đặt bàn.")

    st.markdown("### Đơn đã thanh toán")

    if st.session_state.order_history:
        history = [{
            "Khách hàng":x["customer"],
            "Bàn":x["table"],
            "Thời gian":x["time"],
            "Tổng tiền":money(x["total"]),
            "Thanh toán":x["payment_method"]
        } for x in st.session_state.order_history]

        st.dataframe(pd.DataFrame(history), use_container_width=True, hide_index=True)
    else:
        st.info("Chưa có đơn hàng.")


# =====================================================
# 13. THỐNG KÊ DOANH THU
# =====================================================

elif page == "📊 Doanh thu":

    st.markdown('<div class="section-title">📊 THỐNG KÊ DOANH THU</div>', unsafe_allow_html=True)

    paid_orders = revenue_data()

    # Chọn khoảng thời gian
    today = date.today()

    period = st.selectbox(
        "Chọn thời gian thống kê",
        ["Hôm nay","7 ngày gần nhất","Tháng này","Năm nay","Tất cả"]
    )

    if period == "Hôm nay":
        start_date = today
        end_date = today
    elif period == "7 ngày gần nhất":
        start_date = today - timedelta(days=6)
        end_date = today
    elif period == "Tháng này":
        start_date = today.replace(day=1)
        end_date = today
    elif period == "Năm nay":
        start_date = today.replace(month=1, day=1)
        end_date = today
    else:
        start_date = date.min
        end_date = date.max

    selected_orders = [
        x for x in paid_orders
        if start_date <= order_date(x) <= end_date
    ]

    total_revenue = sum(x["total"] for x in selected_orders)
    total_orders = len(selected_orders)
    average = total_revenue / total_orders if total_orders else 0

    total_items = sum(
        item["qty"]
        for order in selected_orders
        for item in order["items"].values()
    )

    # Các chỉ số
    c1, c2 = st.columns(2)
    c3, c4 = st.columns(2)

    c1.metric("💰 Tổng doanh thu", money(total_revenue))
    c2.metric("🧾 Đơn đã thanh toán", total_orders)
    c3.metric("🍖 Số món đã bán", total_items)
    c4.metric("📈 Trung bình mỗi đơn", money(average))

    st.markdown("---")

    # Biểu đồ doanh thu
    st.markdown("## 📈 BIỂU ĐỒ DOANH THU")

    if selected_orders:
        revenue_by_day = {}

        for order in selected_orders:
            day = order_date(order).strftime("%d/%m")
            revenue_by_day[day] = revenue_by_day.get(day, 0) + order["total"]

        chart_df = pd.DataFrame(
            list(revenue_by_day.items()),
            columns=["Ngày","Doanh thu"]
        )

        st.bar_chart(chart_df.set_index("Ngày"))

    else:
        st.info("Chưa có doanh thu trong khoảng thời gian này.")

    st.markdown("---")

    # Món bán chạy
    st.markdown("## 🏆 MÓN ĂN BÁN CHẠY")

    best_sellers = {}

    for order in selected_orders:
        for item in order["items"].values():
            name = item["name"]
            best_sellers[name] = best_sellers.get(name, 0) + item["qty"]

    if best_sellers:
        best_df = pd.DataFrame(
            [{"Tên món":k, "Số lượng bán":v} for k,v in best_sellers.items()]
        ).sort_values("Số lượng bán", ascending=False)

        st.dataframe(best_df, use_container_width=True, hide_index=True)

        st.bar_chart(best_df.set_index("Tên món"))

    else:
        st.info("Chưa có dữ liệu món bán.")

    st.markdown("---")

    # Lịch sử doanh thu
    st.markdown("## 🧾 CHI TIẾT DOANH THU")

    if selected_orders:
        revenue_rows = []

        for order in selected_orders:
            revenue_rows.append({
                "Thời gian":order["time"],
                "Khách hàng":order["customer"],
                "Bàn":order["table"],
                "Tổng tiền":order["total"],
                "Phương thức":order["payment_method"]
            })

        revenue_df = pd.DataFrame(revenue_rows)

        st.dataframe(
            revenue_df,
            use_container_width=True,
            hide_index=True
        )

        csv = revenue_df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "📥 XUẤT BÁO CÁO DOANH THU CSV",
            csv,
            "bao_cao_doanh_thu.csv",
            "text/csv",
            use_container_width=True
        )

    else:
        st.info("Không có hóa đơn trong khoảng thời gian đã chọn.")


# =====================================================
# 14. FOOTER
# =====================================================

st.markdown("""
<div class="footer">
    <h3 style="color:#ff852e">🔥 BBQ HOUSE</h3>
    <p>THE TASTE OF GREAT BBQ</p>
    <p>Địa chỉ: TP. Hồ Chí Minh</p>
    <p>Hotline: 0900 123 456</p>
    <p>© 2026 BBQ HOUSE. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
