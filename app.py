
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="BBQ HOUSE | Nhà hàng nướng",
    page_icon="🔥",
    layout="wide"
)

# =====================================
# 1. GIAO DIỆN
# =====================================
st.markdown("""
<style>
.stApp {
    background: #111714;
    color: #f5f1e8;
}
header[data-testid="stHeader"] {
    background: #111714;
}
h1, h2, h3, p, label {
    color: #f5f1e8 !important;
}
section[data-testid="stSidebar"] {
    background: #1c2923;
}
.food-card {
    background: #1c2923;
    border: 1px solid #34483c;
    border-radius: 15px;
    padding: 12px;
}
.price {
    color: #ff9d52;
    font-size: 21px;
    font-weight: bold;
}
.hero {
    background: linear-gradient(90deg, #14271f, #315a43);
    padding: 35px 20px;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 25px;
}
.hero h1 {
    color: #ffb36b !important;
    font-size: 48px;
}
.hero p {
    color: #fff !important;
}
.footer {
    background: #173c2e;
    padding: 35px 25px;
    border-radius: 15px;
    margin-top: 40px;
}
.footer h2, .footer h3 {
    color: #ffbd79 !important;
}
.footer a {
    color: #f5f1e8 !important;
    text-decoration: none;
}
.footer a:hover {
    color: #ffbd79 !important;
}
div.stButton > button {
    background: #d85b35;
    color: white;
    border: none;
    border-radius: 9px;
    font-weight: bold;
}
div.stButton > button:hover {
    background: #f0784e;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# =====================================
# 2. THỰC ĐƠN
# =====================================
MENU = [
    {
        "name": "Ba chỉ bò Mỹ",
        "category": "Thịt bò",
        "price": 129000,
        "desc": "Ba chỉ bò Mỹ thái lát, mềm thơm.",
        "image": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=700"
    },
    {
        "name": "Bò cuộn nấm kim châm",
        "category": "Thịt bò",
        "price": 119000,
        "desc": "Bò cuộn nấm kim châm tươi ngon.",
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947?w=700"
    },
    {
        "name": "Dẻ sườn bò Mỹ",
        "category": "Thịt bò",
        "price": 159000,
        "desc": "Dẻ sườn bò đậm vị sốt BBQ.",
        "image": "https://images.unsplash.com/photo-1558030006-450675393462?w=700"
    },
    {
        "name": "Ba chỉ heo",
        "category": "Thịt heo",
        "price": 85000,
        "desc": "Ba chỉ heo thái lát, ướp gia vị.",
        "image": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=700"
    },
    {
        "name": "Sườn heo BBQ",
        "category": "Thịt heo",
        "price": 139000,
        "desc": "Sườn heo nướng sốt BBQ.",
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947?w=700"
    },
    {
        "name": "Nạc vai heo",
        "category": "Thịt heo",
        "price": 89000,
        "desc": "Nạc vai heo tươi, đậm đà.",
        "image": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=700"
    },
    {
        "name": "Gà nướng mật ong",
        "category": "Thịt gà",
        "price": 99000,
        "desc": "Gà nướng mật ong thơm ngon.",
        "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=700"
    },
    {
       {
    "name": "Mực nướng sa tế",
    "category": "Hải sản",
    "price": 129000,
    "desc": "Mực tươi nướng sa tế cay thơm, đậm vị.",
    "image": "https://recipe1.ezmember.co.kr/cache/recipe/2018/01/27/1c31e970a3f07270e3d5f4ac91b2daae1.jpg"
},
    },
    {
        "name": "Tôm nướng muối ớt",
        "category": "Hải sản",
        "price": 139000,
        "desc": "Tôm nướng muối ớt đậm vị.",
        "image": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=700"
    },
    {
        "name": "Cá hồi nướng",
        "category": "Hải sản",
        "price": 169000,
        "desc": "Cá hồi nướng sốt bơ chanh.",
        "image": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=700"
    },
    {
        "name": "Khoai tây chiên",
        "category": "Món ăn kèm",
        "price": 35000,
        "desc": "Khoai tây chiên vàng giòn.",
        "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=700"
    },
    {
        {
    "name": "Salad trộn",
    "category": "Món ăn kèm",
    "price": 45000,
    "desc": "Xà lách tươi, cà chua, dưa leo và sốt salad.",
    "image": "https://static.mywebsites360.com/a76870229dec4044a289aa0e5a642d07/i/bd0feec58af349908fd6293a75c6232c/1/4SoifmQp45JMgBnHp7ed2/What%2527s%20on%20the%20Menu_%20A%20Sneak%20Peek%20at%20Motown%20Extreme%25E2%2580%2599s%20Dinner1.jpg"
},
    },
    {
        "name": "Cơm chiên trứng",
        "category": "Món ăn kèm",
        "price": 45000,
        "desc": "Cơm chiên trứng nóng hổi.",
        "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=700"
    },
    {
        "name": "Kim chi",
        "category": "Món ăn kèm",
        "price": 25000,
        "desc": "Kim chi cải thảo chua cay.",
        "image": "https://images.unsplash.com/photo-1583224994255-7e2f4a4c5d5f?w=700"
    },
    {
        "name": "Lẩu kim chi",
        "category": "Lẩu",
        "price": 229000,
        "desc": "Lẩu kim chi chua cay.",
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=700"
    },
    {
        "name": "Lẩu nấm",
        "category": "Lẩu",
        "price": 219000,
        "desc": "Nước lẩu nấm thanh ngọt.",
        "image": "https://images.unsplash.com/photo-1547592180-85f173990554?w=700"
    },
    {
        "name": "Coca-Cola",
        "category": "Đồ uống",
        "price": 18000,
        "desc": "Nước ngọt có gas.",
        "image": "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=700"
    },
    {
        "name": "Trà đào",
        "category": "Đồ uống",
        "price": 30000,
        "desc": "Trà đào mát lạnh.",
        "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=700"
    },
    {
        "name": "Nước suối",
        "category": "Đồ uống",
        "price": 12000,
        "desc": "Nước suối đóng chai.",
        "image": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=700"
    }
]


def money(value):
    return f"{int(value):,}".replace(",", ".") + "đ"


# =====================================
# 3. KHỞI TẠO DỮ LIỆU
# =====================================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None


# =====================================
# 4. HEADER
# =====================================
st.markdown("""
<div class="hero">
    <h1>🔥 BBQ HOUSE</h1>
    <p>THE ART OF KOREAN BBQ</p>
    <p>Hương vị nướng tuyệt hảo - Trọn vẹn từng khoảnh khắc</p>
</div>
""", unsafe_allow_html=True)

nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    st.markdown("[TRANG CHỦ](#trang-chu)")
with nav2:
    st.markdown("[VỀ BBQ HOUSE](#ve-bbq-house)")
with nav3:
    st.markdown("[MENU](#menu)")
with nav4:
    st.markdown("[ĐẶT BÀN](#dat-ban)")

st.divider()


# =====================================
# 5. GIỚI THIỆU
# =====================================
st.markdown('<div id="trang-chu"></div>', unsafe_allow_html=True)

st.markdown("""
## CHÀO MỪNG ĐẾN VỚI BBQ HOUSE

Không chỉ là một bữa ăn, BBQ HOUSE mang đến trải nghiệm
ẩm thực nướng hấp dẫn với những món ăn được chuẩn bị
chu đáo, không gian ấm cúng và những khoảnh khắc đáng nhớ.
""")

st.markdown('<div id="ve-bbq-house"></div>', unsafe_allow_html=True)

st.divider()


# =====================================
# 6. THÔNG TIN KHÁCH HÀNG
# =====================================
st.markdown('<div id="dat-ban"></div>', unsafe_allow_html=True)
st.header("📅 THÔNG TIN ĐẶT BÀN / GỌI MÓN")

col1, col2 = st.columns(2)

with col1:
    customer = st.text_input(
        "Tên khách hàng",
        placeholder="Nhập tên của bạn"
    )

with col2:
    table_no = st.text_input(
        "Số bàn",
        placeholder="Ví dụ: Bàn 05"
    )


# =====================================
# 7. MENU
# =====================================
st.markdown('<div id="menu"></div>', unsafe_allow_html=True)

st.header("🍖 MENU BBQ HOUSE")
st.caption("Khám phá thực đơn hấp dẫn của chúng tôi.")

categories = ["Tất cả"] + list(
    dict.fromkeys(item["category"] for item in MENU)
)

c1, c2 = st.columns([1, 2])

with c1:
    selected_category = st.selectbox(
        "Danh mục món ăn",
        categories
    )

with c2:
    keyword = st.text_input(
        "Tìm kiếm món ăn",
        placeholder="Nhập tên món..."
    )

filtered = [
    item for item in MENU
    if (
        selected_category == "Tất cả"
        or item["category"] == selected_category
    )
    and keyword.lower() in item["name"].lower()
]

if not filtered:
    st.info("Không tìm thấy món ăn phù hợp.")

for start in range(0, len(filtered), 3):
    cols = st.columns(3)

    for col, item in zip(cols, filtered[start:start + 3]):
        with col:
            st.markdown('<div class="food-card">', unsafe_allow_html=True)

            try:
                st.image(
                    item["image"],
                    use_container_width=True
                )
            except Exception:
                st.write("🍖")

            st.subheader(item["name"])
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
                key="qty_" + item["name"]
            )

            if st.button(
                "＋ THÊM VÀO GIỎ",
                key="add_" + item["name"],
                use_container_width=True
            ):
                found = next(
                    (
                        x for x in st.session_state.cart
                        if x["name"] == item["name"]
                    ),
                    None
                )

                if found:
                    found["qty"] += int(qty)
                else:
                    st.session_state.cart.append({
                        "name": item["name"],
                        "price": item["price"],
                        "qty": int(qty)
                    })

                st.toast("Đã thêm món vào giỏ hàng!")

            st.markdown("</div>", unsafe_allow_html=True)


# =====================================
# 8. GIỎ HÀNG
# =====================================
st.divider()
st.header("🛒 GIỎ HÀNG CỦA BẠN")

if st.session_state.cart:

    for index, item in enumerate(st.session_state.cart):
        a, b, c, d = st.columns([3, 1, 1, 1])

        a.write(item["name"])
        b.write(f"x {item['qty']}")
        c.write(money(item["price"] * item["qty"]))

        if d.button("Xóa", key=f"remove_{index}"):
            st.session_state.cart.pop(index)
            st.rerun()

    subtotal = sum(
        x["price"] * x["qty"]
        for x in st.session_state.cart
    )

    tax = round(subtotal * 0.08)
    total = subtotal + tax

    x, y, z = st.columns(3)

    x.metric("Tạm tính", money(subtotal))
    y.metric("VAT 8%", money(tax))
    z.metric("Tổng thanh toán", money(total))

    p1, p2 = st.columns(2)

    with p1:
        if st.button("🧹 XÓA GIỎ HÀNG", use_container_width=True):
            st.session_state.cart = []
            st.rerun()

    with p2:
        if st.button(
            "💳 THANH TOÁN",
            type="primary",
            use_container_width=True
        ):
            if not customer.strip():
                st.warning("Vui lòng nhập tên khách hàng.")
            else:
                st.session_state.invoice = {
                    "code": "BBQ" + datetime.now().strftime(
                        "%Y%m%d%H%M%S"
                    ),
                    "date": datetime.now().strftime(
                        "%d/%m/%Y %H:%M:%S"
                    ),
                    "customer": customer.strip(),
                    "table": table_no.strip() or "Chưa chọn",
                    "items": [
                        dict(x) for x in st.session_state.cart
                    ],
                    "subtotal": subtotal,
                    "tax": tax,
                    "total": total
                }

                st.session_state.cart = []
                st.success("Thanh toán thành công!")
                st.rerun()

else:
    st.info("Giỏ hàng đang trống.")


# =====================================
# 9. HÓA ĐƠN
# =====================================
if st.session_state.invoice:

    invoice = st.session_state.invoice

    st.divider()
    st.header("🧾 HÓA ĐƠN THANH TOÁN")

    st.markdown("## 🔥 BBQ HOUSE")

    st.write("Mã hóa đơn:", invoice["code"])
    st.write("Thời gian:", invoice["date"])
    st.write("Khách hàng:", invoice["customer"])
    st.write("Số bàn:", invoice["table"])

    invoice_rows = []

    for item in invoice["items"]:
        invoice_rows.append({
            "Tên món": item["name"],
            "Đơn giá": money(item["price"]),
            "Số lượng": item["qty"],
            "Thành tiền": money(
                item["price"] * item["qty"]
            )
        })

    st.dataframe(
        pd.DataFrame(invoice_rows),
        use_container_width=True,
        hide_index=True
    )

    st.write("Tạm tính:", money(invoice["subtotal"]))
    st.write("VAT 8%:", money(invoice["tax"]))

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
        use_container_width=True
    )

    csv_data = pd.DataFrame(invoice_rows).to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "⬇️ TẢI CHI TIẾT CSV",
        data=csv_data,
        file_name=f"{invoice['code']}.csv",
        mime="text/csv",
        use_container_width=True
    )

    if st.button("TẠO HÓA ĐƠN MỚI"):
        st.session_state.invoice = None
        st.rerun()


# =====================================
# 10. ĐẶT BÀN - ƯU ĐÃI - TUYỂN DỤNG
# =====================================
st.divider()

st.header("✨ TRẢI NGHIỆM TẠI BBQ HOUSE")

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("### 📅 ĐẶT BÀN")
    st.write("Liên hệ với chúng tôi để được hỗ trợ đặt bàn.")

with f2:
    st.markdown("### 🎉 ƯU ĐÃI - SỰ KIỆN")
    st.write("Theo dõi các chương trình ưu đãi và sự kiện.")

with f3:
    st.markdown("### 🤝 TUYỂN DỤNG")
    st.write("Cùng gia nhập đội ngũ BBQ HOUSE.")


# =====================================
# 11. FOOTER
# =====================================
st.markdown("""
<div class="footer">

<h2>🔥 BBQ HOUSE</h2>
<p>THE ART OF KOREAN BBQ</p>
<p>Hương vị nướng tuyệt hảo - Trọn vẹn từng khoảnh khắc.</p>

<hr>

<h3>KHÁM PHÁ BBQ HOUSE</h3>

<p><a href="#trang-chu">01　TRANG CHỦ</a></p>
<p><a href="#ve-bbq-house">02　VỀ BBQ HOUSE</a></p>
<p><a href="#menu">03　MENU</a></p>
<p><a href="#dat-ban">04　ĐẶT BÀN</a></p>
<p>05　ƯU ĐÃI - SỰ KIỆN</p>
<p>06　TUYỂN DỤNG</p>

<hr>

<h3>LIÊN HỆ</h3>
<p>Hotline: 1900 000 000</p>
<p>Email: bbqhouse@example.com</p>
<p>Địa chỉ: Thông tin nhà hàng sẽ được cập nhật.</p>

<hr>

<h3>KẾT NỐI VỚI CHÚNG TÔI</h3>
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
