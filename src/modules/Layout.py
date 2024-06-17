import streamlit as st

class Layout:

    def show_header(self, types_files):
        """
        Displays the header of the app
        """
        st.markdown(
            f"""
            <h3 style='text-align: center;'> Ask DocuChat about your {types_files} files ! 😎</h3>
            """,
            unsafe_allow_html=True,
        )

    def show_api_key_missing(self):
        """
        Displays a message if the user has not entered an API key
        """
        st.markdown(
            """
            <div style='text-align: center;'>
            <h6>Enter your <a href="https://platform.openai.com/account/api-keys" target="_blank">OpenAI API key</a> to start chatting.
            It will not be stored in anyway. However, please rotate your keys after the use.</h6>
            </div>
            """,
            unsafe_allow_html=True,
        )
