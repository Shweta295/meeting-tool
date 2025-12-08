# Meeting Summarizer Tool

A simple web-based tool to summarize meeting transcripts and generate follow-up emails using Google Gemini AI.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get your Google Gemini API key:**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create an API key
   - Copy the API key

3. **Add your API key:**
   - Open `meeting_summarizer.py`
   - Replace `absjdhfhhfoisjfoiejijojo` with your actual API key

## How to Run

1. **Start the application:**
   ```bash
   streamlit run meeting_summarizer.py
   ```

2. **Use the tool:**
   - Click "Browse files" to upload a `.txt` transcript file
   - Review the transcript displayed
   - Click "Generate Summary and Email" button
   - View the generated summary and email draft
   - Files are automatically saved as `summary.txt` and `email_draft.txt`

## Example

A sample transcript file (`transcript.txt`) is included in this project for testing.

## Output Files

- `summary.txt` - Meeting summary with key points, decisions, and action items
- `email_draft.txt` - Professional follow-up email draft

