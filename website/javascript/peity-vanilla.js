/*!
  Peity Vanila JS 0.0.8
  Copyright © 2022 RailsJazz
  https://railsjazz.com
 */

(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
  typeof define === 'function' && define.amd ? define(factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.peity = factory());
})(this, (function () { 'use strict';

  const isFunction = (o) =>
    o !== null && typeof o === "function" && !!o.apply;

  const svgElement = (tag, attrs) => {
    const element = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (var attr in attrs) {
      element.setAttribute(attr, attrs[attr]);
    }
    return element;
  };

  const svgSupported =
    "createElementNS" in document && svgElement("svg", {}).createSVGRect();

  class Peity {
    static defaults = {};
    static graphers = {};

    constructor(element, type, options = {}) {
      this.element = element;
      this.type = type;
      this.options = Object.assign(
        {},
        Peity.defaults[this.type],
        JSON.parse(element.dataset["peity"] || "{}"),
        options
      );

      if(this.element._peity) {
        this.element._peity.destroy();
      }
      this.element._peity = this;
    }

    draw() {
      const options = this.options;
      Peity.graphers[this.type](this);
      if (isFunction(options.after)) options.after.call(this, options);
    }

    fill() {
      var fill = this.options.fill;

      return isFunction(fill)
        ? fill
        : function (_, i) {
            return fill[i % fill.length];
          };
    }

    prepare(width, height) {
      if (!this.svg) {
        this.element.style.display = "none";
        this.element.after(
          (this.svg = svgElement("svg", {
            class: "peity",
          }))
        );
      }

      this.svg.innerHTML = "";
      this.svg.setAttribute("width", width);
      this.svg.setAttribute("height", height);

      return this.svg;
    }

    get values() {
      return this.element.innerText
        .split(this.options.delimiter)
        .map((value) => parseFloat(value));
    }

    mount() {
      if (!svgSupported) return;

      this.element.addEventListener("DOMSubtreeModified", this.draw.bind(this));
      this.draw();

      this.mounted = true;
    }

    unmount() {
      this.element.removeEventListener("DOMSubtreeModified", this.draw);
      this.svg.remove();
      this.mounted = false;
    }

    destroy() {
      this.unmount();

      delete this.element._peity;
    }

    static register(type, defaults, grapher) {
      Peity.defaults[type] = defaults;
      Peity.graphers[type] = grapher;
    }
  }

  const renderer$2 = (peity) => {
    if (!peity.options.delimiter) {
      const delimiter = peity.element.innerText.match(/[^0-9\.]/);
      peity.options.delimiter = delimiter ? delimiter[0] : ",";
    }

    let values = peity.values.map((n) => (n > 0 ? n : 0));

    if (peity.options.delimiter == "/") {
      let v1 = values[0];
      let v2 = values[1];
      values = [v1, Math.max(0, v2 - v1)];
    }

    let i = 0;
    let length = values.length;
    let sum = 0;

    for (; i < length; i++) {
      sum += values[i];
    }

    if (!sum) {
      length = 2;
      sum = 1;
      values = [0, 1];
    }

    let diameter = peity.options.radius * 2;

    const svg = peity.prepare(
      peity.options.width || diameter,
      peity.options.height || diameter
    );

    const width = svg.clientWidth;
    const height = svg.clientHeight;
    const cx = width / 2;
    const cy = height / 2;

    const radius = Math.min(cx, cy);
    let innerRadius = peity.options.innerRadius;

    if (peity.type == "donut" && !innerRadius) {
      innerRadius = radius * 0.5;
    }

    const fill = peity.fill();

    const scale = (value, radius) => {
      const radians = (value / sum) * Math.PI * 2 - Math.PI / 2;

      return [radius * Math.cos(radians) + cx, radius * Math.sin(radians) + cy];
    };

    let cumulative = 0;

    for (i = 0; i < length; i++) {
      const value = values[i];
      const portion = value / sum;
      let node;

      if (portion == 0) continue;

      if (portion == 1) {
        if (innerRadius) {
          const x2 = cx - 0.01;
          const y1 = cy - radius;
          const y2 = cy - innerRadius;

          node = svgElement("path", {
            d: [
              "M",
              cx,
              y1,
              "A",
              radius,
              radius,
              0,
              1,
              1,
              x2,
              y1,
              "L",
              x2,
              y2,
              "A",
              innerRadius,
              innerRadius,
              0,
              1,
              0,
              cx,
              y2,
            ].join(" "),
            "data-value": value,
          });
        } else {
          node = svgElement("circle", {
            cx: cx,
            cy: cy,
            "data-value": value,
            r: radius,
          });
        }
      } else {
        const cumulativePlusValue = cumulative + value;

        let d = ["M"].concat(
          scale(cumulative, radius),
          "A",
          radius,
          radius,
          0,
          portion > 0.5 ? 1 : 0,
          1,
          scale(cumulativePlusValue, radius),
          "L"
        );

        if (innerRadius) {
          d = d.concat(
            scale(cumulativePlusValue, innerRadius),
            "A",
            innerRadius,
            innerRadius,
            0,
            portion > 0.5 ? 1 : 0,
            0,
            scale(cumulative, innerRadius)
          );
        } else {
          d.push(cx, cy);
        }

        cumulative += value;

        node = svgElement("path", {
          d: d.join(" "),
          "data-value": value,
        });
      }

      node.setAttribute("fill", fill.call(peity, value, i, values));

      svg.append(node);
    }
  };

  const defaults$2 = {
    fill: ["#ff9900", "#fff4dd", "#ffc66e"],
    radius: 8,
  };

  const renderer$1 = (peity) => {
    const values = peity.values;
    const max = Math.max.apply(
      Math,
      peity.options.max == undefined ? values : values.concat(peity.options.max)
    );
    const min = Math.min.apply(
      Math,
      peity.options.min == undefined ? values : values.concat(peity.options.min)
    );

    const svg = peity.prepare(peity.options.width, peity.options.height);
    const width = svg.clientWidth;
    const height = svg.clientHeight;
    const diff = max - min;
    const padding = peity.options.padding;
    const fill = peity.fill();

    const xScale = (input) => {
      return (input * width) / values.length;
    };

    const yScale = (input) => {
      return height - (diff ? ((input - min) / diff) * height : 1);
    };

    for (var i = 0; i < values.length; i++) {
      let x = xScale(i + padding);
      let w = xScale(i + 1 - padding) - x;
      let value = values[i];
      let valueY = yScale(value);
      let y1 = valueY;
      let y2 = valueY;
      let h;

      if (!diff) {
        h = 1;
      } else if (value < 0) {
        y1 = yScale(Math.min(max, 0));
      } else {
        y2 = yScale(Math.max(min, 0));
      }

      h = y2 - y1;

      if (h == 0) {
        h = 1;
        if (max > 0 && diff) y1--;
      }

      svg.append(
        svgElement("rect", {
          "data-value": value,
          fill: fill.call(peity, value, i, values),
          x: x,
          y: y1,
          width: w,
          height: h,
        })
      );
    }
  };

  const defaults$1 = {
    delimiter: ",",
    fill: ["#4D89F9"],
    height: 16,
    min: 0,
    padding: 0.1,
    width: 32,
  };

  const renderer = (peity) => {
    const values = peity.values;
    if (values.length == 1) values.push(values[0]);
    const max = Math.max.apply(
      Math,
      peity.options.max == undefined ? values : values.concat(peity.options.max)
    );
    const min = Math.min.apply(
      Math,
      peity.options.min == undefined ? values : values.concat(peity.options.min)
    );

    const svg = peity.prepare(peity.options.width, peity.options.height);
    const strokeWidth = peity.options.strokeWidth;
    const width = svg.clientWidth;
    const height = svg.clientHeight - strokeWidth;
    const diff = max - min;

    const xScale = (input) => {
      return input * (width / (values.length - 1));
    };

    const yScale = (input) => {
      let y = height;

      if (diff) {
        y -= ((input - min) / diff) * height;
      }

      return y + strokeWidth / 2;
    };

    let zero = yScale(Math.max(min, 0));
    let coords = [0, zero];

    for (var i = 0; i < values.length; i++) {
      coords.push(xScale(i), yScale(values[i]));
    }

    coords.push(width, zero);

    if (peity.options.fill) {
      svg.append(
        svgElement("polygon", {
          fill: peity.options.fill,
          points: coords.join(" "),
        })
      );
    }

    if (strokeWidth) {
      svg.append(
        svgElement("polyline", {
          fill: "none",
          points: coords.slice(2, coords.length - 2).join(" "),
          stroke: peity.options.stroke,
          "stroke-width": strokeWidth,
          "stroke-linecap": "square",
        })
      );
    }
  };

  const defaults = {
    delimiter: ",",
    fill: "#c6d9fd",
    height: 16,
    min: 0,
    stroke: "#4d89f9",
    strokeWidth: 1,
    width: 32,
  };

  Peity.register("pie", defaults$2, renderer$2);
  Peity.register("donut", defaults$2, renderer$2);
  Peity.register("bar", defaults$1, renderer$1);
  Peity.register("line", defaults, renderer);

  const peity = function (element, type, options) {
    const peity = new Peity(element, type, options);
    peity.mount();

    return peity;
  };

  peity.defaults = Peity.defaults;
  peity.graphers = Peity.graphers;

  return peity;

}));
//# sourceMappingURL=peity-vanilla.js.map
