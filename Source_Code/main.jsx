import React from "react";
import ReactDOM from "react-dom/client";//ReactDOM, which is responsible for connecting the React application to the HTML page.
import App from "./App";
import "./styles.css";//loads the CSS file that provides the styling for the application.

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode> 
    <App />
  </React.StrictMode>
);
