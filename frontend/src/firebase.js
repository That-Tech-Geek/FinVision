import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyBRbgTlgoi6LfCfT5va4m1cqhILWcjJSPM",
  authDomain: "finvision-68f62.firebaseapp.com",
  projectId: "finvision-68f62",
  storageBucket: "finvision-68f62.firebasestorage.app",
  messagingSenderId: "179926209377",
  appId: "1:179926209377:web:31b488bc982ee788f5ab20",
  measurementId: "G-H5K34YDGVY"
};

import { getAuth, GoogleAuthProvider } from "firebase/auth";

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
