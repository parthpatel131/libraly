import streamlit as st
import pandas as pd

# Initialize session state for books if not exists
if 'books' not in st.session_state:
    st.session_state.books = [
        {"title": "Python Programming", "available": True},
        {"title": "Data Structures", "available": True},
        {"title": "AI Basics", "available": True}
    ]

# Initialize message state
if 'message' not in st.session_state:
    st.session_state.message = ""
if 'message_type' not in st.session_state:
    st.session_state.message_type = "info"

def borrow_book(title):
    """Borrow a book by title"""
    for book in st.session_state.books:
        if book["title"].lower() == title.lower():
            if book["available"]:
                book["available"] = False
                st.session_state.message = f"✅ '{title}' has been borrowed successfully!"
                st.session_state.message_type = "success"
            else:
                st.session_state.message = f"❌ '{title}' is already borrowed."
                st.session_state.message_type = "error"
            return
    st.session_state.message = f"❌ Book '{title}' not found in library."
    st.session_state.message_type = "error"

def return_book(title):
    """Return a book by title"""
    for book in st.session_state.books:
        if book["title"].lower() == title.lower():
            if not book["available"]:
                book["available"] = True
                st.session_state.message = f"✅ '{title}' has been returned successfully!"
                st.session_state.message_type = "success"
            else:
                st.session_state.message = f"ℹ️ '{title}' was not borrowed."
                st.session_state.message_type = "info"
            return
    st.session_state.message = f"❌ Book '{title}' not found in library."
    st.session_state.message_type = "error"

def reset_books():
    """Reset all books to available"""
    for book in st.session_state.books:
        book["available"] = True
    st.session_state.message = "🔄 All books have been reset to available!"
    st.session_state.message_type = "success"

# Page configuration
st.set_page_config(
    page_title="Library Book Management",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .book-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #4CAF50;
    }
    .book-title {
        font-size: 1.2em;
        font-weight: 600;
        color: #2E7D4F;
        margin-bottom: 0.5rem;
    }
    .book-status {
        font-size: 1em;
        margin-bottom: 1rem;
    }
    .available {
        color: #4CAF50;
    }
    .borrowed {
        color: #FF6B6B;
    }
    .header-style {
        background: linear-gradient(90deg, #4CAF50, #45A049);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🔧 Library Tools")
    st.markdown("---")
    
    st.markdown("#### 📖 Quick Help")
    st.markdown("""
    - **Green ✅**: Book is available
    - **Red ❌**: Book is borrowed
    - Use buttons next to books for quick actions
    - Or use the manual input section
    """)
    
    st.markdown("---")
    st.markdown("#### 🔄 Reset Options")
    if st.button("🔄 Reset All Books", help="Make all books available"):
        reset_books()
        st.rerun()
    
    st.markdown("---")
    st.markdown("#### 📊 Library Stats")
    available_count = sum(1 for book in st.session_state.books if book["available"])
    borrowed_count = len(st.session_state.books) - available_count
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Available", available_count, delta=None)
    with col2:
        st.metric("Borrowed", borrowed_count, delta=None)

# Main content
# Header
st.markdown("""
<div class="header-style">
    <h1>📚 Library Book Management System</h1>
    <p>Manage your library books with ease</p>
</div>
""", unsafe_allow_html=True)

# Book Display Section
st.markdown("## 📖 Book Collection")

# Create columns for responsive layout
for i, book in enumerate(st.session_state.books):
    with st.container():
        col1, col2, col3 = st.columns([3, 2, 2])
        
        with col1:
            st.markdown(f"**{book['title']}**")
        
        with col2:
            if book["available"]:
                st.markdown('<span class="available">Available ✅</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="borrowed">Borrowed ❌</span>', unsafe_allow_html=True)
        
        with col3:
            if book["available"]:
                if st.button(f"📤 Borrow", key=f"borrow_{i}", help=f"Borrow {book['title']}"):
                    borrow_book(book['title'])
                    st.rerun()
            else:
                if st.button(f"📥 Return", key=f"return_{i}", help=f"Return {book['title']}"):
                    return_book(book['title'])
                    st.rerun()
        
        st.markdown("---")

# Manual Interaction Section
st.markdown("## 🔍 Manual Book Management")

col1, col2 = st.columns([2, 1])

with col1:
    book_title = st.text_input(
        "📝 Enter Book Title",
        placeholder="e.g., Python Programming",
        help="Enter the exact title of the book you want to borrow or return"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Add spacing
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📤 Borrow Book", disabled=not book_title):
            if book_title:
                borrow_book(book_title)
                st.rerun()
    
    with col_b:
        if st.button("📥 Return Book", disabled=not book_title):
            if book_title:
                return_book(book_title)
                st.rerun()

# Display messages
if st.session_state.message:
    if st.session_state.message_type == "success":
        st.success(st.session_state.message)
    elif st.session_state.message_type == "error":
        st.error(st.session_state.message)
    else:
        st.info(st.session_state.message)
    
    # Clear message after displaying
    st.session_state.message = ""

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>📚 Library Book Management System | Built with Streamlit</p>
    <p>Perfect for students and library staff</p>
</div>
""", unsafe_allow_html=True)