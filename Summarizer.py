import openai
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re
import random


openai.api_key = "your api key"
chunk_size = 8000
summary = ""
dict = {

}
def chunk_text(transcript_text, chunk_size):

    words = transcript_text.split()


    chunks = []
    current_chunk = []


    for word in words:
        current_chunk.append(word)
        if len(' '.join(current_chunk)) >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []


    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Streamlit app title
# st.title("AI Summarizer")
st.markdown("<h1 style='text-align: center;'>Chat-GPT Powered Summarizer</h1>", unsafe_allow_html=True)

# Input box for entering the YouTube URL
youtube_url = st.text_input("Input YouTube URL", "")
with open("data.txt", 'w') as file:
    file.write("")
col1, col2, col3, col4, col5,col6 = st.columns([0.5, 0.5, 1, 1, 0.5,0.5])
with col3:
    if st.button("Generate Summary", key="button-col2"):

        if youtube_url:

            match = re.search(r"v=([A-Za-z0-9_-]+)", youtube_url)
            if match:
                video_id = match.group(1)
            else:
                raise ValueError("Invalid YouTube URL")

            transcript = YouTubeTranscriptApi.get_transcript(video_id)

            transcript_text = ' '.join(entry['text'] for entry in transcript)

            chunks = chunk_text(transcript_text, chunk_size)

            for chunk in chunks:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"{chunk}\n\nCreate short concise summary"}
                    ],
                    max_tokens=250,
                    temperature=0.5
                )

                summary += response['choices'][0]['message']['content'].strip() + " "


            file.write(summary)

        else:
            st.warning("Please enter a YouTube URL.")

with col4:
    if st.button("Generate Quiz", key="button-col4"):
        if youtube_url:

            match = re.search(r"v=([A-Za-z0-9_-]+)", youtube_url)
            if match:
                video_id = match.group(1)
            else:
                raise ValueError("Invalid YouTube URL")

            transcript = YouTubeTranscriptApi.get_transcript(video_id)

            transcript_text = ' '.join(entry['text'] for entry in transcript)

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates questions."},
                    {"role": "user", "content": transcript_text},
                    {"role": "user", "content": "Generate 10 quiz questions based on the text with multiple choices."}
                ]
            )

            # The assistant's reply
            quiz_questions = response['choices'][0]['message']['content']


            st.write(quiz_questions)
        else:
            st.warning("Please enter a YouTube URL.")

