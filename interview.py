import time
import re
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import numpy as np

# ---------------- SETTINGS ----------------
fs = 44100
device_id = 1   # change if your microphone uses a different number

# Load Whisper model
model = whisper.load_model("small")

questions = [
    "Tell me about yourself",
    "What are your strengths?",
    "Why should we hire you?"
]

# Keywords for simple local scoring
question_keywords = {
    "Tell me about yourself": ["graduate", "student", "skills", "project", "data", "python", "background", "experience"],
    "What are your strengths?": ["hardworking", "quick learner", "communication", "problem solving", "teamwork", "adaptable", "organized"],
    "Why should we hire you?": ["skills", "contribution", "team", "learn", "value", "dedicated", "growth", "project", "responsible"]
}

# ---------------- RECORD FUNCTION ----------------
def record_answer():
    while True:
        print("\n🎤 Speak your answer... Press ENTER when done")

        frames = []

        def callback(indata, frames_count, time_info, status):
            if status:
                print(status)
            frames.append(indata.copy())

        stream = sd.InputStream(
            samplerate=fs,
            channels=1,
            device=device_id,
            callback=callback
        )

        stream.start()
        time.sleep(0.3)   # give stream a moment to start
        input()           # press Enter to stop
        stream.stop()
        stream.close()

        if len(frames) == 0:
            print("⚠️ No audio captured. Please speak again and press Enter after a few seconds.")
            continue

        audio = np.concatenate(frames, axis=0)
        write("answer.wav", fs, audio)

        result = model.transcribe("answer.wav")
        return result["text"].strip()

# ---------------- LOCAL EVALUATION FUNCTION ----------------
def evaluate_answer(question, answer):
    answer_lower = answer.lower()
    words = re.findall(r"\b\w+\b", answer_lower)
    word_count = len(words)

    score = 0
    strengths = []
    improvements = []

    # 1. Length scoring
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

    # 2. Keyword relevance scoring
    matched_keywords = []
    expected_keywords = question_keywords.get(question, [])

    for kw in expected_keywords:
        if kw in answer_lower:
            matched_keywords.append(kw)

    if len(matched_keywords) >= 4:
        score += 4
        strengths.append("Your answer is relevant to the question and includes strong key points.")
    elif len(matched_keywords) >= 2:
        score += 3
        strengths.append("Your answer is somewhat relevant and includes a few important points.")
        improvements.append("Try including more role-relevant details and strengths.")
    elif len(matched_keywords) >= 1:
        score += 2
        improvements.append("Your answer touches the topic, but it needs stronger relevant points.")
    else:
        score += 1
        improvements.append("Your answer needs more relevant details related to the question.")

    # 3. Basic structure scoring
    if any(word in answer_lower for word in ["because", "for example", "for instance", "such as", "for my project"]):
        score += 2
        strengths.append("You gave some reasoning/examples, which improves the answer.")
    else:
        score += 1
        improvements.append("Add an example or reason to make your answer stronger.")

    # Final cap
    if score > 10:
        score = 10

    # Build sample better answer
    sample_better_answer = generate_better_answer(question)

    # If strengths empty
    if not strengths:
        strengths.append("You attempted the answer and addressed the question.")

    # If improvements empty
    if not improvements:
        improvements.append("Try making your answer more confident and polished.")

    return {
        "score": score,
        "strengths": " ".join(strengths),
        "improvements": " ".join(improvements),
        "sample_better_answer": sample_better_answer
    }

# ---------------- SAMPLE ANSWERS ----------------
def generate_better_answer(question):
    samples = {
        "Tell me about yourself":
            "I am a recent graduate with a strong interest in data analytics and AI-based applications. I enjoy working on projects that solve practical problems, and I have been building projects using Python, Streamlit, and machine learning concepts. I am especially interested in learning, improving my technical skills, and contributing to meaningful work in a professional environment.",

        "What are your strengths?":
            "My key strengths are that I am a quick learner, dedicated, and willing to put in consistent effort to improve. I am also organized in my work, enjoy solving problems step by step, and I stay committed to completing tasks properly. In addition, I am comfortable learning new tools and technologies whenever required.",

        "Why should we hire you?":
            "You should hire me because I am motivated to learn, adaptable, and genuinely interested in contributing to the role. I have been actively building practical projects to strengthen my technical and problem-solving skills, and I am willing to put in the effort needed to grow quickly. I believe I can bring dedication, responsibility, and a strong learning attitude to the team."
    }

    return samples.get(question, "Try giving a more structured and role-relevant answer.")

# ---------------- MAIN INTERVIEW ----------------
print("💼 AI INTERVIEW STARTED\n")

all_results = []

for q in questions:
    print(f"\n🧑 Interviewer: {q}")

    answer = record_answer()
    print("\n📝 Your Answer:")
    print(answer)

    print("\n⏳ Evaluating answer...")
    feedback = evaluate_answer(q, answer)

    print("\n📊 FEEDBACK")
    print("Score:", feedback["score"], "/10")
    print("Strengths:", feedback["strengths"])
    print("Improvements:", feedback["improvements"])
    print("Better Answer:", feedback["sample_better_answer"])
    print("-" * 70)

    all_results.append({
        "question": q,
        "answer": answer,
        "feedback": feedback
    })

# ---------------- FINAL SUMMARY ----------------
print("\n✅ INTERVIEW COMPLETED")
print("\n📋 FINAL SUMMARY\n")

for idx, item in enumerate(all_results, start=1):
    print(f"Question {idx}: {item['question']}")
    print("Your Answer:", item["answer"])
    print("Score:", item["feedback"]["score"], "/10")
    print("Strengths:", item["feedback"]["strengths"])
    print("Improvements:", item["feedback"]["improvements"])
    print("Better Answer:", item["feedback"]["sample_better_answer"])
    print("=" * 80)