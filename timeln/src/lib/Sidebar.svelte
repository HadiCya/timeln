<script>
  let isCollapsed = false;

  function toggleSidebar() {
    isCollapsed = !isCollapsed;
  }

  function toggleTextbox() {
    isCollapsed = !isCollapsed;
  }
</script>

<div class="side-bar {isCollapsed ? 'collapse' : ''}">
  <div class="logo-name-wrapper">
    <div class="logo-name">
      <span class="logo-name__name">CSSScript</span>
    </div>
    <button class="logo-name__button" on:click={toggleSidebar}>
      <i
        class="bx bx-arrow-from-right logo-name__icon {isCollapsed
          ? 'collapse'
          : ''}"
        id="logo-name__icon"
      />
    </button>
  </div>

  <div class="messagebox is-horizontal float-left-child">
    <textarea
      rows="4"
      cols="30"
      class="messagebox textarea {isCollapsed ? 'collapse' : ''}"
      placeholder="Submit a Query"
      on:click={toggleTextbox}
    />
  </div>
  <div class="message is-horizontal float-left-child">
    <i
      class="message-icon bx bx-message-square-edit"
      on:click={toggleTextbox}
    />
    <span class="tooltip">Submit Query</span>
  </div>

  <label class="checkbox">
    <input type="checkbox" />
    Checkbox 1
  </label>

  <label class="checkbox">
    <input type="checkbox" />
    Checkbox 2
  </label>

  <label class="checkbox">
    <input type="checkbox" />
    Checkbox 3
  </label>
  <label class="checkbox">
    <input type="checkbox" />
    Checkbox 4
  </label>

  <div class="file has-name">
    <label class="file-label">
      <input class="file-input" type="file" name="resume" />
      <span class="file-cta">
        <span class="file-icon">
          <i class="fas fa-upload" />
        </span>
        <span class="file-label"> Choose a file… </span>
      </span>
      <span id="fileName" class="file-name">
        Screen Shot 2017-07-29 at 15.54.25.png
      </span>
    </label>
  </div>
</div>

<style>
  .side-bar {
    width: 35rem;
    background-color: #17171e;
    position: fixed;
    top: 0;
    transition: all 0.5s ease;
  }

  .logo-name-wrapper {
    display: flex;
    font-size: 1.2rem;
  }

  .logo-name {
    display: flex;
    align-items: center;
  }

  .logo-name__name {
    margin-left: 0.9rem;
    white-space: nowrap;
  }

  .logo-name__button {
    position: absolute;
    top: 50%;
    right: 0;
    font-size: 1.8rem;
    transform: translateY(-50%);
    background-color: transparent;
    border: none;
    cursor: pointer;
  }

  .messagebox {
    width: 100%;
  }

  .textarea {
    resize: none;
  }

  .side-bar.collapse {
    width: 6.4rem;
  }

  .side-bar.collapse .logo-name {
    opacity: 0;
    pointer-events: none;
  }

  .side-bar.collapse .message-icon {
    transform: translateX(0);
    opacity: 1;
    cursor: pointer;
    height: 100%;
    width: 100%;
    text-align: center;
    vertical-align: middle;
    line-height: 2;
    transition: opacity 0.1s ease;
  }

  .side-bar.collapse .logo-name__button {
    right: 0.5rem;
  }

  .side-bar.collapse .messagebox {
    width: 0%;
    height: 0%;
  }

  .side-bar.collapse .message {
    height: 4rem;
    padding: 0;
    opacity: 1;
    width: 100%;
  }

  .side-bar.collapse .file {
    display: none;
  }

  .has-name {
    color: #000;
  }
</style>
