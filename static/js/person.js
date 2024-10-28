const $filmBtn = $("#film-btn");
const $filmTab = $("#film-tab");
const $infoTab = $("#info-tab");
const $filmPane = $("#film-tab-pane");
const $infoPane = $("#info-tab-pane");

function filmBtnClickHandler() {
  $infoPane.removeClass("active");
  $infoTab.removeClass("active");
  $filmTab.addClass("active");
  $filmPane.addClass("active");
}

function clearFilmBtnActive() {
  $filmBtn.removeClass("active");
}

$filmBtn.on("click", filmBtnClickHandler);
$infoTab.on("click", clearFilmBtnActive);
