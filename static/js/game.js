function getSquareFromPoint(x, y) {
    return document.elementsFromPoint(x, y).find(square => {
        return square.classList.contains("square")
    })
}

function move(obj, x, y) {
    const objSize = obj.getBoundingClientRect().width
    const board = document.querySelector(".board")
    const boardRect = board.getBoundingClientRect()

    let objLeft = x - objSize / 2
    let objTop = y - objSize / 2

    if (objLeft < boardRect.left) objLeft = boardRect.left
    else if (objLeft + objSize > boardRect.right) objLeft = boardRect.right - objSize

    if (objTop < boardRect.top) objTop = boardRect.top
    else if (objTop + objSize > boardRect.bottom) objTop = boardRect.bottom - objSize

    obj.style.left = objLeft + "px"
    obj.style.top = objTop + "px"
}

function setDraggingStyle(obj) {
    const objSize = obj.getBoundingClientRect().width
    obj.style.width = objSize + "px"
    obj.style.height = objSize + "px"
    obj.style.position = "absolute"
    obj.style.cursor = "grabbing"
}

function clearDraggingStyle(obj) {
    obj.style.position = null
    obj.style.width = null
    obj.style.height = null
    obj.style.cursor = null
    obj.style.left = null
    obj.style.top = null
}


const socket = io()

socket.on("success", function (data) {
    const figure = document.querySelector(`[data-id="${data["from"]}"]`)
    const destSquare = document.getElementById(data["to"])

    destSquare.appendChild(figure)
    figure.dataset.id = destSquare.id
    clearDraggingStyle(figure)
})

socket.on("fail", function (data) {
    const figure = document.querySelector(`[data-id="${data["from"]}"]`)
    clearDraggingStyle(figure)
})

const figures = document.querySelectorAll(".figure")

figures.forEach(figure => {
    figure.onmousedown = function (event) {
        // только левая кнопка мыши
        if (event.button !== 0) {
            return
        }

        setDraggingStyle(figure)
        move(figure, event.x, event.y)

        /* при быстром перемещении курсор может оказаться вне фигуры,
         поэтому onmousemove применяем к документу */
        document.onmousemove = function (event) {
            move(figure, event.x, event.y)
        }

        figure.onmouseup = function (event) {
            document.onmousemove = null

            const destSquare = getSquareFromPoint(event.x, event.y)

            socket.emit("move", {from: figure.dataset.id, to: destSquare.id})
        }
    }
})