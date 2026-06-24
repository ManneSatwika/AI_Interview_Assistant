# AI Interview Assistant 🎤

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Whisper](https://img.shields.io/badge/OpenAI-Whisper-black)
![Status](https://img.shields.io/badge/Project-Completed-success)

An **AI-powered interview practice assistant** built with **Streamlit** that helps users practice interview questions using **voice recording, speech transcription, answer scoring, resume-based question generation, and PDF report generation**.

---

## 📌 Project Overview

**AI Interview Assistant** simulates a basic interview practice environment where a user can:

* select an interview role
* upload a resume in PDF format
* receive role-based and resume-based interview questions
* record answers directly in the app
* convert spoken answers to text using **Whisper**
* get **answer scoring + feedback**
* download a **final PDF interview report**

This project was built as a **portfolio project** to demonstrate practical skills in:

* Python
* Streamlit
* speech-to-text integration
* PDF processing
* report generation
* end-to-end application building

---

## 🚀 Features

### 🎯 1. Role-Based Interview Questions

The app provides interview questions based on the selected role.

**Supported roles:**

* Data Analyst
* Python Developer
* Java Developer
* HR / General

---

### 📄 2. Resume Upload and Resume-Based Questions

Users can upload a **resume in PDF format**.
The app extracts text from the resume and adds additional interview questions based on the skills or technologies found in the resume.

For example:

* if the resume mentions **Python**, the app can ask about Python projects
* if it mentions **Streamlit**, the app can ask about Streamlit-based work
* if it mentions **Data Analytics**, the app can ask project-related analytics questions

---

### 🎙️ 3. Voice Recording in Streamlit

Users can record answers directly inside the Streamlit application using an audio recorder interface.

---

### 🧠 4. Speech-to-Text Transcription with Whisper

The recorded audio is converted into text using **OpenAI Whisper**.

This allows the app to:

* capture spoken interview answers
* display the transcribed response
* evaluate the answer automatically

---

### 📊 5. Answer Scoring and Feedback

Each answer is evaluated using a rule-based scoring system.

The app provides:

* **score out of 10**
* **strengths**
* **areas for improvement**
* **better sample answer**

---

### 📝 6. Final Interview Summary

At the end of the interview, the app displays a complete summary of:

* all interview questions
* transcribed answers
* score for each answer
* strengths and improvements
* overall performance

---

### 📄 7. PDF Interview Report Download

The user can download a **PDF report** containing the full interview summary.

The report includes:

* selected role
* all questions
* user answers
* scores
* strengths
* improvements
* better sample answers
* overall average score

---

## 🛠️ Tech Stack

This project uses the following tools and libraries:

* **Python**
* **Streamlit**
* **OpenAI Whisper**
* **pdfplumber**
* **ReportLab**
* **NumPy**
* **SciPy**
* **sounddevice**
* **streamlit-audiorecorder**

---

## 📂 Project Structure

```bash
AI_Interview_Assistant/
│── app.py
│── interview.py
│── README.md
│── requirements.txt
│── .gitignore
```

---

## ⚙️ Installation and Setup

### 1) Clone the repository

```bash
git clone https://github.com/ManneSatwika/AI_Interview_Assistant.git
cd AI_Interview_Assistant
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Run the Streamlit app

```bash
streamlit run app.py
```

---

## ▶️ How to Use

1. Open the Streamlit app
2. Select an interview role from the sidebar
3. Upload your resume (optional)
4. Click **Start Interview**
5. Read the displayed interview question
6. Record your answer using the voice recorder
7. Click **Transcribe & Evaluate**
8. View your:

   * transcribed answer
   * score
   * strengths
   * improvements
   * better sample answer
9. Click **Next Question**
10. After the final question, download the **PDF interview report**

---

## 📊 Evaluation Logic

The current version uses a **rule-based answer evaluation system**.

The score is calculated based on factors such as:

* answer length
* presence of role-related words
* presence of examples or explanation words
* overall detail in the answer

The app then generates:

* a score
* strengths
* improvements
* a better sample answer

---

## 📄 PDF Report Contents

The final downloadable PDF report includes:

* **Selected role**
* **All interview questions**
* **User’s transcribed answers**
* **Score for each answer**
* **Strengths**
* **Improvements**
* **Better sample answers**
* **Overall average score**

---

## 💡 Future Improvements

Possible future enhancements for this project include:

* AI-based scoring using LLM APIs
* confidence / communication analysis
* more advanced resume-based question generation
* support for more job roles
* database integration to save interview history
* deployment on Streamlit Cloud
* better UI/UX improvements

---

## 🎯 Learning Outcomes from This Project

This project helped in learning and practicing:

* Streamlit app development
* integrating voice recording into a web app
* speech-to-text transcription using Whisper
* resume parsing from PDF files
* rule-based answer evaluation
* PDF report generation
* building an end-to-end AI-style portfolio project

---

## 👩‍💻 Author

**Satwika Manne**

GitHub: https://github.com/ManneSatwika

---

## ⭐ Support

If you found this project useful, consider giving it a **star** on GitHub.
