<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Семейный Бюджет: Выход в Ноль</title>
    <style>
        body { background-color: #121212; color: white; font-family: sans-serif; padding: 20px; }
        .header { border-bottom: 1px solid #333; padding-bottom: 20px; margin-bottom: 20px; }
        .stats { color: #aaa; font-size: 0.9em; }
        .total-box { background: #1e3a2f; color: #4caf50; padding: 15px; border-radius: 10px; display: inline-block; margin-top: 10px; }
        
        .envelopes-grid { display: flex; gap: 20px; flex-wrap: wrap; margin-top: 20px; }
        .envelope { background: #1e1e1e; padding: 15px; border-radius: 12px; width: 160px; text-align: center; }
        
        /* Цвета индикаторов под конвертами */
        .bar { height: 4px; width: 100%; margin-top: 10px; border-radius: 2px; }
        .bg-green { background-color: #2196f3; } /* Синий как на фото изначально */
        .bg-orange { background-color: #ff9800; }
        .bg-red { background-color: #f44336; }

        .ai-input { margin-top: 40px; background: #1e1e1e; padding: 20px; border-radius: 15px; }
        input { width: 100%; background: #2a2a2a; border: 1px solid #444; color: white; padding: 12px; border-radius: 8px; }
    </style>
</head>
<body>

<div class="header">
    <h1>⚖️ Семейный Бюджет: Выход в Ноль</h1>
    <div class="stats">
        Доход: 18000 ₪ | Фикс. платежи: 10990 ₪ | Биржа: 500 ₪
    </div>
    <div class="total-box">Доступно на месяц: <span id="main-total">6510</span> ₪</div>
</div>

<div class="envelopes-grid" id="grid">
    </div>

<div class="ai-input">
    <p>Напиши расход (например: <b>продукты 150</b>)</p>
    <input type="text" id="ai-field" placeholder="Введите название и сумму..." onkeypress="runAI(event)">
</div>

<script>
    // Твои конверты из приложения
    let data = [
        { id: 'prod', name: "Продукты", balance: 250, limit: 2000 },
        { id: 'urok', name: "Доп. уроки", balance: 1850, limit: 2500 },
        { id: 'car', name: "Машина", balance: 700, limit: 1500 },
        { id: 'pamp', name: "Памперсы", balance: 450, limit: 600 },
        { id: 'razn', name: "Разное", balance: 380, limit: 1000 }
    ];

    function draw() {
        const grid = document.getElementById('grid');
        grid.innerHTML = '';
        data.forEach(env => {
            let pct = (env.balance / env.limit) * 100;
            let colorClass = 'bg-green'; // Изначально синий
            if (pct < 40) colorClass = 'bg-orange';
            if (pct < 15) colorClass = 'bg-red';

            grid.innerHTML += `
                <div class="envelope">
                    <div style="font-size: 0.8em; color: #888">${env.name}</div>
                    <div style="font-size: 1.5em; margin: 10px 0">${env.balance} ₪</div>
                    <div class="bar ${colorClass}"></div>
                </div>
            `;
        });
        document.getElementById('main-total').innerText = data.reduce((s, e) => s + e.balance, 0);
    }

    function runAI(e) {
        if (e.key === 'Enter') {
            let val = document.getElementById('ai-field').value.toLowerCase();
            let [name, price] = val.split(' ');
            let amount = parseFloat(price);

            let target = data.find(item => item.name.toLowerCase().includes(name));
            if (target && amount) {
                target.balance -= amount;
                document.getElementById('ai-field').value = '';
                draw();
            }
        }
    }
    draw();
</script>
</body>
</html>

