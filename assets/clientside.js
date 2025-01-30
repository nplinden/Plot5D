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
        keys, // spider
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
      filters,
      aliases,
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
      console.log(`filters=${JSON.stringify(filters, null, "	")}`);
      if (x === null || y === null) {
        return window.dash_clientside.no_update;
      }
      if (row_dropdown == null || col_dropdown == null) {
        return window.dash_clientside.no_update;
      }
      if (row_val_dropdown == undefined || col_val_dropdown == undefined) {
        return window.dash_clientside.no_update;
      }

      let candidates = data;
      // Applying the filters
      if (filters !== undefined) {
        for (const [key, value] of Object.entries(filters)) {
          const min = value.min ? value.min : Number.NEGATIVE_INFINITY;
          const max = value.max ? value.max : Number.POSITIVE_INFINITY;
          candidates = candidates
            .filter((v) => v[key] > min)
            .filter((v) => v[key] < max);
        }
      }

      let layout = {
        grid: {
          rows: row_val_dropdown.length,
          columns: col_val_dropdown.length,
          pattern: "independent",
          xgap: 0.1,
          ygap: 0.1,
        },
        showlegend: false,
        coloraxis: {
          colorscale: [
            [0.0, "#1864ab"],
            [0.14285714285714285, "#7065b9"],
            [0.2857142857142857, "#af61b7"],
            [0.42857142857142855, "#e35ea5"],
            [0.5714285714285714, "#ff6587"],
            [0.7142857142857143, "#ff7c63"],
            [0.8571428571428571, "#ff9e3d"],
            [1.0, "#fcc419"],
          ],
          colorbar: {
            xref: "paper",
            x: 1.07,
            title: aliases[color] || color,
          },
        },
      };

      let plotdata = [];
      let indexArray = new Array(row_val_dropdown.length)
        .fill(0)
        .map(() => new Array(col_val_dropdown.length).fill(0));
      row_val_dropdown.forEach((row, irow) => {
        const row_candidates = candidates.filter((v) => v[row_dropdown] == row);

        col_val_dropdown.forEach((col, icol) => {
          const index = irow * col_val_dropdown.length + icol + 1;
          indexArray[irow][icol] = index;
          if (icol == 0) {
            layout[`yaxis${index}`] = {
              title: aliases[y] || y,
            };
          }
          if (irow == row_val_dropdown.length - 1) {
            layout[`xaxis${index}`] = {
              title: aliases[x] || x,
            };
          }
          const toplot = row_candidates.filter((v) => v[col_dropdown] == col);
          plotdata.push({
            x: toplot.map((v) => v[x]),
            y: toplot.map((v) => v[y]),
            customdata: toplot.map((v) => v["_index"]),
            xaxis: `x${index}`,
            yaxis: `y${index}`,
            mode: "markers",
            marker: {
              color: toplot.map((v) => v[color] || "#e8590c"),
              coloraxis: "coloraxis",
            },
            type: "scattergl",
          });
        });
      });

      let count = plotdata
        .map((v) => v.x.length)
        .reduce((acc, current) => acc + current);
      layout["title"] = { text: `Number of data points: ${count}` };

      let annotations = [];
      console.log(row_dropdown);
      for (let irow in row_val_dropdown) {
        annotations.push({
          y: 1 - (2 * irow + 1) / 2 / row_val_dropdown.length,
          x: 1.05,
          xref: "paper",
          yref: "paper",
          text: `${aliases[row_dropdown] || row_dropdown}=${
            row_val_dropdown[irow]
          }`,
          font: { weight: 700 }, // bold
          textangle: 90,
          xanchor: "center",
          ax: 0,
          ay: 0,
          showarrow: false,
        });
      }
      for (let icol in col_val_dropdown) {
        annotations.push({
          x: (2 * icol + 1) / 2 / col_val_dropdown.length,
          y: 1.05,
          xref: "paper",
          yref: "paper",
          text: `${aliases[col_dropdown] || col_dropdown}=${
            col_val_dropdown[icol]
          }`,
          font: { weight: 700 }, // bold
          xanchor: "center",
          ax: 0,
          ay: 0,
          showarrow: false,
        });
      }
      layout["annotations"] = annotations;

      let new_style = { ...style };
      new_style.display = "block";
      console.log(new_style);
      return [{ data: plotdata, layout: layout }, new_style];
    },

    build_spider: function (
      selected,
      spider_slct,
      data,
      spider_style,
      affix_style
    ) {
      console.log("Entering build_spider callback");
      if (!selected) {
        return window.dash_clientside.no_update;
      }
      let idx = selected.points.map((v) => v.customdata);
      let values = idx.map((v) => data[v]);

      if (!spider_slct) {
        return window.dash_clientside.no_update;
      }
      let dimensions = [];
      for (column of spider_slct) {
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
      console.log(JSON.stringify({ ...spider_slct }, null, "\t"));
      let new_spider_style = { ...spider_style };
      new_spider_style.display = "block";
      let new_affix_style = { ...affix_style };
      new_affix_style.display = "block";
      console.log(
        `new_affix_style=${JSON.stringify(new_affix_style, null, "\t")}`
      );
      return [
        { data: [pardata], layout: layout },
        { ...spider_slct },
        new_spider_style,
        new_affix_style,
      ];
    },

    store_spider_filters: function (restyle_data, data) {
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

    download_filtered_csv: function (
      n_clicks,
      spider_slct_memory,
      spider_filters_memory,
      selected,
      data
    ) {
      // Applying 5DPlot selection to the data
      let idx = selected.points.map((v) => v.customdata);
      let values = idx.map((v) => data[v]);

      // Applying spider graph range filters to the data
      if (
        spider_filters_memory !== undefined &&
        spider_slct_memory !== undefined
      ) {
        for (const [col_idx, ranges] of Object.entries(spider_filters_memory)) {
          col_name = spider_slct_memory[col_idx];
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
      }

      if (values.length === 0) {
        return window.dash_clientside.no_update;
      }

      const columns = Object.keys(values[0]).filter((v) => v != "_index");
      let csv = columns.join(",") + "\n";
      for (record of values) {
        csv += recordToLine(columns, record);
      }
      console.log(`${csv}`);
      return {
        content: csv,
        filename: "selection.csv",
      };
    },
  },
});

const recordToLine = function (columns, record) {
  let line = "";
  for (col of columns) {
    line += `${record[col]},`;
  }
  return line.slice(0, -1) + "\n";
};
