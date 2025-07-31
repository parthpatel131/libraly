import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
import base64

# Configure page
st.set_page_config(
    page_title="Tirth Yatra Hotel",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Room pricing and images
ROOM_PRICES = {
    "Standard Single": 1500,
    "Deluxe Single": 2200,
    "Standard Double": 2500,
    "Deluxe Double": 3200,
    "Premium Double": 4000,
    "Junior Suite": 5500,
    "Executive Suite": 7500,
    "Presidential Suite": 12000
}

ROOM_IMAGES = {
    "Standard Single": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&h=500&fit=crop",
    "Deluxe Single": "https://images.unsplash.com/photo-1522771739844-6a9f6d5f14af?w=800&h=500&fit=crop",
    "Standard Double": "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800&h=500&fit=crop",
    "Deluxe Double": "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800&h=500&fit=crop",
    "Premium Double": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&h=500&fit=crop",
    "Junior Suite": "https://images.unsplash.com/photo-1521783988139-89397d761dce?w=800&h=500&fit=crop",
    "Executive Suite": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=500&fit=crop",
    "Presidential Suite": "https://images.unsplash.com/photo-1574358336084-408ef9e69d7a?w=800&h=500&fit=crop"
}

ROOM_AMENITIES = {
    "Standard Single": ["Free WiFi", "AC", "TV", "Room Service"],
    "Deluxe Single": ["Free WiFi", "AC", "Smart TV", "Mini Fridge", "Room Service", "Balcony"],
    "Standard Double": ["Free WiFi", "AC", "TV", "Room Service", "Twin/King Bed"],
    "Deluxe Double": ["Free WiFi", "AC", "Smart TV", "Mini Fridge", "Room Service", "Balcony", "City View"],
    "Premium Double": ["Free WiFi", "AC", "Smart TV", "Mini Bar", "Room Service", "Balcony", "Premium Bedding", "Coffee Maker"],
    "Junior Suite": ["Free WiFi", "AC", "Smart TV", "Mini Bar", "24/7 Room Service", "Separate Living Area", "Premium Amenities"],
    "Executive Suite": ["Free WiFi", "AC", "Smart TV", "Full Bar", "24/7 Room Service", "Separate Living & Dining", "Luxury Amenities", "Butler Service"],
    "Presidential Suite": ["Free WiFi", "AC", "Smart TV", "Full Bar", "24/7 Room Service", "3 Separate Rooms", "Luxury Amenities", "Personal Butler", "Private Terrace"]
}

# Initialize session state for rooms data
if 'rooms' not in st.session_state:
    st.session_state.rooms = {
        101: {"type": "Standard Single", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None},
        102: {"type": "Deluxe Single", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None},
        103: {"type": "Standard Double", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None},
        104: {"type": "Deluxe Double", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None},
        105: {"type": "Premium Double", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None},
        106: {"type": "Standard Single", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None},
        107: {"type": "Standard Double", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None},
        108: {"type": "Junior Suite", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None},
        109: {"type": "Executive Suite", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None},
        110: {"type": "Presidential Suite", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None},
        201: {"type": "Deluxe Single", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None},
        202: {"type": "Premium Double", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None},
        203: {"type": "Junior Suite", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None},
        204: {"type": "Executive Suite", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None},
        301: {"type": "Presidential Suite", "booked": False, "customer": None, "checkin_time": None, "payment_status": None, "payment_amount": None}
    }

# Payment processing functions
def generate_upi_qr(amount, room_no, customer_name):
    """Generate UPI QR code for payment"""
    upi_id = "tirthyatra@paytm"  # Example UPI ID
    upi_url = f"upi://pay?pa={upi_id}&am={amount}&cu=INR&tn=Room{room_no}-{customer_name}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(upi_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode()

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #FF6B35, #F7931E);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .room-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 2px solid #e0e6ed;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    
    .room-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    .room-available {
        border-color: #4CAF50;
        background: linear-gradient(135deg, #f8fff8, #e8f5e8);
    }
    
    .room-booked {
        border-color: #f44336;
        background: linear-gradient(135deg, #fff8f8, #ffe8e8);
    }
    
    .price-tag {
        background: linear-gradient(135deg, #FF6B35, #F7931E);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .amenities-list {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .payment-section {
        background: linear-gradient(135deg, #e3f2fd, #bbdefb);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #2196F3;
        margin: 1rem 0;
    }
    
    .qr-container {
        text-align: center;
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .payment-success {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        text-align: center;
        margin: 1rem 0;
    }
    
    .payment-pending {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #ffc107;
        text-align: center;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #FF6B35, #F7931E);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🕉️ तीर्थ यात्रा होटल</h1>
    <h2>Tirth Yatra Hotel</h2>
    <p>Sacred Journey Accommodation - Premium Rooms & Modern Amenities</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for quick actions
with st.sidebar:
    st.markdown("### 🏨 Hotel Dashboard")
    
    # Hotel Statistics
    total_rooms = len(st.session_state.rooms)
    booked_rooms = sum(1 for room in st.session_state.rooms.values() if room["booked"])
    available_rooms = total_rooms - booked_rooms
    occupancy_rate = (booked_rooms / total_rooms) * 100
    total_revenue = sum(room.get("payment_amount", 0) for room in st.session_state.rooms.values() if room.get("payment_status") == "Paid")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Rooms", total_rooms)
        st.metric("Available", available_rooms)
    with col2:
        st.metric("Booked", booked_rooms)
        st.metric("Revenue", f"₹{total_revenue:,}")
    
    st.metric("Occupancy Rate", f"{occupancy_rate:.1f}%")
    
    st.markdown("---")
    
    # Quick Room Search
    st.markdown("### 🔍 Quick Search")
    search_type = st.selectbox("Filter by:", ["All Rooms", "Available Only", "By Room Type", "By Price Range"])
    
    if search_type == "By Room Type":
        selected_type = st.selectbox("Select Type:", list(ROOM_PRICES.keys()))
        filtered_rooms = {k: v for k, v in st.session_state.rooms.items() if v["type"] == selected_type}
    elif search_type == "Available Only":
        filtered_rooms = {k: v for k, v in st.session_state.rooms.items() if not v["booked"]}
    elif search_type == "By Price Range":
        price_range = st.slider("Price Range (₹)", 1000, 15000, (1000, 15000), step=500)
        filtered_rooms = {k: v for k, v in st.session_state.rooms.items() 
                         if price_range[0] <= ROOM_PRICES[v["type"]] <= price_range[1]}
    else:
        filtered_rooms = st.session_state.rooms
    
    st.write(f"Found {len(filtered_rooms)} rooms")

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["🏨 Room Gallery", "💳 Payment Center", "📊 Analytics", "⚙️ Management"])

with tab1:
    st.markdown("## 🏨 Premium Room Collection")
    
    # Room type filter
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        show_type = st.selectbox("Show Rooms:", ["All Rooms", "Available Only", "Booked Only"])
    with col_filter2:
        sort_by = st.selectbox("Sort by:", ["Room Number", "Price (Low to High)", "Price (High to Low)", "Room Type"])
    
    # Filter and sort rooms
    if show_type == "Available Only":
        display_rooms = {k: v for k, v in st.session_state.rooms.items() if not v["booked"]}
    elif show_type == "Booked Only":
        display_rooms = {k: v for k, v in st.session_state.rooms.items() if v["booked"]}
    else:
        display_rooms = st.session_state.rooms
    
    # Sort rooms
    if sort_by == "Price (Low to High)":
        display_rooms = dict(sorted(display_rooms.items(), key=lambda x: ROOM_PRICES[x[1]["type"]]))
    elif sort_by == "Price (High to Low)":
        display_rooms = dict(sorted(display_rooms.items(), key=lambda x: ROOM_PRICES[x[1]["type"]], reverse=True))
    elif sort_by == "Room Type":
        display_rooms = dict(sorted(display_rooms.items(), key=lambda x: x[1]["type"]))
    
    # Display rooms in a grid
    rooms_per_row = 2
    room_items = list(display_rooms.items())
    
    for i in range(0, len(room_items), rooms_per_row):
        cols = st.columns(rooms_per_row)
        
        for j, col in enumerate(cols):
            if i + j < len(room_items):
                room_no, info = room_items[i + j]
                
                with col:
                    # Room card container
                    status_class = "room-available" if not info["booked"] else "room-booked"
                    
                    with st.container():
                        st.markdown(f'<div class="room-card {status_class}">', unsafe_allow_html=True)
                        
                        # Room image
                        st.image(ROOM_IMAGES[info["type"]], caption=f"Room {room_no}", use_container_width=True)
                        
                        # Room details
                        st.markdown(f"### Room {room_no}")
                        st.markdown(f"**{info['type']}**")
                        
                        # Price tag
                        price = ROOM_PRICES[info["type"]]
                        st.markdown(f'<div class="price-tag">₹{price:,}/night</div>', unsafe_allow_html=True)
                        
                        # Status
                        if info["booked"]:
                            st.markdown("🔴 **Status:** Occupied")
                            st.markdown(f"**Guest:** {info['customer']}")
                            if info.get("payment_status"):
                                payment_color = "🟢" if info["payment_status"] == "Paid" else "🟡"
                                st.markdown(f"{payment_color} **Payment:** {info['payment_status']}")
                        else:
                            st.markdown("🟢 **Status:** Available")
                        
                        # Amenities
                        with st.expander("🏨 Amenities"):
                            amenities = ROOM_AMENITIES[info["type"]]
                            for amenity in amenities:
                                st.markdown(f"✓ {amenity}")
                        
                        # Action buttons
                        if info["booked"]:
                            col_btn1, col_btn2 = st.columns(2)
                            with col_btn1:
                                if st.button(f"💳 Payment", key=f"payment_{room_no}"):
                                    st.session_state.selected_payment_room = room_no
                                    st.rerun()
                            with col_btn2:
                                if st.button(f"🚪 Checkout", key=f"checkout_{room_no}"):
                                    customer_name = info["customer"]
                                    st.session_state.rooms[room_no]["booked"] = False
                                    st.session_state.rooms[room_no]["customer"] = None
                                    st.session_state.rooms[room_no]["checkin_time"] = None
                                    st.session_state.rooms[room_no]["payment_status"] = None
                                    st.session_state.rooms[room_no]["payment_amount"] = None
                                    st.success(f"✅ {customer_name} checked out from Room {room_no}!")
                                    st.rerun()
                        else:
                            if st.button(f"🏨 Book Room {room_no}", key=f"book_{room_no}"):
                                st.session_state.selected_room = room_no
                                st.rerun()
                        
                        st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown("## 💳 Payment Processing Center")
    
    # Payment summary
    pending_payments = [(k, v) for k, v in st.session_state.rooms.items() 
                       if v["booked"] and v.get("payment_status") != "Paid"]
    
    if pending_payments:
        st.markdown("### 🟡 Pending Payments")
        for room_no, info in pending_payments:
            col_pay1, col_pay2, col_pay3 = st.columns([2, 1, 1])
            
            with col_pay1:
                st.markdown(f"**Room {room_no}** - {info['customer']}")
                st.markdown(f"Amount: ₹{ROOM_PRICES[info['type']]:,}")
            
            with col_pay2:
                if st.button(f"💳 Process", key=f"process_payment_{room_no}"):
                    st.session_state.selected_payment_room = room_no
                    st.rerun()
            
            with col_pay3:
                status = info.get("payment_status", "Pending")
                color = "🟢" if status == "Paid" else "🟡" if status == "Processing" else "🔴"
                st.markdown(f"{color} {status}")
    else:
        st.success("🎉 All payments are up to date!")
    
    # Payment processing form
    if hasattr(st.session_state, 'selected_payment_room'):
        room_no = st.session_state.selected_payment_room
        room_info = st.session_state.rooms[room_no]
        amount = ROOM_PRICES[room_info["type"]]
        
        st.markdown("---")
        st.markdown(f"### 💳 Payment for Room {room_no}")
        
        col_pay_info1, col_pay_info2 = st.columns(2)
        with col_pay_info1:
            st.markdown(f"**Guest Name:** {room_info['customer']}")
            st.markdown(f"**Room Type:** {room_info['type']}")
        with col_pay_info2:
            st.markdown(f"**Amount:** ₹{amount:,}")
            st.markdown(f"**Status:** {room_info.get('payment_status', 'Pending')}")
        
        # Payment method selection
        payment_method = st.radio("Select Payment Method:", 
                                 ["💳 UPI Payment", "💰 Cash Payment", "🏦 Card Payment", "📱 Online Transfer"])
        
        if payment_method == "💳 UPI Payment":
            st.markdown('<div class="payment-section">', unsafe_allow_html=True)
            st.markdown("#### 📱 UPI Payment")
            
            col_upi1, col_upi2 = st.columns([1, 1])
            
            with col_upi1:
                st.markdown("**Scan QR Code to Pay:**")
                qr_code = generate_upi_qr(amount, room_no, room_info['customer'])
                st.markdown(f'<div class="qr-container"><img src="data:image/png;base64,{qr_code}" width="200"></div>', 
                           unsafe_allow_html=True)
                st.markdown("**UPI ID:** tirthyatra@paytm")
            
            with col_upi2:
                st.markdown("**Payment Details:**")
                st.text_input("Transaction ID:", key=f"txn_id_{room_no}")
                
                col_upi_btn1, col_upi_btn2 = st.columns(2)
                with col_upi_btn1:
                    if st.button("✅ Confirm Payment", key=f"confirm_upi_{room_no}"):
                        st.session_state.rooms[room_no]["payment_status"] = "Paid"
                        st.session_state.rooms[room_no]["payment_amount"] = amount
                        st.success("✅ UPI Payment confirmed!")
                        delattr(st.session_state, 'selected_payment_room')
                        st.rerun()
                
                with col_upi_btn2:
                    if st.button("❌ Cancel", key=f"cancel_upi_{room_no}"):
                        delattr(st.session_state, 'selected_payment_room')
                        st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        elif payment_method == "💰 Cash Payment":
            st.markdown('<div class="payment-section">', unsafe_allow_html=True)
            st.markdown("#### 💰 Cash Payment")
            
            received_amount = st.number_input("Amount Received (₹):", 
                                            min_value=0, 
                                            value=amount, 
                                            key=f"cash_amount_{room_no}")
            
            if received_amount >= amount:
                change_amount = received_amount - amount
                if change_amount > 0:
                    st.success(f"Change to return: ₹{change_amount}")
                
                col_cash1, col_cash2 = st.columns(2)
                with col_cash1:
                    if st.button("✅ Confirm Cash Payment", key=f"confirm_cash_{room_no}"):
                        st.session_state.rooms[room_no]["payment_status"] = "Paid"
                        st.session_state.rooms[room_no]["payment_amount"] = amount
                        st.success("✅ Cash payment confirmed!")
                        delattr(st.session_state, 'selected_payment_room')
                        st.rerun()
                
                with col_cash2:
                    if st.button("❌ Cancel", key=f"cancel_cash_{room_no}"):
                        delattr(st.session_state, 'selected_payment_room')
                        st.rerun()
            else:
                st.error(f"Insufficient amount! Need ₹{amount - received_amount} more.")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        elif payment_method == "🏦 Card Payment":
            st.markdown('<div class="payment-section">', unsafe_allow_html=True)
            st.markdown("#### 🏦 Card Payment")
            
            card_number = st.text_input("Card Number:", placeholder="XXXX-XXXX-XXXX-XXXX", key=f"card_num_{room_no}")
            
            col_card1, col_card2 = st.columns(2)
            with col_card1:
                expiry = st.text_input("Expiry (MM/YY):", key=f"expiry_{room_no}")
            with col_card2:
                cvv = st.text_input("CVV:", type="password", key=f"cvv_{room_no}")
            
            col_card_btn1, col_card_btn2 = st.columns(2)
            with col_card_btn1:
                if st.button("💳 Process Card Payment", key=f"process_card_{room_no}"):
                    if card_number and expiry and cvv:
                        st.session_state.rooms[room_no]["payment_status"] = "Paid"
                        st.session_state.rooms[room_no]["payment_amount"] = amount
                        st.success("✅ Card payment processed successfully!")
                        delattr(st.session_state, 'selected_payment_room')
                        st.rerun()
                    else:
                        st.error("Please fill all card details!")
            
            with col_card_btn2:
                if st.button("❌ Cancel", key=f"cancel_card_{room_no}"):
                    delattr(st.session_state, 'selected_payment_room')
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        elif payment_method == "📱 Online Transfer":
            st.markdown('<div class="payment-section">', unsafe_allow_html=True)
            st.markdown("#### 📱 Online Bank Transfer")
            
            st.markdown("**Bank Details:**")
            st.code("""
Bank Name: State Bank of India
Account Name: Tirth Yatra Hotel Pvt Ltd
Account Number: 1234567890123456
IFSC Code: SBIN0001234
Branch: Sacred Journey Branch
            """)
            
            reference_no = st.text_input("Reference/Transaction Number:", key=f"ref_no_{room_no}")
            
            col_online1, col_online2 = st.columns(2)
            with col_online1:
                if st.button("✅ Confirm Transfer", key=f"confirm_online_{room_no}"):
                    if reference_no:
                        st.session_state.rooms[room_no]["payment_status"] = "Paid"
                        st.session_state.rooms[room_no]["payment_amount"] = amount
                        st.success("✅ Online transfer confirmed!")
                        delattr(st.session_state, 'selected_payment_room')
                        st.rerun()
                    else:
                        st.error("Please enter reference number!")
            
            with col_online2:
                if st.button("❌ Cancel", key=f"cancel_online_{room_no}"):
                    delattr(st.session_state, 'selected_payment_room')
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown("## 📊 Hotel Analytics & Reports")
    
    # Financial Overview
    col_fin1, col_fin2, col_fin3, col_fin4 = st.columns(4)
    
    total_revenue = sum(room.get("payment_amount", 0) for room in st.session_state.rooms.values() 
                       if room.get("payment_status") == "Paid")
    pending_revenue = sum(ROOM_PRICES[room["type"]] for room in st.session_state.rooms.values() 
                         if room["booked"] and room.get("payment_status") != "Paid")
    avg_room_rate = sum(ROOM_PRICES.values()) / len(ROOM_PRICES)
    
    with col_fin1:
        st.metric("Total Revenue", f"₹{total_revenue:,}")
    with col_fin2:
        st.metric("Pending Revenue", f"₹{pending_revenue:,}")
    with col_fin3:
        st.metric("Average Room Rate", f"₹{avg_room_rate:,.0f}")
    with col_fin4:
        st.metric("Total Potential", f"₹{sum(ROOM_PRICES.values()):,}")
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("### 🏨 Room Type Distribution")
        room_type_data = {}
        for room in st.session_state.rooms.values():
            room_type = room["type"]
            if room_type in room_type_data:
                room_type_data[room_type] += 1
            else:
                room_type_data[room_type] = 1
        
        st.bar_chart(room_type_data)
    
    with col_chart2:
        st.markdown("### 💰 Revenue by Room Type")
        revenue_data = {}
        for room in st.session_state.rooms.values():
            if room.get("payment_status") == "Paid":
                room_type = room["type"]
                amount = room.get("payment_amount", 0)
                if room_type in revenue_data:
                    revenue_data[room_type] += amount
                else:
                    revenue_data[room_type] = amount
        
        if revenue_data:
            st.bar_chart(revenue_data)
        else:
            st.info("No revenue data available yet")
    
    # Occupancy Analysis
    st.markdown("### 📈 Occupancy Analysis")
    
    occupancy_data = {"Available": available_rooms, "Occupied": booked_rooms}
    col_occ1, col_occ2 = st.columns([2, 1])
    
    with col_occ1:
        st.bar_chart(occupancy_data)
    
    with col_occ2:
        if booked_rooms > 0:
            st.metric("Occupancy Rate", f"{occupancy_rate:.1f}%")
            if occupancy_rate > 80:
                st.success("🟢 High Occupancy")
            elif occupancy_rate > 50:
                st.warning("🟡 Medium Occupancy")
            else:
                st.info("🔵 Low Occupancy")
        else:
            st.info("No current occupancy")
    
    # Payment Status Overview
    st.markdown("### 💳 Payment Status Overview")
    
    payment_status = {"Paid": 0, "Pending": 0}
    for room in st.session_state.rooms.values():
        if room["booked"]:
            if room.get("payment_status") == "Paid":
                payment_status["Paid"] += 1
            else:
                payment_status["Pending"] += 1
    
    col_pay_chart1, col_pay_chart2 = st.columns(2)
    with col_pay_chart1:
        if payment_status["Paid"] > 0 or payment_status["Pending"] > 0:
            st.bar_chart(payment_status)
        else:
            st.info("No payment data available")
    
    with col_pay_chart2:
        st.markdown("**Payment Summary:**")
        st.markdown(f"✅ Paid: {payment_status['Paid']} rooms")
        st.markdown(f"⏳ Pending: {payment_status['Pending']} rooms")
        
        if payment_status["Pending"] > 0:
            st.warning(f"₹{pending_revenue:,} in pending payments")

with tab4:
    st.markdown("## ⚙️ Hotel Management")
    
    # Bulk Operations
    st.markdown("### 🔄 Bulk Operations")
    
    col_bulk1, col_bulk2, col_bulk3 = st.columns(3)
    
    with col_bulk1:
        if st.button("🧹 Clear All Bookings"):
            if st.session_state.get('confirm_clear', False):
                for room_no in st.session_state.rooms:
                    st.session_state.rooms[room_no]["booked"] = False
                    st.session_state.rooms[room_no]["customer"] = None
                    st.session_state.rooms[room_no]["checkin_time"] = None
                    st.session_state.rooms[room_no]["payment_status"] = None
                    st.session_state.rooms[room_no]["payment_amount"] = None
                st.success("✅ All bookings cleared!")
                st.session_state.confirm_clear = False
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("⚠️ Click again to confirm clearing all bookings")
    
    with col_bulk2:
        if st.button("💳 Mark All Payments as Paid"):
            for room in st.session_state.rooms.values():
                if room["booked"] and room.get("payment_status") != "Paid":
                    room["payment_status"] = "Paid"
                    room["payment_amount"] = ROOM_PRICES[room["type"]]
            st.success("✅ All payments marked as paid!")
            st.rerun()
    
    with col_bulk3:
        if st.button("📊 Generate Report"):
            st.session_state.show_report = True
    
    # Detailed Room Management
    st.markdown("### 🏨 Individual Room Management")
    
    selected_room_mgmt = st.selectbox(
        "Select Room for Management:",
        options=list(st.session_state.rooms.keys()),
        format_func=lambda x: f"Room {x} - {st.session_state.rooms[x]['type']} ({'Occupied' if st.session_state.rooms[x]['booked'] else 'Available'})"
    )
    
    if selected_room_mgmt:
        room_info = st.session_state.rooms[selected_room_mgmt]
        
        col_mgmt1, col_mgmt2 = st.columns(2)
        
        with col_mgmt1:
            st.markdown(f"**Room {selected_room_mgmt} Details:**")
            st.write(f"Type: {room_info['type']}")
            st.write(f"Price: ₹{ROOM_PRICES[room_info['type']]:,}/night")
            st.write(f"Status: {'Occupied' if room_info['booked'] else 'Available'}")
            
            if room_info['booked']:
                st.write(f"Guest: {room_info['customer']}")
                st.write(f"Check-in: {room_info['checkin_time']}")
                st.write(f"Payment: {room_info.get('payment_status', 'Pending')}")
        
        with col_mgmt2:
            if room_info['booked']:
                if st.button(f"🚪 Force Checkout Room {selected_room_mgmt}"):
                    customer_name = room_info['customer']
                    st.session_state.rooms[selected_room_mgmt]["booked"] = False
                    st.session_state.rooms[selected_room_mgmt]["customer"] = None
                    st.session_state.rooms[selected_room_mgmt]["checkin_time"] = None
                    st.session_state.rooms[selected_room_mgmt]["payment_status"] = None
                    st.session_state.rooms[selected_room_mgmt]["payment_amount"] = None
                    st.success(f"✅ {customer_name} checked out from Room {selected_room_mgmt}")
                    st.rerun()
                
                if room_info.get('payment_status') != 'Paid':
                    if st.button(f"💳 Mark Payment as Paid"):
                        st.session_state.rooms[selected_room_mgmt]["payment_status"] = "Paid"
                        st.session_state.rooms[selected_room_mgmt]["payment_amount"] = ROOM_PRICES[room_info['type']]
                        st.success("✅ Payment marked as paid!")
                        st.rerun()
            else:
                st.info("Room is available for booking")

# Handle room booking
if hasattr(st.session_state, 'selected_room'):
    room_no = st.session_state.selected_room
    room_info = st.session_state.rooms[room_no]
    
    st.markdown("---")
    st.markdown(f"## 🏨 Book Room {room_no}")
    
    col_book1, col_book2 = st.columns([1, 1])
    
    with col_book1:
        st.image(ROOM_IMAGES[room_info["type"]], caption=f"Room {room_no}", use_container_width=True)
        
        st.markdown(f"### {room_info['type']}")
        st.markdown(f"**Price:** ₹{ROOM_PRICES[room_info['type']]:,}/night")
        
        # Amenities
        st.markdown("**Amenities:**")
        amenities = ROOM_AMENITIES[room_info["type"]]
        for amenity in amenities:
            st.markdown(f"✓ {amenity}")
    
    with col_book2:
        with st.form(f"booking_form_{room_no}"):
            st.markdown("### 📝 Guest Information")
            
            guest_name = st.text_input("Guest Name*:", placeholder="Enter full name")
            phone = st.text_input("Phone Number*:", placeholder="+91-XXXXXXXXXX")
            email = st.text_input("Email:", placeholder="guest@example.com")
            
            col_date1, col_date2 = st.columns(2)
            with col_date1:
                checkin_date = st.date_input("Check-in Date:", datetime.now().date())
            with col_date2:
                checkout_date = st.date_input("Check-out Date:", datetime.now().date() + timedelta(days=1))
            
            nights = (checkout_date - checkin_date).days
            total_amount = ROOM_PRICES[room_info['type']] * nights if nights > 0 else ROOM_PRICES[room_info['type']]
            
            st.markdown(f"**Duration:** {nights} night(s)")
            st.markdown(f"**Total Amount:** ₹{total_amount:,}")
            
            id_proof = st.selectbox("ID Proof:", ["Aadhar Card", "PAN Card", "Driving License", "Passport"])
            id_number = st.text_input("ID Number:", placeholder="Enter ID number")
            
            special_requests = st.text_area("Special Requests:", placeholder="Any special requirements...")
            
            # Payment selection for booking
            advance_payment = st.selectbox("Advance Payment:", ["Full Payment", "50% Advance", "₹1000 Token"])
            
            if advance_payment == "Full Payment":
                advance_amount = total_amount
            elif advance_payment == "50% Advance":
                advance_amount = total_amount // 2
            else:
                advance_amount = 1000
            
            st.markdown(f"**Advance Amount:** ₹{advance_amount:,}")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit_booking = st.form_submit_button("✅ Confirm Booking", use_container_width=True)
            with col_btn2:
                cancel_booking = st.form_submit_button("❌ Cancel", use_container_width=True)
            
            if submit_booking:
                if guest_name.strip() and phone.strip():
                    st.session_state.rooms[room_no]["booked"] = True
                    st.session_state.rooms[room_no]["customer"] = guest_name.strip()
                    st.session_state.rooms[room_no]["checkin_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    st.session_state.rooms[room_no]["payment_status"] = "Pending"
                    st.session_state.rooms[room_no]["payment_amount"] = 0
                    
                    st.success(f"🎉 Room {room_no} successfully booked for {guest_name}!")
                    st.info(f"Please proceed to payment of ₹{advance_amount:,}")
                    
                    # Set up for payment
                    st.session_state.selected_payment_room = room_no
                    
                    if hasattr(st.session_state, 'selected_room'):
                        delattr(st.session_state, 'selected_room')
                    st.rerun()
                else:
                    st.error("❌ Please fill in required fields (Name and Phone)!")
            
            if cancel_booking:
                if hasattr(st.session_state, 'selected_room'):
                    delattr(st.session_state, 'selected_room')
                st.rerun()

# Show detailed report if requested
if st.session_state.get('show_report', False):
    st.markdown("---")
    st.markdown("## 📋 Detailed Hotel Report")
    
    # Generate comprehensive report
    report_data = []
    for room_no, info in st.session_state.rooms.items():
        report_data.append({
            "Room": room_no,
            "Type": info["type"],
            "Price": f"₹{ROOM_PRICES[info['type']]:,}",
            "Status": "Occupied" if info["booked"] else "Available",
            "Guest": info.get("customer", "N/A"),
            "Check-in": info.get("checkin_time", "N/A"),
            "Payment": info.get("payment_status", "N/A"),
            "Amount": f"₹{info.get('payment_amount', 0):,}" if info.get('payment_amount') else "₹0"
        })
    
    df_report = pd.DataFrame(report_data)
    
    # Display report
    st.dataframe(df_report, use_container_width=True)
    
    # Summary statistics
    col_sum1, col_sum2, col_sum3 = st.columns(3)
    
    with col_sum1:
        st.markdown("**📊 Summary Statistics:**")
        st.write(f"Total Rooms: {len(st.session_state.rooms)}")
        st.write(f"Occupied: {booked_rooms}")
        st.write(f"Available: {available_rooms}")
    
    with col_sum2:
        st.markdown("**💰 Financial Summary:**")
        st.write(f"Total Revenue: ₹{total_revenue:,}")
        st.write(f"Pending Revenue: ₹{pending_revenue:,}")
        st.write(f"Potential Revenue: ₹{sum(ROOM_PRICES.values()):,}")
    
    with col_sum3:
        st.markdown("**📈 Performance:**")
        st.write(f"Occupancy Rate: {occupancy_rate:.1f}%")
        st.write(f"Average Room Rate: ₹{avg_room_rate:,.0f}")
        st.write(f"Revenue Per Room: ₹{total_revenue/len(st.session_state.rooms) if len(st.session_state.rooms) > 0 else 0:,.0f}")
    
    # Download report
    csv = df_report.to_csv(index=False)
    st.download_button(
        label="📥 Download Report as CSV",
        data=csv,
        file_name=f"tirth_yatra_report_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv"
    )
    
    if st.button("❌ Close Report"):
        st.session_state.show_report = False
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 10px; margin-top: 2rem;">
    <h3>🕉️ तीर्थ यात्रा होटल</h3>
    <p><strong>Sacred Journey Accommodation</strong></p>
    <p>🏨 Premium Hospitality for Pilgrims | 📞 Contact: +91-9876-543210 | 📧 info@tirthyatra.com</p>
    <p>🏦 UPI: tirthyatra@paytm | 🌐 www.tirthyatrahotel.com</p>
    <p><em>Developed with Streamlit & Modern Technology ❤️</em></p>
</div>
""", unsafe_allow_html=True)