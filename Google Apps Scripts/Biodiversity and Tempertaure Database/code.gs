var SHEETNAME="temp"

function doGet(e) {
  let sheet;
  if (this.sheet == null) {
      this.sheet = SpreadsheetApp.getActiveSpreadsheet();
  }

  let SHEET = this.sheet.getSheetByName(SHEETNAME);
  lastLog=SHEET.getRange("C1").getValue();
  SHEET.getRange("C1").setValue(lastLog+1);
  ContentService.createTextOutput(SHEET.getRange("B"+lastLog).setValue(e.parameter.temp.split(",")[1]));
  ContentService.createTextOutput(SHEET.getRange("A"+lastLog).setValue(e.parameter.temp.split(",")[0]));
  return "ok"
}


function importTimeOnHour() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Temperature Sensor Data");
  var intervalInMinutes = 60; // import interval in minutes
  var timezone = "Australia/Melbourne";
  var date = new Date();
  var currentTime = Utilities.formatDate(date, timezone, "yyyy-MM-dd hh:mm a");
  var currentMinute = date.getMinutes();
  
  var timezone = "Australia/Melbourne";
  var currentTime = new Date();
  currentTime.setHours(currentTime.getHours() + 1);
  currentTime.setMinutes(0)
  currentTime.setSeconds(0)
  var melbourneTime = Utilities.formatDate(currentTime, timezone, "yyyy-MM-dd hh:mm a");

  if (currentMinute % intervalInMinutes != 0) {
    // if current minute is not on the hour, exit the function
    return;
  }
  
  var lastRow = sheet.getLastRow();
  var nextRow = lastRow + 1;
  
  var cell = sheet.getRange("A" + nextRow);
  cell.setValue(melbourneTime);
  cell.setNumberFormat("MM/dd/yyyy HH:mm:ss");
}

function importTimeOnHour() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Temperature Sensor Data");
  var lastRow = sheet.getLastRow();
  var values = sheet.getRange(1, 1, lastRow).getValues();
  var lastRowA = 0
    for (var j = values.length - 1; j >= 0; j--) {
      if (values[j][0] !== '') {
        lastRowA = j + 1
        break
      }
    } 
  var timezone = "Australia/Melbourne";
  var currentTime = new Date();
  currentTime.setHours(currentTime.getHours() + 1);
  currentTime.setMinutes(0)
  currentTime.setSeconds(0)
  var melbourneTime = Utilities.formatDate(currentTime, timezone, "yyyy-MM-dd hh:mm a");

  var nextRow = lastRowA + 1;

  var cell = sheet.getRange("A" + nextRow);
  cell.setValue(melbourneTime);
  cell.setNumberFormat("MM/dd/yyyy HH:mm:ss");
}

function createHourlyTrigger() {
  // Delete existing triggers
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() === "importTimeOnHour") { // Replace "myFunction" with the name of your function
      ScriptApp.deleteTrigger(triggers[i]);
    }
  }

  // Create new trigger
  ScriptApp.newTrigger("importTimeOnHour") // Replace "myFunction" with the name of your function
      .timeBased()
      .everyHours(1)
      .nearMinute(0)
      .create();
}

// Possibly will have to copy the removeDuplicateHours from the Raw Heat Sensor Temperature Data Script here since the time duplicated at the 10th hour 3 times on the second day the script starting running. Write code to trigger the function five minutes after importHour. 