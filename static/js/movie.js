const $castBtn = $("#cast-btn");
const $castTab = $("#cast-tab");
const $overviewTab = $("#overview-tab");
const $castPane = $("#cast-tab-pane");
const $overviewPane = $("#overview-tab-pane");

function castBtnClickHandler() {
  $overviewPane.removeClass("active");
  $overviewTab.removeClass("active");
  $castTab.addClass("active");
  $castPane.addClass("active");
}

function clearCastBtnActive() {
  $castBtn.removeClass("active");
}

$castBtn.on("click", castBtnClickHandler);
$overviewTab.on("click", clearCastBtnActive);
