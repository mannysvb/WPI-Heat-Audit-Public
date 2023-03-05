// This code should run on the Raw Heat Sensor Temperature Data
var sheetState = {
  "Grasslands": false,
  "HeatHaven1": false,
  "HeatHaven3": false,
  "FoodForest": false,
  "CommunityGardens": false,
  "PlayBushTucker": false,
  "ProjectReal": false
  };

listOfSheets = ["FoodForest", "Grasslands", "HeatHaven1", "HeatHaven2", "CommunityGardens", "PlayBushTucker", "ProjectReal"]
GrasslandsSheet = ["Grasslands"]

function onChange(e) {
  if (e && e.user) {
    var userEmails = ["sustainability@banksiagardens.org.au", "jonathan.c@banksiagardens.org.au", "stephen.e.fanning@gmail.com",
    "eschuman20@gmail.com"] 
    // This check doesn't work, it only ignores the changes made by the owner's account. If you need to make changes and aren't the    owner just comment out the function above.
    //var changedBy = e.user.email;
    var changedBy = Session.getActiveUser().getEmail()
    Logger.log(changedBy)
    var index = userEmails.indexOf(changedBy);
    Logger.log(index)
    if (index !== -1) {
    //Logger.log(changedBy)
    //if (userEmails.includes(changedBy)) {
      return; // If email matches, exit function without running the rest of the code
    }
    if (sheetState[e.source.getActiveSheet().getName()]) { // check if the sheet has already been processed
      return;
    }
    runMacro(e.source.getActiveSheet().getName());

    // Set the format as date time for column A
    var sheet = e.source.getActiveSheet();
    var range = sheet.getRange("A:A");
    var dateFormat = "MM/dd/yyyy hh:mm:ss";
    range.setNumberFormat(dateFormat);
  }
}


function runMacro(sheetName) {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
  if (spreadsheet) {
    var currentCell = spreadsheet.getCurrentCell();
    spreadsheet.getCurrentCell().offset(0, 3).activate();
    spreadsheet.getCurrentCell().setFormulaR1C1('=TEXT(R[0]C[-3], "dd/mm/yyyy HH:mm:ss")');
    spreadsheet.getCurrentCell().offset(0, 1).activate();
    spreadsheet.getCurrentCell().setFormulaR1C1('=TEXT(R[0]C[-3],"#.##")');
    sheetState[sheetName] = true;
  } else {
    Logger.log("Sheet not found: " + sheetName);
  }
}

function formatDate(date) {
  var datetimeString = date.toLocaleString();
  var milliseconds = Date.parse(datetimeString);
  var formattedDate = new Date(milliseconds).toLocaleString('en-US', {timeZone: 'UTC'});
  return formattedDate;
}

function checkMissing(){
  for (var i = 0; i < listOfSheets.length; i++){
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(listOfSheets[i]);
    var lastRow = sheet.getLastRow();
    var values = sheet.getRange(1, 7, lastRow).getValues();
    var lastRowG = 0
    for (var j = values.length - 1; j >= 0; j--) {
      if (values[j][0] !== '') {
        lastRowG = j + 1
        break
      }
    } 
    var values2 = sheet.getRange(1, 1, lastRow).getValues();
    var lastRowA = 0
    for (var k = values2.length - 1; k >= 0; k--) {
      if (values2[k][0] !== '') {
        lastRowA = k + 1
        break
      }
    } 

    var range = sheet.getRange("G" + lastRowG)
    
    var lastReadingHour = range.getValues();
    var dateLastReading = new Date(lastReadingHour);
    var hourLastReading = dateLastReading.getHours();

    var currentDay = new Date();
    var currentHourInUTC = currentDay.getUTCHours();

    if (currentHourInUTC == hourLastReading) {
    } else {
      var nextRow = lastRowA + 1;
      var newRangeTime = sheet.getRange("A" + nextRow);
      var newRangeTemp = sheet.getRange("B" + nextRow);
      var colD = sheet.getRange("D" + nextRow)
      var colE = sheet.getRange("E" + nextRow)
      newRangeTemp.setValue("Missing");
      var currentDate = new Date();
      currentDate.setMinutes(0);
      currentDate.setSeconds(0);
      var utcDateString = currentDate.toISOString().slice(0, 19).replace('T', ' ');
      newRangeTime.setValue(utcDateString)
      var timezone = "Australia/Melbourne";
      newRangeTime.setValue(Utilities.formatDate(new Date(newRangeTime.getValue()), timezone, "MM/dd/yyyy HH:mm:ss"));
      colD.setValue(Utilities.formatDate(new Date(newRangeTime.getValue()), timezone, "dd/MM/yyyy HH:mm:ss"));
      colD.setNumberFormat("@");
      // Write Code later to make column D =text format since the condition only works with a
      colE.setValue("Missing")
      newRangeTime.setNumberFormat("@");
    }
  }
}

function removeDuplicateHours() {
  // The following identifies different sheets within the workbook
  var sheetNames = ["FoodForest", "Grasslands", "HeatHaven1", "HeatHaven2", "CommunityGardens", "PlayBushTucker", "ProjectReal"];
  sheetNames.forEach(function(sheetName) {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
    var range = sheet.getRange("G1:H"); // This assumes that the data starts at row 1
    var data = range.getValues();

    if (!data) {
      return null;
    }

    var newData = [];
    var hours = {};
    for (var i = 0; i < data.length; i++) {
      var date = new Date(data[i][0]);
      var hour = date.getHours();
      var day = date.getDate();
      if (!hours[day] || !hours[day][hour]) {
        if (!hours[day]) {
          hours[day] = {};
        }
        hours[day][hour] = true;
        newData.push(data[i]);
      }
    }
    console.log(newData)
    var newRange = sheet.getRange(1, 10, newData.length, newData[0].length);
    newRange.setValues(newData);
  });
}

function removeDuplicateHoursTriggers() {
  // Delete existing triggers
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() == "removeDuplicateHours") {
      ScriptApp.deleteTrigger(triggers[i]);
    }
  }
  // Create new time-driven trigger
  ScriptApp.newTrigger("removeDuplicateHours")
    .timeBased()
    .everyHours(1)
    .nearMinute(16)
    .create();
}

function checkMissingTriggers() {
  // Delete existing triggers
  var triggers = ScriptApp.getProjectTriggers();
  for (var i = 0; i < triggers.length; i++) {
    if (triggers[i].getHandlerFunction() == "checkMissing") {
      ScriptApp.deleteTrigger(triggers[i]);
    }
  }
  // Create new time-driven trigger
  ScriptApp.newTrigger("checkMissing")
    .timeBased()
    .everyHours(1)
    .nearMinute(11)
    .create();
}