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
