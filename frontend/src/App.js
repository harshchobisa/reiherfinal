import React, { Component } from "react";

import HomePage from "./Pages/HomePage";
import LandingPage from "./Pages/LandingPage";
import LoginPage from "./Pages/LoginPage";
import SignupPage from "./Pages/SignupPage";
import MentorOnboarding from "./Pages/MentorOnboarding";
import MenteeOnboarding from "./Pages/MenteeOnboarding";
import FamilyPage from "./Pages/FamilyPage";
import AdminPage from "./Pages/AdminPage";

import "./App.css";
import { HashRouter, Route } from "react-router-dom";
import { Nav, Navbar, Container } from "react-bootstrap";

import "bootstrap/dist/css/bootstrap.min.css";

class App extends Component {
  state = {
    user: "",
  };
  constructor(props) {
    super(props);
    this.handler = this.handler.bind(this);
  }
  handler(username) {
    console.log(`in handler ${username}`);

    this.setState({ user: username });
  }

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
          <Navbar.Collapse className="justify-content-end">
            <Navbar.Text>Signed in as: {this.state.user} </Navbar.Text>
            <Navbar.Text>
              <a href="#login">Switch user</a>
            </Navbar.Text>
          </Navbar.Collapse>
        </Navbar>
        <HashRouter>
          <div className="App">
            <Route exact path="/" component={LandingPage} />
            <Route path="/home" component={HomePage} />
            <Route
              path="/login"
              render={() => <LoginPage handler={this.handler} />}
            />
            <Route path="/signup" component={SignupPage} />
            <Route path="/family" component={FamilyPage} />
            <Route path="/mentor_onboarding" component={MentorOnboarding} />
            <Route path="/mentee_onboarding" component={MenteeOnboarding} />
            <Route path="/admin" component={AdminPage} />
          </div>
        </HashRouter>
      </Container>
    );
  }
}

export default App;
