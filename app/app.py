import logging
import streamlit as st
from claude import Claude
from git_helper import clone_or_fetch_from_repo, read_src_files
from streamlit_modal import Modal

modal = Modal("Your report has been generated. Would you like to improve your response?",
              key="modal_key", padding=30, max_width=700)

st.set_page_config(page_title="Brita", initial_sidebar_state="collapsed")
st.title("The Code Documentation Generator")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "think_twice_state" not in st.session_state:
    st.session_state["think_twice_state"] = "First"

with st.sidebar:
    api_key = st.sidebar.text_input('Submit your API Key')
    github_url = st.sidebar.text_input('Submit your GitHub URL')
    generate = st.sidebar.button("[ Generate ]")
    
    if generate:
        if not api_key or not github_url:
            st.sidebar.error("Please provide both API Key and GitHub URL to proceed.")
        else:
            st.session_state["api_key"] = api_key
            st.session_state["github_url"] = github_url
            st.session_state["ready"] = True

if st.session_state.get("api_key", False):
    # Get one instance of the client per session.
    st.session_state["client"] = Claude(st.session_state["api_key"])

if all(key in st.session_state for key in ["api_key", "github_url", "ready"]):
    if "action_button_clicked" not in st.session_state:
        st.success(f"We're ready to work on the project {st.session_state['github_url']}", icon="✅")
        st.success(
            "Brita can help with generating a Readme or Docstrings for your project. "
            "Choose from the options below to get started:"
        )
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col2:
            readme_clicked = st.button('[   Readme   ]')
        with col3:
            docstrings_clicked = st.button('[ Docstrings ]')

        if readme_clicked or docstrings_clicked:
            st.session_state["action"] = "readme" if readme_clicked else "docstrings"
            st.session_state["ready"] = False
            st.session_state["action_button_clicked"] = True

            repo, repo_path = clone_or_fetch_from_repo(github_url)
            file_content_dict = read_src_files(repo_path, st.session_state["action"])

            if file_content_dict:
                payload = {
                    "action": st.session_state["action"],
                    "think_twice_action": None,
                    "code": file_content_dict[list(file_content_dict.keys())[0]],
                    "project": "howdoi",
                    "project_url": st.session_state["github_url"],
                }
                st.session_state["messages"].append(
                    st.session_state["client"].ask_claude(payload)
                )
                st.session_state["result"] = True
                st.rerun()
            else:
                st.error("No source files were found in the repository.")
else:
    st.warning("Please submit your API Key and GitHub URL in the sidebar to get started", icon="🖋️")

if st.session_state.get("result", False):

    if modal.is_open():
        with modal.container():
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                moreaccurate_clicked = st.button('[ More Accurate ]')
            with col2:
                morerobust_clicked = st.button('[ More Robust ]')
            with col3:
                nothanks_clicked = st.button('[ No Thanks ]')

            if any([moreaccurate_clicked, morerobust_clicked, nothanks_clicked]):
                st.session_state["think_twice_state"] = "Third"
                if moreaccurate_clicked:
                    st.session_state["think_twice_action"] = "accuracy"
                if morerobust_clicked:
                    st.session_state["think_twice_action"] = "robustness"
                if nothanks_clicked:
                    st.session_state["think_twice_action"] = None
                modal.close()

    if st.session_state["think_twice_state"] == "First":
        st.success("Success! Please review and choose your next action:", icon="🎉")
        col1, col2 = st.columns([1, 1])

        with col1:
            st.download_button("[ Download Result ]", st.session_state["messages"][0][0].text)
        with col2:
            open_modal = st.button("[ Think Twice ]")
            if open_modal:
                modal.open()

        message_placeholder = st.empty()
        with st.chat_message("assistant"):
            st.markdown(st.session_state["messages"][0][0].text, unsafe_allow_html=True)

        if open_modal:
            st.session_state["think_twice_state"] = "Second"
            open_modal = False

    if st.session_state["think_twice_state"] == "Third":
        if st.session_state["think_twice_action"] is not None:
            repo, repo_path = clone_or_fetch_from_repo(github_url)
            file_content_dict = read_src_files(repo_path, st.session_state["action"])
            payload = {
                "action": st.session_state["action"],
                "think_twice_action": st.session_state["think_twice_action"],
                "code": file_content_dict[list(file_content_dict.keys())[0]],
                "project": "howdoi",
                "project_url": st.session_state["github_url"],
            }
            st.session_state["messages"] = []
            st.session_state["messages"].append(
                st.session_state["client"].ask_claude(payload)
            )
            st.session_state["result"] = True
        st.session_state["think_twice_state"] = "Fourth"
        st.rerun()
    
    if st.session_state["think_twice_state"] == "Fourth":
        st.success("Success! Please review the improved result and choose your next action:", icon="🎉")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.download_button("[ Download Updated Result ]", st.session_state["messages"][0][0].text)

        with st.chat_message("assistant"):
            st.markdown(st.session_state["messages"][0][0].text, unsafe_allow_html=True)

st.markdown("""
<style>
   #stDecoration {
      display: none;
   }

   h1 {
      font-size: 82px;
      text-align: center;
      text-transform: uppercase;
   }
   
   .st-emotion-cache-13ln4jf {
      padding: 20rem 10rem 10rem;
      max-width: none;
   }
   
   .stAlert > .st-au { 
      color: black;    
      background-color: yellow;
   }
   
   .st-emotion-cache-1tpl0xr > p {
      font-size: 18px;
   }
   
   .stAlert {
      max-width: fit-content;
      margin: 3rem auto;
   }
   
   .stButton, .stDownloadButton {
      display: flex;
      justify-content: center;
   }
   
   .st-emotion-cache-ytkq5y {
      display: none;
   }
   
     h2 {
      padding-left: 20px
   }
</style>
""", unsafe_allow_html=True)
