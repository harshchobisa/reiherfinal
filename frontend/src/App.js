import React, { Component } from "react";

import HomePage from "./Pages/HomePage";
import LandingPage from "./Pages/LandingPage";
import LoginPage from "./Pages/LoginPage";
import SignupPage from "./Pages/SignupPage";
import MentorOnboarding from "./Pages/MentorOnboarding";
import MenteeOnboarding from "./Pages/MenteeOnboarding";
import FamilyPage from "./Pages/FamilyPage";

import "./App.css";
import { HashRouter, Route } from "react-router-dom";
import { Nav, Navbar, Container } from "react-bootstrap";

import "bootstrap/dist/css/bootstrap.min.css";

class App extends Component {
  render() {
    return (
      <Container>
        <Navbar bg="primary" variant="dark">
          <Navbar.Brand href="#/">MentorSEAS</Navbar.Brand>
          <Nav className="mr-auto">
            <Nav.Link href="#/">Home</Nav.Link>
            <Nav.Link href="#login">Login</Nav.Link>
            <Nav.Link href="#home">Dashboard</Nav.Link>
          </Nav>
        </Navbar>
        <HashRouter>
          <div className="App">
            <Route exact path="/" component={LandingPage} />
            <Route path="/home" component={HomePage} />
            <Route path="/login" component={LoginPage} />
            <Route path="/signup" component={SignupPage} />
            <Route path="/family" component={FamilyPage} />
            <Route path="/mentor_onboarding" component={MentorOnboarding} />
            <Route path="/mentee_onboarding" component={MenteeOnboarding} />
          </div>
        </HashRouter>
      </Container>
    );
  }
}

export default App;
