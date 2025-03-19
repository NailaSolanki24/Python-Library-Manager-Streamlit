import streamlit as st
import json
import os

data_file = 'library.json'

# Load and save data
def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file, indent=4)

# Streamlit UI
st.title("📚 Library Manager")

# Navigation
menu = ["Home", "Add Book", "Remove Book", "Search Book", "View All Books", "Statistics"]
choice = st.sidebar.selectbox("Menu", menu)

# Load Library Data
library = load_data()

if choice == "Home":
    st.subheader("Welcome to the Library Manager 📖")
    st.write("Use the sidebar to navigate.")

elif choice == "Add Book":
    st.subheader("➕ Add a New Book")
    title = st.text_input("Enter book title")
    author = st.text_input("Enter author name")
    year = st.text_input("Enter publication year")
    genre = st.text_input("Enter genre")
    read = st.checkbox("Mark as Read")

    if st.button("Add Book"):
        new_book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
        library.append(new_book)
        save_library(library)
        st.success(f'Book "{title}" added successfully!')

elif choice == "Remove Book":
    st.subheader("🗑 Remove a Book")
    book_titles = [book["title"] for book in library]
    book_to_remove = st.selectbox("Select a book to remove", book_titles)

    if st.button("Remove Book"):
        library = [book for book in library if book["title"] != book_to_remove]
        save_library(library)
        st.success(f'Book "{book_to_remove}" removed!')

elif choice == "Search Book":
    st.subheader("🔍 Search for a Book")
    search_term = st.text_input("Enter title or author name")

    if st.button("Search"):
        results = [book for book in library if search_term.lower() in book["title"].lower() or search_term.lower() in book["author"].lower()]
        if results:
            for book in results:
                status = "Read" if book["read"] else "Not Read"
                st.write(f"**{book['title']}** by {book['author']}, {book['year']}, {book['genre']} - {status}")
        else:
            st.warning("No matching books found.")

elif choice == "View All Books":
    st.subheader("📖 All Books")
    if library:
        for book in library:
            status = "Read" if book["read"] else "Not Read"
            st.write(f"**{book['title']}** by {book['author']}, {book['year']}, {book['genre']} - {status}")
    else:
        st.warning("No books in the library.")

elif choice == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books = len(library)
    read_books = len([book for book in library if book["read"]])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0

    st.write(f"📚 Total Books: {total_books}")
    st.write(f"✅ Books Read: {read_books}")
    st.write(f"📈 Percentage Read: {percentage_read:.2f}%")
