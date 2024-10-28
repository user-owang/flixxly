const $releaseRadar = $("#rr-tab-pane");
const $pastFilms = $("#pf-tab-pane");
const $rrBtn = $("#rr-tab");
const $pfBtn = $("#pf-tab");

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
    rrPage += 1;
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
    pfPage += 1;
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

$rrBtn.on("click", function () {
  rrPage = 1;
});

$pfBtn.on("click", function () {
  pfPage = 1;
});

create_autoscroll($releaseRadar, rrScrollHandler);
create_autoscroll($pastFilms, pfScrollHandler);
