from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

# Функция для загрузки данных из CSV
def load_risk_table():
    filepath = os.path.join(os.path.dirname(__file__), "heart_risk_table.csv")
    with open(filepath, mode="r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        # Отладка: выводим заголовки и данные
        print("Заголовки CSV:", reader.fieldnames)  # Выводим заголовки
        data = list(reader)
        print("Данные CSV:", data)  # Выводим содержимое
        return data

# Функция для получения интервала возраста
def get_age_interval(age):
    age_ranges = [(40, 44), (45, 49), (50, 54), (55, 59), (60, 64), (65, 69)]
    for start, end in age_ranges:
        if start <= age <= end:
            return f"{start}-{end}"
    return None  

# Функция для получения интервала систолического АД
def get_bp_interval(bloodpressure):
    bp_ranges = [(100, 119), (120, 139), (140, 159), (160, 179)]
    for start, end in bp_ranges:
        if start <= bloodpressure <= end:
            return f"{start}-{end}"
    return None

# Функция для получения интервала уровня холестерина
def get_cholesterol_interval(cholesterol):
    cholesterol_ranges = [(3.0, 3.9), (4.0, 4.9), (5.0, 5.9), (6.0, 6.9)]
    for start, end in cholesterol_ranges:
        if start <= cholesterol <= end:
            return f"{start}-{end}"
    return None

# Функция для поиска риска по данным
def find_risk(age, bloodpressure, cholesterol, smokestatus, gender, risk_table): 
    age = get_age_interval(age)
    bloodpressure = get_bp_interval(bloodpressure)
    cholesterol = get_cholesterol_interval(cholesterol)

    print(f"Ищем риск для возраста: {age}, давления: {bloodpressure}, холестерина: {cholesterol}, статус курения: {smokestatus}, пол: {gender}")
    
    for row in risk_table:
        print(f"Текущая строка: {row}")  # Выводим строку из таблицы для отладки
        if all(key in row for key in ["age", "bloodpressure", "cholesterol", "smokestatus", "gender"]):
            if (row["age"].strip() == age and 
                row["bloodpressure"].strip() == bloodpressure and 
                row["cholesterol"].strip() == cholesterol and 
                row["smokestatus"].strip().lower() == smokestatus.lower() and 
                row["gender"].strip().upper() == gender.upper()):
                return row["risk"]
        else:
            print("Ошибка: отсутствует ключ в строке")
    
    return "Нет данных"

# Функция для классификации риска
def risk_classification(age, risk):  
    try:
        risk = float(risk)
        if age < 50:
            if risk < 2.5:
                return "Низкий риск"
            elif risk < 7.5:
                return "Умеренный риск"
            else:
                return "Высокий риск"
        elif 50 <= age <= 69:
            if risk < 5:
                return "Низкий риск"
            elif risk < 10:
                return "Умеренный риск"
            else:
                return "Высокий риск"
        else:
            return "Нет данных"
    except ValueError:
        return "Ошибка: некорректные данные"

# Главная страница
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Выводим данные формы в консоль для отладки
            print(f"Received form data: {request.form}")

            # Получаем данные из формы
            age = int(request.form["age"])
            gender = request.form["gender"].upper()
            smokestatus = request.form["smokestatus"].capitalize()
            cholesterol = float(request.form["cholesterol"].replace(",", "."))
            bloodpressure = int(request.form["bloodpressure"])

            # Загружаем таблицу с рисками
            risk_table = load_risk_table()

            # Печатаем содержимое таблицы для отладки
            print(f"Risk Table: {risk_table}")

            # Ищем риск
            risk = find_risk(age, bloodpressure, cholesterol, smokestatus, gender, risk_table)

            # Выводим найденный риск для отладки
            print(f"Calculated risk: {risk}")

            # Классифицируем риск
            risk_category = risk_classification(age, risk)

            # Отображаем результаты на странице
            return render_template("index.html", risk=risk, risk_category=risk_category)

        except ValueError as e:
            print(f"Ошибка: {e}")  # Выводим ошибку в консоль
            return render_template("index.html", error="Ошибка! Введите корректные данные.")
    
    return render_template("index.html", risk=None, risk_category=None)

if __name__ == "__main__":
    app.run(debug=True)
