#app.py

import streamlit as st
from streamlit_app import scrap_data


def main():
    st.title("Welcome to the Web Application!")

    options = ["CREATE COPY", "SCRAP DATA"]
    choice = st.selectbox("Choose an operation:", options)

    if choice == "CREATE COPY":
        st.subheader("You selected 'CREATE COPY'")
        # Here, you can call the function that handles the 'CREATE COPY' operation.
        # e.g. create_copy()

    elif choice == "SCRAP DATA":
        # Here, you can call the function that handles the 'SCRAP DATA' operation.
        scrap_data.main()

if __name__ == "__main__":
    main()
