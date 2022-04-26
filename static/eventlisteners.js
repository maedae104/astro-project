const btn = document.querySelector("button")

btn.onclick = (evt) => {
        console.log("subscribe for updates")
        //fetch request to user-profile
        fetch('/user-profile')
        .then(response => response.text())
        .then(serverData => serverData.text())
}

