                    "items": invoice_items,
                    "total": sum(x["subtotal"] for x in invoice_items)
                }
                st.session_state.cart = []
                st.success("Thanh toán thành công!")
                st.rerun()

# =========================
# HÓA ĐƠN
# =========================
if st.session_state.invoice:
    invoice = st.session_state.invoice
    st.divider()
    st.markdown('<div class="section-title">🧾 Hóa đơn thanh toán</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="panel">
        <h2 style="color:#ff7043; margin:0;">BBQ HOUSE</h2>
        <p class="muted">HÓA ĐƠN THANH TOÁN</p>
        <p><b>Mã hóa đơn:</b> {invoice["code"]}</p>
        <p><b>Thời gian:</b> {invoice["date"]}</p>
        <p><b>Khách hàng:</b> {invoice["customer"]}</p>
        <p><b>Số bàn:</b> {invoice["table"]}</p>
        <p><b>Điện thoại:</b> {invoice["phone"]}</p>
    </div>
    """, unsafe_allow_html=True)

    invoice_data = []
    for item in invoice["items"]:
        invoice_data.append({
            "Tên món": item["name"],
            "Đơn giá": money(item["price"]),
            "Số lượng": item["quantity"],
            "Thành tiền": money(item["subtotal"])
        })
    st.dataframe(pd.DataFrame(invoice_data), use_container_width=True, hide_index=True)
    st.markdown(f'<div class="total">TỔNG THANH TOÁN: {money(invoice["total"])}</div>', unsafe_allow_html=True)

    # Tạo file CSV để tải hóa đơn
    csv_df = pd.DataFrame([
        {
            "Ma hoa don": invoice["code"],
            "Thoi gian": invoice["date"],
            "Khach hang": invoice["customer"],
            "So ban": invoice["table"],
            "So dien thoai": invoice["phone"],
            "Ten mon": item["name"],
            "Don gia": item["price"],
            "So luong": item["quantity"],
            "Thanh tien": item["subtotal"]
        }
        for item in invoice["items"]
    ])
    csv_bytes = csv_df.to_csv(index=False).encode("utf-8-sig")

    # Tạo hóa đơn dạng văn bản
    text_lines = [
        "                 BBQ HOUSE",
        "             HOA DON THANH TOAN",
        "=" * 42,
        f"Ma hoa don: {invoice['code']}",
        f"Thoi gian: {invoice['date']}",
        f"Khach hang: {invoice['customer']}",
        f"So ban: {invoice['table']}",
        f"So dien thoai: {invoice['phone']}",
        "-" * 42,
        "TEN MON | DON GIA | SL | THANH TIEN",
        "-" * 42
    ]
    for item in invoice["items"]:
        text_lines.append(
            f"{item['name']} | {item['price']} | {item['quantity']} | {item['subtotal']}"
        )
    text_lines += [
        "-" * 42,
        f"TONG THANH TOAN: {invoice['total']} VND",
        "Cam on quy khach va hen gap lai!"
    ]
    txt_bytes = "\n".join(text_lines).encode("utf-8-sig")

    d1, d2 = st.columns(2)
    with d1:
        st.download_button(
            "⬇️ Tải hóa đơn Excel/CSV",
            data=csv_bytes,
            file_name=f"{invoice['code']}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with d2:
        st.download_button(
            "⬇️ Tải hóa đơn TXT",
            data=txt_bytes,
            file_name=f"{invoice['code']}.txt",
            mime="text/plain",
            use_container_width=True
        )

    if st.button("＋ Tạo đơn hàng mới", use_container_width=True):
        st.session_state.invoice = None
        st.session_state.cart = []
        st.rerun()

st.markdown("""
<div style="text-align:center; color:#777; padding:30px 0 5px 0;">
    BBQ HOUSE · Cảm ơn quý khách đã lựa chọn chúng tôi ❤️
</div>
""", unsafe_allow_html=True)
