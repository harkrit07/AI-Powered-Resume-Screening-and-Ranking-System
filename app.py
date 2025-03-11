import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import altair as alt


# -------------------------- Layout Styling --------------------------
st.markdown(
    """
    <style>
    /* Set Background to Clean White */
    .stApp {
        background-color: #000000;
    }

    /* Main Title */
    .main-title {    
        font-size: 35px;  
        font-weight: bold; 
        text-align: center;   
        color: #FFFF99;   
        padding: 10px;
    }
    .sub-title{
        font-weight: bold;
        text-align: center;
        color: #FFFF99;
        padding: 10px;
    }
    /* Resume Ranking Card */
    .resume-card {
        padding: 15px;
        background: #FFFF99;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
    }
    
    /* File Uploader Button */
    .stFileUploader label {
        color: white !important;
    }

    /* Text Area Styling */
    .stTextArea label {
        font-weight: bold !important;
        color: white !important;
    }

    /* Progress Bar Styling */
    .stProgress > div > div > div > div {
        background-color: #3498DB !important;
    }

    /* CSV Download Button */
    .download-button {
        display: block;
        text-align: center;
        padding: 12px;
        font-size: 18px;
        font-weight: bold;
        color: white;
        text-emphasis: None;
        background-color: #FFFF99;
        border-radius: 10px;
        margin-top: 20px;
    }
    
    /* Footer Styling */
    .footer {
        margin-top: 30px;
        text-align: center;
        padding: 20px;
        background-color: #FFFF99;
        color: black;
        border-radius: 10px;
        font-size: 14px;
    }  
    
    /* Center Align and Color Guidelines */
    .reference {
        color: #000000;
        font-size: 25px; 
    }
    
    .best-match {
        background-color: green; 
        color: #000000;
        border-radius: 4px;
        padding-left: 10px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------------- SidePanel --------------------------
with st.sidebar:
    st.header("FAQs")
    with st.expander("Q1: How do I upload my resume?"):
        st.markdown("A: Click on the 'Upload Resumes' button and select your PDF files.")
    with st.expander("Q2: What file formats are supported?"):
        st.markdown("A: Currently, only PDF files are supported.")
    with st.expander("Q3: How is the matching score calculated?"):
        st.markdown("A: The matching score is calculated using TF-IDF vectorization and cosine similarity.")
    with st.expander("Q4: Can I upload multiple resumes?"):
        st.markdown("A: Yes, you can upload multiple PDF files at once.")
    with st.expander("Q5: How do I download the ranking report?"):
        st.markdown("A: After the resumes are ranked, click on the 'Download Ranking Report' button to download the CSV file.")
        
        
# Reference Section
with st.sidebar:
    st.markdown('<div class="reference">Reference</div>', unsafe_allow_html=True)
    st.markdown('<a href="https://www.resume.com/">🔗 How to Write a Resume?</a>', unsafe_allow_html=True)



# -------------------------- Title of Web App --------------------------
st.markdown('<h7 class="main-title">AI Resume Screening & Ranking System</h7>',unsafe_allow_html=True)


# Upload Resume Section
uploaded_files = st.file_uploader("📤 Upload Resumes", type=["pdf"], accept_multiple_files=True)


# Job Description Text Area
job_description = st.text_area("📝 Enter Job Description")



# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text


# Function to Rank Resumes
def rank_resumes(job_description, resumes):
    documents = [job_description] + resumes
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()
    job_description_vector = vectors[0]
    resume_vectors = vectors[1:]
    cosine_similarities = cosine_similarity(
        [job_description_vector], resume_vectors).flatten()
    return cosine_similarities
if uploaded_files and job_description:
    st.markdown('<h2 class="sub-title">Application Ranking</h2>',unsafe_allow_html=True)
    resumes = []
    for file in uploaded_files:
        text = extract_text_from_pdf(file)
        resumes.append(text)


    # Rank resumes
    scores = rank_resumes(job_description, resumes)


    # To Display scores
    results = pd.DataFrame(
        {"Resume": [file.name for file in uploaded_files], "Score": scores})
    results = results.sort_values(by="Score", ascending=False)


    # To Display results
    for i, row in results.iterrows():
        st.markdown(
            f"""
            <div class="resume-card">
                <h3>📑 {row['Resume']}</h3>
                <p>Matching Score: <b>{row['Score']}%</b></p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(row["Score"] / 100)


    # Show best match
    top_resume = results.iloc[0]
    st.markdown(
        f"<div class='best-match'>Best Match:  {top_resume['Resume']}   with   {top_resume['Score']}%   match!</div>",
        unsafe_allow_html=True,
    )


    # Bar Chart Visualization
    st.markdown('<h2 class="sub-title">📊 Resume Visualization</h2>',unsafe_allow_html=True)
    chart = alt.Chart(results).mark_bar(color='black').encode(
        x=alt.X('Resume', title='Resume', axis=alt.Axis(labelFontWeight='bold', titleFontWeight='bold')),
        y=alt.Y('Score', title='Score', axis=alt.Axis(labelFontWeight='bold', titleFontWeight='bold'))
    )
    st.altair_chart(chart, use_container_width=True)


    # CSV Download Button
    import base64
    csv = results.to_csv(index=False).encode('utf-8')
    st.markdown(
        f'<a href="data:file/csv;base64,{csv.decode()}" download="resume_ranking.csv" class="download-button"> Download Ranking Report</a>',
        unsafe_allow_html=True,
    )


# -------------------------- Footer --------------------------
st.markdown(
    """
    <div class="footer">
        <div>© 2025 AI Resume Screening & Ranking System</div>
        <div style="margin-top: 5px; font-size: 12px;">👩‍💻 Developed by Harkrit</div>
    </div>
    """,
    unsafe_allow_html=True
)


