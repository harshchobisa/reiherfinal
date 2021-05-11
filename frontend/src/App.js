import React, { Component } from "react";

import HomePage from "./Pages/HomePage";
import LandingPage from "./Pages/LandingPage";
import LoginPage from "./Pages/LoginPage";
import SignupPage from "./Pages/SignupPage";
import MentorOnboarding from "./Pages/MentorOnboarding";
import MenteeOnboarding from "./Pages/MenteeOnboarding";

import "./App.css";
import { HashRouter, Route } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

class App extends Component {
  render() {
    return (
      <HashRouter>
        <div className="App">
          <Route exact path="/" component={LandingPage} />
          <Route path="/home" component={HomePage} />
          <Route path="/login" component={LoginPage} />
          <Route path="/signup" component={SignupPage} />
          <Route path="/mentor_onboarding" component={MentorOnboarding} />
          <Route path="/mentee_onboarding" component={MenteeOnboarding} />
        </div>
      </HashRouter>
    );
  }
}

export default App;
