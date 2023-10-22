<svelte:options accessors={true} />

<script>
  import { onMount, onDestroy } from "svelte";
  import * as d3 from "d3";
  import PopupBox from "./PopupBox.svelte";

  let scatterSVG;

  let data = [
    {
      date: new Date(2018, 1, 1),
      title: "Event 1",
      content: "Description for event 1",
    },
    {
      date: new Date(1400, 6, 1),
      title: "Event 2",
      content: "Description for event 2",
    },
    {
      date: new Date(2018, 9, 2),
      title: "Event 3",
      content: "Description for event 3",
    },
  ];

  onMount(() => {
    let width = 1300;
    let height = 100;
    let margin = { top: 40, right: 60, bottom: 40, left: 60 };
    var circles = [];

    const svg = d3
      .select(scatterSVG)
      .attr("width", width)
      .attr("height", height);

    const xScale = d3
      .scaleTime()
      .domain(d3.extent(data, (d) => d.date))
      .range([margin.left, width - margin.right])
      .nice();

    circles = svg
      .append("g")
      .selectAll("dot")
      .data(data)
      .enter()
      .append("circle");

    circles
      .attr("cx", (d) => xScale(d.date))
      .attr("cy", height / 2)
      .attr("r", 6)
      .on("mouseover", function (d, i) {
        d3.select(this)
          .transition()
          .duration(100)
          .attr("r", 10)
          .attr("fill", "#ff0000");
      })
      .on("mouseout", function (d, i) {
        d3.select(this)
          .transition()
          .duration(100)
          .attr("r", 6)
          .attr("fill", "#000000");
      })
      .on("click", function (event, d) {
        const point = this;
        const pointRect = point.getBoundingClientRect();
        const popupWidth = 200; // Adjust this width as needed

        const buttonPosition = {
          top: pointRect.bottom + window.scrollY + 10 + "px", // Adjust the top offset as needed
          left:
            pointRect.left +
            window.scrollX -
            popupWidth / 2 +
            pointRect.width / 2 +
            "px",
        };

        d.showInfo = !d.showInfo;
        d.buttonPosition = buttonPosition;
        data = data;
      });

    svg
      .append("g")
      .attr("transform", "translate(0," + (height - 40) + ")")
      .style("color", "black")
      .call(d3.axisBottom(xScale).ticks(width / 80));
  });
</script>

<div class="scatterPlot">
  <svg bind:this={scatterSVG} />
  {#each data as event}
    {#if event.showInfo}
      <PopupBox
        title={event.title}
        content={event.content}
        position={event.buttonPosition}
      />
    {/if}
  {/each}
</div>

<style>
  .scatterPlot {
    font-size: 1.5em;
  }
</style>
