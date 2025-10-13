import streamlit as st
import google.generativeai as genai

# Configure Gemini API
API_KEY = "AIzaSyBdeCZuVDAbaTailEnjD54XSIIXmAoXbBA"  # Replace with your actual API key
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
    st.title("AI Meeting Summarizer + Email Generator")
    st.write("=== Demo Flow: Transcript → Summary → Email ===")
    st.write("")
    
    # File upload section
    st.header("1. Upload Transcript")
    uploaded_file = st.file_uploader("Choose a transcript file", type=['txt'])
    
    if uploaded_file is not None:
        # Read the uploaded file
        transcript_content = uploaded_file.read().decode('utf-8')
        
        # Display the transcript
        st.text_area("Meeting Transcript", transcript_content, height=200, disabled=True)
        transcript_length = len(transcript_content)
        st.info(f"📄 Transcript length: {transcript_length} characters")
        
        # Generate button
        if st.button("🚀 Generate"):
            # Generate summary
            with st.spinner("Generating summary..."):
                st.header("2. Summary")
                summary = generate_summary(transcript_content)
                st.write(summary)
                
                # Display word count
                word_count = len(summary.split())
                st.info(f"📊 Word count: {word_count}")
                
                # Save summary to file
                with open('summary.txt', 'w', encoding='utf-8') as f:
                    f.write(summary)
                st.success("✅ Summary saved to summary.txt")
            
            # Generate email
            with st.spinner("Generating email..."):
                st.header("3. Follow-up Email")
                email = generate_email(transcript_content, summary)
                st.text_area("Email Draft", email, height=250, disabled=True)
                
                # Save email to file
                with open('email_draft.txt', 'w', encoding='utf-8') as f:
                    f.write(email)
                st.success("✅ Email draft saved to email_draft.txt")
            
            # Flow complete
            st.write("")
            st.write("=== Flow Complete! ===")


if __name__ == "__main__":
    main()

