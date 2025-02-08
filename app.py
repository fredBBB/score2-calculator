<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Калькулятор сердечно-сосудистого риска SCORE 2</title>
    <style>
        /* Темная тема */
        body {
            font-family: Arial, sans-serif;
            background-color: #181818;
            color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            flex-direction: column;
        }
        h1 {
            text-align: center;
            color: #f1f1f1;
        }
        .container {
            background-color: #222;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            width: 100%;
            max-width: 600px;
        }
        label {
            font-size: 16px;
            margin-bottom: 5px;
            display: block;
            color: #ccc;
        }
        input, select, button {
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border: 1px solid #444;
            border-radius: 4px;
            box-sizing: border-box;
            background-color: #333;
            color: #f4f4f4;
        }
        input:focus, select:focus, button:focus {
            outline: none;
            border-color: #666;
        }
        button {
            background-color: #FF5A5A; /* Ярко-красно-розовый цвет */
            color: white;
            font-size: 16px;
            cursor: pointer;
            border: 1px solid #FF5A5A; /* Тот же ярко-красно-розовый цвет для рамки */
        }
        button:hover {
            background-color: #FF4C4C; /* Темнее, но все еще ярко-красный оттенок при наведении */
        }
        .result {
            margin-top: 20px;
            padding: 20px;
            border: 1px solid #444;
            border-radius: 8px;
            background-color: #333;
            text-align: center;
        }
        .result h3 {
            font-size: 36px; /* Увеличиваем размер шрифта для текста с результатом */
            margin: 0;
        }
        .result p {
            font-size: 24px; /* Увеличиваем размер шрифта для категории риска */
            font-weight: bold;
            margin-top: 10px;
        }
        .error {
            color: red;
            font-weight: bold;
            text-align: center;
        }
        .input-error {
            border-color: #FF5A5A; /* Ярко-красно-розовый цвет */
            background-color: #3f2f2f; /* Немного темный фон для подсвеченного поля */
        }
        .input-error:focus {
            border-color: #FF4C4C; /* Более темный оттенок при фокусе */
            background-color: #4a3c3c; /* Еще темнее фон при фокусе */
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>Калькулятор сердечно-сосудистого риска SCORE 2</h1>

        <form id="risk-form" method="POST" onsubmit="return calculateRisk(event)">
            <label for="age">Возраст:</label>
            <input type="text" id="age" name="age" required placeholder="Введите возраст в диапазоне от 40 до 69 лет" autocomplete="off">
            <div id="age-error" class="error-message"></div><br>

            <label for="gender">Пол:</label>
            <select name="gender" id="gender" autocomplete="off">
                <option value="Ж">Женский</option>
                <option value="М">Мужской</option>
            </select><br>

            <label for="smokestatus">Пациент курит?:</label>
            <select name="smokestatus" id="smokestatus" autocomplete="off">
                <option value="Да">Да</option>
                <option value="Нет">Нет</option>
            </select><br>

            <label for="cholesterol">Уровень холестерина не-ЛПВ (ммоль/л):</label>
            <input type="text" id="cholesterol" name="cholesterol" required placeholder="Укажите уровень холестерина в диапазоне от 3.0 до 6.9" autocomplete="off">
            <div id="cholesterol-error" class="error-message"></div><br>

            <label for="bloodpressure">Систолическое давление:</label>
            <input type="text" id="bloodpressure" name="bloodpressure" required placeholder="Укажите давление в диапазоне от 100 до 179" autocomplete="off">
            <div id="bloodpressure-error" class="error-message"></div><br>

            <button type="submit" id="calculate-button">Рассчитать риск</button>
        </form>

        <!-- Результаты или ошибка -->
        <div id="result" class="result" style="display:none;">
            <h3 id="result-risk"></h3>
            <p id="result-category"></p>
            <button onclick="resetForm()">Рассчитать снова</button>
        </div>

        <p id="error-message" class="error" style="display:none;"></p>
    </div>

    <script>
        function calculateRisk(event) {
            event.preventDefault(); // Предотвращаем отправку формы

            let age = parseInt(document.getElementById("age").value);
            let cholesterol = parseFloat(document.getElementById("cholesterol").value);
            let bloodpressure = parseInt(document.getElementById("bloodpressure").value);
            let smokestatus = document.getElementById("smokestatus").value;
            let gender = document.getElementById("gender").value;

            // Простая логика расчета риска (пример, можно заменить на свою логику)
            let risk = 0;
            if (age >= 40 && age <= 69 && cholesterol >= 3.0 && cholesterol <= 6.9 && bloodpressure >= 100 && bloodpressure <= 179) {
                risk = (age - 40) * 0.5 + (cholesterol - 3) * 1.5 + (bloodpressure - 100) * 0.3;
                risk = Math.min(risk, 100); // Ограничиваем риск 100%
            } else {
                document.getElementById("error-message").style.display = 'block';
                document.getElementById("error-message").textContent = "Пожалуйста, введите корректные данные.";
                return;
            }

            let riskCategory = risk <= 10 ? "Низкий риск" : (risk <= 20 ? "Средний риск" : "Высокий риск");

            // Показываем результаты
            document.getElementById("result").style.display = 'block';
            document.getElementById("result-risk").textContent = `Риск: ${risk.toFixed(2)}%`;
            document.getElementById("result-category").textContent = riskCategory;

            // Скрываем сообщение об ошибке, если все прошло хорошо
            document.getElementById("error-message").style.display = 'none';
        }

        function resetForm() {
            document.getElementById("risk-form").reset();
            document.getElementById("result").style.display = 'none';
            document.getElementById("error-message").style.display = 'none';
        }
    </script>

</body>
</html>
