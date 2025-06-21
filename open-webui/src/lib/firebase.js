import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, GithubAuthProvider, signInWithPopup } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyAU17UbyEiXkzbxCqt5HKjuvKVQC5IEGIk",
  authDomain: "optiflexai.firebaseapp.com",
  projectId: "optiflexai",
  storageBucket: "optiflexai.firebasestorage.app",
  messagingSenderId: "23233290281",
  appId: "1:23233290281:web:2334a20b757dca4a06bc38"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const googleProvider = new GoogleAuthProvider();
const githubProvider = new GithubAuthProvider();

export { auth, googleProvider, githubProvider, signInWithPopup };
