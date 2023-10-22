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

  let isCollapsed = false;
  let message = "";
  let startDate = "";
  let endDate = "";
  let files = [];

  function toggleSidebar() {
    isCollapsed = !isCollapsed;
  }

  function toggleTextbox() {}

  async function submitData() {
    // Initialize Firestore
    const db = getFirestore(firebaseApp);
    const submissionsCollection = collection(db, "submissions");

    // Create a new document in Firestore with text, start date, and end date
    const submissionData = {
      text: message,
      start_date: startDate,
      end_date: endDate,
      pdfs: [],
    };

    try {
      const docRef = await addDoc(submissionsCollection, submissionData);

      // Get the document ID for reference
      console.log("Document written with ID: ", docRef.id);

      // Check if files exist and upload them to Firebase Storage
      if (files && files.length > 0) {
        for (const { file, description } of files) {
          const pdfUrl = await uploadPDF(file, docRef.id);
          submissionData.pdfs.push({ url: pdfUrl, description });
        }
      }

      await updateDoc(doc(submissionsCollection, docRef.id), {
        pdfs: submissionData.pdfs,
      });

      // Reset the form and file input
      message = "";
      startDate = "";
      endDate = "";
      files = [];
    } catch (error) {
      console.error("Error adding document: ", error);
    }
  }

  async function uploadPDF(file, docId) {
    // Initialize Firebase Storage
    const storage = getStorage(firebaseApp);
    const storageRef = ref(storage, `pdfs/${docId}/${file.name}`);

    try {
      await uploadBytes(storageRef, file);
      const pdfUrl = await getDownloadURL(storageRef); // Get the download URL
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

<div class="side-bar {isCollapsed ? 'collapsed' : ''}">
  <div class="logo-name-wrapper">
    <div class="logo-name">
      <span class="logo-name__name">timeln</span>
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
      bind:value={message}
    />
  </div>

  <div class="date-range-container">
    <div class="date-range">
      <label for="start-date">Start date:</label>
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

  <label for="many">(Optional) Upload PDF(s) to parse:</label>
  <input
    id="many"
    type="file"
    multiple
    accept="application/pdf"
    on:change={handleFileChange}
  />

  {#if files}
    <h2>Selected files:</h2>
    {#each files as { file, description }, index (index)}
      <div class="file-description">
        <p>{file.name}</p>
        <textarea
          rows="2"
          cols="20"
          bind:value={files[index].description}
          placeholder="Description"
        />
      </div>
    {/each}
  {/if}

  <div class="message">
    <button class="message-icon bx bx-message-square-edit" on:click={submitData}
      >Submit</button
    >
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

  .date-range {
    margin: 10px 0;
  }

  .date-range label {
    color: #fff;
    font-size: 16px;
  }

  .date-range input {
    width: 80%;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  .date-range-container {
    display: flex;
    justify-content: space-between;
  }

  .file-description {
    display: flex;
    align-items: center;
  }

  .file-description textarea {
    margin-left: 10px;
  }
</style>
