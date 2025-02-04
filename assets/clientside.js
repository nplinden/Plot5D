window.dash_clientside = Object.assign({}, window.dash_clientside, {
  clientside: {
    update_dropdown: function (data, metadata) {
      if (data.length === 0 || data === undefined) {
        return [];
      }
      keys = Object.keys(data[0]).filter((v) => v !== "_index");
      return [
        [
          {
            group: "Discrete",
            items: metadata["discrete"].map((v) => {
              return { value: v, label: v };
            }),
          },
          {
            group: "Continuous",
            items: metadata["continuous"].map((v) => {
              return { value: v, label: v };
            }),
          },
        ], // row
        [
          {
            group: "Discrete",
            items: metadata["discrete"].map((v) => {
              return { value: v, label: v };
            }),
          },
          {
            group: "Continuous",
            items: metadata["continuous"].map((v) => {
              return { value: v, label: v };
            }),
          },
        ], // col
        keys, // x
        keys, // y
        keys, // color
        keys, // spider
      ];
    },

    updateRowSelect: function (option, data, loaded) {
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

    buildMainplot: function (
      x,
      y,
      color,
      rowname,
      rowvals,
      colname,
      colvals,
      filters,
      aliases,
      data,
      style
    ) {
      console.log(`x=${x}`);
      console.log(`y=${y}`);
      console.log(`color=${color}`);
      console.log(`row_dropdown=${rowname}`);
      console.log(`row_value_dropdown=${rowvals}`);
      console.log(`col_dropdown=${colname}`);
      console.log(`col_value_dropdown=${colvals}`);
      if (x === null || y === null) {
        return window.dash_clientside.no_update;
      }

      const col_b = !!colvals && colvals.length > 0;
      const row_b = !!rowvals && rowvals.length > 0;

      let fig = {};
      candidates = applyFilters(data, filters);
      if (col_b && row_b) {
        if (x && y) {
          console.log("Building 2D Grid Scatter Plots");
          fig = buildScatterSubplot(
            x,
            y,
            color,
            rowname,
            rowvals,
            colname,
            colvals,
            aliases,
            candidates,
            style
          );
        } else {
          console.log("Can't build 2D Scatter Grid, no x and y value provided");
          return window.dash_clientside.no_update;
        }
      } else if (row_b) {
        console.log("Building Row Scatter Plots");
        if (x && y) {
          fig = buildScatterRowsPlot(
            x,
            y,
            color,
            rowname,
            rowvals,
            aliases,
            candidates
          );
        } else {
          console.log(
            "Can't build Row Scatter Plots, no x and y value provided"
          );
          return window.dash_clientside.no_update;
        }
      } else if (col_b) {
        console.log("Can't build Col Scatter Plots, not implemented");
        return window.dash_clientside.no_update;
      } else if (x && y) {
        console.log("Building Simple Scatter Plot");
        fig = buildSingleScatter(x, y, color, aliases, candidates);
      } else {
        return window.dash_clientside.no_update;
      }

      let new_style = { ...style };
      new_style.display = "block";
      return [fig, new_style];
    },

    storeMainplotSelection: function (selected, data) {
      if (!selected) {
        return window.dash_clientside.no_update;
      }
      let idx = selected.points.map((v) => v.customdata);
      let values = idx.map((v) => data[v]);
      return values;
    },

    buildSpider: function (
      selected,
      spider_slct,
      data,
      spider_style,
      affix_style
    ) {
      const spider_b = !!spider_slct && spider_slct.length > 0;
      if (!spider_b) {
        return window.dash_clientside.no_update;
      }

      console.log("Entering buildSpider callback");
      let values;
      if (selected) {
        values = selected;
      } else {
        values = data;
      }

      let dimensions = [];
      for (column of spider_slct) {
        const dim_values = values.map((v) => v[column]);
        dimensions.push({
          label: column,
          values: dim_values,
        });
      }
      const npoints = values.length;

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
      // console.log(JSON.stringify({ ...spider_slct }, null, "\t"));
      let new_spider_style = { ...spider_style };
      new_spider_style.display = "block";
      let new_affix_style = { ...affix_style };
      new_affix_style.display = "block";
      // console.log(
      //   `new_affix_style=${JSON.stringify(new_affix_style, null, "\t")}`
      // );
      return [
        { data: [pardata], layout: layout },
        { ...spider_slct },
        new_spider_style,
        new_affix_style,
      ];
    },

    storeSpiderFilters: function (restyle_data, data) {
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
      return data;
    },

    storeSpiderSelection: function (
      spider_filters_memory,
      spider_slct_memory,
      selected
    ) {
      let values = selected;

      console.log(
        `spider_slct_memory=${JSON.stringify(spider_slct_memory, null, "\t")}`
      );
      values = filterFromSpider(
        spider_filters_memory,
        values,
        spider_slct_memory
      );
      return values;
    },

    DownloadFilteredCsv: function (n_clicks, spiderSelection) {
      if (spiderSelection.length === 0) {
        return window.dash_clientside.no_update;
      }
      console.log(spiderSelection);

      const columns = Object.keys(spiderSelection[0]).filter(
        (v) => v != "_index"
      );
      let csv = columns.join(",") + "\n";
      for (record of spiderSelection) {
        csv += recordToLine(columns, record);
      }
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

const applyFilter = function (data, key, min, max) {
  return data.filter((v) => v[key] > min).filter((v) => v[key] < max);
};

const applyFilters = function (data, filters) {
  // console.log(`filters=${JSON.stringify(filters, null, "\t")}`);
  if (!filters) {
    return data;
  }
  candidates = data;
  for (const [key, value] of Object.entries(filters)) {
    const min = value.min ? value.min : Number.NEGATIVE_INFINITY;
    const max = value.max ? value.max : Number.POSITIVE_INFINITY;
    candidates = applyFilter(candidates, key, min, max);
  }
  return candidates;
};

const COLORSCALE = [
  [0.0, "#1864ab"],
  [0.14285714285714285, "#7065b9"],
  [0.2857142857142857, "#af61b7"],
  [0.42857142857142855, "#e35ea5"],
  [0.5714285714285714, "#ff6587"],
  [0.7142857142857143, "#ff7c63"],
  [0.8571428571428571, "#ff9e3d"],
  [1.0, "#fcc419"],
];

const buildScatterSubplot = function (
  x,
  y,
  color,
  rowname,
  rowvals,
  colname,
  colvals,
  aliases,
  candidates
) {
  let layout = {
    grid: {
      rows: rowvals.length,
      columns: colvals.length,
      pattern: "independent",
      xgap: 0.1,
      ygap: 0.1,
    },
    showlegend: false,
    coloraxis: {
      colorscale: COLORSCALE,
      colorbar: {
        xref: "paper",
        x: 1.07,
        title: aliases[color] || color,
      },
    },
  };

  let plotdata = [];

  rowvals.forEach((row, irow) => {
    const row_candidates = candidates.filter((v) => v[rowname] == row);
    colvals.forEach((col, icol) => {
      const index = irow * colvals.length + icol + 1;
      if (icol == 0) {
        layout[`yaxis${index}`] = {
          title: aliases[y] || y,
        };
      }
      if (irow == rowvals.length - 1) {
        layout[`xaxis${index}`] = {
          title: aliases[x] || x,
        };
      }
      const toplot = row_candidates.filter((v) => v[colname] == col);
      plotdata.push({
        x: toplot.map((v) => v[x]),
        y: toplot.map((v) => v[y]),
        customdata: toplot.map((v) => v["_index"]),
        xaxis: `x${index}`,
        yaxis: `y${index}`,
        mode: "markers",
        marker: {
          color: toplot.map((v) => v[color] || "#c92a2a"),
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
  for (let irow in rowvals) {
    let val;
    if (aliases[rowname]) {
      if (
        aliases[rowname].slice(0, 1) == "$" &&
        aliases[rowname].slice(-1) == "$"
      ) {
        const content = aliases[rowname].slice(1, -1);
        val = `\$\\mathbf{${content}=${rowvals[irow]}}\$`;
      }
    }
    const text = val ? val : `${rowname}=${rowvals[irow]}`;
    annotations.push({
      y: 1 - (2 * irow + 1) / 2 / rowvals.length,
      x: 1.05,
      xref: "paper",
      yref: "paper",
      text: text,
      font: { weight: 700 }, // bold
      textangle: 90,
      xanchor: "center",
      ax: 0,
      ay: 0,
      showarrow: false,
    });
  }
  for (let icol in colvals) {
    let val;
    if (aliases[colname]) {
      if (
        aliases[colname].slice(0, 1) == "$" &&
        aliases[colname].slice(-1) == "$"
      ) {
        const content = aliases[colname].slice(1, -1);
        val = `\$\\mathbf{${content}=${colvals[icol]}}\$`;
      }
    }
    const text = val ? val : `${colname}=${colvals[icol]}`;
    annotations.push({
      x: (2 * icol + 1) / 2 / colvals.length,
      y: 1.05,
      xref: "paper",
      yref: "paper",
      text: text,
      font: { weight: 700 }, // bold
      xanchor: "center",
      ax: 0,
      ay: 0,
      showarrow: false,
    });
  }
  layout["annotations"] = annotations;

  return { data: plotdata, layout: layout };
};

const buildSingleScatter = function (x, y, color, aliases, candidates) {
  let layout = {
    showlegend: false,
    yaxis: {
      title: aliases[y] || y,
    },
    xaxis: {
      title: aliases[x] || x,
    },
    coloraxis: {
      colorscale: COLORSCALE,
      colorbar: {
        xref: "paper",
        x: 1.07,
        title: aliases[color] || color,
      },
    },
  };

  fig = {
    x: candidates.map((v) => v[x]),
    y: candidates.map((v) => v[y]),
    customdata: candidates.map((v) => v["_index"]),
    mode: "markers",
    marker: {
      color: candidates.map((v) => v[color] || "#c92a2a"),
      coloraxis: "coloraxis",
    },
    type: "scattergl",
  };

  layout["title"] = { text: `Number of data points: ${candidates.length}` };
  return { data: fig, layout: layout };
};

const buildScatterRowsPlot = function (
  x,
  y,
  color,
  rowname,
  rowvals,
  aliases,
  candidates
) {
  let layout = {
    grid: {
      rows: rowvals.length,
      columns: 1,
      pattern: "independent",
      xgap: 0.1,
      ygap: 0.1,
    },
    showlegend: false,
    coloraxis: {
      colorscale: COLORSCALE,
      colorbar: {
        xref: "paper",
        x: 1.07,
        title: aliases[color] || color,
      },
    },
  };

  let plotdata = [];

  rowvals.forEach((row, irow) => {
    const toplot = candidates.filter((v) => v[rowname] == row);
    const index = irow + 1;
    if (irow == rowvals.length - 1) {
      layout[`xaxis${index}`] = {
        title: aliases[x] || x,
      };
    }
    plotdata.push({
      x: toplot.map((v) => v[x]),
      y: toplot.map((v) => v[y]),
      customdata: toplot.map((v) => v["_index"]),
      xaxis: `x${index}`,
      yaxis: `y${index}`,
      mode: "markers",
      marker: {
        color: toplot.map((v) => v[color] || "#c92a2a"),
        coloraxis: "coloraxis",
      },
      type: "scattergl",
    });
  });
  let count = plotdata
    .map((v) => v.x.length)
    .reduce((acc, current) => acc + current);
  layout["title"] = { text: `Number of data points: ${count}` };

  let annotations = [];
  for (let irow in rowvals) {
    let val;
    if (aliases[rowname]) {
      if (
        aliases[rowname].slice(0, 1) == "$" &&
        aliases[rowname].slice(-1) == "$"
      ) {
        const content = aliases[rowname].slice(1, -1);
        val = `\$\\mathbf{${content}=${rowvals[irow]}}\$`;
      }
    }
    const text = val ? val : `${rowname}=${rowvals[irow]}`;
    annotations.push({
      y: 1 - (2 * irow + 1) / 2 / rowvals.length,
      x: 1.05,
      xref: "paper",
      yref: "paper",
      text: text,
      font: { weight: 700 }, // bold
      textangle: 90,
      xanchor: "center",
      ax: 0,
      ay: 0,
      showarrow: false,
    });
  }
  layout["annotations"] = annotations;

  return { data: plotdata, layout: layout };
};

// built in Math.max fails on very big arrays
function getMax(arr) {
  let len = arr.length;
  let max = -Infinity;

  while (len--) {
    max = arr[len] > max ? arr[len] : max;
  }
  return max;
}

function getMin(arr) {
  let len = arr.length;
  let min = +Infinity;

  while (len--) {
    max = arr[len] < min ? arr[len] : min;
  }
  return max;
}

const inDisjointed = function (value, disjointed) {
  for (interval of disjointed) {
    if (value < interval[1] && value > interval[0]) {
      return true;
    }
  }
  return false;
};

const filterFromSpider = function (filters, arr, idtoColumn) {
  let bools = new Array(arr.length).fill(true);
  outer: for (const iobj in arr) {
    for (const [key, value] of Object.entries(filters)) {
      if (!inDisjointed(arr[iobj][idtoColumn[key]], value)) {
        bools[iobj] = false;
        continue outer;
      }
    }
  }
  return arr.filter((_, i) => bools[i]);
};
