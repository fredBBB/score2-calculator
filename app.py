from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

# Функция для загрузки данных из CSV
def load_risk_table():
    filepath = os.path.join(os.path.dirname(__file__), "heart_risk_table.csv")
    with open(filepath, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        data = list(reader)
        return data

# Функция для получения интервала возраста
def get_age_interval(age):
    age_ranges = [("40-44", "40-44"), ("45-49", "45-49"), ("50-54", "50-54"), ("55-59", "55-59"), ("60-64", "60-64"), ("65-69", "65-69")]
    for start, end in age_ranges:
        if start <= age <= end:
            return f"{start}-{end}"
    return None  

# Функция для получения интервала систолического АД
def get_bp_interval(bloodpressure):
    bp_ranges = [("100-119", "100-119"), ("120-139", "120-139"), ("140-159", "140-159"), ("160-179", "160-179")]
    for start, end in bp_ranges:
        if start <= bloodpressure <= end:
            return f"{start}-{end}"
    return None

# Функция для получения интервала уровня холестерина
def get_cholesterol_interval(cholesterol):
    cholesterol_ranges = [("3.0-3.9", "3.0-3.9"), ("4.0-4.9", "4.0-4.9"), ("5.0-5.9", "5.0-5.9"), ("6.0-6.9", "6.0-6.9")]
    for start, end in cholesterol_ranges:
        if start <= cholesterol <= end:
            return f"{start}-{end}"
    return None

# Функция для поиска риска по данным
def find_risk(age, bloodpressure, cholesterol, smokestatus, gender, risk_table): 
    age = get_age_interval(age)
    bloodpressure = get_bp_interval(bloodpressure)
    cholesterol = get_cholesterol_interval(cholesterol)

    for row in risk_table:
        if (row["age"].strip() == age and 
            row["bloodpressure"].strip() == bloodpressure and 
            row["cholesterol"].strip() == cholesterol and 
            row["smokestatus"].strip().lower() == smokestatus.lower() and 
            row["gender"].strip().upper() == gender.upper()):
            return row["risk"]
    return "Нет данных"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            age = int(request.form["age"])
            gender = request.form["gender"].upper()
            smokestatus = request.form["smokestatus"].capitalize()
            cholesterol = float(request.form["cholesterol"].replace(",", "."))
            bloodpressure = int(request.form["bloodpressure"])

            # Загружаем таблицу с рисками
            risk_table = load_risk_table()

            # Ищем риск
            risk = find_risk(age, bloodpressure, cholesterol, smokestatus, gender, risk_table)

            return render_template("index.html", risk=risk)

        except ValueError as e:
            return render_template("index.html", error="Ошибка! Введите корректные данные.")
    
    return render_template("index.html", risk=None)

if __name__ == "__main__":
    app.run(debug=True)

