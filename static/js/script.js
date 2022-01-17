//global variables
var monthEl = $(".c-main");
var dataCel = $(".c-cal__cel");
var dataHour = $(".hour_cell");
var dateObj = new Date();
var month = dateObj.getUTCMonth() + 1;
var day = dateObj.getUTCDate();
var year = dateObj.getUTCFullYear();

var reservedHours = [];
var counterReservedHours = 1;

var monthText = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];
var indexYear = 0;
var indexMonth = month;
var inputDate = $(this).data();

// ------ functions control -------
// Onclick hour cell
$(document).on("click", ".hour_cell", function () {
  var th = $(this).data().hours.slice(0, 2);

  for (var i = 0; i < counterReservedHours; i++) {
    if (i + 1 == counterReservedHours && reservedHours[i] != th) {
      counterReservedHours++;
      reservedHours[i] = th;
      break;
    } else if (reservedHours[i] == th) {
      reservedHours.splice(reservedHours.indexOf(th), 1);
      counterReservedHours--;
      break;
    }
  }
  $(this).toggleClass("isSelected");
});

dataCel.on("click", function () {
  var thisEl = $(this);
  var thisDay = $(this).attr("data-day").slice(8);
  var thisMonth = $(this).attr("data-day").slice(5, 7);

  $(".c-aside__num").text(thisDay);
  $(".c-aside__month").text(monthText[thisMonth - 1]);
  $(".c-aside__year").text(dateObj.getUTCFullYear() + indexYear);
  xhttp(thisDay, thisMonth);

  dataCel.removeClass("isSelected");
  thisEl.addClass("isSelected");
});

//function for move the months
function moveNext(fakeClick, indexNext) {
  for (var i = 0; i < fakeClick; i++) {
    $(".c-main").css({
      left: "-=100%",
    });
    $(".c-paginator__month").css({
      left: "-=100%",
    });
    switch (true) {
      case indexNext:
        indexMonth += 1;
        break;
    }
  }
}

function movePrev(fakeClick, indexPrev) {
  for (var i = 0; i < fakeClick; i++) {
    $(".c-main").css({
      left: "+=100%",
    });
    $(".c-paginator__month").css({
      left: "+=100%",
    });
    switch (true) {
      case indexPrev:
        indexMonth -= 1;
        break;
    }
  }
}

//months paginator
function buttonsMonthPaginator(buttonId, mainClass, monthClass, next, prev) {
  switch (true) {
    case next:
      $(buttonId).on("click", function () {
        if (indexMonth >= 2) {
          $(mainClass).css({
            left: "+=100%",
          });
          $(monthClass).css({
            left: "+=100%",
          });
          indexMonth -= 1;
        }

        return indexMonth;
      });
      break;
    case prev:
      $(buttonId).on("click", function () {
        if (indexMonth <= 11) {
          $(mainClass).css({
            left: "-=100%",
          });
          $(monthClass).css({
            left: "-=100%",
          });
          indexMonth += 1;
        }
        return indexMonth;
      });
      break;
  }
}

buttonsMonthPaginator("#next", monthEl, ".c-paginator__month", false, true);
buttonsMonthPaginator("#prev", monthEl, ".c-paginator__month", true, false);

//months paginator
function buttonsYearPaginator(buttonId, monthClass, next, prev) {
  switch (true) {
    case next:
      $(buttonId).on("click", function () {
        if (indexYear >= 1) {
          $(monthClass).css({
            left: "+=100%",
          });
          indexYear -= 1;
        }
        year = dateObj.getUTCFullYear() + indexYear;
        $(".c-aside__year").text(dateObj.getUTCFullYear() + indexYear);

        return indexYear;
      });
      break;
    case prev:
      $(buttonId).on("click", function () {
        if (indexYear <= 1) {
          $(monthClass).css({
            left: "-=100%",
          });
          indexYear += 1;
        }
        year = dateObj.getUTCFullYear() + indexYear;
        $(".c-aside__year").text(dateObj.getUTCFullYear() + indexYear);

        return indexYear;
      });
      break;
  }
}

buttonsYearPaginator("#nextYear", ".c-paginator__year", false, true);
buttonsYearPaginator("#prevYear", ".c-paginator__year", true, false);

//launch function to set the current month
moveNext(indexMonth - 1, false);
//fill the year
document.getElementById("firstY").innerHTML = dateObj.getUTCFullYear();
document.getElementById("secondY").innerHTML = dateObj.getUTCFullYear() + 1;
document.getElementById("thirdY").innerHTML = dateObj.getUTCFullYear() + 2;
//fill the sidebar with current day
$(".c-aside__num").text(day);
$(".c-aside__month").text(monthText[month - 1]);
$(".c-aside__year").text(year);

function xhttp(day, month) {
  // Create an XMLHttpRequest object
  const xhttp = new XMLHttpRequest();
  var hourArray;
  // Define a callback function
  xhttp.onload = function () {
    var parser, xmlDoc;
    var text = this.responseText;
    parser = new DOMParser();
    xmlDoc = parser.parseFromString(text, "text/xml");
    hourArray = xmlDoc.getElementsByTagName("item");

    booking_hours(hourArray);
  };
  // Send a request
  //console.log(month + "/" + day + "/" + year);
  xhttp.open("GET", "hours.xml");
  //xhttp.open("GET","http://127.0.0.1:8000/trainer/reservationInfo/3/" +year +"-" +month +"-" +day +"/");
  xhttp.send();
}

function booking_hours(hourArray) {
  console.log("heyyyy");

  var table;
  for (var i = 0; i < hourArray.length; i++) {
    if (parseInt(hourArray[i].childNodes[0].nodeValue) < 9)
      table +=
        "<div data-hours='0" +
        hourArray[i].childNodes[0].nodeValue +
        ".00-0" +
        (parseInt(hourArray[i].childNodes[0].nodeValue) + 1) +
        ".00' class='hour_cell'>" +
        "<p>" +
        "0" +
        hourArray[i].childNodes[0].nodeValue +
        ".00 - 0" +
        (parseInt(hourArray[i].childNodes[0].nodeValue) + 1) +
        ".00" +
        "</p></div>";
    else if (parseInt(hourArray[i].childNodes[0].nodeValue) == 9) {
      table +=
        "<div data-hours='0" +
        hourArray[i].childNodes[0].nodeValue +
        ".00-0" +
        (parseInt(hourArray[i].childNodes[0].nodeValue) + 1) +
        ".00' class='hour_cell'>" +
        "<p>" +
        "0" +
        hourArray[i].childNodes[0].nodeValue +
        ".00 - " +
        (parseInt(hourArray[i].childNodes[0].nodeValue) + 1) +
        ".00" +
        "</p></div>";
    } else {
      table +=
        "<div data-hours='" +
        hourArray[i].childNodes[0].nodeValue +
        ".00-" +
        (parseInt(hourArray[i].childNodes[0].nodeValue) + 1) +
        ".00' class='hour_cell'>" +
        "<p>" +
        hourArray[i].childNodes[0].nodeValue +
        ".00 - " +
        (parseInt(hourArray[i].childNodes[0].nodeValue) + 1) +
        ".00" +
        "</p></div>";
    }
  }

  document.getElementById("hoursList").innerHTML = table.slice(9);
}

// fill the month table with column headings
function day_title(day_name) {
  document.write("<div class='c-cal__col'>" + day_name + "</div>");
}
// fills the month table with numbers
function fill_table(month, month_length, indexMonth) {
  day = 1;
  // begin the new month table
  document.write("<div class='c-main c-main-" + indexMonth + "'>");
  //document.write("<b>"+month+" "+year+"</b>")

  // column headings
  document.write("<div class='c-cal__row'>");
  day_title("Sun");
  day_title("Mon");
  day_title("Tue");
  day_title("Wed");
  day_title("Thu");
  day_title("Fri");
  day_title("Sat");
  document.write("</div>");

  // pad cells before first day of month
  document.write("<div class='c-cal__row'>");
  for (var i = 1; i < start_day; i++) {
    if (start_day > 7) {
    } else {
      document.write("<div class='c-cal__cel'></div>");
    }
  }

  // fill the first week of days
  for (var i = start_day; i < 8; i++) {
    document.write(
      "<div data-day='2017-" +
        indexMonth +
        "-0" +
        day +
        "'class='c-cal__cel'><p>" +
        day +
        "</p></div>"
    );
    day++;
  }
  document.write("</div>");

  // fill the remaining weeks
  while (day <= month_length) {
    document.write("<div class='c-cal__row'>");
    for (var i = 1; i <= 7 && day <= month_length; i++) {
      if (day >= 1 && day <= 9) {
        document.write(
          "<div data-day='" +
            year +
            "-" +
            indexMonth +
            "-0" +
            day +
            "'class='c-cal__cel'><p>" +
            day +
            "</p></div>"
        );
        day++;
      } else {
        document.write(
          "<div data-day='" +
            year +
            "-" +
            indexMonth +
            "-" +
            day +
            "' class='c-cal__cel'><p>" +
            day +
            "</p></div>"
        );
        day++;
      }
    }
    document.write("</div>");
    // the first day of the next month
    start_day = i;
  }

  document.write("</div>");
}
