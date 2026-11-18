
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="BBQ HOUSE",
    page_icon="🔥",
    layout="wide"
)

# =========================
# GIAO DIỆN
# =========================
st.markdown("""
<style>
.stApp {
    background: #101010;
    color: #f5f5f5;
}
section[data-testid="stSidebar"] {
    background: #191919;
}
h1, h2, h3, p, label {
    color: #f5f5f5 !important;
}
.food-card {
    background: #202020;
    border: 1px solid #383838;
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 10px;
}
.price {
    color: #ffb347;
    font-size: 20px;
    font-weight: 800;
}
div.stButton > button {
    background: #e64b32;
    color: white;
    border: 0;
    border-radius: 9px;
    font-weight: 700;
}
div.stButton > button:hover {
    background: #ff6548;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# THỰC ĐƠN BBQ HOUSE
# GIÁ THAM KHẢO
# =========================
MENU = [
    {
        "name": "Ba chỉ bò Mỹ",
        "category": "Thịt nướng",
        "price": 129000,
        "desc": "Ba chỉ bò Mỹ tươi, mềm, thích hợp nướng",
        "image": "https://images.unsplash.com/photo-1608877907149-a206d75ba011?w=700"
    },
    {
        "name": "Bò cuộn nấm kim châm",
        "category": "Thịt nướng",
        "price": 119000,
        "desc": "Thịt bò cuộn nấm kim châm",
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947?w=700"
    },
    {
        "name": "Dẻ sườn bò Mỹ",
        "category": "Thịt nướng",
        "price": 159000,
        "desc": "Dẻ sườn bò đậm vị sốt BBQ",
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=700"
    },
    {
        "name": "Nạc vai heo",
        "category": "Thịt nướng",
        "price": 89000,
        "desc": "Nạc vai heo ướp sốt đặc biệt",
        "image": "https://images.unsplash.com/photo-1607623814075-e51df1bdc82f?w=700"
    },
    {
        "name": "Ba chỉ heo",
        "category": "Thịt nướng",
        "price": 85000,
        "desc": "Ba chỉ heo thái lát, mềm thơm",
        "image": "https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=700"
    },
    {
        "name": "Sườn heo BBQ",
        "category": "Thịt nướng",
        "price": 139000,
        "desc": "Sườn heo nướng sốt BBQ",
        "image": "https://images.unsplash.com/photo-1544025162-d76694265947?w=700"
    },
    {
        "name": "Gà nướng mật ong",
        "category": "Thịt nướng",
        "price": 99000,
        "desc": "Gà ướp mật ong thơm ngọt",
        "image": "https://images.unsplash.com/photo-1532550907401-a500c9a57435?w=700"
    },
    {
        "name": "Mực nướng sa tế",
        "category": "Hải sản",
        "price": 129000,
        "desc": "Mực tươi nướng sa tế cay nhẹ",
        "image": "https://images.unsplash.com/photo-1559737558-2f5a35f4523b?w=700"
    },
    {
        "name": "Tôm nướng muối ớt",
        "category": "Hải sản",
        "price": 139000,
        "desc": "Tôm nướng muối ớt",
        "image": "https://images.unsplash.com/photo-1565680018434-b513d5e5fd47?w=700"
    },
    {
        "name": "Bạch tuộc nướng",
        "category": "Hải sản",
        "price": 149000,
        "desc": "Bạch tuộc giòn dai, ướp đậm đà",
        "image": "https://images.unsplash.com/photo-1559737558-2f5a35f4523b?w=700"
    },
    {
        "name": "Cá hồi nướng",
        "category": "Hải sản",
        "price": 169000,
        "desc": "Cá hồi nướng sốt bơ chanh",
        "image": "https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=700"
    },
    {
        "name": "Kim chi",
        "category": "Món ăn kèm",
        "price": 25000,
        "desc": "Kim chi cải thảo chua cay",
        "image": "https://images.unsplash.com/photo-1583224994255-7e2f4a4c5d5f?w=700"
    },
    {
        "name": "Rau củ nướng",
        "category": "Món ăn kèm",
        "price": 39000,
        "desc": "Rau củ theo mùa",
        "image": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=700"
    },
    {
        "name": "Khoai tây chiên",
        "category": "Món ăn kèm",
        "price": 35000,
        "desc": "Khoai tây chiên giòn",
        "image": "https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=700"
    },
    {
        "name": "Cơm chiên trứng",
        "category": "Món ăn kèm",
        "price": 45000,
        "desc": "Cơm chiên trứng nóng hổi",
        "image": "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=700"
    },
    {
        "name": "Lẩu kim chi",
        "category": "Lẩu",
        "price": 229000,
        "desc": "Lẩu kim chi chua cay, dùng 2-3 người",
        "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=700"
    },
    {
        "name": "Lẩu nấm",
        "category": "Lẩu",
        "price": 219000,
        "desc": "Nước lẩu nấm thanh ngọt",
        "image": "https://images.unsplash.com/photo-1547592180-85f173990554?w=700"
    },
    {
        "name": "Coca-Cola",
        "category": "Đồ uống",
        "price": 18000,
        "desc": "Nước ngọt có gas",
        "image": "https://images.unsplash.com/photo-1554866585-cd94860890b7?w=700"
    },
    {
        "name": "Trà đào",
        "category": "Đồ uống",
        "price": 30000,
        "desc": "Trà đào mát lạnh",
        "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=700"
    },
    {
        "name": "Nước suối",
        "category": "Đồ uống",
        "price": 12000,
        "desc": "Nước suối đóng chai",
        "image": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=700"
    },
]


def money(value):
    return f"{int(value):,}".replace(",", ".") + "đ"


# =========================
# KHỞI TẠO GIỎ HÀNG
# =========================
if "cart" not in st.session_state:
    st.session_state.cart = []

if "invoice" not in st.session_state:
    st.session_state.invoice = None


# =========================
# TIÊU ĐỀ
# =========================
st.markdown(
    "<h1 style='text-align:center;color:#ff7043'>🔥 BBQ HOUSE</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;color:#bbbbbb'>NƯỚNG NGON - VUI TRỌN BỮA TIỆC</p>",
    unsafe_allow_html=True
)

st.divider()


# =========================
# THÔNG TIN KHÁCH HÀNG
# =========================
left, right = st.columns([2, 1])

with left:
    customer = st.text_input(
        "Tên khách hàng",
        placeholder="Nhập tên khách hàng"
    )

with right:
    table_no = st.text_input(
        "Số bàn",
        placeholder="Ví dụ: Bàn 05"
    )


# =========================
# THỰC ĐƠN
# =========================
st.header("🍽️ Thực đơn")

categories = ["Tất cả"] + list(
    dict.fromkeys(item["category"] for item in MENU)
)

c1, c2 = st.columns([1, 2])

with c1:
    selected_category = st.selectbox(
        "Danh mục",
        categories
    )

with c2:
    keyword = st.text_input(
        "Tìm món ăn",
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
    st.info("Không tìm thấy món phù hợp.")


# =========================
# HIỂN THỊ MÓN ĂN
# =========================
for start in range(0, len(filtered), 3):
    cols = st.columns(3)

    for col, item in zip(cols, filtered[start:start + 3]):
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
                "＋ Thêm vào giỏ",
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

                st.toast(
                    f"Đã thêm {item['name']} vào giỏ hàng"
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


# =========================
# GIỎ HÀNG
# =========================
st.divider()
st.header("🛒 Giỏ hàng")

if st.session_state.cart:

    for index, item in enumerate(st.session_state.cart):
        a, b, c, d = st.columns([3, 1, 1, 1])

        a.write(item["name"])
        b.write(f"x {item['qty']}")
        c.write(
            money(item["price"] * item["qty"])
        )

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
    y.metric("VAT (8%)", money(tax))
    z.metric("Tổng thanh toán", money(total))

    p1, p2 = st.columns(2)

    with p1:
        if st.button(
            "🧹 Xóa toàn bộ giỏ hàng",
            use_container_width=True
        ):
            st.session_state.cart = []
            st.rerun()

    with p2:
        if st.button(
            "💳 THANH TOÁN",
            type="primary",
            use_container_width=True
        ):
            if not customer.strip():
                st.warning(
                    "Vui lòng nhập tên khách hàng trước khi thanh toán."
                )
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
                        dict(x)
                        for x in st.session_state.cart
                    ],
                    "subtotal": subtotal,
                    "tax": tax,
                    "total": total,
                }

                st.session_state.cart = []

                st.success("Thanh toán thành công!")
                st.rerun()

else:
    st.info(
        "Giỏ hàng đang trống. Hãy chọn món ở thực đơn phía trên."
    )


# =========================
# HÓA ĐƠN THANH TOÁN
# =========================
if st.session_state.invoice:

    invoice = st.session_state.invoice

    st.divider()
    st.header("🧾 Hóa đơn thanh toán")

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
        f"**VAT (8%):** {money(invoice['tax'])}"
    )

    st.markdown(
        f"<h2 style='color:#ff7043'>TỔNG CỘNG: {money(invoice['total'])}</h2>",
        unsafe_allow_html=True
    )

    # Nội dung hóa đơn dạng TXT
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
        + f"\nTONG CONG: {money(invoice['total'])}\n"
        + "Cam on quy khach!"
    )

    st.download_button(
        "⬇️ Tải hóa đơn (.txt)",
        data=invoice_text,
        file_name=f"{invoice['code']}.txt",
        mime="text/plain",
        use_container_width=True
    )

    # Xuất chi tiết hóa đơn CSV
    csv_data = pd.DataFrame(invoice_rows).to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "⬇️ Tải chi tiết hóa đơn (.csv)",
        data=csv_data,
        file_name=f"{invoice['code']}.csv",
        mime="text/csv",
        use_container_width=True
    )

    if st.button("Tạo hóa đơn mới"):
        st.session_state.invoice = None
        st.rerun()


# =========================
# CHÂN TRANG
# =========================
st.caption(
    "BBQ HOUSE • Giá bán trong ứng dụng là giá tham khảo."
)
