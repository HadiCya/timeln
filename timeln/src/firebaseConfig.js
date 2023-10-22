import { initializeApp } from "firebase/app";

const firebaseConfig = {
  apiKey: "AIzaSyBS6So54cT4djgj-gd9iNkK6zCj8UGIfcw",
  authDomain: "timeln-44e94.firebaseapp.com",
  projectId: "timeln-44e94",
  storageBucket: "timeln-44e94.appspot.com",
  messagingSenderId: "475384406000",
  appId: "1:475384406000:web:fdd7768f0fec58faad0735",
};

const firebaseApp = initializeApp(firebaseConfig);
export { firebaseApp };
