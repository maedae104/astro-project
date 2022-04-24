
const radio = document.querySelector("text-updates")
radio.addEventListener('click', function () {
    if (radio.checked) {
        console.log("text update requested")
    } else {
        console.log("no text update");
    }
});