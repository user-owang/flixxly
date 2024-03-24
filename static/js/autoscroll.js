function create_autoscroll(container, request) {
  container.on(
    "scroll",
    _.debounce(function () {
      console.log("scroll");
      let distanceFromBottom =
        container.prop("scrollHeight") -
        (container.scrollTop() + container.height());
      if (distanceFromBottom <= 400) {
        console.log("trigger");
        request();
      }
    }, 50)
  );
}

function hide(lmnt) {
  lmnt.addClass("hidden");
}

function show(lmnt) {
  lmnt.removeClass("hidden");
}

async function getFollows() {
  const response = await axios.get("/api/get-follows");
  return response["data"];
}
async function getWatchlist() {
  const response = await axios.get("/api/get-watchlist");
  return response["data"];
}
async function getSeenlist() {
  const response = await axios.get("/api/get-seenlist");
  return response["data"];
}

let currUserFollows;
let currUserWatch;
let currUserSeen;

async function getCurrUser() {
  currUserFollows = await getFollows();
  currUserSeen = await getSeenlist();
  currUserWatch = await getWatchlist();
  console.log(currUserFollows, currUserSeen, currUserWatch);
}

getCurrUser();

function buildMovieCard(response, container, displaySeenlistBtn, URLprefix) {
  if (response["data"]["results"].length > 0) {
    for (let movie of response["data"]["results"]) {
      let image = '<div class="no-poster"></div>';
      if (movie["poster_path"]) {
        image = `<img src="${URLprefix}${movie["poster_path"]}" alt=""/>`;
      }
      let watchBtn = "";
      if (currUserWatch["user"]) {
        watchBtn = `<form
        method="POST"
        action="/movies/add-watchlist/${movie["id"]}"
      >
        <button class="btn btn-primary btn-sm">Watchlist</button>
      </form>`;
        if (currUserWatch["watchlist"].includes(movie["id"])) {
          watchBtn = `<form
          method="POST"
          action="/movies/remove-watchlist/${movie["id"]}"
        >
          <button class="btn btn-outline-primary btn-sm">
            Remove from watchlist
          </button>
        </form>`;
        }
      }
      let seenBtn = "";
      if (currUserSeen["user"]) {
        console.log("make seenBtn");
        seenBtn = `<form
        method="POST"
        action="/movies/add-seenlist/${movie["id"]}"
      >
        <button class="btn btn-primary btn-sm" id="add-seen">
          Seen it
        </button>
      </form>`;
        if (currUserSeen["seenlist"].includes(movie["id"])) {
          seenBtn = `<form
          method="POST"
          action="/movies/remove-seenlist/${movie["id"]}"
        >
          <button class="btn btn-outline-primary btn-sm">
            Remove from seenlist
          </button>
        </form>`;
        }
      }
      if (!displaySeenlistBtn) {
        seenBtn = "";
      }
      movieCard = `
      <div class="card movie-card">
        <div class="card-contents">
          <a href="/movies/${movie["id"]}">
            ${image}
          </a>
          <div class="text">
            <div class="top-card">
              <a href="/movies/${movie["id"]}">
                <div><h3>${movie["title"]}</h3></div>
              </a>
              <p><small>${movie["formatted_date"]}</small></p>
              <div class="buttons">
                ${watchBtn}
                ${seenBtn}
              </div>
            </div>
            <div class="bottom-card">
              <p>${movie["overview"]}</p>
            </div>
          </div>
        </div>
      </div>`;
      container.append(movieCard);
    }
  }
}

function buildPersonCard(response, container, URLprefix) {
  if (response["data"]["results"].length > 0) {
    for (let person of response["data"]["results"]) {
      let image = '<div class="no-profile"></div>';
      if (person["profile_path"]) {
        image = `<img src='${URLprefix}${person["profile_path"]}' alt=""/>`;
      }
      let followBtn = "";
      if (currUserFollows["user"]) {
        followBtn = `
        <form
          method="POST"
          action="/people/add-follow/${person["id"]}"
        >
          <button class="btn btn-primary btn-sm">Follow</button>
        </form>`;
        if (currUserFollows["follows"].includes(person["id"])) {
          followBtn = `
          <form
            method="POST"
            action="/people/remove-follow/${person["id"]}"
          >
            <button class="btn btn-outline-primary btn-sm">
              Unfollow
            </button>
          </form>`;
        }
      }
      let KFmovies = "";
      for (let movie of person["known_for"]) {
        if ((KFmovies = "")) {
          KFmovies += `<a href="/movies/${movie["id"]}">${movie["title"]}</a>`;
        } else {
          KFmovies += `, <a href="/movies/${movie["id"]}">${movie["title"]}</a>`;
        }
      }

      personCard = `
      <div class="card person-card">
        <div class="card-contents">
          <a href="/people/${person["id"]}">
            ${image}
          </a>
          <div class="text">
            <div class="top-card">
              <a href="/people/${person["id"]}">
                <div>${person["name"]}</div>
              </a>
              <div>
                ${followBtn}
              </div>
            </div>
            <div class="bottom-card">
              <div>Known for: ${person["known_for_department"]}</div>
              <div>
                ${KFmovies}
              </div>
            </div>
          </div>
        </div>
      </div>`;
      container.append(personCard);
    }
  }
}
