<script>
  import Timeline from "./lib/Timeline.svelte";
  import Sidebar from "./lib/Sidebar.svelte";

  let showTimelineOne = false;
  let showTimelineTwo = false;
let showTimelineThree = false;
var timelineCount = 1;
function newTimeline () {
  timelineCount += 1
  if (timelineCount == 1) {
    showTimelineOne = !showTimelineOne
  }
  if (timelineCount == 2) {
    showTimelineTwo = !showTimelineTwo
  }
  if (timelineCount == 3) {
    showTimelineThree = !showTimelineThree
  }
  if (timelineCount > 3) {
    timelineCount = 1;
  }
}
</script>

<div class="background" />

<Sidebar />
<div class="centering {showTimelineOne ? 'hideTimeline' : ''}"><Timeline /></div>
<!-- <div class="{showTimelineTwo ? 'hideTimeline' : ''}"><Timeline /></div>
<div class="{showTimelineThree ? 'hideTimeline' : ''}"><Timeline /></div> -->

<!-- <button class="bx submitButton" on:click={newTimeline}>NewTimeline</button> -->

<style>
  .background::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url("./src/assets/timelnlogoMono.png");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    opacity: 0.03;
    z-index: -100;
  }

  .hideTimeline {
    display: none;
  }

  .centering {
    margin: 0;
  position: absolute;
  top: 50%;
  transform: translate(-50%,);
  }
</style>
