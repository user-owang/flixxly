$(function () {
  const guess = $("#guess");
  const searchResults = $(".search-results");
  const playArea = $(".play-area");

  async function startGame() {
    response = await axios.get("/api/game_setup");
    actors = response.data;
    newNode = document.createElement("ul");
    newNode.innerHTML = `<li><img src="${actors["actor1"]["img_url"]}" alt="">${actors["actor1"]["name"]} <ul class="actor${actors["actor1"]["id"]}"></ul></li>`;
    secondLI = document.createElement("li");
    secondLI.innerHTML = `<img src="${actors["actor2"]["img_url"]}" alt="">${actors["actor2"]["name"]}`;
    secondLI.classList.add(actors["actor2"]["id"]);
    newNode.append(secondLI);
    playArea.append(newNode);
  }

  // function addMovie(movie) {}

  // async function checkIfValid(target) {
  //   if (target.classList.contains("movie")) {
  //     const response = await axios.post("/api/get_movie", { id: target.id });
  //     const movie = response.data;
  //   } else if (target.classList.contains("person")) {
  //     const response = await axios.post("/api/get_actor", { id: target.id });
  //     const actor = response.data;
  //   }
  // }

  // searchResults.on("click", "li", async function (evt) {
  //   await checkIfValid(evt.target);
  //   searchResults.empty()
  // });

  async function ShowSearchResults() {
    const response = await axios.post("/api/search", { term: guess.val() });
    const search = response.data;
    for (const result of search["results"]) {
      const newResult = document.createElement("li");
      newResult.id = result["id"];
      newResult.classList.add(result["media_type"]);
      if (result["media_type"] === "movie") {
        newResult.innerHTML = `<span><img src="${result["img_url"]}" alt=""></span><span>${result.title}</span>`;
      } else if (result["media_type"] === "person") {
        newResult.innerHTML = `<span><img src="${result["img_url"]}" alt=""></span><span>${result.name}</span>`;
      }
      searchResults.append(newResult);
    }
  }

  async function SearchHandler() {
    console.log("handler");
    await ShowSearchResults();
    guess.val("");
  }

  $("#search-bar").submit(async function (evt) {
    evt.preventDefault();
    await SearchHandler();
  });
  startGame();
});
