function doGet() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  var rows = sheet.getDataRange().getValues();
  var now = new Date();
  var currentMonth = now.getMonth();
  var currentYear = now.getFullYear();
  
  var spent = {};
  var history = [];

  // Идем по строкам со второй
  for (var i = 1; i < rows.length; i++) {
    try {
      var date = new Date(rows[i][0]);
      // Проверяем, что это текущий месяц и год
      if (date.getMonth() === currentMonth && date.getFullYear() === currentYear) {
        var cat = rows[i][1];
        var amt = parseFloat(rows[i][2]);
        
        if (cat && !isNaN(amt)) {
          spent[cat] = (spent[cat] || 0) + amt;
          history.push({
            date: Utilities.formatDate(date, "GMT+2", "dd.MM HH:mm"),
            category: cat,
            amount: amt
          });
        }
      }
    } catch(e) { /* пропускаем битые строки */ }
  }

  var result = {
    spent: spent,
    history: history.reverse().slice(0, 10)
  };
  
  return ContentService.createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  var data = JSON.parse(e.postData.contents);
  // Записываем: Дата | Категория | Сумма
  sheet.appendRow([new Date(), data.category, data.amount]);
  return ContentService.createTextOutput("OK");
}
