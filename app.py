import streamlit as st
import google.generativeai as genai
from datetime import datetime

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MerchandiserAI – বায়ার কমিউনিকেশন সহকারী",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# STYLING
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;600;700&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'Hind Siliguri', sans-serif;
}

.hero {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    padding: 2.5rem 2rem;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    margin-bottom: 0.3rem;
    letter-spacing: -0.5px;
}
.hero p { 
    font-size: 1.05rem; 
    opacity: 0.85; 
    margin: 0.3rem 0;
}
.hero .badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    padding: 0.2rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    margin-top: 0.5rem;
}

.output-card {
    background: #f0faf4;
    border-left: 5px solid #1a7f4b;
    padding: 1.5rem;
    border-radius: 0 12px 12px 0;
    margin-top: 1.2rem;
    font-size: 0.97rem;
    line-height: 1.7;
}

.tip-box {
    background: #fff8e1;
    border-left: 4px solid #f59e0b;
    padding: 1rem 1.2rem;
    border-radius: 0 8px 8px 0;
    margin: 1rem 0;
    font-size: 0.9rem;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #f8fafc;
    padding: 0.5rem;
    border-radius: 12px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.5rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    background: #1a7f4b !important;
    color: white !important;
}

.stButton > button {
    background: #1a7f4b;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1rem;
    padding: 0.6rem 1.5rem;
    transition: all 0.2s;
    width: 100%;
}
.stButton > button:hover {
    background: #156b3f;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(26,127,75,0.3);
}

footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)
# ─────────────────────────────────────────────
# 🔒 LOGIN SYSTEM (THE GATEKEEPER)
# ─────────────────────────────────────────────
def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        user = st.session_state["username_input"].strip()
        pwd = st.session_state["password_input"].strip()
        
        # Check if passwords dict exists in secrets and matches
        if "passwords" in st.secrets and user in st.secrets["passwords"] and st.secrets["passwords"][user] == pwd:
            st.session_state["password_correct"] = True
            del st.session_state["password_input"]  # Clear from memory for security
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    # Show Login Screen
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class='hero' style='padding: 2rem; margin-bottom: 1rem;'>
            <h2>🔒 Factory Login</h2>
            <p>Please enter your access credentials to use MerchandiserAI.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.text_input("Factory ID (Username)", key="username_input")
        st.text_input("Access Code (Password)", type="password", key="password_input")
        st.button("Log In", on_click=password_entered)
        
        if "password_correct" in st.session_state and not st.session_state["password_correct"]:
            st.error("❌ Incorrect Factory ID or Access Code. Contact Admin for access.")
            
    return False

if not check_password():
    st.stop() # Stops the rest of the app from loading until logged in!

# ─────────────────────────────────────────────
# GEMINI SETUP (Your existing code continues here...)
# ─────────────────────────────────────────────
# try:
#     genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# ...
# ─────────────────────────────────────────────
# GEMINI SETUP
# ─────────────────────────────────────────────
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception:
    st.error("⚠️ API key সেট করা হয়নি। secrets.toml ফাইলে GEMINI_API_KEY যোগ করুন।")
    st.stop()

# ─────────────────────────────────────────────
# HERO SECTION & LANGUAGE TOGGLE
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🧵 MerchandiserAI</h1>
    <p>বাংলাদেশের গার্মেন্টস শিল্পের জন্য AI-চালিত বায়ার কমিউনিকেশন সহকারী</p>
    <p><em>Your AI Copilot for Professional Buyer Communication</em></p>
</div>
""", unsafe_allow_html=True)

col_spacer1, col_lang, col_spacer2 = st.columns([1, 2, 1])
with col_lang:
    app_language = st.radio(
        "🌐 App Language / অ্যাপের ভাষা:",
        options=["বাংলা", "English"],
        horizontal=True
    )

# Dynamic Language Variables
is_en = app_language == "English"
lang_name = "English" if is_en else "Bangla (বাংলা)"

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📋 Tech Pack" if is_en else "📋 Tech Pack বুঝুন",
    "✉️ Buyer Email" if is_en else "✉️ Buyer Email লিখুন",
    "🚨 Red Flags" if is_en else "🚨 Red Flag চেক করুন"
])

# ══════════════════════════════════════════════
# TAB 1 — TECH PACK TRANSLATOR
# ══════════════════════════════════════════════
with tab1:
    st.subheader("📋 Understand Tech Pack" if is_en else "📋 টেক প্যাক / বায়ারের ডকুমেন্ট বুঝুন")
    
    tip_text = "<strong>How to use:</strong> Paste any part of a buyer's email or tech pack below. The AI will explain it simply and tell you the next steps." if is_en else "<strong>কীভাবে ব্যবহার করবেন:</strong> বায়ারের ইমেইল বা টেক প্যাক থেকে যেকোনো অংশ কপি করে নিচে পেস্ট করুন। সহজ ভাষায় বুঝিয়ে দেওয়া হবে + পরবর্তী পদক্ষেপ বলা হবে।"
    
    st.markdown(f"""
    <div class="tip-box">
    💡 {tip_text}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        buyer_name = st.text_input("Buyer Name" if is_en else "বায়ারের নাম", placeholder="e.g., H&M, Zara, Next, Primark...")
    with col2:
        specific_q = st.text_input(
            "Specific Question? (Optional)" if is_en else "নির্দিষ্ট প্রশ্ন আছে? (ঐচ্ছিক)",
            placeholder="e.g., What is the GSM? Where to source fabric?" if is_en else "যেমন: GSM কত হবে? Fabric কোথা থেকে নেব?"
        )

    tech_text = st.text_area(
        "Paste Tech Pack / Buyer Document Here" if is_en else "টেক প্যাক / বায়ারের ডকুমেন্ট এখানে পেস্ট করুন",
        height=220,
        placeholder="Paste specifications, emails, or tech pack details here..." if is_en else "বায়ারের ইমেইল, টেক প্যাক বা যেকোনো স্পেসিফিকেশন এখানে পেস্ট করুন..."
    )

    btn_text1 = "🔍 Analyze Tech Pack" if is_en else "🔍 বিশ্লেষণ করো"
    if st.button(btn_text1, key="tp_btn"):
        if not tech_text.strip():
            st.warning("Please paste the document." if is_en else "টেক প্যাকের টেক্সট পেস্ট করুন।")
        else:
            spinner_text = "AI is analyzing... (10-20 sec)" if is_en else "AI বিশ্লেষণ করছে... (১০-২০ সেকেন্ড)"
            with st.spinner(spinner_text):
                prompt = f"""You are a senior RMG (Ready Made Garments) merchandising expert with 25 years of experience 
in Bangladesh's garment export industry, working with global buyers like H&M, Zara, Primark, Next, and Walmart.

A merchandiser in a Bangladesh factory has shared this document from {buyer_name or 'a buyer'}:

---
{tech_text}
---

{f'Their specific question: {specific_q}' if specific_q else ''}

Provide a structured, practical analysis. YOU MUST WRITE THE ENTIRE RESPONSE IN {lang_name}:

## 1. Simple Summary ({lang_name})
Explain what the buyer wants in very simple {lang_name}. Imagine explaining to a junior merchandiser on their first week. Use bullet points. Be specific.

## 2. Key Requirements ({lang_name})
List ALL critical specs: fabric composition, GSM, colors (Pantone if mentioned), measurements, certifications, packaging, labeling, lead time.

## 3. Action Steps ({lang_name})
Step-by-step numbered list of what the merchandiser must do RIGHT NOW and in what order.

## 4. Technical Specs Summary
Extract any measurements, sizes, tolerances, or technical numbers in a clean table format.

## 5. ⚠️ Critical Warnings ({lang_name})
Any part of this document that could cause: sample rejection, shipment delay, or payment issues — explain in plain {lang_name} WHY it's risky and what to do about it.

Be practical. Use Bangladesh RMG context throughout."""

                try:
                    resp = model.generate_content(prompt)
                    st.markdown("### ✅ Analysis Complete" if is_en else "### ✅ বিশ্লেষণ সম্পন্ন")
                    st.markdown(f'<div class="output-card">{resp.text}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "📥 Download Analysis (.txt)" if is_en else "📥 Analysis ডাউনলোড করুন (.txt)",
                        resp.text,
                        file_name=f"techpack_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")

# ══════════════════════════════════════════════
# TAB 2 — BUYER EMAIL DRAFTER
# ══════════════════════════════════════════════
with tab2:
    st.subheader("✉️ Draft Professional Buyer Email" if is_en else "✉️ Professional Buyer Email লিখুন")
    
    tip_text2 = "<strong>How to use:</strong> Describe the situation in your own words. The AI will write a perfectly formatted, professional email ready to send." if is_en else "<strong>কীভাবে ব্যবহার করবেন:</strong> পরিস্থিতি বাংলায় বলুন — AI সঠিক industry format-এ professional email লিখে দেবে। Subject line থেকে sign-off পর্যন্ত সব কিছু।"
    
    st.markdown(f"""
    <div class="tip-box">
    💡 {tip_text2}
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        buyer = st.text_input("Buyer Name" if is_en else "বায়ারের নাম", placeholder="H&M, Zara, Next...", key="b2")
        order_no = st.text_input("Order/Style No.", placeholder="H&M-S26-0012")
    with col2:
        email_opts = [
            "Delay Notification", "Sample Approval", "Price Negotiation", 
            "Clarification Request", "Shipment Confirmation", "Problem Reporting", 
            "Follow-up", "Other"
        ] if is_en else [
            "শিপমেন্ট দেরি হবে (Delay Notification)", "স্যাম্পল অ্যাপ্রুভাল চাওয়া (Sample Approval)",
            "দাম নিয়ে আলোচনা (Price Negotiation)", "টেক প্যাক সম্পর্কে প্রশ্ন (Clarification Request)",
            "শিপমেন্ট নিশ্চিতকরণ (Shipment Confirmation)", "সমস্যা জানানো (Problem Reporting)",
            "ফলো-আপ (Follow-up / চেজ করা)", "অন্য (Other)"
        ]
        email_type = st.selectbox("Email Type" if is_en else "Email-এর ধরন", email_opts)
        urgency = st.selectbox("Urgency" if is_en else "জরুরি মাত্রা", ["Normal", "Urgent", "Very Urgent"])
    with col3:
        your_name = st.text_input("Your Name & Title" if is_en else "আপনার নাম ও পদবী", placeholder="Rahim, Sr. Merchandiser")
        factory = st.text_input("Company Name" if is_en else "কোম্পানির নাম", placeholder="XYZ Garments Ltd.")

    situation = st.text_area(
        "Describe the situation (The more details, the better the email)" if is_en else "পরিস্থিতি বাংলায় বা ইংরেজিতে বলুন (যত বিস্তারিত বলবেন, ততো ভালো email পাবেন)",
        height=150,
        placeholder="e.g. Fabric supplier delayed delivery. We need a 2 week extension on shipment..." if is_en else "যেমন: আমাদের fabric supplier Gazipur থেকে দেরিতে deliver করেছে। Original ship date ১৫ মে ছিল..."
    )

    btn_text2 = "✉️ Generate Email" if is_en else "✉️ Email তৈরি করো"
    if st.button(btn_text2, key="email_btn"):
        if not situation.strip():
            st.warning("Please describe the situation." if is_en else "পরিস্থিতি বর্ণনা করুন।")
        else:
            spinner_text2 = "Drafting professional email..." if is_en else "Professional email লেখা হচ্ছে..."
            with st.spinner(spinner_text2):
                prompt = f"""You are a senior RMG merchandising expert in Bangladesh with 20+ years of buyer communication experience with global fashion brands.

Write a professional buyer email for this situation:

Buyer: {buyer or 'the buyer'}
Order/Style: {order_no or 'N/A'}  
Email Type: {email_type}
Urgency: {urgency}
From: {your_name or 'Senior Merchandiser'}, {factory or 'our factory'}

Situation: {situation}

Format your response EXACTLY like this:

---
**📧 SUBJECT LINE:**
[Industry-standard subject: Buyer | Factory | Season/Order | Topic - IN ENGLISH]

**📝 EMAIL BODY:**
[Complete professional email body - IN ENGLISH]
---

**💡 Strategy Explanation ({lang_name}):**
[2-3 sentences explaining the strategy behind the email in {lang_name}]

**➡️ Next Steps ({lang_name}):**
[2-3 numbered follow-up steps to take after sending, in {lang_name}]

**⚠️ Mistakes to Avoid ({lang_name}):**
[2-3 common mistakes to avoid in this specific scenario, in {lang_name}]

Requirements:
- The EMAIL BODY and SUBJECT MUST be in professional English.
- The explanations and advice MUST be in {lang_name}.
- Use appropriate industry terms (TNA, AQL, GSM, FOB, ETD, ETA, L/C, B/L etc.)
- Tone must match urgency: {urgency}
- Be diplomatic but professional"""

                try:
                    resp = model.generate_content(prompt)
                    st.markdown("### ✅ Your Email is Ready" if is_en else "### ✅ আপনার Professional Email প্রস্তুত")
                    st.markdown(f'<div class="output-card">{resp.text}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "📥 Download Email" if is_en else "📥 Email ডাউনলোড করুন",
                        resp.text,
                        file_name=f"buyer_email_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")

# ══════════════════════════════════════════════
# TAB 3 — RED FLAG DETECTOR
# ══════════════════════════════════════════════
with tab3:
    st.subheader("🚨 LC / Compliance Document Red Flag Detector")
    
    tip_text3 = "<strong>How to use:</strong> Paste LC terms, compliance requirements, or any buyer document. The AI will catch dangerous clauses before they become costly mistakes." if is_en else "<strong>কীভাবে ব্যবহার করবেন:</strong> LC টার্মস, compliance requirements বা যেকোনো buyer document পেস্ট করুন। AI বিপদের জায়গাগুলো আগেই ধরে ফেলবে — costly mistake এড়িয়ে চলুন।"
    
    st.markdown(f"""
    <div class="tip-box">
    💡 {tip_text3}
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        doc_opts = [
            "LC (Letter of Credit) Terms", "Compliance Audit Requirements",
            "Purchase Order (PO) Terms & Conditions", "Quality Manual / AQL",
            "Buyer Code of Conduct", "Shipping / Packing Instructions", "Other Document"
        ] if is_en else [
            "LC (Letter of Credit) Terms", "Compliance Audit Requirements (WRAP, BSCI, Sedex, GOTS)",
            "Purchase Order (PO) Terms & Conditions", "Quality Manual / AQL Requirements",
            "Buyer Code of Conduct", "Shipping / Packing Instructions", "অন্য Buyer Document"
        ]
        doc_type = st.selectbox("Document Type" if is_en else "ডকুমেন্টের ধরন", doc_opts)
    with col2:
        factory_info = st.text_area(
            "About Your Factory (Optional but recommended)" if is_en else "আপনার Factory সম্পর্কে বলুন (ঐচ্ছিক কিন্তু গুরুত্বপূর্ণ)",
            height=100,
            placeholder="e.g. We are a woven factory, no internal washing plant, standard lead time 90 days..." if is_en else "যেমন: আমরা woven factory, WRAP certified, lead time ৯০ দিন, LC payment করি..."
        )

    doc_text = st.text_area(
        "Paste Document Here" if is_en else "ডকুমেন্ট এখানে পেস্ট করুন",
        height=250,
        placeholder="Paste LC terms, PO conditions, or compliance text here..." if is_en else "LC টার্মস, compliance চেকলিস্ট, PO conditions বা যেকোনো buyer document এর টেক্সট এখানে পেস্ট করুন..."
    )

    btn_text3 = "🚨 Detect Red Flags" if is_en else "🚨 Red Flags খুঁজে বের করো"
    if st.button(btn_text3, key="rf_btn"):
        if not doc_text.strip():
            st.warning("Please paste the document." if is_en else "ডকুমেন্ট পেস্ট করুন।")
        else:
            spinner_text3 = "Scanning document for risks... please wait..." if is_en else "ডকুমেন্ট বিশ্লেষণ করা হচ্ছে... মনোযোগ দিয়ে পড়ুন..."
            with st.spinner(spinner_text3):
                prompt = f"""You are Bangladesh's top RMG compliance and LC expert — a consultant who has saved factories from millions of dollars in losses by catching document errors early.

Analyze this {doc_type} for a Bangladesh garment factory.
WRITE YOUR ENTIRE ANALYSIS IN {lang_name}.

Factory Context: {factory_info or 'Standard Bangladesh export-oriented RMG factory'}

Document:
---
{doc_text}
---

Provide a structured risk assessment in {lang_name}:

## 🚨 CRITICAL RED FLAGS
For each critical issue found:
- **Issue:** [What is the issue]
- **Risk:** [What could go wrong — shipment rejection? payment delay? audit failure?]
- **Solution:** [Exactly what to do RIGHT NOW, step by step]

If no critical issues: write "✅ No critical red flags found" (in {lang_name})

## ⚠️ Warnings
Conditions that need attention but are manageable. Explain each briefly in {lang_name}.

## ✅ Standard Clauses
Briefly list clauses that are standard and fine. (Keep this short)

## 📋 Action Checklist
Numbered list of things the factory must verify or prepare immediately.

## 💡 Expert Advice
1-2 practical tips based on Bangladesh RMG industry experience.

Be specific. Name exact clause types. Use Bangladesh industry context."""

                try:
                    resp = model.generate_content(prompt)
                    st.markdown("### ✅ Analysis Complete" if is_en else "### ✅ Red Flag Analysis সম্পন্ন")
                    st.markdown(f'<div class="output-card">{resp.text}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "📥 Download Analysis" if is_en else "📥 Analysis ডাউনলোড করুন",
                        resp.text,
                        file_name=f"redflag_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
                except Exception as e:
                    st.error(f"Error: {e}")

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#888; padding:1rem; font-size:0.9rem;'>
    🧵 <strong>MerchandiserAI</strong> — Built for the Bangladesh Garment Industry<br>
    For support or subscription WhatsApp: <strong>+880 XXXXXXXXXX</strong>
</div>
""", unsafe_allow_html=True)