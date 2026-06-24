import streamlit as st
import whisper
import re
import os
import pdfplumber
from audiorecorder import audiorecorder

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Interview Assistant", page_icon="🎤", layout="wide")

st.title("🎤 AI Interview Assistant")
st.write("Select a role, upload your resume, record your answers, and get interview feedback.")

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return whisper.load_model("small")

model = load_model()

# ---------------- ROLE-BASED QUESTION BANK ----------------
role_questions = {
    "Data Analyst": [
        "Tell me about yourself.",
        "Explain a data analytics project you worked on.",
        "What is the difference between INNER JOIN and LEFT JOIN?",
        "How do you clean messy data before analysis?",
        "Why do you want to work as a Data Analyst?"
    ],
    "Python Developer": [
        "Tell me about yourself.",
        "What Python projects have you built?",
        "What is the difference between a list and a tuple in Python?",
        "How do you handle exceptions in Python?",
        "Why do you want to work as a Python Developer?"
    ],
    "Java Developer": [
        "Tell me about yourself.",
        "Explain a Java project you have worked on.",
        "What are the OOP principles in Java?",
        "What is the difference between ArrayList and LinkedList?",
        "Why do you want to work as a Java Developer?"
    ],
    "HR / General": [
        "Tell me about yourself.",
        "What are your strengths?",
        "What are your weaknesses?",
        "Why should we hire you?",
        "Where do you see yourself in five years?"
    ]
}

# ---------------- SAMPLE ANSWERS ----------------
def generate_better_answer(question):
    samples = {
        "Tell me about yourself.":
            "I am a recent graduate with a strong interest in technology, problem solving, and building practical projects. I have been working on projects using Python, Streamlit, and AI-related tools, which helped me improve my technical, analytical, and communication skills. I am looking for an opportunity where I can continue learning, contribute to meaningful work, and grow professionally.",

        "What are your strengths?":
            "My strengths include being a quick learner, staying consistent with my work, and being willing to put in effort to improve. I also enjoy solving problems step by step, learning new tools, and completing tasks responsibly.",

        "Why should we hire you?":
            "You should hire me because I am motivated to learn, adaptable, and committed to improving my skills continuously. I have been building practical projects to strengthen my technical knowledge, and I am confident that I can contribute dedication, responsibility, and a strong willingness to grow in this role."
    }
    return samples.get(question, "Try answering in a structured way: introduction, key point, example, and conclusion.")

# ---------------- RESUME TEXT EXTRACTION ----------------
def extract_resume_text(uploaded_file):
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        st.error(f"Error reading resume: {e}")
    return text

# ---------------- CREATE PERSONALIZED QUESTIONS ----------------
def generate_personalized_questions(selected_role, resume_text):
    questions = role_questions[selected_role].copy()
    resume_lower = resume_text.lower()

    if "streamlit" in resume_lower:
        questions.append("I noticed you have worked with Streamlit. Can you explain one project where you used it and the challenges you faced?")

    if "python" in resume_lower:
        questions.append("You mentioned Python in your resume. Which Python project are you most proud of and why?")

    if "java" in resume_lower:
        questions.append("I see Java on your resume. Can you explain a Java project you built and your role in it?")

    if "data" in resume_lower or "analytics" in resume_lower:
        questions.append("You mentioned data analytics related work. Can you explain how you approached one analytics project from data cleaning to insights?")

    return questions

# ---------------- SCORING FUNCTION ----------------
def evaluate_answer(question, answer):
    answer_lower = answer.lower()
    words = re.findall(r"\b\w+\b", answer_lower)
    word_count = len(words)

    score = 0
    strengths = []
    improvements = []

    if word_count >= 40:
        score += 4
        strengths.append("Your answer had good detail and explanation.")
    elif word_count >= 20:
        score += 3
        strengths.append("Your answer had a reasonable amount of detail.")
        improvements.append("Try adding one or two more points to make it stronger.")
    elif word_count >= 10:
        score += 2
        improvements.append("Your answer is a bit short. Add more detail and examples.")
    else:
        score += 1
        improvements.append("Your answer is too short. Try explaining more clearly with examples.")

    if any(word in answer_lower for word in ["project", "experience", "skills", "learn", "team", "data", "python", "java", "analysis"]):
        score += 4
        strengths.append("Your answer includes relevant role-related points.")
    else:
        score += 2
        improvements.append("Try connecting your answer more directly to your skills, projects, or role.")

    if any(word in answer_lower for word in ["because", "for example", "for instance", "such as"]):
        score += 2
        strengths.append("You included reasoning/examples, which improves the answer.")
    else:
        score += 1
        improvements.append("Add an example or explanation to make the answer stronger.")

    if score > 10:
        score = 10

    if not strengths:
        strengths.append("You attempted the answer and addressed the question.")
    if not improvements:
        improvements.append("Try making your answer more polished and confident.")

    return {
        "score": score,
        "strengths": " ".join(strengths),
        "improvements": " ".join(improvements),
        "sample_better_answer": generate_better_answer(question)
    }

# ---------------- PDF REPORT FUNCTION ----------------
def generate_pdf_report(role, results):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI Interview Assistant - Interview Report", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"<b>Selected Role:</b> {role}", styles["Normal"]))
    story.append(Spacer(1, 12))

    total_score = 0

    for i, item in enumerate(results, start=1):
        question = item["question"]
        answer = item["answer"]
        score = item["feedback"]["score"]
        strengths = item["feedback"]["strengths"]
        improvements = item["feedback"]["improvements"]
        better_answer = item["feedback"]["sample_better_answer"]

        total_score += score

        story.append(Paragraph(f"<b>Question {i}:</b> {question}", styles["Heading3"]))
        story.append(Paragraph(f"<b>Your Answer:</b> {answer}", styles["Normal"]))
        story.append(Paragraph(f"<b>Score:</b> {score} / 10", styles["Normal"]))
        story.append(Paragraph(f"<b>Strengths:</b> {strengths}", styles["Normal"]))
        story.append(Paragraph(f"<b>Improvements:</b> {improvements}", styles["Normal"]))
        story.append(Paragraph(f"<b>Better Sample Answer:</b> {better_answer}", styles["Normal"]))
        story.append(Spacer(1, 16))

    avg_score = total_score / len(results) if results else 0
    story.append(Paragraph("<b>Overall Performance</b>", styles["Heading2"]))
    story.append(Paragraph(f"Average Score: {avg_score:.1f} / 10", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ---------------- SESSION STATE ----------------
if "selected_role" not in st.session_state:
    st.session_state.selected_role = None
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "results" not in st.session_state:
    st.session_state.results = []

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Setup Interview")

selected_role = st.sidebar.selectbox(
    "Choose Interview Role",
    ["Data Analyst", "Python Developer", "Java Developer", "HR / General"]
)

uploaded_resume = st.sidebar.file_uploader("Upload Resume (PDF)", type=["pdf"])

if st.sidebar.button("Start Interview"):
    st.session_state.selected_role = selected_role

    resume_text = ""
    if uploaded_resume is not None:
        resume_text = extract_resume_text(uploaded_resume)
        st.session_state.resume_text = resume_text

    st.session_state.questions = generate_personalized_questions(selected_role, resume_text)
    st.session_state.current_question_index = 0
    st.session_state.results = []

    st.success("Interview initialized successfully!")
    st.rerun()

# ---------------- MAIN INTERVIEW FLOW ----------------
if st.session_state.questions:
    st.subheader(f"🎯 Role: {st.session_state.selected_role}")

    if st.session_state.current_question_index < len(st.session_state.questions):
        current_question = st.session_state.questions[st.session_state.current_question_index]

        st.markdown("## 📌 Interview Question")
        st.info(current_question)

        st.markdown("## 🎙️ Record Your Answer")
        st.write("Click start recording, speak your answer, then stop recording.")

        audio = audiorecorder("▶️ Start Recording", "⏹️ Stop Recording")

        if len(audio) > 0:
            audio_bytes = audio.export().read()
            st.audio(audio_bytes, format="audio/wav")

            with open("answer.wav", "wb") as f:
                f.write(audio_bytes)

            if st.button("🧠 Transcribe & Evaluate"):
                with st.spinner("Transcribing and evaluating..."):
                    result = model.transcribe("answer.wav")
                    answer_text = result["text"].strip()

                    feedback = evaluate_answer(current_question, answer_text)

                    st.success("Answer processed successfully!")
                    st.markdown("## 📝 Your Answer")
                    st.write(answer_text)

                    st.markdown("## 📊 Feedback")
                    st.write(f"**Score:** {feedback['score']} / 10")
                    st.write(f"**Strengths:** {feedback['strengths']}")
                    st.write(f"**Improvements:** {feedback['improvements']}")

                    st.markdown("## 💡 Better Sample Answer")
                    st.write(feedback["sample_better_answer"])

                    already_saved = any(
                        item["question"] == current_question for item in st.session_state.results
                    )

                    if not already_saved:
                        st.session_state.results.append({
                            "question": current_question,
                            "answer": answer_text,
                            "feedback": feedback
                        })

        if st.button("➡ Next Question"):
            if len(st.session_state.results) > st.session_state.current_question_index:
                st.session_state.current_question_index += 1
                st.rerun()
            else:
                st.warning("Please record and evaluate this question before moving to the next one.")

    else:
        # ---------------- FINAL SUMMARY + PDF DOWNLOAD ----------------
        st.success("🎉 Interview Completed!")

        st.markdown("# 📋 Final Summary")
        total_score = 0

        for i, item in enumerate(st.session_state.results, start=1):
            st.markdown(f"## Question {i}")
            st.write(f"**Question:** {item['question']}")
            st.write(f"**Your Answer:** {item['answer']}")
            st.write(f"**Score:** {item['feedback']['score']} / 10")
            st.write(f"**Strengths:** {item['feedback']['strengths']}")
            st.write(f"**Improvements:** {item['feedback']['improvements']}")
            st.write(f"**Better Answer:** {item['feedback']['sample_better_answer']}")
            st.markdown("---")
            total_score += item["feedback"]["score"]

        avg_score = total_score / len(st.session_state.results) if st.session_state.results else 0
        st.markdown("## 🏁 Overall Performance")
        st.write(f"**Average Score:** {avg_score:.1f} / 10")

        pdf_buffer = generate_pdf_report(
            st.session_state.selected_role,
            st.session_state.results
        )

        st.download_button(
            label="📄 Download Interview Report PDF",
            data=pdf_buffer,
            file_name="AI_Interview_Report.pdf",
            mime="application/pdf"
        )

        if st.button("🔄 Restart Interview"):
            st.session_state.current_question_index = 0
            st.session_state.results = []
            st.session_state.questions = []
            st.session_state.resume_text = ""
            if os.path.exists("answer.wav"):
                os.remove("answer.wav")
            st.rerun()

else:
    st.info("Choose a role, optionally upload your resume, and click **Start Interview** from the sidebar.")