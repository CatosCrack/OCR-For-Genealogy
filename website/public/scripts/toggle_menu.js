var searchIcon = document.getElementById("search_icon");
var searchArea = document.getElementsByClassName("mobile_search_area")[0];
var toggle = false;

searchIcon.addEventListener("click", function() {
    // Toggle on and off the visibility of the search area
    toggle = !toggle;

    if (toggle) {
        searchArea.classList.toggle("active");
        searchIcon.src = "images/close_icon.svg";
    } else {
        searchArea.classList.toggle("active");
        searchIcon.src = "images/search_icon.svg";
    }
});