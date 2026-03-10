<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Бюджет</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #eef2f5; margin: 0; padding: 20px; color: #333; }
        .container { max-width: 500px; margin: 0 auto; }
        
        /* Блок с балансом */
        .balance-board { display: flex; justify-content: space-between; text-align: center; margin-bottom: 20px; font-weight: bold; }
        .balance-board div { background: #fff; padding: 15px 10px; border-radius: 10px; width: 30%; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .limit { color: #333; }
        .spent { color: #d9534f; }
        .left { color: #5cb85c; }
        .val { font-size: 18px; margin-top: 5px; display: block; }

        /* Место под колесо бюджета */
        .wheel-placeholder { background: #fff; padding: 20px; text-align: center; border-radius: 10px; margin-bottom: 20px; color: #777; border: 2px dashed #ccc; }

        /* Карточки (Новая трата и Фикс. счета) */
        .card { background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px; }
        .card h3 { margin-top: 0; font-size: 16px; border-bottom: 1px solid #eee; padding-bottom: 10px; margin-bottom: 15px; color: #444; }
        
        label { font-size: 12px; color: #666; display: block; margin-bottom: 5px; }
        select, input { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; font-size: 16px; }
        button { width: 100%; padding: 15px; background-color: #e4e2db; border: none; border-radius: 6px; font-weight: bold; color: #555; cursor: pointer; }
        button:hover { background-color: #d4d2cb; }

        /* Фиксированные счета */
        .fixed-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 1px solid #f9f9f9; padding-bottom: 5px; }
        .fixed-row span { font-size: 14px; color: #333; }
        .fixed-row input { width: 80px; margin-bottom: 0; padding: 8px; text-align: center; }
    </style>
</head>
<body>

<div class="container">

    <div class="balance-board">
        <div class="limit">ЛИМИТ<span class="val" id="val-limit">8504 ₪</span></div>
        <div class="spent">ТРАТЫ<span class="val" id="val-spent">0 ₪</span></div>
        <div class="left">ОСТАТОК<span class="val" id="val-left">8504 ₪</span></div>
    </div>

    <div class="wheel-placeholder">
        Здесь твое Колесо Бюджета
    </div>

    <div class="card">
        <h3>+ Новая трата</h3>
        <label>Куда?</label>
        <select id="category">
            <option>Продукты и Хозтовары</option>
            <option>Аптека</option>
            <option>Прочее</option>
        </select>

        <label>Сколько ₪ (только целые числа)</label>
        <input type="number" id="amount" placeholder="0" step="1">

        <button onclick="addExpense()">ЗАПИСАТЬ</button>
    </div>

    <div class="card">
        <h3>Фиксированные счета</h3>
        
        <div class="fixed-row">
            <span>Машканта</span>
            <input type="number" placeholder="0" step="1">
        </div>
        <div class="fixed-row">
            <span>Арнона</span>
            <input type="number" placeholder="0" step="1">
        </div>
        <div class="fixed-row">
            <span>Электричество</span>
            <input type="number" placeholder="0" step="1">
        </div>
        <div class="fixed-row">
            <span>Вода и Газ</span>
            <input type="number" placeholder="0" step="1">
        </div>
        <div class="fixed-row">
            <span>Кружки (Арина, Натан, Лео)</span>
            <input type="number" placeholder="0" step="1">
        </div>
        <div class="fixed-row">
            <span>Доп. уроки (Артур)</span>
            <input type="number" placeholder="0" step="1">
        </div>
    </div>

</div>

<script>
    // Жестко заданный стартовый лимит
    const START_LIMIT = 8504; 
    let currentSpent = 0;

    function updateBoard() {
        // Math.round принудительно отсекает любые десятичные дроби
        let cleanSpent = Math.round(currentSpent);
        let cleanLeft = Math.round(START_LIMIT - cleanSpent);

        document.getElementById('val-spent').innerText = cleanSpent + " ₪";
        document.getElementById('val-left').innerText = cleanLeft + " ₪";
    }

    function addExpense() {
        let inputVal = document.getElementById('amount').value;
        
        // Превращаем введенное значение строго в целое число
        let expense = Math.round(Number(inputVal));

        if (expense > 0) {
            currentSpent += expense;
            document.getElementById('amount').value = ''; // Очищаем поле
            updateBoard();
        }
    }
</script>

</body>
</html>
