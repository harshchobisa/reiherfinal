import React, { Component } from "react";

import LoginPage from "./Pages/LoginPage";
import SignupPage from "./Pages/SignupPage";

import "./App.css";
import { HashRouter, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

class App extends Component {
  render() {
    return (
      <HashRouter>
        <div className="App">
          {/* <Route exact path="/" component={Temp} /> */}
          <Route path="/login" component={LoginPage} />
          <Route path="/signup" component={SignupPage} />
        </div>
      </HashRouter>
    );
  }
}

export default App;
