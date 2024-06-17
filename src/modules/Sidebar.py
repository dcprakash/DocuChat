import streamlit as st

class Sidebar:
    MODEL_OPTIONS = ["gpt-4o"]
    TEMPERATURE_MIN_VALUE = 0.0
    TEMPERATURE_MAX_VALUE = 1.0
    TEMPERATURE_DEFAULT_VALUE = 0.0
    TEMPERATURE_STEP = 0.01

    @staticmethod
    def about():
        about = st.sidebar.expander("About DocuChat 😎")
        sections = [
            "###### DocuChat, Empowering you to explore and understand your data effortlessly.",
            "###### Powered by [Langchain](https://python.langchain.com/v0.2/docs/introduction/), [OpenAI](https://platform.openai.com/docs/introduction/overview), and [Github](https://www.linkedin.com/in/chinvar/).",
        ]
        for section in sections:
            about.write(section)

    @staticmethod
    def reset_chat_button():
        if st.button("Reset chat"):
            st.session_state["reset_chat"] = True
        st.session_state.setdefault("reset_chat", False)

    def model_selector(self):
        model = st.selectbox("Model", options=self.MODEL_OPTIONS)
        st.session_state["model"] = model

    def temperature_slider(self):
        temperature = st.slider(
            label="Temperature",
            min_value=self.TEMPERATURE_MIN_VALUE,
            max_value=self.TEMPERATURE_MAX_VALUE,
            value=self.TEMPERATURE_DEFAULT_VALUE,
            step=self.TEMPERATURE_STEP,
        )
        st.session_state["temperature"] = temperature

    def show_options(self):
        with st.sidebar.expander("Hyperparameters ⚙️", expanded=False):
            self.reset_chat_button()
            self.model_selector()
            self.temperature_slider()
        st.session_state.setdefault("model", self.MODEL_OPTIONS[0])
        st.session_state.setdefault("temperature", self.TEMPERATURE_DEFAULT_VALUE)
