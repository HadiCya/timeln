<script>
  export let title;
  export let content;
  export let position = { top: 0, left: 0 };
</script>

<div class="popup-box" style="top: {position.top}+10; left: {position.left};">
  <div class="text-base font-normal text-gray-500 dark:text-gray-400">
    <p>{title}</p>
    <p>{content}</p>
    <div>
      <button class="bx submitButton">Submit</button>
    </div>
  </div>
</div>

<style>
  .popup-box {
    position: fixed;
    background: whitesmoke;
    padding: 20px;
    width: 300px;
  }
</style>
