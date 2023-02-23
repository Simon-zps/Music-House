import React from "react";
import ReactDOM from "react-dom";
import Home from "./Home";

export default function App() {
  return (
    <Home />
  );
}

// Get app div inside our HTML
const appDiv = document.getElementById("app");

// Render our components inside the app div
ReactDOM.render(<App />, appDiv);
