window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        update_dropdown: function(data) {
            if (data.length === 0 || data === undefined) {
                return []
            }
            keys = Object.keys(data[0])
            return [
                keys, // row
                keys, // col
                keys, // x
                keys, // y
                keys, // color
            ]
        },
        update_discrete_dropdown: function(option, data) {
            if (data === undefined) {
                return []
            } else if (data.length === 0){
                return []
            } else if (option == null) {
                return []
            } else if (option === undefined) {
                return []
            }
            let unique = [...new Set(data.map((v) => v[option]))].sort()
            return unique
        },
        update_subplot: function(row, col, rowvals, colvals, data) {
            // let nrows = rowvals.length
            // let colvals = colvals.length
            // for (let irow in rowvals) {
            //     console.log(irow)
            // }
        }
    }
});