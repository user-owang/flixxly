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

window.addEventListener("load", function () {
  const pic = document.getElementById("user-picture");
  const picbox = document.getElementById("user-picture-box");

  if (pic.width < 220 && pic.height < 330) {
    if (pic.width / pic.height >= 2 / 3) {
      picbox.style.height = `${(pic.height * 220) / pic.width}px`;
      picbox.style.width = "220px";
    } else {
      picbox.style.height = "330px";
    }
    picbox.removeChild(pic);
  } else {
    if (pic.width / pic.height >= 2 / 3) {
      pic.style.width = "220px";
      pic.style.height = "auto";
    } else {
      pic.style.width = "auto";
      pic.style.height = "330px";
    }
    pic.classList.remove("hidden");
  }
});
