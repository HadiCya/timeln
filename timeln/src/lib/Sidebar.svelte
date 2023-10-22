<script>
  let isCollapsed = false;

  function toggleSidebar() {
    isCollapsed = !isCollapsed;
  }

  function toggleTextbox() {
    isCollapsed = !isCollapsed;
  }
</script>

<div class="side-bar {isCollapsed ? 'collapsed' : ''}">
  <div class="logo-name-wrapper">
    <div class="logo-name">
      <span class="logo-name__name">CSSScript</span>
    </div>
    <button class="logo-name__button" on:click={toggleSidebar}>
      <i class="bx bx-arrow-from-right" />
    </button>
  </div>

  <div class="messagebox">
    <textarea
      rows="4"
      cols="30"
      class="textarea"
      placeholder="Submit a Query"
      on:click={toggleTextbox}
    />
  </div>

  <div class="message">
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
        <span class="file-label">Choose a file…</span>
      </span>
      <span id="fileName" class="file-name"
        >Screen Shot 2017-07-29 at 15.54.25.png</span
      >
    </label>
  </div>
</div>

<style>
  /* Sidebar Styles */
  .side-bar {
    width: 20%;
    height: 100%;
    min-width: 6.4rem;
    background-color: #17171e;
    position: fixed;
    top: 0;
    left: 0;
    transition: all 0.5s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
  }

  .collapsed {
    width: 6.4rem;
  }

  .logo-name-wrapper {
    display: flex;
    align-items: center;
  }

  .logo-name {
    display: flex;
    align-items: center;
  }

  .logo-name__name {
    margin-left: 0.9rem;
    white-space: nowrap;
    color: #fff; /* Text color */
  }

  .logo-name__button {
    font-size: 1.8rem;
    background-color: transparent;
    border: none;
    cursor: pointer;
    color: #fff; /* Icon color */
  }

  .messagebox {
    width: 100%;
  }

  .textarea {
    resize: none;
  }

  .message-icon {
    cursor: pointer;
  }
</style>
