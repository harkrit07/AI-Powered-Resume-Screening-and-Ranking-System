# AI-Powered-Resume-Screening-and-Ranking-System

## Overview
The AI-Powered Resume Screening System is a web application designed to streamline the categorization of resumes through automation. Developed using Python and Streamlit, this innovative system employs machine learning algorithms to analyze resume content and predict the appropriate job category.

Supporting PDF, DOCX, and TXT formats, the application is versatile, catering to a wide array of use cases. It’s an ideal solution for recruiters, HR professionals, and organizations seeking to enhance their resume screening process and boost overall efficiency.

Key Feature: Resume Text Extraction
Efficiently extracts text from resumes in PDF, DOCX, and TXT formats.

## How It Works
Upload a Resume: Users can upload a resume in PDF, DOCX, or TXT format.

Text Extraction: The system extracts text from the uploaded file.

Text Cleaning: The extracted text is cleaned and preprocessed to remove unnecessary elements (e.g., URLs, special characters).

Prediction: The cleaned text is passed through a pre-trained machine learning model to predict the job category.

Result Display: The predicted job category is displayed to the user. or TXT format.

## Technology Used
Python: Core programming language.

Streamlit: For building the web application interface.

Scikit-learn: For machine learning model training and prediction.

PyPDF2: For extracting text from PDF files.

python-docx: For extracting text from DOCX files.

Regex (re): For text cleaning and preprocessing.
