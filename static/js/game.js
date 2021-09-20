const figures = document.querySelectorAll(".figure")

figures.forEach(f => {
    f.onmousedown = function (event) {
        // только левая кнопка мыши
        if (event.button !== 0) {
            return
        }

        const size = f.getBoundingClientRect().width

        function move(event) {
            f.style.left = event.x - size / 2 + "px"
            f.style.top = event.y - size / 2 + "px"
        }

        function setStyle() {
            f.style.width = size + "px"
            f.style.height = size + "px"
            f.style.position = "absolute"
            f.style.cursor = "grabbing"
        }

        function clearStyle() {
            f.style.position = null
            f.style.width = null
            f.style.height = null
            f.style.cursor = null
            f.style.left = null
            f.style.top = null
        }

        function getSquareFromPoint(event) {
            return document.elementsFromPoint(event.x, event.y).find(sq => {
                return sq.classList.contains("square")
            })
        }

        setStyle()
        move(event)

        /* при быстром перемещении курсор может оказаться вне фигуры,
         поэтому onmousemove применяем к документу */
        document.onmousemove = function (event) {
            move(event)
        }

        f.onmouseup = function (event) {
            document.onmousemove = null

            const square = getSquareFromPoint(event)

            square.appendChild(f)

            clearStyle()
        }
    }
})