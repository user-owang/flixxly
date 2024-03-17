const $movieSwitch = $("#trending-movies");
const $peopleSwitch = $("#trending-people");
const $movieDisplay = $(".trending-movies");
const $peopleDisplay = $(".trending-people");

function showMoviesHandler() {
  $peopleSwitch.removeClass("selected");
  $movieSwitch.addClass("selected");

  hide($peopleDisplay);
  show($movieDisplay);
}

function showPeopleHandler() {
  $movieSwitch.removeClass("selected");
  $peopleSwitch.addClass("selected");

  hide($movieDisplay);
  show($peopleDisplay);
}

$movieSwitch.on("click", showMoviesHandler);
$peopleSwitch.on("click", showPeopleHandler);
