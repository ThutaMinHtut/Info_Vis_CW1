
from flask import Flask, render_template, request, jsonify
from experiment_logic import generate_data, save_heatmap, save_scatterplot, random_question
import os
import json
import time
import random

app = Flask(__name__)

# Initialize log data
log_data = {
    "questions": [],
    "start_time": None,
    "total_time": None
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_experiment", methods=["POST"])
def start_experiment():
    log_data["start_time"] = time.time()  # Start experiment timer
    log_data["questions"] = []  # Reset questions list for new experiment
    return jsonify({"status": "Experiment started!"})

@app.route("/get_question", methods=["GET"])
def get_question():
    # Generate new data and random question
    data = generate_data()
    vis_type = random.choice(["heatmap", "scatterplot"])
    image_path = f"static/images/plot_{int(time.time())}.png"

    # Save heatmap or scatterplot 
    if vis_type == "heatmap":
        save_heatmap(data, image_path)
    else:
        save_scatterplot(data, image_path)

    # Create question and determine the correct answer
    question_text, correct_answer = random_question(data)
    log_data["questions"].append({
        "question": question_text,
        "correct_answer": correct_answer,
        "image_path": image_path,
        "response_time": None,
        "participant_response": None,
        "is_correct": None
    })
    return jsonify({"question": question_text, "image_path": image_path, "options": list(range(1, 13)) if "month" in question_text else list(range(1, 11))})

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    response_data = request.get_json()
    answer = response_data["answer"]
    question_time = response_data["question_time"]

    # Update the latest question log with participant's response
    question_data = log_data["questions"][-1]
    question_data["participant_response"] = answer
    question_data["response_time"] = question_time
    question_data["is_correct"] = (answer == question_data["correct_answer"])

    return jsonify({"status": "Answer recorded!"})

@app.route("/end_experiment", methods=["POST"])
def end_experiment():
    log_data["total_time"] = time.time() - log_data["start_time"]  
    with open("experiment_results.json", "w") as file:
        json.dump(log_data, file, indent=4)
    return jsonify({"status": "Experiment completed!", "results_file": "experiment_results.json"})

if __name__ == "__main__":
    app.run(debug=True)
