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
    margin-bottom: 2rem;
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
# GEMINI SETUP
# ─────────────────────────────────────────────
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-flash")
except Exception:
    st.error("⚠️ API key সেট করা হয়নি। secrets.toml ফাইলে GEMINI_API_KEY যোগ করুন।")
    st.stop()

# ─────────────────────────────────────────────
# HERO SECTION
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🧵 MerchandiserAI</h1>
    <p>বাংলাদেশের গার্মেন্টস শিল্পের জন্য AI-চালিত বায়ার কমিউনিকেশন সহকারী</p>
    <p><em>Your AI Copilot for Professional Buyer Communication</em></p>
    <span class="badge">✅ বাংলা ও English উভয় ভাষায় কাজ করে</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📋 Tech Pack বুঝুন",
    "✉️ Buyer Email লিখুন",
    "🚨 Red Flag চেক করুন"
])

# ══════════════════════════════════════════════
# TAB 1 — TECH PACK TRANSLATOR
# ══════════════════════════════════════════════
with tab1:
    st.subheader("📋 টেক প্যাক / বায়ারের ডকুমেন্ট বুঝুন")
    st.markdown("""
    <div class="tip-box">
    💡 <strong>কীভাবে ব্যবহার করবেন:</strong> বায়ারের ইমেইল বা টেক প্যাক থেকে যেকোনো অংশ কপি করে নিচে পেস্ট করুন।
    সহজ বাংলায় বুঝিয়ে দেওয়া হবে + পরবর্তী পদক্ষেপ বলা হবে।
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        buyer_name = st.text_input("বায়ারের নাম", placeholder="যেমন: H&M, Zara, Next, Primark...")
    with col2:
        specific_q = st.text_input(
            "নির্দিষ্ট প্রশ্ন আছে? (ঐচ্ছিক)",
            placeholder="যেমন: GSM কত হবে? Fabric কোথা থেকে নেব?"
        )

    tech_text = st.text_area(
        "টেক প্যাক / বায়ারের ডকুমেন্ট এখানে পেস্ট করুন",
        height=220,
        placeholder="বায়ারের ইমেইল, টেক প্যাক বা যেকোনো স্পেসিফিকেশন এখানে পেস্ট করুন..."
    )

    if st.button("🔍 বিশ্লেষণ করো", key="tp_btn"):
        if not tech_text.strip():
            st.warning("টেক প্যাকের টেক্সট পেস্ট করুন।")
        else:
            with st.spinner("AI বিশ্লেষণ করছে... (১০-২০ সেকেন্ড)"):
                prompt = f"""You are a senior RMG (Ready Made Garments) merchandising expert with 25 years of experience 
in Bangladesh's garment export industry, working with global buyers like H&M, Zara, Primark, Next, and Walmart.

A merchandiser in a Bangladesh factory has shared this document from {buyer_name or 'a buyer'}:

---
{tech_text}
---

{f'Their specific question: {specific_q}' if specific_q else ''}

Provide a structured, practical analysis:

## ১. সহজ বাংলা ব্যাখ্যা (Simple Bangla Summary)
Explain what the buyer wants in very simple Bangla. Imagine explaining to a junior merchandiser on their first week. Use bullet points. Be specific.

## ২. Key Requirements (English)
List ALL critical specs: fabric composition, GSM, colors (Pantone if mentioned), measurements, certifications, packaging, labeling, lead time.

## ৩. আপনার করণীয় (Action Steps — বাংলায়)
Step-by-step numbered list of what the merchandiser must do RIGHT NOW and in what order.

## ৪. Technical Specs Summary
Extract any measurements, sizes, tolerances, or technical numbers in a clean table format.

## ৫. ⚠️ বিপদের জায়গা (Critical Warnings)
Any part of this document that could cause: sample rejection, shipment delay, or payment issues — explain in plain Bangla WHY it's risky and what to do about it.

Be practical. Use Bangladesh RMG context throughout."""

                try:
                    resp = model.generate_content(prompt)
                    st.markdown("### ✅ বিশ্লেষণ সম্পন্ন")
                    st.markdown(f'<div class="output-card">{resp.text}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "📥 Analysis ডাউনলোড করুন (.txt)",
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
    st.subheader("✉️ Professional Buyer Email লিখুন")
    st.markdown("""
    <div class="tip-box">
    💡 <strong>কীভাবে ব্যবহার করবেন:</strong> পরিস্থিতি বাংলায় বলুন — AI সঠিক industry format-এ professional email লিখে দেবে।
    Subject line থেকে sign-off পর্যন্ত সব কিছু।
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        buyer = st.text_input("বায়ারের নাম", placeholder="H&M, Zara, Next...")
        order_no = st.text_input("Order/Style No.", placeholder="H&M-S26-0012")
    with col2:
        email_type = st.selectbox("Email-এর ধরন", [
            "শিপমেন্ট দেরি হবে (Delay Notification)",
            "স্যাম্পল অ্যাপ্রুভাল চাওয়া (Sample Approval)",
            "দাম নিয়ে আলোচনা (Price Negotiation)",
            "টেক প্যাক সম্পর্কে প্রশ্ন (Clarification Request)",
            "শিপমেন্ট নিশ্চিতকরণ (Shipment Confirmation)",
            "সমস্যা জানানো (Problem Reporting)",
            "ফলো-আপ (Follow-up / চেজ করা)",
            "অন্য (Other)"
        ])
        urgency = st.selectbox("জরুরি মাত্রা", ["Normal", "Urgent", "Very Urgent"])
    with col3:
        your_name = st.text_input("আপনার নাম ও পদবী", placeholder="Rahim, Sr. Merchandiser")
        factory = st.text_input("কোম্পানির নাম", placeholder="XYZ Garments Ltd.")

    situation = st.text_area(
        "পরিস্থিতি বাংলায় বলুন (যত বিস্তারিত বলবেন, ততো ভালো email পাবেন)",
        height=150,
        placeholder="যেমন: আমাদের fabric supplier Gazipur থেকে দেরিতে deliver করেছে। Original ship date ছিল ১৫ মে কিন্তু এখন ১ জুনের আগে ship করা সম্ভব না। বায়ার H&M খুব strict এবং এর আগেও একবার complain করেছে। কীভাবে email লিখব যাতে relationship নষ্ট না হয়?"
    )

    if st.button("✉️ Email তৈরি করো", key="email_btn"):
        if not situation.strip():
            st.warning("পরিস্থিতি বর্ণনা করুন।")
        else:
            with st.spinner("Professional email লেখা হচ্ছে..."):
                prompt = f"""You are a senior RMG merchandising expert in Bangladesh with 20+ years of buyer communication experience with global fashion brands.

Write a professional buyer email for this situation:

Buyer: {buyer or 'the buyer'}
Order/Style: {order_no or 'N/A'}  
Email Type: {email_type}
Urgency: {urgency}
From: {your_name or 'Senior Merchandiser'}, {factory or 'our factory'}

Situation (in Bangla): {situation}

Format your response EXACTLY like this:

---
**📧 SUBJECT LINE:**
[Industry-standard subject: Buyer | Factory | Season/Order | Topic]

**📝 EMAIL BODY:**
[Complete professional email body]
---

**🇧🇩 কেন এই approach কাজ করবে (Bangla explanation):**
[2-3 sentences explaining the strategy]

**➡️ Email পাঠানোর পর কী করবেন:**
[2-3 numbered follow-up steps in Bangla]

**⚠️ এই ধরনের পরিস্থিতিতে যা করবেন না:**
[2-3 common mistakes to avoid, in Bangla]

Requirements:
- Use correct RMG email format
- Subject must follow: [Buyer] | [Factory] | [Season] | [Topic] convention
- Use appropriate industry terms (TNA, AQL, GSM, FOB, ETD, ETA, L/C, B/L etc.)
- Tone must match urgency: {urgency}
- Be diplomatic but professional
- Include specific details from the situation"""

                try:
                    resp = model.generate_content(prompt)
                    st.markdown("### ✅ আপনার Professional Email প্রস্তুত")
                    st.markdown(f'<div class="output-card">{resp.text}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "📥 Email ডাউনলোড করুন",
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
    st.markdown("""
    <div class="tip-box">
    💡 <strong>কীভাবে ব্যবহার করবেন:</strong> LC টার্মস, compliance requirements বা যেকোনো buyer document পেস্ট করুন।
    AI বিপদের জায়গাগুলো আগেই ধরে ফেলবে — costly mistake এড়িয়ে চলুন।
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        doc_type = st.selectbox("ডকুমেন্টের ধরন", [
            "LC (Letter of Credit) Terms",
            "Compliance Audit Requirements (WRAP, BSCI, Sedex, GOTS)",
            "Purchase Order (PO) Terms & Conditions",
            "Quality Manual / AQL Requirements",
            "Buyer Code of Conduct",
            "Shipping / Packing Instructions",
            "অন্য Buyer Document"
        ])
    with col2:
        factory_info = st.text_area(
            "আপনার Factory সম্পর্কে বলুন (ঐচ্ছিক কিন্তু গুরুত্বপূর্ণ)",
            height=100,
            placeholder="যেমন: আমরা woven factory, WRAP certified, lead time ৯০ দিন, LC payment করি..."
        )

    doc_text = st.text_area(
        "ডকুমেন্ট এখানে পেস্ট করুন",
        height=250,
        placeholder="LC টার্মস, compliance চেকলিস্ট, PO conditions বা যেকোনো buyer document এর টেক্সট এখানে পেস্ট করুন..."
    )

    if st.button("🚨 Red Flags খুঁজে বের করো", key="rf_btn"):
        if not doc_text.strip():
            st.warning("ডকুমেন্ট পেস্ট করুন।")
        else:
            with st.spinner("ডকুমেন্ট বিশ্লেষণ করা হচ্ছে... মনোযোগ দিয়ে পড়ুন..."):
                prompt = f"""You are Bangladesh's top RMG compliance and LC expert — a consultant who has saved factories from millions of dollars in losses by catching document errors early.

Analyze this {doc_type} for a Bangladesh garment factory:

Factory Context: {factory_info or 'Standard Bangladesh export-oriented RMG factory'}

Document:
---
{doc_text}
---

Provide a structured risk assessment:

## 🚨 CRITICAL RED FLAGS — অবিলম্বে ব্যবস্থা নিন
For each critical issue found:
- **সমস্যা:** [What is the issue]
- **বিপদ:** [What could go wrong — shipment rejection? payment delay? audit failure?]
- **সমাধান:** [Exactly what to do RIGHT NOW, step by step]

If no critical issues: write "✅ কোনো critical red flag পাওয়া যায়নি"

## ⚠️ সতর্কতা — মনোযোগ দিন
Conditions that need attention but are manageable. Explain each briefly in Bangla.

## ✅ স্বাভাবিক বিষয়
Briefly list clauses that are standard and fine. (Keep this short)

## 📋 এখনই করুন — Action Checklist
Numbered list of things the factory must verify or prepare immediately.

## 💡 বিশেষজ্ঞ পরামর্শ
1-2 practical tips based on Bangladesh RMG industry experience.

Be specific. Name exact clause types. Use Bangladesh industry context. Write warnings in Bangla where it helps understanding."""

                try:
                    resp = model.generate_content(prompt)
                    st.markdown("### ✅ Red Flag Analysis সম্পন্ন")
                    st.markdown(f'<div class="output-card">{resp.text}</div>', unsafe_allow_html=True)
                    st.download_button(
                        "📥 Analysis ডাউনলোড করুন",
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
    🧵 <strong>MerchandiserAI</strong> — বাংলাদেশের গার্মেন্টস শিল্পের জন্য তৈরি<br>
    সাহায্য বা subscription-এর জন্য WhatsApp করুন: <strong>+880 XXXXXXXXXX</strong>
</div>
""", unsafe_allow_html=True)
