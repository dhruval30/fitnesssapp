import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
from groq import Groq  # Import the Groq client
from flask import Flask, jsonify
import random
import time
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "gsjhgfshgf"  

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb+srv://dhruval:2V0Aegnl7SYBTEBr@carpool-app.wtiwm.mongodb.net/fitness_app"  # Update this URI for your MongoDB setup
mongo = PyMongo(app)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'username': request.form['username']})

        if existing_user is None:
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'username': request.form['username'], 'password': hashed_password})
            session['username'] = request.form['username']
            return redirect(url_for('dashboard'))
        return 'Username already exists!'

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'username': request.form['username']})

        if login_user:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['username'] = request.form['username']
                return redirect(url_for('dashboard'))
        return 'Invalid username/password combination!'

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def initialize_groq_diet_plan(weight, height, bmi, body_type, diet_pref, goal):
    groq_api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=groq_api_key)

    system_prompt = {
        "role": "system",
        "content": "You are a helpful diet planning assistant. Provide a short, customized diet plan based on the user's profile."
    }

    chat_history = [system_prompt]

    user_prompt = (
        f"Generate a diet plan for a user with these details:\n"
        f"- Weight: {weight} kg\n- Height: {height} cm\n- BMI: {bmi:.2f}\n"
        f"- Body Type: {body_type}\n- Dietary Preference: {diet_pref}\n"
        f"- Goal: {goal}"
    )

    chat_history.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=500,
        temperature=1.2
    )

    return response.choices[0].message.content


@app.route('/ai-diet-plan', methods=['GET', 'POST'])
def ai_diet_plan():
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        bmi = weight / ((height / 100) ** 2)
        body_type = request.form['body_type']
        diet_pref = request.form['diet_pref']
        goal = request.form['goal']
        
        diet_plan = initialize_groq_diet_plan(weight, height, bmi, body_type, diet_pref, goal)
        
        return diet_plan 

    return render_template('ai_diet_plan.html')

@app.route('/exercise-recommendation', methods=['GET', 'POST'])
def exercise_recommendation():
    if request.method == 'POST':
        gender = request.form['gender']
        age = int(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        bmi = weight / ((height / 100) ** 2)
        body_type = request.form['body_type']
        exercise_behavior = request.form['exercise_behavior']
        workout_frequency = request.form['workout_frequency']
        goal = request.form['goal']

        exercise_plan = initialize_groq_exercise_plan(
            gender, age, height, weight, bmi, body_type, exercise_behavior, workout_frequency, goal
        )
        
        return exercise_plan  

    return render_template('exercise_recommendation.html')

def initialize_groq_exercise_plan(gender, age, height, weight, bmi, body_type, exercise_behavior, workout_frequency, goal):
    groq_api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=groq_api_key)

    system_prompt = {
        "role": "system",
        "content": "You are a fitness coach. Provide a customized exercise recommendation based on user profile data."
    }

    user_prompt = (
        f"Provide an exercise plan for a {age}-year-old {gender} with the following details:\n"
        f"- Height: {height} cm\n- Weight: {weight} kg\n- BMI: {bmi:.2f}\n"
        f"- Body Type: {body_type}\n- Exercise Behavior: {exercise_behavior}\n"
        f"- Weekly Workout Frequency: {workout_frequency} times per week\n- Goal: {goal}"
    )

    chat_history = [system_prompt, {"role": "user", "content": user_prompt}]
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=chat_history,
        max_tokens=500,
        temperature=1.2
    )

    return response.choices[0].message.content

@app.route('/activity_tracking')
def activity_tracking():
    if 'activity_data' not in session:
        session['activity_data'] = {
            "steps": random.randint(1000, 1500),
            "heart_rate": random.randint(60, 80),
            "calories_burned": round(random.uniform(50, 80), 2),
            "last_updated": datetime.now().isoformat(),
            "data_points": []  
        }
    return render_template('activity_tracking.html')

@app.route('/get_activity_data')
def get_activity_data():
    activity_data = session['activity_data']
    last_updated = datetime.fromisoformat(activity_data["last_updated"])
    current_time = datetime.now()

    if "data_points" not in activity_data:
        activity_data["data_points"] = []

    if current_time - last_updated > timedelta(seconds=5):
        new_steps = activity_data["steps"] + random.randint(5, 15)
        new_heart_rate = min(120, activity_data["heart_rate"] + random.randint(-1, 3))
        new_calories = activity_data["calories_burned"] + round(random.uniform(0.5, 1.5), 2)

        activity_data.update({
            "steps": new_steps,
            "heart_rate": new_heart_rate,
            "calories_burned": new_calories,
            "last_updated": current_time.isoformat()
        })

        activity_data["data_points"].append({
            "timestamp": current_time.isoformat(),
            "steps": new_steps,
            "heart_rate": new_heart_rate,
            "calories_burned": new_calories
        })
        
        session['activity_data'] = activity_data

    return jsonify(activity_data)

@app.route('/session_summary')
def session_summary():
    data_points = session['activity_data'].get("data_points", [])

    if not data_points:
        return "No data available for analysis."

    total_steps = data_points[-1]["steps"] - data_points[0]["steps"]
    avg_heart_rate = sum(point["heart_rate"] for point in data_points) / len(data_points)
    total_calories = data_points[-1]["calories_burned"] - data_points[0]["calories_burned"]

    summary = {
        "total_steps": total_steps,
        "average_heart_rate": round(avg_heart_rate, 2),
        "total_calories_burned": round(total_calories, 2)
    }
    
    return jsonify(summary)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

