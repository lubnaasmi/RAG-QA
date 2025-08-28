

from main import answer # my function
import os
import streamlit as st
import pandas as pd


# ----------------------------- Streamlit UI -----------------------------

import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Q&A", layout="wide")

st.markdown("<h1 style='text-align:center;'>📚 RAG – Q&A</h1>", unsafe_allow_html=True)

# List PDFs in the data folder (scrollable)
pdf_folder = "data"
try:
    pdf_files = sorted([f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")])
except FileNotFoundError:
    pdf_files = []
    st.error("`data/` folder not found. Create a folder named `data` next to this file and add PDFs.")

if pdf_files:
    st.markdown(
        """
        <div style='max-height:140px; overflow-y:auto; border:1px solid #ddd; border-radius:6px;'>
            <div style="position:sticky; top:0; background:#f9f9f9; 
                        padding:8px 10px; border-bottom:1px solid #eee; font-size:14px; color:#555;">
                Available PDFs
            </div>
            <div style="padding:8px 10px; line-height:1.6;">
        """ + "".join([f"◽ {f}<br>" for f in pdf_files]) + """
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.warning("No PDF files found in the `data/` folder.")

st.caption("📖 Answers are generated only from stored PDFs.")

# Gap before question
st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    "<h3 style='font-size:20px; font-weight:600;'> 🗨️ Your Question</h3>",
    unsafe_allow_html=True
)

query = st.text_input("", placeholder="Type your question here...", label_visibility="collapsed")

# Helper: detect "unknown" answers
def _is_unknown_answer(text: str) -> bool:
    if not text:
        return True
    s = text.strip().lower().replace("’", "'")
    triggers = [
        "i don't know", "i dont know", "not sure", "i'm not sure", "i am not sure",
        "unknown", "no idea"
    ]
    return any(s == t or s.startswith(t) for t in triggers)

if st.button("Ask") and query.strip():
    with st.spinner("⏳ Analyzing PDFs..."):
        answer_text, primary_page, title, sources = answer(query)

    # Gap before answer block
    st.markdown("<br>", unsafe_allow_html=True)

    # --- Answer ---
    st.markdown("<h3 style='font-size:20px; font-weight:600;'>💬 Answer</h3>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style='padding:15px; background-color:#f6fff6; border-radius:10px; 
                    border:1px solid #cce5cc; font-size:16px; color:#444;'>
            {answer_text if answer_text else "—"}
        </div>
        """,
        unsafe_allow_html=True,
    )

    unknown = _is_unknown_answer(answer_text)

    # Only show Title/Page + Sources if the answer is NOT "I don't know"
    if not unknown:
        # Caption: show Title + Page 
        meta = []
        if title:
            meta.append(f"Title: **{title}**")
        if primary_page is not None:
            meta.append(f"Page: **{primary_page}**")
        if meta:
            st.caption(" • ".join(meta))

        # Gap before sources
        st.markdown("<br>", unsafe_allow_html=True)

        # --- Sources ---
        if sources:
            df = pd.DataFrame(sources).rename(columns={"title": "Title", "page": "Page"})
            st.markdown("<h3 style='font-size:20px; font-weight:600;'> 📑 Sources</h3>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
        else:
            st.caption("No sources returned.")
    else:
        # When the answer is unknown, suppress sources/meta
        st.caption("⚠️ No relevant sources to display for this answer.")