const $watchlist = $("div.watchlist");
const $seenlist = $("div.seenlist");
const $following = $("div.following");

const $wlBtn = $("#watchlist");
const $slBtn = $("#seenlist");
const $fBtn = $("#following");

function wlTabHandler() {
  $slBtn.removeClass("selected");
  $fBtn.removeClass("selected");
  $wlBtn.addClass("selected");

  hide($seenlist);
  hide($following);
  show($watchlist);
}

function slTabHandler() {
  $wlBtn.removeClass("selected");
  $fBtn.removeClass("selected");
  $slBtn.addClass("selected");

  hide($watchlist);
  hide($following);
  show($seenlist);
}

function fTabHandler() {
  $slBtn.removeClass("selected");
  $wlBtn.removeClass("selected");
  $fBtn.addClass("selected");

  hide($seenlist);
  hide($watchlist);
  show($following);
}

$wlBtn.on("click", wlTabHandler);
$slBtn.on("click", slTabHandler);
$fBtn.on("click", fTabHandler);
