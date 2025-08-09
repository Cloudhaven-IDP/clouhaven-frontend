import os
import time
import requests
import streamlit as st
from logic import RequestPayload, send_request

# ===== Config (env) =====
REQUEST_API_URL = os.getenv("REQUEST_API_URL", "http://localhost:8088/v1/requests")
STATUS_API_URL  = os.getenv("STATUS_API_URL",  "http://localhost:8088/v1/status")
GITHUB_URL      = os.getenv("CLOUDHAVEN_GITHUB",   "https://github.com/cloudhaven")
LINKEDIN_URL    = os.getenv("CLOUDHAVEN_LINKEDIN", "https://www.linkedin.com/in/afolabifaj/")
BLOG_URL        = os.getenv("CLOUDHAVEN_BLOG",     "https://afajobi.blog.cloudhaven.work")
ASK_URL         = os.getenv("CLOUDHAVEN_ASK_URL",  "https://ask.cloudhaven.work")
REQUEST_ACCESS_URL = os.getenv("CLOUDHAVEN_REQUEST_ACCESS_URL", "https://request-access.cloudhaven.work")
CONTACT_EMAIL   = os.getenv("CLOUDHAVEN_CONTACT_EMAIL", "afolabi.fajobi1@yahoo.com")

st.set_page_config(
    page_title="Access Request",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===== Success view (rendered via ?view=success) =====
def render_success_view(email: str, rid: str | None):
    st.title("Request Submitted ✅")
    st.write(f"Thanks, **{email or 'requestor'}**.")
    st.write("Your request has been recorded. We’re provisioning read‑only access. This page will refresh with updates.")

    box = st.empty()
    # light polling loop; non-fatal if STATUS_API_URL is not reachable yet
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

# ===== Styles =====
st.markdown("""
<style>
[data-testid="stSidebar"] { min-width: 60px; max-width: 60px; overflow-x: hidden; padding-top: 50px; }
[data-testid="stSidebar"] .block-container { padding: 0; }
[data-testid="stSidebar"] a { display: flex; justify-content: center; padding: 10px 0; }
.footer { position: fixed; bottom: 10px; width: 100%; text-align: center; font-size: 0.75rem; color: #aaa; }
.centered-container { display:flex; flex-direction:column; align-items:center; justify-content:center; }
.highlight-link { background-color: #00c6ff33; border-radius: 6px; padding: 8px; margin-top: 10px; text-align:center; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

# ===== Optional logo + header =====
with st.container():
    st.markdown("<div class='centered-container'>", unsafe_allow_html=True)
    for p in (
        os.path.join(os.path.dirname(__file__), "assets", "cloudhavenlogo.png"),
        "assets/cloudhavenlogo.png",
    ):
        if os.path.exists(p):
            st.image(p, width=100)
            break
    st.markdown("<h1 style='color:#00c6ff;'>Access Request</h1></div>", unsafe_allow_html=True)

# If redirected with ?view=success, render success view first
view = st.query_params.get("view", "")
if view == "success":
    email_q = st.query_params.get("email", "")
    rid_q   = st.query_params.get("rid", "")
    render_success_view(email_q, rid_q)
    st.divider()

# ===== Disclaimer =====
st.info("**By clicking Submit, your are agreeing to having tour name stored in our clourdflare store for acess control.**")

st.divider()

# ===== Form =====
with st.form("access_form"):
    name     = st.text_input("Full Name")
    email    = st.text_input("Email")
    resource = st.text_input("Requested Resource")
    reason   = st.text_area("Reason for Access")
    submitted = st.form_submit_button("Submit Request")

    if submitted:
        try:
            result = send_request(
                RequestPayload(name=name, email=email, resource=resource, reason=reason),
                request_api_url=REQUEST_API_URL,
            )
            if result["action"] == "redirect":
                st.success("Registered. Redirecting…")
                st.markdown(
                    f"<meta http-equiv='refresh' content='0; url={result['redirect_url']}'>",
                    unsafe_allow_html=True,
                )
            else:
                ok = result.get("ok", False)
                msg = result.get("message", "Done.")
                (st.success if ok else st.error)(msg)
        except Exception as e:
            st.error(f"Error: {e}")

st.divider()

# ===== CTA below the form (not in sidebar) =====
if ASK_URL:
    st.link_button("💬 Ask me how I work", ASK_URL)

# ===== Sidebar (icons + contact) =====
with st.sidebar:
    st.markdown(f"[![GitHub](https://img.icons8.com/fluency/24/github.png)]({GITHUB_URL})", unsafe_allow_html=True)
    st.markdown(f"[![LinkedIn](https://img.icons8.com/fluency/24/linkedin.png)]({LINKEDIN_URL})", unsafe_allow_html=True)
    st.markdown(f"[![Blog](https://img.icons8.com/ios-filled/24/rss.png)]({BLOG_URL})", unsafe_allow_html=True)

    # Yahoo Mail icon as inline SVG to avoid CDN issues
    yahoo_svg = """
    <svg width="28" height="28" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <defs><linearGradient id="ygrad" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#7B0099"/><stop offset="100%" stop-color="#41005E"/></linearGradient></defs>
      <rect x="1" y="3" width="22" height="18" rx="3" fill="url(#ygrad)"/>
      <path d="M3.5 6.5L12 12l8.5-5.5" fill="none" stroke="#ffffff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M4 19l5.5-5" fill="none" stroke="#ffffff" stroke-width="1.8" stroke-linecap="round"/>
      <path d="M20 19l-5.5-5" fill="none" stroke="#ffffff" stroke-width="1.8" stroke-linecap="round"/>
    </svg>
    """
    st.markdown(
        f"<div style='text-align:center; margin-top:8px;'>"
        f"<a href='mailto:{CONTACT_EMAIL}' title='Email me'>{yahoo_svg}</a>"
        f"</div>",
        unsafe_allow_html=True,
    )

st.markdown("<div class='footer'>Built by Afolabi Fajobi</div>", unsafe_allow_html=True)
