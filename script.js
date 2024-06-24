setInterval(function () {
  var percentageText = document.getElementById("percent");
    console.log(percentageText)
  if (percentageText == undefined) {
    console.log("Percentage not found");
    return;
  }

  var percentage = parseInt(percentageText.replace("%", ""));

  var color = "#90A4AE";

  if (percentage >= 90) {
    color = "#00E676";
  } else if (percentage < 90 && percentage >= 60) {
    color = "#81C784";
  } else if (percentage < 60 && percentage >= 40) {
    color = "#FFEB3B";
  } else if (percentage < 40 && percentage >= 10) {
    color = "#FF9800";
  } else if (percentage < 10 && percentage >= 0) {
    color = "#FF3D00";
  }

  document.querySelector(".column").style.backgroundColor = color;

  document.querySelector(".column").style.height = percentage + "%";
}, 1000);