<script>
  export let content;
  export let position = { top: 0, left: 0 };
</script>

<div
  class="popup-box"
  style="top: {position.top}px; left: {position.left + 240}px;"
>
  <div class="text-base font-normal text-gray-500 dark:text-gray-400">
    <p>{content}</p>
  </div>
</div>

<style>
  .popup-box {
    position: fixed;
    background: whitesmoke;
    padding: 20px;
    width: 200px;
  }
</style>
