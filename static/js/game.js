function dragstartHandler(event) {
    event.dataTransfer.setData("text", event.target.parentElement.id)
}

function dragoverHandler(event) {
    event.preventDefault()
    event.dataTransfer.dropEffect = "move"
}

function dropHandler(event) {
    event.preventDefault()
    const squareId = event.dataTransfer.getData("text")
    const figure = document.getElementById(squareId).firstElementChild
    event.target.appendChild(figure)
}
