import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

// ---------- AUTH ----------
export const loginUser = (data) => API.post("/login", data);
export const signupUser = (data) => API.post("/signup", data);

// ---------- DETECTION ----------
export const manualDetect = (data) =>
  API.post("/predict/manual", data);

export const liveDetect = () =>
  API.get("/predict/live");

export const debugDetect = () =>
  API.get("/predict/debug");

export default API;
