
const aspect_btn = document.querySelector("#view-more")

const eclipse_div = document.getElementById("eclipse-id")


aspect_btn.addEventListener('click', evt => {
        console.log(evt.target)
        console.log(eclipse_div)
        eclipse_div.style.display = 'block'
        });

const sunscribe_btn = document.getElementById("text-button")

sunscribe_btn.onclick = (evt) => {
        console.log("subscribe for updates")
        //fetch request to user-profile
        fetch('/login')
        .then(response => response.text())
        .then(serverData => serverData.text())
}
