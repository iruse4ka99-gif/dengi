function doGet() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  var data = sheet.getDataRange().getValues();
  
  var now = new Date();
  var curMonth = now.getMonth(); 
  var curYear = now.getFullYear();
  
  // Создаем строку для поиска, например ".03.2026"
  var monthStr = ("0" + (curMonth + 1)).slice(-2);
  var targetDateStr = "." + monthStr + "." + curYear;

  var spent = {};
  var history = [];

  for (var i = 1; i < data.length; i++) {
    var rowDate = data[i][0];
    if (!rowDate) continue;

    var isCurrentMonth = false;
    var formattedDate = "";

    // Проверяем дату (даже если она криво записана как текст)
    if (rowDate instanceof Date) {
      if (rowDate.getMonth() === curMonth && rowDate.getFullYear() === curYear) {
        isCurrentMonth = true;
        formattedDate = Utilities.formatDate(rowDate, "GMT+2", "dd.MM HH:mm");
      }
    } else {
      var dateString = String(rowDate);
      if (dateString.indexOf(targetDateStr) !== -1) {
        isCurrentMonth = true;
        formattedDate = dateString.substring(0, 16); // Берем начало строки
      }
    }

    // Если это текущий месяц - считаем деньги
    if (isCurrentMonth) {
      var cat = String(data[i][1]).trim();
      var amt = parseFloat(data[i][2]) || 0;
      
      if (cat) {
        spent[cat] = (spent[cat] || 0) + amt;
        history.push({
          date: formattedDate,
          category: cat,
          amount: amt
        });
      }
    }
  }
  
  return ContentService.createTextOutput(JSON.stringify({
    spent: spent, 
    history: history.reverse().slice(0, 10)
  })).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  var data = JSON.parse(e.postData.contents);
  sheet.appendRow([new Date(), data.category, data.amount]);
  return ContentService.createTextOutput("OK");
}
