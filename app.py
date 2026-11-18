import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import io
import csv

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="BBQ HOUSE - Hệ Thống Quản Lý Nhà Hàng",
    page_icon="🍖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS TÙY CHỈNH: DARK THEME & CAM CHỦ ĐẠO ---
st.markdown("""
    <style>
    /* Tổng thể giao diện Dark Theme */
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1A1A1A;
        border-right: 1px solid #2C2C2C;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #E0E0E0 !important;
        font-weight: 500;
    }
    /* Tiêu đề */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    /* Thẻ món ăn (Card) */
    .food-card {
        background-color: #1E1E1E;
        border: 1px solid #2C2C2C;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: transform 0.2s;
    }
    .food-card:hover {
        border-color: #FF5722;
        transform: translateY(-2px);
    }
    .food-title {
        font-size: 18px;
        font-weight: bold;
        color: #FFFFFF;
        margin-top: 10px;
    }
    .food-price {
        font-size: 16px;
        color: #FF5722;
        font-weight: bold;
    }
    .food-desc {
        font-size: 13px;
        color: #AAAAAA;
        margin-bottom: 10px;
    }
    /* Nút bấm (Buttons) */
    .stButton>button {
        background-color: #FF5722;
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        transition: background-color 0.2s;
    }
    .stButton>button:hover {
        background-color: #E64A19;
        color: white;
    }
    /* Metric Cards */
    [data-testid="metric-container"] {
        background-color: #1E1E1E;
        border: 1px solid #2C2C2C;
        padding: 15px;
        border-radius: 10px;
    }
    /* Input Fields */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div, .stDateInput>div>div>input, .stTimeInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #262626;
        color: #FFFFFF;
        border: 1px solid #3C3C3C;
        border-radius: 6px;
    }
    /* Dataframes */
    [data-testid="stDataFrame"] {
        border: 1px solid #2C2C2C;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- KHỞI TẠO DỮ LIỆU SESSION STATE ---
if 'menu_items' not in st.session_state:
    st.session_state.menu_items = [
        {"id": 1, "name": "Ba chỉ bò Mỹ", "price": 129000, "category": "Thịt bò", "desc": "Ba chỉ bò Mỹ tươi ngon, vân mỡ đan xen hoàn hảo.", "image": "https://images.unsplash.com/photo-1544025162-d76694265947?w=500&auto=format&fit=crop&q=80"},
        {"id": 2, "name": "Sườn bò nướng", "price": 189000, "category": "Thịt bò", "desc": "Sườn bò tẩm ướp sốt đặc biệt, mềm mọng nước.", "image": "https://images.unsplash.com/photo-1558030006-450675393462?w=500&auto=format&fit=crop&q=80"},
        {"id": 3, "name": "Lõi vai bò Mỹ", "price": 159000, "category": "Thịt bò", "desc": "Phần thịt săn chắc, ngọt đậm đà vị bò.", "image": "https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=500&auto=format&fit=crop&q=80"},
        {"id": 4, "name": "Bò cuộn nấm", "price": 99000, "category": "Thịt bò", "desc": "Thịt bò cuộn nấm kim châm giòn ngọt thanh.", "image": "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=500&auto=format&fit=crop&q=80"},
        {"id": 5, "name": "Ba chỉ heo nướng", "price": 89000, "category": "Thịt heo", "desc": "Ba chỉ heo cắt lát vừa phải, nướng xèo xèo thơm phức.", "image": "https://images.unsplash.com/photo-1607305387299-a3d9611cd469?w=500&auto=format&fit=crop&q=80"},
        {"id": 6, "name": "Sườn heo BBQ", "price": 129000, "category": "Thịt heo", "desc": "Sườn heo óng ánh sốt BBQ đậm đà chuẩn vị.", "image": "https://images.unsplash.com/photo-1544025162-d76694265947?w=500&auto=format&fit=crop&q=80"},
        {"id": 7, "name": "Nạc vai heo", "price": 99000, "category": "Thịt heo", "desc": "Thịt vai mềm vừa tới, không bị ngấy mỡ.", "image": "https://images.unsplash.com/photo-1432139555190-58524dae6a55?w=500&auto=format&fit=crop&q=80"},
        {"id": 8, "name": "Tôm sú nướng", "price": 149000, "category": "Hải sản", "desc": "Tôm sú tươi sống nướng muối ớt cay nồng.", "image": "https://images.unsplash.com/photo-1565680314524-dbe2661af7d0?w=500&auto=format&fit=crop&q=80"},
        {"id": 9, "name": "Mực nướng sa tế", "price": 139000, "category": "Hải sản", "desc": "Mực ống tươi giòn sần sật phết sa tế cay thơm.", "image": "https://images.unsplash.com/photo-1599487484170-7c9e6e5cef84?w=500&auto=format&fit=crop&q=80"},
        {"id": 10, "name": "Bạch tuộc nướng", "price": 159000, "category": "Hải sản", "desc": "Bạch tuộc đại dương nướng chao đậm đà giòn sần sật.", "image": "https://images.unsplash.com/photo-1544025162-d76694265947?w=500&auto=format&fit=crop&q=80"},
        {"id": 11, "name": "Hàu nướng phô mai", "price": 99000, "category": "Hải sản", "desc": "Hàu sữa béo ngậy ngập tràn phô mai kéo sợi thơm lừng.", "image": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?w=500&auto=format&fit=crop&q=80"},
        {"id": 12, "name": "Nấm kim châm", "price": 35000, "category": "Món ăn kèm", "desc": "Nấm kim châm tươi sạch ăn kèm lẩu hoặc nướng.", "image": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=500&auto=format&fit=crop&q=80"},
        {"id": 13, "name": "Rau củ tổng hợp", "price": 45000, "category": "Món ăn kèm", "desc": "Bắp, khoai lang, hành tây và đậu bắp tươi ngon.", "image": "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=500&auto=format&fit=crop&q=80"},
        {"id": 14, "name": "Kim chi Hàn Quốc", "price": 30000, "category": "Món ăn kèm", "desc": "Kim chi cải thảo giòn cay chuẩn vị xứ Hàn.", "image": "https://images.unsplash.com/photo-1583225224424-95877c5e27a7?w=500&auto=format&fit=crop&q=80"},
        {"id": 15, "name": "Lẩu Thái hải sản", "price": 259000, "category": "Lẩu", "desc": "Nước lẩu chua cay đậm vị sả ớt kèm hải sản tươi.", "image": "https://images.unsplash.com/photo-1547592166-23ac45744acd?w=500&auto=format&fit=crop&q=80"},
        {"id": 16, "name": "Lẩu kim chi", "price": 229000, "category": "Lẩu", "desc": "Lẩu kim chi thịt bò ấm nóng, chuẩn vị truyền thống.", "image": "https://images.unsplash.com/photo-1555126634-323283e090fa?w=500&auto=format&fit=crop&q=80"},
        {"id": 17, "name": "Cơm chiên hải sản", "price": 69000, "category": "Món ăn no", "desc": "Cơm chiên vàng giòn hạt tơi kèm tôm mực tươi.", "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=500&auto=format&fit=crop&q=80"},
        {"id": 18, "name": "Trà đào cam sả", "price": 39000, "category": "Đồ uống", "desc": "Thức uống thanh mát giải nhiệt hoàn hảo.", "image": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?w=500&auto=format&fit=crop&q=80"},
        {"id": 19, "name": "Nước ngọt", "price": 25000, "category": "Đồ uống", "desc": "Coca, Sprite, hoặc Pepsi lạnh sảng khoái.", "image": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500&auto=format&fit=crop&q=80"},
        {"id": 20, "name": "Nước suối", "price": 15000, "category": "Đồ uống", "desc": "Nước khoáng đóng chai tinh khiết.", "image": "https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=500&auto=format&fit=crop&q=80"}
    ]

if 'cart' not in st.session_state:
    st.session_state.cart = {}

if 'bookings' not in st.session_state:
    st.session_state.bookings = [
        {"id": "BK001", "name": "Nguyễn Văn A", "phone": "0901234567", "date": "2026-11-20", "time": "18:30", "guests": 4, "note": "Ngồi gần cửa sổ", "status": "Đã xác nhận"},
        {"id": "BK002", "name": "Trần Thị B", "phone": "0912345678", "date": "2026-11-20", "time": "19:00", "guests": 6, "note": "Sinh nhật", "status": "Đã xác nhận"}
    ]

if 'orders' not in st.session_state:
    st.session_state.orders = [
        {
            "id": "OD001", "customer": "Nguyễn Văn A", "table": "Bàn 03", 
            "items": [{"name": "Ba chỉ bò Mỹ", "price": 129000, "qty": 2}, {"name": "Lẩu Thái hải sản", "price": 259000, "qty": 1}],
            "subtotal": 517000, "discount": 0, "vat": 51700, "total": 568700,
            "payment_method": "Tiền mặt", "time": "2026-11-19 19:30"
        }
    ]

# --- THANH ĐIỀU HƯỚNG BÊN TRÁI (SIDEBAR) ---
st.sidebar.markdown("<h2 style='text-align: center; color: #FF5722;'>🔥 BBQ HOUSE</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #888;'>Hệ thống Quản lý Nhà hàng Chuyên nghiệp</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu_selection = st.sidebar.radio(
    "Điều hướng",
    ["🏠 Trang chủ", "🍖 Thực đơn", "📅 Đặt bàn", "🛒 Gọi món", "💳 Thanh toán", "📋 Quản lý", "📊 Doanh thu"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Hotline hỗ trợ:** 1900 6868\n\n🕒 **Giờ mở cửa:** 10:00 - 23:00")

# --- 1. TRANG CHỦ ---
if menu_selection == "🏠 Trang chủ":
    st.markdown("""
        <div style='padding: 30px; background: linear-gradient(135deg, #1E1E1E 0%, #2A1B18 100%); border-radius: 15px; text-align: center; border: 1px solid #FF5722;'>
            <h1 style='color: #FF5722; font-size: 42px; margin-bottom: 10px;'>CHÀO MỪNG ĐẾN VỚI BBQ HOUSE</h1>
            <p style='font-size: 18px; color: #CCCCCC;'>Nơi hội tụ những hương vị nướng than hoa thượng hạng, không gian ấm cúng và phong cách phục vụ tận tâm.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Thống kê nhanh
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Tổng số món ăn", value=f"{len(st.session_state.menu_items)} Món")
    with col2:
        st.metric(label="Tổng đơn hàng", value=f"{len(st.session_state.orders)} Đơn")
    with col3:
        st.metric(label="Lượt đặt bàn", value=f"{len(st.session_state.bookings)} Bàn")
        
    st.markdown("---")
    st.subheader("🌟 Món Nổi Bật Được Yêu Thích Nhất")
    
    feat_cols = st.columns(3)
    featured_items = [st.session_state.menu_items[0], st.session_state.menu_items[1], st.session_state.menu_items[7]]
    
    for idx, item in enumerate(featured_items):
        with feat_cols[idx]:
            st.markdown(f"""
                <div class="food-card">
                    <img src="{item['image']}" style="width:100%; height:180px; object-fit:cover; border-radius:8px;">
                    <div class="food-title">{item['name']}</div>
                    <div class="food-desc">{item['desc']}</div>
                    <div class="food-price">{item['price']:,}đ</div>
                </div>
            """, unsafe_allow_html=True)

# --- 2. THỰC ĐƠN ---
elif menu_selection == "🍖 Thực đơn":
    st.title("🍖 Thực Đơn Nhà Hàng BBQ HOUSE")
    
    # Tìm kiếm và lọc danh mục
    col_search, col_cat = st.columns([2, 1])
    with col_search:
        search_query = st.text_input("🔍 Tìm kiếm món ăn", placeholder="Nhập tên món ăn...")
    with col_cat:
        categories = ["Tất cả", "Thịt bò", "Thịt heo", "Hải sản", "Món ăn kèm", "Lẩu", "Món ăn no", "Đồ uống"]
        selected_category = st.selectbox("Lọc theo danh mục", categories)
        
    st.markdown("---")
    
    # Lọc danh sách món
    filtered_items = st.session_state.menu_items
    if selected_category != "Tất cả":
        filtered_items = [item for item in filtered_items if item['category'] == selected_category]
    if search_query:
        filtered_items = [item for item in filtered_items if search_query.lower() in item['name'].lower()]
        
    # Hiển thị dạng lưới thẻ món ăn
    cols_per_row = 3
    for i in range(0, len(filtered_items), cols_per_row):
        row_cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(filtered_items):
                item = filtered_items[i + j]
                with row_cols[j]:
                    st.markdown(f"""
                        <div class="food-card">
                            <img src="{item['image']}" style="width:100%; height:160px; object-fit:cover; border-radius:8px;" onerror="this.onerror=null;this.src='https://images.unsplash.com/photo-1544025162-d76694265947?w=500&auto=format&fit=crop&q=80';">
                            <div class="food-title">{item['name']}</div>
                            <div class="food-desc">{item['desc']}</div>
                            <div class="food-price">{item['price']:,}đ</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    qty_key = f"qty_{item['id']}"
                    qty = st.number_input(f"Số lượng ({item['name']})", min_value=1, max_value=20, value=1, key=qty_key, label_visibility="collapsed")
                    if st.button(f"🛒 Thêm vào giỏ", key=f"add_{item['id']}"):
                        if item['name'] in st.session_state.cart:
                            st.session_state.cart[item['name']]['qty'] += qty
                        else:
                            st.session_state.cart[item['name']] = {
                                "price": item['price'],
                                "qty": qty
                            }
                        st.success(f"Đã thêm {qty}x {item['name']} vào giỏ hàng!")

# --- 3. ĐẶT BÀN ---
elif menu_selection == "📅 Đặt bàn":
    st.title("📅 Đặt Bàn Trực Tuyến")
    st.write("Vui lòng điền thông tin bên dưới để đặt bàn trước tại BBQ HOUSE.")
    
    with st.form("booking_form"):
        col1, col2 = st.columns(2)
        with col1:
            cust_name = st.text_input("Họ và tên khách hàng *")
            phone = st.text_input("Số điện thoại *")
            guests = st.number_input("Số lượng khách", min_value=1, max_value=50, value=2)
        with col2:
            booking_date = st.date_input("Ngày đặt bàn", min_value=date.today())
            booking_time = st.time_input("Giờ đặt bàn", value=time(18, 0))
            note = st.text_area("Ghi chú thêm (Yêu cầu đặc biệt, ghế trẻ em...)")
            
        submitted = st.form_submit_button("Xác Nhận Đặt Bàn")
        if submitted:
            if cust_name and phone:
                booking_id = f"BK{len(st.session_state.bookings)+1:03d}"
                st.session_state.bookings.append({
                    "id": booking_id,
                    "name": cust_name,
                    "phone": phone,
                    "date": str(booking_date),
                    "time": str(booking_time),
                    "guests": guests,
                    "note": note,
                    "status": "Đã xác nhận"
                })
                st.success(f"🎉 Cảm ơn quý khách {cust_name}! Đặt bàn thành công với Mã: {booking_id}. Chúng tôi sẽ liên hệ sớm để xác nhận.")
            else:
                st.error("Vui lòng điền đầy đủ Họ tên và Số điện thoại!")
                
    st.markdown("---")
    st.subheader("📋 Danh Sách Bàn Đặt Gần Đây")
    if st.session_state.bookings:
        df_bookings = pd.DataFrame(st.session_state.bookings)
        st.dataframe(df_bookings, use_container_width=True)
    else:
        st.info("Chưa có lịch đặt bàn nào.")

# --- 4. GỌI MÓN ---
elif menu_selection == "🛒 Gọi món":
    st.title("🛒 Giỏ Hàng & Gọi Món")
    
    if not st.session_state.cart:
        st.info("Giỏ hàng của bạn đang trống. Hãy ghé trang **Thực đơn** để chọn món nhé!")
    else:
        st.subheader("Danh sách món đã chọn")
        total_amount = 0
        
        items_to_delete = []
        for name, details in list(st.session_state.cart.items()):
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            with col1:
                st.write(f"**{name}**")
                st.caption(f"{details['price']:,}đ / phần")
            with col2:
                new_qty = st.number_input(f"SL {name}", min_value=1, max_value=50, value=details['qty'], key=f"cart_qty_{name}", label_visibility="collapsed")
                st.session_state.cart[name]['qty'] = new_qty
            with col3:
                subtotal = details['price'] * new_qty
                total_amount += subtotal
                st.write(f"**{subtotal:,}đ**")
            with col4:
                if st.button("🗑️ Xóa", key=f"del_{name}"):
                    items_to_delete.append(name)
            st.markdown("---")
            
        for name in items_to_delete:
            del st.session_state.cart[name]
            st.rerun()
            
        st.markdown(f"### Tổng cộng tạm tính: <span style='color: #FF5722;'>{total_amount:,}đ</span>", unsafe_allow_html=True)
        
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button("🗑️ Xóa toàn bộ giỏ hàng"):
                st.session_state.cart = {}
                st.rerun()
        with col_act2:
            if st.button("💳 Tiến hành đến trang Thanh toán"):
                st.switch_page = True # Chuyển hướng dữ liệu ngầm cho trang thanh toán
                st.success("Giỏ hàng đã sẵn sàng thanh toán! Vui lòng chọn mục **Thanh toán** ở menu bên trái.")

# --- 5. THANH TOÁN ---
elif menu_selection == "💳 Thanh toán":
    st.title("💳 Thanh Toán Hóa Đơn")
    
    if not st.session_state.cart:
        st.warning("Giỏ hàng đang trống! Vui lòng gọi món trước khi thanh toán.")
    else:
        col_info, col_bill = st.columns([1, 1])
        
        with col_info:
            st.subheader("Thông tin khách hàng")
            pay_customer = st.text_input("Tên khách hàng", value="Khách lẻ")
            pay_table = st.selectbox("Số bàn", ["Bàn 01", "Bàn 02", "Bàn 03", "Bàn 04", "Bàn 05", "Bàn VIP 1", "Bàn VIP 2"])
            discount_pct = st.slider("Giảm giá (%)", 0, 50, 0)
            payment_method = st.radio("Phương thức thanh toán", ["Tiền mặt", "Chuyển khoản QR", "Thẻ ngân hàng"])
            
        with col_bill:
            st.subheader("Chi tiết hóa đơn")
            subtotal = sum(d['price'] * d['qty'] for d in st.session_state.cart.values())
            discount_amount = subtotal * (discount_pct / 100)
            after_discount = subtotal - discount_amount
            vat = after_discount * 0.1 # VAT 10%
            grand_total = after_discount + vat
            
            bill_df = []
            for name, d in st.session_state.cart.items():
                bill_df.append({
                    "Món": name,
                    "SL": d['qty'],
                    "Đơn giá": f"{d['price']:,}đ",
                    "Thành tiền": f"{d['price']*d['qty']:,}đ"
                })
            st.table(pd.DataFrame(bill_df))
            
            st.markdown(f"**Tạm tính:** {subtotal:,}đ")
            if discount_pct > 0:
                st.markdown(f"**Giảm giá ({discount_pct}%):** -{discount_amount:,.0f}đ")
            st.markdown(f"**VAT (10%):** {vat:,.0f}đ")
            st.markdown(f"### Tổng thanh toán: <span style='color: #FF5722;'>{grand_total:,.0f}đ</span>", unsafe_allow_html=True)
            
            if st.button("✅ Xác Nhận Thanh Toán & Xuất Hóa Đơn"):
                order_id = f"OD{len(st.session_state.orders)+1:03d}"
                new_order = {
                    "id": order_id,
                    "customer": pay_customer,
                    "table": pay_table,
                    "items": [{"name": k, "price": v['price'], "qty": v['qty']} for k, v in st.session_state.cart.items()],
                    "subtotal": subtotal,
                    "discount": discount_amount,
                    "vat": vat,
                    "total": grand_total,
                    "payment_method": payment_method,
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.orders.append(new_order)
                
                st.success(f"🎉 Thanh toán thành công! Mã đơn hàng: {order_id}")
                
                # Tạo nội dung hóa đơn để tải về
                receipt_text = f"""
========================================
           NHÀ HÀNG BBQ HOUSE           
          HÓA ĐƠN THANH TOÁN            
========================================
Mã đơn: {order_id}
Khách hàng: {pay_customer}
Bàn: {pay_table}
Thời gian: {datetime.now().strftime("%Y-%m-%d %H:%M")}
----------------------------------------
"""
                for item in new_order['items']:
                    receipt_text += f"- {item['name']} x{item['qty']} : {item['price']*item['qty']:,}đ\n"
                receipt_text += f"""----------------------------------------
Tạm tính: {subtotal:,}đ
Giảm giá: {discount_amount:,.0f}đ
VAT (10%): {vat:,.0f}đ
TỔNG CỘNG: {grand_total:,.0f}đ
Phương thức: {payment_method}
========================================
     Cảm ơn quý khách & Hẹn gặp lại!     
"""
                st.download_button(
                    label="📥 Tải hóa đơn (TXT)",
                    data=receipt_text,
                    file_name=f"HoaDon_{order_id}.txt",
                    mime="text/plain"
                )
                
                # Xóa giỏ hàng sau khi thanh toán thành công
                st.session_state.cart = {}

# --- 6. QUẢN LÝ ---
elif menu_selection == "📋 Quản lý":
    st.title("📋 Quản Lý Đơn Hàng & Đặt Bàn")
    
    tab1, tab2 = st.tabs(["📦 Quản lý Đơn hàng", "📅 Quản lý Đặt bàn"])
    
    with tab1:
        st.subheader("Danh sách đơn hàng đã thanh toán")
        if st.session_state.orders:
            orders_summary = []
            for o in st.session_state.orders:
                orders_summary.append({
                    "Mã đơn": o['id'],
                    "Khách hàng": o['customer'],
                    "Bàn": o['table'],
                    "Tổng tiền": f"{o['total']:,.0f}đ",
                    "Thanh toán": o['payment_method'],
                    "Thời gian": o['time']
                })
            st.dataframe(pd.DataFrame(orders_summary), use_container_width=True)
            
            # Xem chi tiết đơn hàng
            selected_order_id = st.selectbox("Chọn mã đơn hàng xem chi tiết", [o['id'] for o in st.session_state.orders])
            detail_order = next((o for o in st.session_state.orders if o['id'] == selected_order_id), None)
            if detail_order:
                st.markdown(f"**Chi tiết đơn hàng {detail_order['id']} - Bàn: {detail_order['table']} - Khách: {detail_order['customer']}**")
                items_df = pd.DataFrame(detail_order['items'])
                st.table(items_df)
        else:
            st.info("Chưa có đơn hàng nào được ghi nhận.")
            
    with tab2:
        st.subheader("Danh sách thông tin đặt bàn")
        if st.session_state.bookings:
            df_bk_mgmt = pd.DataFrame(st.session_state.bookings)
            st.dataframe(df_bk_mgmt, use_container_width=True)
            
            # Hủy lịch đặt bàn
            bk_id_to_cancel = st.selectbox("Chọn Mã đặt bàn cần cập nhật/hủy", [b['id'] for b in st.session_state.bookings])
            if st.button("Hủy lịch đặt bàn này"):
                st.session_state.bookings = [b for b in st.session_state.bookings if b['id'] != bk_id_to_cancel]
                st.success(f"Đã hủy lịch đặt bàn {bk_id_to_cancel} thành công!")
                st.rerun()
        else:
            st.info("Không có lịch đặt bàn nào.")

# --- 7. DOANH THU ---
elif menu_selection == "📊 Doanh thu":
    st.title("📊 Báo Cáo Doanh Thu & Thống Kê")
    
    if not st.session_state.orders:
        st.info("Chưa có dữ liệu doanh thu để thống kê.")
    else:
        total_revenue = sum(o['total'] for o in st.session_state.orders)
        total_orders_count = len(st.session_state.orders)
        avg_revenue = total_revenue / total_orders_count if total_orders_count > 0 else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Tổng Doanh Thu", value=f"{total_revenue:,.0f}đ")
        with col2:
            st.metric(label="Tổng Số Hóa Đơn", value=f"{total_orders_count} Đơn")
        with col3:
            st.metric(label="Doanh Thu Trung Bình / Đơn", value=f"{avg_revenue:,.0f}đ")
            
        st.markdown("---")
        st.subheader("📋 Chi tiết danh sách hóa đơn")
        revenue_df = pd.DataFrame([{
            "Mã đơn": o['id'],
            "Khách hàng": o['customer'],
            "Bàn": o['table'],
            "Tổng tiền (VNĐ)": o['total'],
            "Phương thức": o['payment_method'],
            "Thời gian": o['time']
        } for o in st.session_state.orders])
        
        st.dataframe(revenue_df, use_container_width=True)
        
        # Xuất báo cáo CSV
        csv_data = revenue_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Xuất Báo Cáo Doanh Thu (CSV)",
            data=csv_data,
            file_name="BaoCaoDoanhThu_BBQHouse.csv",
            mime="text/csv"
        )
