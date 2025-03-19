import json
import streamlit as st
import plotly.express as px
# print(px.__version__)
# exit()
import random
import streamlit as st
st.set_page_config(page_title="Library Management", page_icon="📚", layout="wide")


# File to store books
BOOKS_FILE = "books.json"

def load_books():
    try:
        with open(BOOKS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_books(books):
    with open(BOOKS_FILE, "w") as file:
        json.dump(books, file, indent=4)

# UI Customization - Adding CSS for a better look
st.markdown(
    """
  <style>
    body {
        background: linear-gradient(to right, #3a7bd5, #3a6073);
        color: white;
    }
    .stApp {
        background: linear-gradient(to right, #3a7bd5, #3a6073);
        color: white;
    }
    .book-box {
        padding: 10px;
        margin: 10px 0;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.2);
        color: white;
    }
    h2, h3, label {
        color: white !important;
        font-size: 40px !important;
        font-weight: bold;
        

    }
    input, select {
        font-size: 28px !important;
    }
      /* Navigation Heading */
    .stSidebar h2 {
        color: black !important;
        font-size: 62px !important;
        font-weight: bold;
    }
    choice,radio{
     font-size: 48px !important;
    }
</style>


    """,
    unsafe_allow_html=True,
)

def add_book(title, author, genre, year):
    books = load_books()
    books.append({"title": title, "author": author, "genre": genre, "year": year})
    save_books(books)

def delete_book(title):
    books = load_books()
    books = [book for book in books if book["title"].lower() != title.lower()]
    save_books(books)

def edit_book(old_title, new_title, author, genre, year):
    books = load_books()
    for book in books:
        if book["title"].lower() == old_title.lower():
            book.update({"title": new_title, "author": author, "genre": genre, "year": year})
    save_books(books)

def search_books(query):
    books = load_books()
    return [book for book in books if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()]

def main():
    st.title("📚 Personal Library Manager")
    
    st.sidebar.markdown('<h2 style="color: black;">Navigation</h2>', unsafe_allow_html=True)

    
    choice = st.sidebar.radio("Go to", [
        "📖 Add Book", 
        "📚 View Books", 
        "🔍 Search Book", 
        "📝 Edit/Delete Book", 
        "📊 Statistics", 
        "🎲 Random Recommendation"
    ])
    
    if choice == "📖 Add Book":
        st.subheader("✨ Add a New Book to Your Library")
        title = st.text_input("📌 Book Title")
        author = st.text_input("✍️ Author Name")
        genre = st.selectbox("📂 Genre", ["Fiction", "Non-Fiction", "Science", "History", "Biography", "Fantasy", "Others"])
        year = st.number_input("📅 Year", min_value=1800, max_value=2025, step=1)
        
        if st.button("➕ Add Book", help="Click to add the book!"):
            add_book(title, author, genre, year)
            st.markdown('<p style="color: white; font-size: 38px;">🎉 Book added successfully!</p>', unsafe_allow_html=True)


    elif choice == "📚 View Books":
        st.markdown("<h3 style='color: white;'>📖 Your Library Collection</h3>", unsafe_allow_html=True)

        books = load_books()
        genre_filter = st.selectbox("📌 Filter by Genre", ["All"] + list(set(book["genre"] for book in books)))
        
        if books:
            for book in books:
                if genre_filter == "All" or book["genre"] == genre_filter:
                    st.markdown(f"""
                        <div class='book-box'>
                            <strong>📖 {book['title']}</strong><br>
                            ✍️ {book['author']} ({book['year']})<br>
                            📂 Genre: *{book['genre']}*
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"❌ Delete {book['title']}"):
                        delete_book(book['title'])
                        st.warning(f"⚠️ {book['title']} deleted!")
        else:
           st.markdown('<p style="color: white; font-size: 18px;">🚀 No books found. Start adding some!</p>', unsafe_allow_html=True)


    elif choice == "🔍 Search Book":
        st.subheader("🔎 Search for a Book")
        query = st.text_input("🔍 Enter book title or author")
        if query:
            results = search_books(query)
            if results:
                for book in results:
                    st.markdown(f"📘 **{book['title']}** - ✍️ {book['author']} ({book['year']}) - 📂 *{book['genre']}*")
            else:
              st.markdown('<p style="color: white; font-size: 18px;">⚠️ No matching books found.</p>', unsafe_allow_html=True)


    elif choice == "📝 Edit/Delete Book":
        st.subheader("✏️ Edit or ❌ Delete a Book")
        books = load_books()
        
        if books:  # Check if there are any books available
            book_titles = [book["title"] for book in books]
            selected_book = st.selectbox("📘 Select a book", book_titles)
            
            if selected_book:
                book_data = next(book for book in books if book["title"] == selected_book)
                new_title = st.text_input("📖 Title", value=book_data["title"])
                new_author = st.text_input("✍️ Author", value=book_data["author"])
                new_genre = st.selectbox("📂 Genre", ["Fiction", "Non-Fiction", "Science", "History", "Biography", "Fantasy", "Others"], index=["Fiction", "Non-Fiction", "Science", "History", "Biography", "Fantasy", "Others"].index(book_data["genre"]))
                new_year = st.number_input("📅 Year", min_value=1800, max_value=2025, step=1, value=book_data["year"])
                
                if st.button("✅ Update Book"):
                    edit_book(selected_book, new_title, new_author, new_genre, new_year)
                    st.markdown('<p style="color: white; font-size: 18px;">📖 Book updated successfully!</p>', unsafe_allow_html=True)

                if st.button("❌ Delete Book"):
                    delete_book(selected_book)
                    st.markdown('<p style="color: white; font-size: 18px; background-color: rgba(255, 165, 0, 0.3); padding: 10px; border-radius: 5px;">⚠️ Book deleted!</p>', unsafe_allow_html=True)

        else:
         st.markdown('<p style="color: white; font-size: 18px; background-color: rgba(255, 165, 0, 0.3); padding: 10px; border-radius: 5px;">🚀 No books available to edit or delete.</p>', unsafe_allow_html=True)

    elif choice == "📊 Statistics":
        st.markdown("<h3 style='color: white;'>📊 Library Statistics</h3>", unsafe_allow_html=True)

        books = load_books()
        total_books = len(books)
        st.markdown(
    f"""
    <div style="background-color: #1e90ff; padding: 10px; border-radius: 5px;">
        <p style="color: white; font-weight: bold; font-size: 24px;">📚 Total Books in Library: {total_books}</p>
    </div>
    """,
    unsafe_allow_html=True
)

    elif choice == "🎲 Random Recommendation":
        st.markdown('<h2 style="color: white;">📖 Your Random Book Recommendation</h2>', unsafe_allow_html=True)

        books = load_books()
        if books:
            book = random.choice(books)
        st.markdown(
    f"""
    <div style="background-color: #28a745; padding: 12px; border-radius: 5px;">
        <p style="color: white; font-weight: bold; font-size: 24px;">
            📘 {book['title']} - ✍️ {book['author']} ({book['year']}) - 📂 <i>{book['genre']}</i>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
    else:
        st.markdown('<div style="background-color: #1e3c72; padding: 10px; border-radius: 5px; color: white;">🚀 No books available for recommendation.</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
