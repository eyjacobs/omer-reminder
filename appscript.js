function doPost(e) {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var name = e.parameter.name || '';
  var phone = e.parameter.phone;
  var carrier = e.parameter.carrier;
  var timezone = e.parameter.timezone;

  sheet.appendRow([new Date(), name, phone, carrier, timezone]);

  return ContentService.createTextOutput('OK');
}

function getHebrewMonth() {
  var today = new Date();
  var month = today.getMonth() + 1;
  var day = today.getDate();

  if (month === 4 && day < 18) return 'Nissan';
  if ((month === 4 && day >= 18) || (month === 5 && day < 18)) return 'Iyar';
  if (month === 5 && day >= 18) return 'Sivan';

  return 'the month';
}
