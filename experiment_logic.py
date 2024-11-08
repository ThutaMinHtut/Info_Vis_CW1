
import numpy as np
import matplotlib.pyplot as plt
import random
import os
from datetime import datetime
from flask import Flask, send_file

# Generate random data for absences
def generate_data():
    return np.random.randint(0, 50, (10, 12))  # 10 schools, 12 months

# Save plot images
def save_heatmap(data, filepath):
    plt.imshow(data, cmap='hot', interpolation='nearest')
    plt.colorbar(label="Absences")
    plt.title("Heatmap of School Absences")
    plt.xlabel("Months")
    plt.ylabel("Schools")
    plt.savefig(filepath)
    plt.close()

def save_scatterplot(data, filepath):
    for school_id in range(10):
        plt.scatter(range(1, 13), data[school_id], label=f'School {school_id + 1}')
    plt.title("Scatterplot of School Absences")
    plt.xlabel("Months")
    plt.ylabel("Absences")
    plt.legend()
    plt.savefig(filepath)
    plt.close()

# Generate a random question
def random_question(data):
    question_type = random.choice(["school", "month"])
    high_low = random.choice(["highest", "lowest"])
    answer = None

    if question_type == "school":
        school = random.randint(1, 10)
        answer = np.argmax(data[school-1]) + 1 if high_low == "highest" else np.argmin(data[school-1]) + 1
        question = f"For School {school}, which month has the {high_low} absences?"
    else:
        month = random.randint(1, 12)
        school_absences = data[:, month-1]
        answer = np.argmax(school_absences) + 1 if high_low == "highest" else np.argmin(school_absences) + 1
        question = f"For Month {month}, which school has the {high_low} absences?"

    return question, answer
