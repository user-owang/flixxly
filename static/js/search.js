const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const term = urlParams.get("q");
let page = 1;
let mTotalPages;
let pTotalPages;

const $moviesTab = $("#movies-btn");
const $peopleTab = $("#people-btn");
const $usersTab = $("#users-btn");
const $results = $(".results");

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
    const $movieResults = $(".movie-results");
    response = await movieSearch();
    console.log(response);
    buildMovieCard(
      response,
      $movieResults,
      true,
      "https://media.themoviedb.org/t/p/w94_and_h141_bestv2"
    );
    console.log("kill yourself");
  } else {
    return;
  }
}

async function movieTabHandler() {
  $usersTab.removeClass("selected");
  $peopleTab.removeClass("selected");
  $moviesTab.addClass("selected");

  page = 1;
  $results.empty();
  response = await movieSearch();

  const movieResults = document.createElement("section");
  movieResults.classList.add("movie-results");
  movieResults.innerHTML += `<h2>${response["data"]["total_results"]} movie result(s) found</h2>`;
  const $movieResults = $(movieResults);
  buildMovieCard(
    response,
    $movieResults,
    true,
    "https://media.themoviedb.org/t/p/w94_and_h141_bestv2"
  );

  $results.append(movieResults);

  create_autoscroll($movieResults, movieTabScrollHandler);
}

$moviesTab.on("click", movieTabHandler);

async function personTabScrollHandler() {
  if (page < pTotalPages) {
    page += 1;
    const $personResults = $(".person-results");
    response = await personSearch();
    buildPersonCard(
      response,
      $personResults,
      "https://media.themoviedb.org/t/p/w90_and_h90_face"
    );
  } else {
    return;
  }
}

async function personTabHandler() {
  $usersTab.removeClass("selected");
  $moviesTab.removeClass("selected");
  $peopleTab.addClass("selected");

  page = 1;
  $results.empty();
  response = await personSearch();

  const personResults = document.createElement("section");
  personResults.classList.add("person-results");
  personResults.innerHTML += `<h2>${response["data"]["total_results"]} person result(s) found</h2>`;
  const $personResults = $(personResults);
  buildPersonCard(
    response,
    $personResults,
    "https://media.themoviedb.org/t/p/w90_and_h90_face"
  );

  $results.append(personResults);

  create_autoscroll($personResults, personTabScrollHandler);
}

$peopleTab.on("click", personTabHandler);

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
          style="background-image: url('{{user.img_url}}');"
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
      container.innerHTML += userCard;
    }
  }
}

async function userTabHandler() {
  $peopleTab.removeClass("selected");
  $moviesTab.removeClass("selected");
  $usersTab.addClass("selected");

  page = 1;
  $results.empty();
  response = await userSearch();

  userResults = document.createElement("section");
  userResults.classList.add("user-results");
  userResults.innerHTML += `<h2>${response["data"]["total_results"]} user result(s) found</h2>`;
  buildUserCard(response, userResults);

  $results.append(userResults);
}

$usersTab.on("click", userTabHandler);
