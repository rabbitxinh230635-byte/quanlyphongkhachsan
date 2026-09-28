import streamlit as st
from datetime import datetime, date

# =========================================================
# CẤU HÌNH APP
# =========================================================

st.set_page_config(
    page_title="Hotel Room Management",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>
    .main {
        background-color: #f5f7fa;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .header-box {
        background: linear-gradient(135deg, #17324d, #245b82);
        padding: 25px 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
    }

    .header-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .header-subtitle {
        font-size: 15px;
        opacity: 0.9;
    }

    .room-card {
        background: white;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        border: 1px solid #e8edf2;
    }

    .room-number {
        font-size: 23px;
        font-weight: 700;
        color: #17324d;
    }

    .room-type {
        color: #6b7280;
        font-size: 14px;
        margin-bottom: 10px;
    }

    .status {
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
    }

    .available {
        background: #dcfce7;
        color: #166534;
    }

    .occupied {
        background: #fee2e2;
        color: #991b1b;
    }

    .cleaning {
        background: #fef3c7;
        color: #92400e;
    }

    .maintenance {
        background: #e5e7eb;
        color: #374151;
    }

    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        text-align: center;
    }

    .stat-title {
        color: #6b7280;
        font-size: 14px;
    }

    .stat-value {
        font-size: 30px;
        font-weight: 700;
        color: #17324d;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# DỮ LIỆU PHÒNG MẶC ĐỊNH
# =========================================================

DEFAULT_ROOMS = [
    {"number": "101", "floor": 1, "type": "Standard", "price": 800000, "status": "Trống", "guest": "", "phone": "", "checkin": "", "checkout": ""},
    {"number": "102", "floor": 1, "type": "Standard", "price": 800000, "status": "Đang ở", "guest": "Nguyễn Minh Anh", "phone": "0901234567", "checkin": "28/09/2026", "checkout": "30/09/2026"},
    {"number": "103", "floor": 1, "type": "Superior", "price": 1100000, "status": "Đang dọn", "guest": "", "phone": "", "checkin": "", "checkout": ""},
    {"number": "201", "floor": 2, "type": "Superior", "price": 1100000, "status": "Trống", "guest": "", "phone": "", "checkin": "", "checkout": ""},
    {"number": "202", "floor": 2, "type": "Deluxe", "price": 1500000, "status": "Đang ở", "guest": "Trần Quốc Bảo", "phone": "0912345678", "checkin": "27/09/2026", "checkout": "01/10/2026"},
    {"number": "203", "floor": 2, "type": "Deluxe", "price": 1500000, "status": "Trống", "guest": "", "phone": "", "checkin": "", "checkout": ""},
    {"number": "301", "floor": 3, "type": "Deluxe", "price": 1500000, "status": "Bảo trì", "guest": "", "phone": "", "checkin": "", "checkout": ""},
    {"number": "302", "floor": 3, "type": "Suite", "price": 2500000, "status": "Trống", "guest": "", "phone": "", "checkin": "", "checkout": ""},
    {"number": "303", "floor": 3, "type": "Suite", "price": 2500000, "status": "Đang ở", "guest": "Lê Hoàng Nam", "phone": "0987654321", "checkin": "28/09/2026", "checkout": "02/10/2026"},
    {"number": "401", "floor": 4, "type": "Suite", "price": 2500000, "status": "Trống", "guest": "", "phone": "", "checkin": "", "checkout": ""},
]

# =========================================================
# SESSION STATE
# =========================================================

if "rooms" not in st.session_state:
    st.session_state.rooms = DEFAULT_ROOMS.copy()

if "booking_history" not in st.session_state:
    st.session_state.booking_history = []

if "selected_room" not in st.session_state:
    st.session_state.selected_room = None


# =========================================================
# HÀM HỖ TRỢ
# =========================================================

def format_money(value):
    return f"{value:,.0f} đ".replace(",", ".")


def get_status_class(status):
    mapping = {
        "Trống": "available",
        "Đang ở": "occupied",
        "Đang dọn": "cleaning",
        "Bảo trì": "maintenance"
    }
    return mapping.get(status, "maintenance")


def find_room(room_number):
    for room in st.session_state.rooms:
        if room["number"] == room_number:
            return room
    return None


def update_room(room_number, **kwargs):
    room = find_room(room_number)
    if room:
        room.update(kwargs)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("## 🏨 HOTEL MANAGER")
    st.caption("Hệ thống quản lý phòng khách sạn")

    st.divider()

    menu = st.radio(
        "MENU",
        [
            "📊 Tổng quan",
            "🛏️ Quản lý phòng",
            "📝 Nhận phòng",
            "🚪 Trả phòng",
            "👥 Khách đang lưu trú",
            "📋 Lịch sử đặt phòng"
        ]
    )

    st.divider()

    st.markdown("### Hệ thống")
    st.success("● Hệ thống đang hoạt động")

    st.caption(
        f"Cập nhật: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="header-box">
    <div class="header-title">🏨 Hotel Room Management</div>
    <div class="header-subtitle">
        Hệ thống quản lý phòng và lưu trú khách sạn
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# TỔNG QUAN
# =========================================================

if menu == "📊 Tổng quan":

    rooms = st.session_state.rooms

    total = len(rooms)
    available = sum(r["status"] == "Trống" for r in rooms)
    occupied = sum(r["status"] == "Đang ở" for r in rooms)
    cleaning = sum(r["status"] == "Đang dọn" for r in rooms)
    maintenance = sum(r["status"] == "Bảo trì" for r in rooms)

    occupancy = (occupied / total * 100) if total else 0

    st.subheader("📊 Tổng quan hôm nay")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Tổng phòng", total)
    c2.metric("Phòng trống", available)
    c3.metric("Đang ở", occupied)
    c4.metric("Đang dọn", cleaning)
    c5.metric("Bảo trì", maintenance)

    st.write("")

    left, right = st.columns([1, 1])

    with left:
        st.markdown("### 📈 Tình trạng phòng")

        st.progress(occupancy / 100)

        st.write(
            f"**Công suất phòng hiện tại: {occupancy:.1f}%**"
        )

        st.write(f"🟢 Trống: **{available}** phòng")
        st.write(f"🔴 Đang ở: **{occupied}** phòng")
        st.write(f"🟡 Đang dọn: **{cleaning}** phòng")
        st.write(f"⚫ Bảo trì: **{maintenance}** phòng")

    with right:
        st.markdown("### 🛎️ Phòng đang có khách")

        occupied_rooms = [
            r for r in rooms
            if r["status"] == "Đang ở"
        ]

        if occupied_rooms:
            for room in occupied_rooms:
                st.info(
                    f"**Phòng {room['number']} – {room['type']}**\n\n"
                    f"Khách: **{room['guest']}**\n\n"
                    f"Check-in: {room['checkin']} | "
                    f"Check-out: {room['checkout']}"
                )
        else:
            st.success("Hiện chưa có khách lưu trú.")

    st.divider()

    st.subheader("🛏️ Sơ đồ phòng")

    cols = st.columns(5)

    for index, room in enumerate(rooms):
        with cols[index % 5]:

            status_class = get_status_class(room["status"])

            st.markdown(
                f"""
                <div class="room-card">
                    <div class="room-number">
                        🛏️ {room["number"]}
                    </div>

                    <div class="room-type">
                        {room["type"]} · Tầng {room["floor"]}
                    </div>

                    <span class="status {status_class}">
                        {room["status"]}
                    </span>

                    <p style="margin-top:10px;">
                        <b>{format_money(room["price"])}</b>/đêm
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# QUẢN LÝ PHÒNG
# =========================================================

elif menu == "🛏️ Quản lý phòng":

    st.subheader("🛏️ Quản lý phòng")

    col1, col2, col3 = st.columns(3)

    with col1:
        search = st.text_input(
            "🔎 Tìm phòng",
            placeholder="Nhập số phòng..."
        )

    with col2:
        status_filter = st.selectbox(
            "Trạng thái",
            ["Tất cả", "Trống", "Đang ở", "Đang dọn", "Bảo trì"]
        )

    with col3:
        type_filter = st.selectbox(
            "Loại phòng",
            ["Tất cả"] +
            sorted(list(set(r["type"] for r in st.session_state.rooms)))
        )

    filtered_rooms = st.session_state.rooms

    if search:
        filtered_rooms = [
            r for r in filtered_rooms
            if search.lower() in r["number"].lower()
        ]

    if status_filter != "Tất cả":
        filtered_rooms = [
            r for r in filtered_rooms
            if r["status"] == status_filter
        ]

    if type_filter != "Tất cả":
        filtered_rooms = [
            r for r in filtered_rooms
            if r["type"] == type_filter
        ]

    st.write(f"Hiển thị **{len(filtered_rooms)}** phòng")

    for room in filtered_rooms:

        with st.container(border=True):

            col1, col2, col3, col4, col5 = st.columns(
                [1, 2, 2, 2, 1]
            )

            with col1:
                st.markdown(f"### {room['number']}")

            with col2:
                st.write(f"**Loại:** {room['type']}")
                st.write(f"Tầng {room['floor']}")

            with col3:
                st.write(f"**Giá:** {format_money(room['price'])}")
                st.write(f"**Trạng thái:** {room['status']}")

            with col4:
                if room["guest"]:
                    st.write(f"👤 {room['guest']}")
                    st.write(f"📞 {room['phone']}")
                else:
                    st.write("Chưa có khách")

            with col5:

                if st.button(
                    "Chi tiết",
                    key=f"detail_{room['number']}"
                ):
                    st.session_state.selected_room = room["number"]

    if st.session_state.selected_room:

        room = find_room(st.session_state.selected_room)

        if room:

            st.divider()
            st.subheader(
                f"🔎 Chi tiết phòng {room['number']}"
            )

            c1, c2 = st.columns(2)

            with c1:
                st.write(f"**Số phòng:** {room['number']}")
                st.write(f"**Loại:** {room['type']}")
                st.write(f"**Tầng:** {room['floor']}")
                st.write(
                    f"**Giá:** {format_money(room['price'])}/đêm"
                )

            with c2:
                new_status = st.selectbox(
                    "Cập nhật trạng thái",
                    [
                        "Trống",
                        "Đang ở",
                        "Đang dọn",
                        "Bảo trì"
                    ],
                    index=[
                        "Trống",
                        "Đang ở",
                        "Đang dọn",
                        "Bảo trì"
                    ].index(room["status"]),
                    key=f"status_{room['number']}"
                )

                if st.button(
                    "💾 Lưu trạng thái",
                    key=f"save_{room['number']}"
                ):
                    update_room(
                        room["number"],
                        status=new_status
                    )

                    st.success("Đã cập nhật trạng thái phòng.")
                    st.rerun()


# =========================================================
# NHẬN PHÒNG
# =========================================================

elif menu == "📝 Nhận phòng":

    st.subheader("📝 Nhận phòng – Check-in")

    available_rooms = [
        r for r in st.session_state.rooms
        if r["status"] == "Trống"
    ]

    if not available_rooms:

        st.warning(
            "Hiện không có phòng trống để nhận khách."
        )

    else:

        with st.form("checkin_form"):

            c1, c2 = st.columns(2)

            with c1:

                room_number = st.selectbox(
                    "🛏️ Chọn phòng",
                    [r["number"] for r in available_rooms]
                )

                guest_name = st.text_input(
                    "👤 Họ và tên khách *"
                )

                phone = st.text_input(
                    "📞 Số điện thoại *"
                )

                identity = st.text_input(
                    "🪪 CCCD / Passport"
                )

            with c2:

                checkin_date = st.date_input(
                    "📅 Ngày nhận phòng",
                    value=date.today()
                )

                checkout_date = st.date_input(
                    "📅 Ngày trả phòng"
                )

                adults = st.number_input(
                    "👥 Số người lớn",
                    min_value=1,
                    max_value=10,
                    value=1
                )

                note = st.text_area(
                    "📝 Ghi chú"
                )

            submitted = st.form_submit_button(
                "✅ Xác nhận nhận phòng",
                use_container_width=True
            )

        if submitted:

            if not guest_name.strip():
                st.error("Vui lòng nhập tên khách.")

            elif not phone.strip():
                st.error("Vui lòng nhập số điện thoại.")

            elif checkout_date <= checkin_date:
                st.error(
                    "Ngày trả phòng phải sau ngày nhận phòng."
                )

            else:

                room = find_room(room_number)

                room["status"] = "Đang ở"
                room["guest"] = guest_name
                room["phone"] = phone
                room["checkin"] = checkin_date.strftime("%d/%m/%Y")
                room["checkout"] = checkout_date.strftime("%d/%m/%Y")

                booking = {
                    "room": room_number,
                    "guest": guest_name,
                    "phone": phone,
                    "identity": identity,
                    "checkin": checkin_date.strftime("%d/%m/%Y"),
                    "checkout": checkout_date.strftime("%d/%m/%Y"),
                    "adults": adults,
                    "note": note,
                    "created_at": datetime.now().strftime(
                        "%d/%m/%Y %H:%M"
                    )
                }

                st.session_state.booking_history.append(
                    booking
                )

                st.success(
                    f"Đã nhận phòng {room_number} cho "
                    f"{guest_name}."
                )

                st.rerun()


# =========================================================
# TRẢ PHÒNG
# =========================================================

elif menu == "🚪 Trả phòng":

    st.subheader("🚪 Trả phòng – Check-out")

    occupied_rooms = [
        r for r in st.session_state.rooms
        if r["status"] == "Đang ở"
    ]

    if not occupied_rooms:

        st.info("Hiện không có khách cần trả phòng.")

    else:

        room_number = st.selectbox(
            "Chọn phòng trả",
            [r["number"] for r in occupied_rooms]
        )

        room = find_room(room_number)

        if room:

            st.markdown(
                f"""
                ### 🛏️ Phòng {room['number']}

                **Khách:** {room['guest']}  
                **Số điện thoại:** {room['phone']}  
                **Ngày nhận:** {room['checkin']}  
                **Ngày trả dự kiến:** {room['checkout']}  
                **Giá phòng:** {format_money(room['price'])}/đêm
                """
            )

            checkout_date = st.date_input(
                "Ngày trả thực tế",
                value=date.today()
            )

            nights = st.number_input(
                "Số đêm",
                min_value=1,
                max_value=365,
                value=1
            )

            room_charge = room["price"] * nights

            extra_charge = st.number_input(
                "Chi phí phát sinh",
                min_value=0,
                value=0,
                step=50000
            )

            total = room_charge + extra_charge

            st.metric(
                "TỔNG THANH TOÁN",
                format_money(total)
            )

            if st.button(
                "🚪 Xác nhận trả phòng",
                use_container_width=True
            ):

                room["status"] = "Đang dọn"
                room["guest"] = ""
                room["phone"] = ""
                room["checkin"] = ""
                room["checkout"] = ""

                st.success(
                    f"Đã trả phòng {room_number}. "
                    f"Phòng chuyển sang trạng thái Đang dọn."
                )

                st.rerun()


# =========================================================
# KHÁCH ĐANG LƯU TRÚ
# =========================================================

elif menu == "👥 Khách đang lưu trú":

    st.subheader("👥 Khách đang lưu trú")

    occupied_rooms = [
        r for r in st.session_state.rooms
        if r["status"] == "Đang ở"
    ]

    if not occupied_rooms:

        st.info("Chưa có khách đang lưu trú.")

    else:

        for room in occupied_rooms:

            with st.container(border=True):

                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.markdown(
                        f"### 🛏️ {room['number']}"
                    )
                    st.write(room["type"])

                with c2:
                    st.write("**Khách hàng**")
                    st.write(room["guest"])
                    st.write(room["phone"])

                with c3:
                    st.write("**Check-in**")
                    st.write(room["checkin"])

                    st.write("**Check-out**")
                    st.write(room["checkout"])

                with c4:
                    st.write("**Giá phòng**")
                    st.write(
                        format_money(room["price"])
                    )

                    if st.button(
                        "Trả phòng",
                        key=f"checkout_guest_{room['number']}"
                    ):
                        st.session_state.selected_room = room["number"]


# =========================================================
# LỊCH SỬ
# =========================================================

elif menu == "📋 Lịch sử đặt phòng":

    st.subheader("📋 Lịch sử nhận phòng")

    history = st.session_state.booking_history

    if not history:

        st.info(
            "Chưa có lịch sử giao dịch trong phiên hiện tại."
        )

    else:

        for index, booking in enumerate(
            reversed(history),
            start=1
        ):

            with st.expander(
                f"#{index} – Phòng {booking['room']} – "
                f"{booking['guest']}"
            ):

                c1, c2 = st.columns(2)

                with c1:
                    st.write(
                        f"**Khách:** {booking['guest']}"
                    )
                    st.write(
                        f"**Điện thoại:** {booking['phone']}"
                    )
                    st.write(
                        f"**CCCD/Passport:** "
                        f"{booking['identity'] or '—'}"
                    )

                with c2:
                    st.write(
                        f"**Check-in:** {booking['checkin']}"
                    )
                    st.write(
                        f"**Check-out:** {booking['checkout']}"
                    )
                    st.write(
                        f"**Số người:** {booking['adults']}"
                    )

                if booking["note"]:
                    st.write(
                        f"**Ghi chú:** {booking['note']}"
                    )

                st.caption(
                    f"Tạo lúc: {booking['created_at']}"
                )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🏨 Hotel Room Management System • Streamlit"
)
