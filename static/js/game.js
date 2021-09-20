const figures = document.querySelectorAll(".figure")

figures.forEach(f => {
    f.onmousedown = function (event) {
        if (event.button !== 0) {
            return
        }

        function move(event) {
            f.style.left = event.x - size / 2 + "px"
            f.style.top = event.y - size / 2 + "px"
        }

        const size = f.getBoundingClientRect().width

        f.style.width = size + "px"
        f.style.height = size + "px"
        f.style.position = "absolute"
        f.style.cursor = "grabbing"

        document.body.appendChild(f)

        move(event)

        document.onmousemove = function (event) {
            move(event)
        }

        f.onmouseup = function (event) {
            document.onmousemove = null

            const square = document.elementsFromPoint(event.x, event.y).find(sq => {
                return sq.classList.contains("square")
            })

            square.appendChild(f)

            f.style.position = null
            f.style.width = null
            f.style.height = null
            f.style.cursor = null
            f.style.left = null
            f.style.top = null
        }
    }
})