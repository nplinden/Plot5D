window.dash_clientside = Object.assign({}, window.dash_clientside, {
  clientside: {
    loading_overlay: function (filename) {
      return true;
    },
    update_dropdown: function (data) {
      if (data.length === 0 || data === undefined) {
        return [];
      }
      keys = Object.keys(data[0]);
      return [
        keys, // row
        keys, // col
        keys, // x
        keys, // y
        keys, // color
        keys, // parcoord
        keys, // table
      ];
    },
    update_row_dropdown: function (option, data, loaded) {
      let value = [];
      if (loaded !== undefined) {
        const content = JSON.parse(atob(loaded.split(",")[1]));
        value = content.row_val_dropdown ?? value;
      }
      if (data === undefined) {
        return [];
      } else if (data.length === 0) {
        return [];
      } else if (option == null) {
        return [];
      } else if (option === undefined) {
        return [];
      }
      const unique = [...new Set(data.map((v) => v[option]))]
        .sort()
        .map((v) => {
          return { value: "" + v, label: "" + v };
        });
      console.log(unique);
      return [unique, value];
    },

    update_col_dropdown: function (option, data, loaded) {
      let value = [];
      if (loaded !== undefined) {
        const content = JSON.parse(atob(loaded.split(",")[1]));
        value = content.col_val_dropdown ?? value;
      }
      if (data === undefined) {
        return [];
      } else if (data.length === 0) {
        return [];
      } else if (option == null) {
        return [];
      } else if (option === undefined) {
        return [];
      }
      const unique = [...new Set(data.map((v) => v[option]))]
        .sort()
        .map((v) => {
          return { value: "" + v, label: "" + v };
        });
      return [unique, value];
    },

    update_subplot: function (
      x,
      y,
      color,
      row_dropdown,
      row_val_dropdown,
      col_dropdown,
      col_val_dropdown,
      x_min,
      x_max,
      y_min,
      y_max,
      color_min,
      color_max,
      data,
      style
    ) {
      console.log(`x=${x}`);
      console.log(`y=${y}`);
      console.log(`color=${color}`);
      console.log(`row_dropdown=${row_dropdown}`);
      console.log(`row_value_dropdown=${row_val_dropdown}`);
      console.log(`col_dropdown=${col_dropdown}`);
      console.log(`col_value_dropdown=${col_val_dropdown}`);
      if (x === null || y === null) {
        return window.dash_clientside.no_update;
      }
      if (row_dropdown == null || col_dropdown == null) {
        return window.dash_clientside.no_update;
      }
      if (row_val_dropdown == undefined || col_val_dropdown == undefined) {
        return window.dash_clientside.no_update;
      }

      x_min = x_min ? x_min : Number.NEGATIVE_INFINITY;
      x_max = x_max ? x_max : Number.POSITIVE_INFINITY;
      y_min = y_min ? y_min : Number.NEGATIVE_INFINITY;
      y_max = y_max ? y_max : Number.POSITIVE_INFINITY;
      color_min = color_min ? color_min : Number.NEGATIVE_INFINITY;
      color_max = color_max ? color_max : Number.POSITIVE_INFINITY;

      let candidates = data
        .filter((v) => v[x] > x_min)
        .filter((v) => v[x] < x_max)
        .filter((v) => v[y] > y_min)
        .filter((v) => v[y] < y_max);
      if (color !== null) {
        candidates = candidates
          .filter((v) => v[color] > color_min)
          .filter((v) => v[color] < color_max);
      }

      let plotdata = [];
      row_val_dropdown.forEach((row, irow) => {
        const row_candidates = candidates.filter((v) => v[row_dropdown] == row);

        col_val_dropdown.forEach((col, icol) => {
          const index = irow * col_val_dropdown.length + icol + 1;
          const toplot = row_candidates.filter((v) => v[col_dropdown] == col);
          plotdata.push({
            x: toplot.map((v) => v[x]),
            y: toplot.map((v) => v[y]),
            customdata: toplot.map((v) => v["index"]),
            xaxis: `x${index}`,
            yaxis: `y${index}`,
            mode: "markers",
            marker: {
              color: toplot.map((v) => v[color] || "#e8590c"),
            },
            type: "scattergl",
          });
        });
      });

      let count = plotdata
        .map((v) => v.x.length)
        .reduce((acc, current) => acc + current);

      let layout = {
        title: {
          text: `Number of data points: ${count}`,
        },
        // template: "plotly_dark",
        grid: {
          rows: row_val_dropdown.length,
          columns: col_val_dropdown.length,
          pattern: "independent",
          xgap: 0.1,
          ygap: 0.1,
        },
        showlegend: false,
      };
      let new_style = { ...style };
      new_style.display = "block";
      console.log(new_style);
      return [{ data: plotdata, layout: layout }, new_style];
    },

    select_data_for_parcoord: function (
      selected,
      parcoord_dropdown,
      data,
      style
    ) {
      console.log("Entering select_data_for_parcoord callback");
      if (!selected) {
        return window.dash_clientside.no_update;
      }
      let idx = selected.points.map((v) => v.customdata);
      let values = idx.map((v) => data[v]);

      if (!parcoord_dropdown) {
        return window.dash_clientside.no_update;
      }
      let dimensions = [];
      for (column of parcoord_dropdown) {
        const dim_values = values.map((v) => v[column]);
        dimensions.push({
          range: [Math.min(...dim_values), Math.max(...dim_values)],
          label: column,
          values: dim_values,
        });
      }
      const npoints = idx.length;

      const pardata = {
        type: "parcoords",
        line: {
          color: "#ff922b",
        },
        dimensions: dimensions,
      };

      let layout = {
        title: {
          text: `Number of data points: ${npoints}`,
        },
      };
      console.log(
        JSON.stringify({ data: [pardata], layout: layout }, null, "\t")
      );
      console.log(JSON.stringify({ ...parcoord_dropdown }, null, "\t"));
      let new_style = { ...style };
      new_style.display = "block";
      console.log(new_style);
      console.log(style);
      return [
        { data: [pardata], layout: layout },
        { ...parcoord_dropdown },
        new_style,
      ];
    },

    store_parcoord_style: function (restyle_data, data) {
      if (!restyle_data) {
        return window.dash_clientside.no_update;
      }
      if (!data) {
        data = {};
      }
      const key = Object.keys(restyle_data[0])[0];
      const idim = parseInt(
        key.replace("dimensions[", "").replace("].constraintrange", "")
      );
      if (!restyle_data[0][key]) {
        return window.dash_clientside.no_update;
      }
      let ranges = restyle_data[0][key][0];
      if (ranges === null) {
        delete data[idim];
      } else {
        if (!Array.isArray(ranges[0])) {
          ranges = [ranges];
        }
        data[idim] = ranges;
      }
      console.log(ranges);
      return data;
    },

    draw_table: function (
      parcoords_dropdown_memory,
      parcoords_memory,
      page_current,
      table_dropdown,
      selected,
      page_size,
      data
    ) {
      if (parcoords_memory === undefined) {
        return window.dash_clientside.no_update;
      }
      if (parcoords_dropdown_memory === undefined) {
        return window.dash_clientside.no_update;
      }
      if (!selected) {
        return window.dash_clientside.no_update;
      }
      if (table_dropdown === undefined) {
        return window.dash_clientside.no_update;
      }

      let idx = selected.points.map((v) => v.customdata);
      let values = idx.map((v) => data[v]);

      // Applying spider graph range filters
      for (const [col_idx, ranges] of Object.entries(parcoords_memory)) {
        col_name = parcoords_dropdown_memory[col_idx];
        queries = [];
        values = values.filter((v) => {
          let ok = false;
          for (const r of ranges) {
            const val = v[col_name];

            if (val < r[1] && val > r[0]) {
              ok = true;
            }
          }
          return ok;
        });
      }
      values = values.map((v) => {
        let obj = {};
        for (const col of table_dropdown) {
          obj[col] = v[col];
        }
        return obj;
      });

      if (values.length === 0) {
        return window.dash_clientside.no_update;
      }

      let page_count = Math.floor(values.length / page_size) + 1;
      if (values.length % page_size == 0) {
        page_count--;
      }
      values = values.slice(
        page_current * page_size,
        (page_current + 1) * page_size
      );

      let columns = Object.keys(values[0]).map((v) => {
        return { name: v, id: v };
      });
      return [values, columns, page_count];
    },
  },
});
