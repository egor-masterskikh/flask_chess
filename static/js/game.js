Draggable.create(".figure", {
    bounds: ".board",
    zIndexBoost: false,
    onDragStart: function (e) {
        // TODO: разместить фигуру так, чтобы курсор оказался в её центре
    },
    onDragEnd: function () {
        let figure = $(this.target)
        let figureSize = figure.width() // or figure.height()

        let figureLeft = figure.position().left
        let figureTop = figure.position().top

        let figureLeft1 = Math.round(figureLeft / figureSize) * figureSize
        let figureTop1 = Math.round(figureTop / figureSize) * figureSize

        let figureXOffset = figureLeft1 - figureLeft
        let figureYOffset = figureTop1 - figureTop

        let [, translateX, translateY] = this.target.style.transform.match(/^translate3d\((-?\d+)px, (-?\d+)px, 0px\)$/)
        translateX = Number(translateX)
        translateY = Number(translateY)

        let translateX1 = translateX + figureXOffset
        let translateY1 = translateY + figureYOffset

        figure.css("transform", `translate3d(${translateX1}px, ${translateY1}px, 0px)`)
    }
})