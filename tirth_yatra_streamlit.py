import streamlit as st
import pandas as pd
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Tirth Yatra Hotel",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for rooms data
if 'rooms' not in st.session_state:
    st.session_state.rooms = {
        101: {"type": "Single", "booked": False, "customer": None, "checkin_time": None},
        102: {"type": "Double", "booked": False, "customer": None, "checkin_time": None},
        103: {"type": "Single", "booked": False, "customer": None, "checkin_time": None},
        104: {"type": "Suite", "booked": False, "customer": None, "checkin_time": None},
        105: {"type": "Double", "booked": False, "customer": None, "checkin_time": None}
    }

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
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 5px solid #FF6B35;
        margin-bottom: 1rem;
    }
    
    .room-available {
        border-left-color: #4CAF50;
        background: linear-gradient(135deg, #f8fff8, #e8f5e8);
    }
    
    .room-booked {
        border-left-color: #f44336;
        background: linear-gradient(135deg, #fff8f8, #ffe8e8);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 1rem;
    }
    
    .booking-form {
        background: linear-gradient(135deg, #f8f9ff, #e6f3ff);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #e3f2fd;
        margin-bottom: 1rem;
    }
    
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin-bottom: 1rem;
    }
    
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        margin-bottom: 1rem;
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
    <p>Sacred Journey Accommodation - Book, View, or Checkout Rooms Easily</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for quick actions
with st.sidebar:
    st.markdown("### 🏨 Quick Actions")
    
    # Hotel Statistics
    total_rooms = len(st.session_state.rooms)
    booked_rooms = sum(1 for room in st.session_state.rooms.values() if room["booked"])
    available_rooms = total_rooms - booked_rooms
    occupancy_rate = (booked_rooms / total_rooms) * 100
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Rooms", total_rooms)
        st.metric("Available", available_rooms)
    with col2:
        st.metric("Booked", booked_rooms)
        st.metric("Occupancy", f"{occupancy_rate:.1f}%")
    
    st.markdown("---")
    
    # Quick Booking Form
    st.markdown("### 📝 Quick Booking")
    with st.form("quick_booking"):
        room_number = st.selectbox(
            "Select Room Number:",
            options=[room_no for room_no, info in st.session_state.rooms.items() if not info["booked"]],
            format_func=lambda x: f"Room {x} ({st.session_state.rooms[x]['type']})"
        )
        customer_name = st.text_input("Guest Name:")
        submit_booking = st.form_submit_button("🔖 Book Room", use_container_width=True)
        
        if submit_booking:
            if room_number and customer_name.strip():
                st.session_state.rooms[room_number]["booked"] = True
                st.session_state.rooms[room_number]["customer"] = customer_name.strip()
                st.session_state.rooms[room_number]["checkin_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.success(f"✅ Room {room_number} booked successfully for {customer_name}!")
                st.rerun()
            else:
                st.error("❌ Please fill in all fields!")
    
    st.markdown("---")
    
    # Quick Checkout
    st.markdown("### 🚪 Quick Checkout")
    booked_room_options = [room_no for room_no, info in st.session_state.rooms.items() if info["booked"]]
    
    if booked_room_options:
        with st.form("quick_checkout"):
            checkout_room = st.selectbox(
                "Select Room to Checkout:",
                options=booked_room_options,
                format_func=lambda x: f"Room {x} - {st.session_state.rooms[x]['customer']}"
            )
            submit_checkout = st.form_submit_button("🏃‍♂️ Checkout", use_container_width=True)
            
            if submit_checkout:
                customer_name = st.session_state.rooms[checkout_room]["customer"]
                st.session_state.rooms[checkout_room]["booked"] = False
                st.session_state.rooms[checkout_room]["customer"] = None
                st.session_state.rooms[checkout_room]["checkin_time"] = None
                st.success(f"✅ {customer_name} checked out from Room {checkout_room}!")
                st.rerun()
    else:
        st.info("No rooms currently booked for checkout.")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## 🏠 Room Status Overview")
    
    # Room status tabs
    tab1, tab2, tab3 = st.tabs(["🔍 All Rooms", "✅ Available Rooms", "❌ Booked Rooms"])
    
    with tab1:
        # Display all rooms
        for room_no, info in st.session_state.rooms.items():
            status_class = "room-available" if not info["booked"] else "room-booked"
            status_text = "Available ✅" if not info["booked"] else "Booked ❌"
            
            with st.container():
                st.markdown(f'<div class="room-card {status_class}">', unsafe_allow_html=True)
                
                col_room1, col_room2, col_room3 = st.columns([2, 2, 1])
                
                with col_room1:
                    st.markdown(f"### Room {room_no}")
                    st.markdown(f"**Type:** {info['type']}")
                    st.markdown(f"**Status:** {status_text}")
                
                with col_room2:
                    if info["booked"]:
                        st.markdown(f"**Guest:** {info['customer']}")
                        st.markdown(f"**Check-in:** {info['checkin_time']}")
                    else:
                        st.markdown("**Ready for booking**")
                        st.markdown("*Available now*")
                
                with col_room3:
                    if info["booked"]:
                        if st.button(f"Checkout", key=f"checkout_{room_no}"):
                            customer_name = info["customer"]
                            st.session_state.rooms[room_no]["booked"] = False
                            st.session_state.rooms[room_no]["customer"] = None
                            st.session_state.rooms[room_no]["checkin_time"] = None
                            st.success(f"✅ {customer_name} checked out from Room {room_no}!")
                            st.rerun()
                    else:
                        if st.button(f"Book Now", key=f"book_{room_no}"):
                            st.session_state.selected_room = room_no
                            st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        # Available rooms only
        available_rooms_list = [(room_no, info) for room_no, info in st.session_state.rooms.items() if not info["booked"]]
        
        if available_rooms_list:
            for room_no, info in available_rooms_list:
                with st.container():
                    col_av1, col_av2, col_av3 = st.columns([2, 2, 1])
                    
                    with col_av1:
                        st.markdown(f"### 🟢 Room {room_no}")
                        st.markdown(f"**Type:** {info['type']}")
                    
                    with col_av2:
                        st.markdown("**Status:** Available ✅")
                        st.markdown("*Ready for immediate booking*")
                    
                    with col_av3:
                        if st.button(f"Book", key=f"book_av_{room_no}"):
                            st.session_state.selected_room = room_no
        else:
            st.info("🎉 All rooms are currently booked!")
    
    with tab3:
        # Booked rooms only
        booked_rooms_list = [(room_no, info) for room_no, info in st.session_state.rooms.items() if info["booked"]]
        
        if booked_rooms_list:
            for room_no, info in booked_rooms_list:
                with st.container():
                    col_bk1, col_bk2, col_bk3 = st.columns([2, 2, 1])
                    
                    with col_bk1:
                        st.markdown(f"### 🔴 Room {room_no}")
                        st.markdown(f"**Type:** {info['type']}")
                    
                    with col_bk2:
                        st.markdown(f"**Guest:** {info['customer']}")
                        st.markdown(f"**Check-in:** {info['checkin_time']}")
                    
                    with col_bk3:
                        if st.button(f"Checkout", key=f"checkout_bk_{room_no}"):
                            customer_name = info["customer"]
                            st.session_state.rooms[room_no]["booked"] = False
                            st.session_state.rooms[room_no]["customer"] = None
                            st.session_state.rooms[room_no]["checkin_time"] = None
                            st.success(f"✅ {customer_name} checked out!")
                            st.rerun()
        else:
            st.info("📭 No rooms are currently booked.")

with col2:
    st.markdown("## 📊 Booking Analytics")
    
    # Create a summary DataFrame
    room_data = []
    for room_no, info in st.session_state.rooms.items():
        room_data.append({
            "Room": f"Room {room_no}",
            "Type": info["type"],
            "Status": "Booked" if info["booked"] else "Available",
            "Guest": info["customer"] if info["booked"] else "N/A"
        })
    
    df = pd.DataFrame(room_data)
    
    # Room type distribution
    st.markdown("### 🏨 Room Types")
    room_type_counts = df["Type"].value_counts()
    st.bar_chart(room_type_counts)
    
    # Booking status
    st.markdown("### 📈 Occupancy Status")
    status_counts = df["Status"].value_counts()
    st.bar_chart(status_counts)
    
    # Current bookings table
    st.markdown("### 📋 Current Bookings")
    booked_df = df[df["Status"] == "Booked"]
    if not booked_df.empty:
        st.dataframe(
            booked_df[["Room", "Type", "Guest"]], 
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No current bookings")

# Handle room selection for booking
if hasattr(st.session_state, 'selected_room'):
    room_no = st.session_state.selected_room
    
    with st.form(f"booking_form_{room_no}"):
        st.markdown(f"### 🔖 Book Room {room_no} ({st.session_state.rooms[room_no]['type']})")
        
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            guest_name = st.text_input("Guest Name:", placeholder="Enter full name")
        with col_form2:
            phone = st.text_input("Phone Number:", placeholder="Contact number")
        
        notes = st.text_area("Special Requests:", placeholder="Any special requirements...")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit_form = st.form_submit_button("✅ Confirm Booking", use_container_width=True)
        with col_btn2:
            cancel_form = st.form_submit_button("❌ Cancel", use_container_width=True)
        
        if submit_form:
            if guest_name.strip():
                st.session_state.rooms[room_no]["booked"] = True
                st.session_state.rooms[room_no]["customer"] = guest_name.strip()
                st.session_state.rooms[room_no]["checkin_time"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                
                st.success(f"🎉 Room {room_no} successfully booked for {guest_name}!")
                if hasattr(st.session_state, 'selected_room'):
                    delattr(st.session_state, 'selected_room')
                st.rerun()
            else:
                st.error("❌ Please enter guest name!")
        
        if cancel_form:
            if hasattr(st.session_state, 'selected_room'):
                delattr(st.session_state, 'selected_room')
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 10px; margin-top: 2rem;">
    <h3>🕉️ तीर्थ यात्रा होटल</h3>
    <p><strong>Sacred Journey Accommodation</strong></p>
    <p>🏨 Premium Hospitality for Pilgrims | 📞 Contact: +91-XXXX-XXXXXX</p>
    <p><em>Developed with Streamlit ❤️</em></p>
</div>
""", unsafe_allow_html=True)