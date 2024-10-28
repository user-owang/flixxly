const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const term = urlParams.get("q");
let page = 1;
let mTotalPages;
let pTotalPages;

const $moviesTab = $("#movies-tab");
const $peopleTab = $("#people-tab");
const $usersTab = $("#users-tab");
const $movieResults = $("#movies-tab-pane");
const $peopleResults = $("#people-tab-pane");
const $userResults = $("#users-tab-pane");

async function movieSearch() {
  const response = await axios.post("/api/search-results", {
    term: term,
    page: page,
    search_type: "movie",
  });
  return response;
}

async function personSearch() {
  const response = await axios.post("/api/search-results", {
    term: term,
    page: page,
    search_type: "person",
  });
  return response;
}

async function userSearch() {
  const response = await axios.post("/api/search-results", {
    term: term,
    search_type: "user",
  });
  return response;
}

async function getMTotalPages() {
  response = await movieSearch();
  mTotalPages = response["data"]["total_pages"];
}
async function getPTotalPages() {
  response = await personSearch();
  pTotalPages = response["data"]["total_pages"];
}
getMTotalPages();
getPTotalPages();

async function movieTabScrollHandler() {
  if (page < mTotalPages) {
    page += 1;
    response = await movieSearch();
    console.log(response);
    buildMovieCard(
      response,
      $movieResults,
      true,
      "https://media.themoviedb.org/t/p/w220_and_h330_face"
    );
  } else {
    return;
  }
}

async function movieTabHandler() {
  page = 1;
  $peopleResults.empty();
  $userResults.empty();
  response = await movieSearch();

  $movieResults.append(
    `<h2>${response["data"]["total_results"]} movie result(s) found</h2>`
  );
  buildMovieCard(
    response,
    $movieResults,
    true,
    "https://media.themoviedb.org/t/p/w220_and_h330_face"
  );
}

$moviesTab.on("click", movieTabHandler);

async function peopleTabScrollHandler() {
  if (page < pTotalPages) {
    page += 1;
    response = await personSearch();
    buildPersonCard(
      response,
      $peopleResults,
      "https://media.themoviedb.org/t/p/w150_and_h150_face"
    );
  } else {
    return;
  }
}

async function peopleTabHandler() {
  page = 1;
  $movieResults.empty();
  $userResults.empty();
  response = await personSearch();

  $peopleResults.append(
    `<h2>${response["data"]["total_results"]} people result(s) found</h2>`
  );
  buildPersonCard(
    response,
    $peopleResults,
    "https://media.themoviedb.org/t/p/w150_and_h150_face"
  );
}

$peopleTab.on("click", peopleTabHandler);

function buildUserCard(response, container) {
  if (response["data"]["results"].length > 0) {
    for (let user of response["data"]["results"]) {
      bio = "";
      if (user["bio"]) {
        bio = `<small>${user["bio"]}</small>`;
      }
      userCard = `
      <div class="card user-card">
        <div class="card-contents">
          <a href="/users/${user["id"]}">
          <div
          class="user-picture"
          style="background-image: url('${user.img_url}');"
        ></div>
          </a>
          <div class="text">
            <a href="/users/${user["id"]}">
              <div><h3>${user["username"]}</h3></div>
            </a>
            ${bio}
          </div>
        </div>
      </div>`;
      container.append(userCard);
    }
  }
}

async function userTabHandler() {
  page = 1;
  $peopleResults.empty();
  $movieResults.empty();
  response = await userSearch();

  $userResults.append(
    `<h2>${response["data"]["total_results"]} user result(s) found</h2>`
  );
  buildUserCard(response, $userResults);
}

$usersTab.on("click", userTabHandler);
create_autoscroll($movieResults, movieTabScrollHandler);
create_autoscroll($peopleResults, peopleTabScrollHandler);
