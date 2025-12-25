import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Meeting Summarizer", page_icon="📝", layout="wide")

# Custom CSS for attractive UI
st.markdown(
    """
<style>
    /* Light overall background so text/content stands out */
    .stApp {
        background: linear-gradient(180deg, #f6f9ff 0%, #ffffff 60%);
        min-height: 100vh;
        color: #0b1226;
    }

    /* Main container: soft card to lift content from background */
    .block-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 32px;
        box-shadow: 0 8px 30px rgba(15, 23, 42, 0.06);
        margin: 20px auto;
        max-width: 1100px;
    }

    /* Headings: dark and clear */
    h1 {
        color: #0b1226;
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 8px;
    }
    h2 { color: #0b1226; font-size: 24px; font-weight:700; }

    /* Buttons: subtle gradient */
    .stButton > button {
        background: linear-gradient(90deg,#5b6ff0,#3ab0c9);
        color: #fff;
        border-radius: 12px;
        padding: 10px 14px;
        font-weight: 700;
        box-shadow: 0 6px 20px rgba(59, 95, 185, 0.12);
    }
    .stButton > button:hover { transform: translateY(-2px); }

    /* File uploader: lighter dashed border */
    .stFileUploader, .stFileUploader div[data-testid="stFileUploadDropzone"] {
        border: 2px dashed rgba(11,18,38,0.06);
        border-radius: 12px;
        padding: 18px;
        background: linear-gradient(180deg, rgba(250,250,255,0.9), rgba(245,249,255,0.9));
    }

    /* Style the button inside the file uploader */
    .stFileUploader button {
        background: linear-gradient(90deg,#5b6ff0,#3ab0c9);
        color: #fff;
        border-radius: 12px;
        padding: 10px 14px;
        font-weight: 700;
        box-shadow: 0 6px 20px rgba(59, 95, 185, 0.12);
    }
    .stFileUploader button:hover { transform: translateY(-2px); }

    /* Text area card wrapper */
    .stTextArea {
        background: linear-gradient(180deg,#ffffff,#fcfdff);
        border: 1px solid rgba(11,18,38,0.06);
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 6px 18px rgba(2,6,23,0.03);
        margin-bottom: 12px;
    }

    /* Ensure textarea text is dark and fully visible (including disabled) */
    .stTextArea textarea {
        background: #ffffff !important;
        color: #0b1226 !important;
        caret-color: #0b1226 !important;
        font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, monospace !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #0b1226 !important;
    }
    .stTextArea textarea[disabled] {
        color: #0b1226 !important;
        background: #ffffff !important;
        opacity: 1 !important;
    }

    /* Labels */
    .stTextArea label, .stTextArea .css-1n76uvr {
        color: #0b1226;
        font-weight: 600;
    }

    /* Highlight card for summary & email to make them pop */
    .card-highlight {
        border: 1px solid rgba(91,111,240,0.12);
        background: linear-gradient(180deg, #fffef7, #ffffff);
        box-shadow: 0 10px 30px rgba(91,111,240,0.04);
        border-radius: 12px;
        padding: 16px;
    }

    /* Force Streamlit text/rendered blocks to dark for readability */
    .stText, .stMarkdown, pre, .streamlit-expanderContent, .stCodeBlock, .element-container .stText {
        color: #0b1226 !important;
        background: transparent !important;
        white-space: pre-wrap !important;
    }

    /* Download buttons: green accent */
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(90deg,#22c55e,#16a34a);
        color: #fff;
        border-radius: 10px;
        padding: 8px 12px;
        font-weight: 700;
    }

    /* Sidebar: light, neutral */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg,#fbfdff 0%, #f7fbff 100%);
        border-radius: 8px;
        padding: 14px;
    }

    /* Small helpers: ensure metrics visible on light background */
    .stMetric {
        background: rgba(11,18,38,0.02);
        border-radius: 8px;
        padding: 10px;
    }

    /* Expander header subtle */
    .streamlit-expanderHeader {
        background: rgba(91,111,240,0.03);
        border-radius: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)


def generate_summary(transcript):
    """Generate a meeting summary using Gemini API."""
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""Generate a concise summary of the following meeting transcript. Keep it between 100-150 words. Focus on key discussions, decisions, and next steps. Structure it with:
- Meeting overview (1-2 sentences)
- Main points discussed
- Key decisions/outcomes
- Any open questions

Transcript:
{transcript}"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def generate_email(transcript_text, summary_text):
    """Generate a follow-up email using Gemini API."""
    try:
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""
        Write a professional follow-up email based on this meeting summary:
        
        {summary_text}
        
        The email should be concise, include action items, and have a professional tone.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating email: {str(e)}"


def main():
    """Main Streamlit application."""
    st.title("🎯 AI Meeting Summarizer + Email Generator")
    st.write("Transform your meeting transcripts into actionable summaries and professional emails")
    st.write("")
    
    # File upload section
    st.header("1️⃣ Upload Transcript")
    uploaded_file = st.file_uploader("Choose a transcript file", type=['txt'])
    
    if uploaded_file is not None:
        # Read the uploaded file
        transcript_content = uploaded_file.read().decode('utf-8')
        
        # Display the transcript
        st.text_area("📄 Meeting Transcript", transcript_content, height=200, disabled=True)
        transcript_length = len(transcript_content)
        st.info(f"📊 Transcript length: {transcript_length} characters")
        
        # Generate button
        if st.button("🚀 Generate Summary & Email"):
            # Generate summary
            with st.spinner("⏳ Generating summary..."):
                st.header("2️⃣ Summary")
                summary = generate_summary(transcript_content)
                st.text_area("Summary Output", summary, height=200, disabled=True)
                
                # Display word count
                word_count = len(summary.split())
                st.info(f"📈 Word count: {word_count} words")
                
                # Save summary to file
                with open('summary.txt', 'w', encoding='utf-8') as f:
                    f.write(summary)
                st.success("✅ Summary saved to summary.txt")
                st.download_button("⬇️ Download Summary", summary, file_name="summary.txt", mime="text/plain")
            
            # Generate email
            with st.spinner("⏳ Generating email..."):
                st.header("3️⃣ Follow-up Email")
                email = generate_email(transcript_content, summary)
                st.text_area("📧 Email Draft", email, height=250, disabled=True)
                
                # Save email to file
                with open('email_draft.txt', 'w', encoding='utf-8') as f:
                    f.write(email)
                st.success("✅ Email draft saved to email_draft.txt")
                st.download_button("⬇️ Download Email Draft", email, file_name="email_draft.txt", mime="text/plain")
            
            # Flow complete
            st.write("")
            st.success("🎉 Flow Complete! Your summary and email are ready to download.")
    else:
        st.info("👆 Please upload a transcript file to get started")


if __name__ == "__main__":
    main()