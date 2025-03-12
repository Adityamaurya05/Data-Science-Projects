import { initializeApp, getApp, getApps } from 'firebase/app';
import { getStorage } from 'firebase/storage';
import { getDatabase } from 'firebase/database';

const firebaseConfig = {
  apiKey: "AIzaSyBo8s8Wec16GUvo4oDni29uZyfNcr7nJ9o",
  authDomain: "indian-classical-dance.firebaseapp.com",
  projectId: "indian-classical-dance",
  storageBucket: "indian-classical-dance.appspot.com",
  messagingSenderId: "446050968447",
  appId: "1:446050968447:web:bed2b2fe980e652b97704a",
  databaseURL: "https://indian-classical-dance-default-rtdb.asia-southeast1.firebasedatabase.app"
};

const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();

export const storage = getStorage(app);
export const database = getDatabase(app);
