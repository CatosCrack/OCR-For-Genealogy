document.addEventListener("DOMContentLoaded", function() {
    var returnButton = document.getElementById("return_button");
    returnButton.addEventListener("click", function(){
        console.log("Return button clicked");
        window.history.back();
    });
});