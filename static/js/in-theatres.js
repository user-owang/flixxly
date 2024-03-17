const $nowShowing = $(".now-showing-movies");
let page = 1;
let totalPages;

async function nowShowingList() {
  const response = await axios.post("/api/now-showing", {
    page: page,
  });
  console.log(response);
  return response;
}

async function getITTotalPages() {
  let test = await nowShowingList();
  totalPages = test["data"]["total_pages"];
  console.log(totalPages);
}

getITTotalPages();

async function nowShowingScrollHandler() {
  if (page < totalPages) {
    page += 1;
    response = await nowShowingList();
    buildMovieCard(
      response,
      $nowShowing,
      true,
      "https://media.themoviedb.org/t/p/w220_and_h330_face"
    );
    console.log("built new page");
  } else {
    return;
  }
}

create_autoscroll($nowShowing, nowShowingScrollHandler);
