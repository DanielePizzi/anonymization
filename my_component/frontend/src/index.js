import React from "react";
import ReactDOM from "react-dom";
import { Streamlit } from "streamlit-component-lib";

const App = () => {
  return <h1>Hello from React in Streamlit!</h1>;
};

Streamlit.setComponentReady();
ReactDOM.render(<App />, document.getElementById("root"));