const $releaseRadar = $(".release-radar");
const $pastFilms = $(".past-films");
const $rrBtn = $("#release-radar");
const $pfBtn = $("#past-films");

let rrPage = 1;
let pfPage = 1;

let rrTotalPages;
let pfTotalPages;

async function getRR() {
  const response = await axios.post(
    "/api/release-radar",
    {
      page: rrPage,
    },
    {
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  return response;
}
async function getPF() {
  const response = await axios.post(
    "/api/past-films",
    {
      page: pfPage,
    },
    {
      headers: {
        "Content-Type": "application/json",
      },
    }
  );
  return response;
}

async function getFTotalPages() {
  rrTest = await getRR();
  rrTotalPages = rrTest["data"]["total_pages"];
  pfTest = await getPF();
  pfTotalPages = pfTest["data"]["total_pages"];
}

getFTotalPages();

async function rrScrollHandler() {
  if (rrPage < rrTotalPages) {
    page += 1;
    response = await getRR();
    buildMovieCard(
      response,
      $releaseRadar,
      false,
      "https://media.themoviedb.org/t/p/w220_and_h330_face"
    );
  } else {
    return;
  }
}

async function pfScrollHandler() {
  if (pfPage < pfTotalPages) {
    page += 1;
    response = await getPF();
    buildMovieCard(
      response,
      $pastFilms,
      true,
      "https://media.themoviedb.org/t/p/w220_and_h330_face"
    );
  } else {
    return;
  }
}

function rrTabHandler() {
  $rrBtn.addClass("selected");
  $pfBtn.removeClass("selected");
  hide($pastFilms);
  show($releaseRadar);
}

function pfTabHandler() {
  $pfBtn.addClass("selected");
  $rrBtn.removeClass("selected");
  show($pastFilms);
  hide($releaseRadar);
}

$rrBtn.on("click", rrTabHandler);
$pfBtn.on("click", pfTabHandler);
