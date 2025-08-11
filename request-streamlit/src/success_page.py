import os
import time
import requests
import streamlit as st

# ------ Config (env) ------
REQUEST_API_URL = os.getenv("REQUEST_API_URL", "http://localhost:8088/v1/requests")
STATUS_API_URL  = os.getenv("STATUS_API_URL",  "http://localhost:8088/v1/status")
GITHUB_URL      = os.getenv("CLOUDHAVEN_GITHUB",   "https://github.com/cloudhaven")
LINKEDIN_URL    = os.getenv("CLOUDHAVEN_LINKEDIN", "https://www.linkedin.com/in/afolabifaj/")
BLOG_URL        = os.getenv("CLOUDHAVEN_BLOG",     "https://afajobi.blog.cloudhaven.work")
ASK_URL         = os.getenv("CLOUDHAVEN_ASK_URL",  "https://ask.cloudhaven.work")
REQUEST_ACCESS_URL = os.getenv("CLOUDHAVEN_REQUEST_ACCESS_URL", "https://request-access.cloudhaven.work")
CONTACT_EMAIL   = os.getenv("CLOUDHAVEN_CONTACT_EMAIL", "afolabi.fajobi1@yahoo.com")

st.set_page_config(page_title="Access Request", page_icon="💠", layout="wide", initial_sidebar_state="expanded")

# ------ Render success view if ?view=success ------
def render_success_view(email: str, rid: str | None):
    st.title("Request Submitted ✅")
    st.write(f"Thanks, **{email or 'requestor'}**.")
    st.write("Your request has been recorded. We’re provisioning read‑only access. This page will refresh with updates.")

    box = st.empty()
    for _ in range(10):
        if not STATUS_API_URL or not email:
            break
        try:
            res = requests.get(f"{STATUS_API_URL}?email={email}", timeout=5)
            if not res.ok:
                box.info("Waiting for status…")
            else:
                data = res.json() or {}
                state = (data.get("state") or "registered").lower()
                if state == "registered":
                    box.info("Status: registered. Waiting for provisioning…")
                elif state == "provisioning":
                    box.info("Status: provisioning…")
                elif state == "provisioned":
                    box.success("Status: provisioned ✅")
                    links = data.get("links") or {}
                    if ASK_URL:
                        st.link_button("Ask: Guided Tour", ASK_URL)
                    for label, url in links.items():
                        st.link_button(label, url)
                    break
                else:
                    box.info(f"Status: {state}")
        except Exception:
            box.info("Waiting for status…")
        time.sleep(2)

# Read query params (compatible across Streamlit versions)
_q = st.experimental_get_query_params()
view = (_q.get("view") or [""])[0]
email_q = (_q.get("email") or [""])[0]
rid_q   = (_q.get("rid") or [""])[0]

if view == "success":
    # draw success view, then continue rendering the rest of the page (no st.stop)
    render_success_view(email_q, rid_q)
    st.divider()
