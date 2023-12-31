<script>
  import {
    getFirestore,
    collection,
    addDoc,
    updateDoc,
    doc,
  } from "firebase/firestore";
  import { firebaseApp } from "../firebaseConfig";
  import {
    getDownloadURL,
    getStorage,
    ref,
    uploadBytes,
  } from "firebase/storage";
  import { writable } from "svelte/store";
  import { store } from "../my-store.js";
  import axios from "axios";

  let isCollapsed = false;

  export const isLoading = writable(false);
  let message = "";
  let startDate = "";
  let endDate = "";
  let files = [];

  function toggleSidebar() {
    isCollapsed = !isCollapsed;
  }

  function toggleTextbox() {}

  async function submitData() {
    store.set([]);
    isLoading.set(true);

    const db = getFirestore(firebaseApp);
    const submissionsCollection = collection(db, "submissions");

    const submissionData = {
      text: message,
      start_date: startDate,
      end_date: endDate,
      pdfs: [],
    };

    try {
      const docRef = await addDoc(submissionsCollection, submissionData);

      console.log("Document written with ID: ", docRef.id);

      if (files && files.length > 0) {
        for (const { file, description } of files) {
          const pdfUrl = await uploadPDF(file, docRef.id);
          submissionData.pdfs.push({ url: pdfUrl, description });
        }
      }

      await updateDoc(doc(submissionsCollection, docRef.id), {
        pdfs: submissionData.pdfs,
      });

      isLoading.set(false);
    } catch (error) {
      isLoading.set(false);
      console.error("Error adding document: ", error);
    }

    const data = {
      text: message,
      start_date: startDate,
      end_date: endDate,
      pdfs: submissionData.pdfs,
    };

    try {
      const response = await axios.post("http://localhost:8000/api", data);
      handleResponse(response.data);
    } catch (error) {
      console.error("Error sending data to Flask: ", error);
    }

    function handleResponse(data) {
      store.set(data);
      console.log($store);
    }

    message = "";
    startDate = "";
    endDate = "";
    files = [];
  }

  async function uploadPDF(file, docId) {
    const storage = getStorage(firebaseApp);
    const storageRef = ref(storage, `pdfs/${docId}/${file.name}`);

    try {
      await uploadBytes(storageRef, file);
      const pdfUrl = await getDownloadURL(storageRef);
      console.log("File uploaded successfully.");
      return pdfUrl;
    } catch (error) {
      console.error("Error uploading file: ", error);
    }
  }

  function handleFileChange(event) {
    const selectedFiles = event.target.files;
    const filesArray = [];
    for (let i = 0; i < selectedFiles.length; i++) {
      filesArray.push({ file: selectedFiles[i], description: "" });
    }
    files = filesArray;
  }
</script>

<link
  href="https://unpkg.com/boxicons@2.0.9/css/boxicons.min.css"
  rel="stylesheet"
/>

<div class="side-bar {isCollapsed ? 'collapsed' : ''}">
  <div class="logo-name-wrapper">
    <div class="logo-name">
      <span class="logo-name__name">
        <img class="logoImage" src="./src/assets/timelnlogo.png" alt="logo" />
      </span>
    </div>
    <button class="logo-name__button" on:click={toggleSidebar}>
      <i
        class="bx logo-name__icon {isCollapsed
          ? 'bx-arrow-from-left'
          : 'bx-arrow-from-right'}"
        id="logo-name__icon"
      />
    </button>
  </div>

  <div id="parentmessage">
    <div class="messagebox">
      <textarea
        rows="4"
        cols="30"
        class="textarea"
        placeholder="Submit a Query"
        on:click={toggleTextbox}
        bind:value={message}
      />
    </div>
    <div class="message float-left-child" on:click={toggleSidebar}>
      <i class="message-icon bx bx-message-square-edit" />
    </div>
  </div>
  <div class="date-range-container">
    <div class="date-range">
      <label class="dateText" for="start-date">Start date:</label>
      <input
        type="date"
        id="start-date"
        name="start-date"
        bind:value={startDate}
      />
    </div>

    <div class="date-range">
      <label for="end-date">End date:</label>
      <input type="date" id="end-date" name="end-date" bind:value={endDate} />
    </div>
  </div>
  <div class="fileParent">
    <label for="many">(Optional) Upload PDF(s) to parse:</label>
    <input
      id="many"
      type="file"
      multiple
      accept="application/pdf"
      on:change={handleFileChange}
      class="chooseFiles"
    />

    {#if files}
      <h2>Selected files:</h2>
      {#each files as { file, description }, index (index)}
        <div class="file-description">
          <p class="fileName">{file.name}</p>
          <textarea
            rows="2"
            cols="20"
            bind:value={files[index].description}
            placeholder="Description"
          />
        </div>
      {/each}
    {/if}
  </div>
  <div>
    <button class="bx submitButton" on:click={submitData}>Submit</button>
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
    height: 4rem;
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
    opacity: 1;
    transition: all 1s ease;
  }

  .textarea {
    resize: none;
    background-color: black;
    border: 1px solid #ccc;
  }

  .message-icon {
    cursor: pointer;
  }

  .date-range {
    margin: 10px 0;
    text-align: center;
    color: white;
  }

  .side-bar.collapsed .date-range {
    display: none;
    transition: all 0.5s ease;
  }

  .date-range label {
    color: #020202;
    font-size: 16px;
  }

  .date-range input {
    width: 80%;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: black;
  }

  .date-range-container {
    display: flex;
    justify-content: space-between;
  }

  .dateText {
    color: white;
  }

  .file-description {
    display: flex;
    align-items: center;
  }

  .file-description textarea {
    margin-left: 10px;
    resize: none;
    background-color: black;
    border: 1px solid #ccc;
  }

  .float-left-child {
    float: left;
  }

  .side-bar.collapsed .messagebox {
    transition: all 1s ease;
    width: 0%;
    height: 0%;
    display: none;
  }

  .message {
    background-color: var(--dark-grey-color);
    display: flex;
    align-items: center;
    padding: 1.55rem 0 1.55rem 1.2rem;
    border-radius: 0.4rem;
    position: relative;
    transition: all 0s ease;
    opacity: 0;
  }

  .message-icon {
    font-size: 2rem;
    width: 0%;
    height: 0%;
    transform: translateX(3rem);
    opacity: 0;
  }

  .side-bar.collapsed .message {
    cursor: pointer;
    height: 4rem;
    padding: 0;
    opacity: 1;
    width: 100%;
  }

  .side-bar.collapsed .message-icon {
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

  .side-bar.collapsed .logo-name {
    display: none;
  }

  .logo-name__button {
    position: absolute;
    right: 0;
    background-color: transparent;
    border: none;
    cursor: pointer;
  }

  .side-bar.collapsed .fileParent {
    display: none;
  }

  .fileParent {
    text-align: center;
    width: 100%;
    margin-top: 60px;
    margin-bottom: 60px;
  }

  .chooseFiles {
    margin-left: 35px;
    margin-top: 60px;
    margin-bottom: 60px;
  }

  .side-bar.collapsed .submitButton {
    display: none;
  }

  .submitButton {
    background-color: #1f2937;
  }

  .fileName {
    text-overflow: ellipsis;
    max-width: 7ch;
  }

  .logoImage {
    height: 4rem;
    margin-bottom: 1rem;
  }
</style>
