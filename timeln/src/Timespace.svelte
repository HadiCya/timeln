<script>
  import Timeline from "./lib/Timeline.svelte";
  import Sidebar from "./lib/Sidebar.svelte";
</script>

<Sidebar />
<Timeline />

<div class="background" />

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
  }
</style>
