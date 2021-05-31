import React, { Component } from "react";

import HomePage from "./Pages/HomePage";
import LandingPage from "./Pages/LandingPage";
import LoginPage from "./Pages/LoginPage";
import SignupPage from "./Pages/SignupPage";
import MentorOnboarding from "./Pages/MentorOnboarding";
import MenteeOnboarding from "./Pages/MenteeOnboarding";
import FamilyPage from "./Pages/FamilyPage";
import AdminPage from "./Pages/AdminPage";
import ResetPage from "./Pages/ResetPage";

import "./App.css";
import { HashRouter, Route } from "react-router-dom";
import { Nav, Navbar, Container } from "react-bootstrap";
import axios from "axios";
import Cookies from "js-cookie";

import "bootstrap/dist/css/bootstrap.min.css";

class App extends Component {
  state = {
    user: "",
    dummy: 0,
  };

  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick = () => {
    this.setState({ dummy: this.state.dummy + 1 });
    window.location.reload();
  };

  componentDidMount() {
    axios({
      method: "post",
      url: "getCurrentUser/",
      headers: {
        "Content-Type": "text/plain",
        "X-CSRFToken": Cookies.get("XSRF-TOKEN"),
      },
      withCredentials: true,
    })
      .then((response) => {
        this.setState({ user: response.data });
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  onSubmit = () => {
    axios({
      method: "post",
      url: "logout/",
      headers: {
        "Content-Type": "text/plain",
        "X-CSRFToken": Cookies.get("XSRF-TOKEN"),
      },
      withCredentials: true,
    })
      .then((response) => {
        console.log(response.status);
        this.setState({ user: "" });
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  render() {
    function TryUsername(props) {
      const user = props.user;

      if (user !== "") {
        return <Navbar.Text>Signed in as: {user} .</Navbar.Text>;
      } else {
        return <div></div>;
      }
    }
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
            <TryUsername user={this.state.user}></TryUsername>
            <Navbar.Text onClick={this.onSubmit}>
              <a href="#login">Logout</a>
            </Navbar.Text>
          </Navbar.Collapse>
        </Navbar>
        <HashRouter>
          <div className="App">
            <Route exact path="/" component={LandingPage} />
            <Route path="/home" component={HomePage} />
            <Route
              path="/login"
              render={() => <LoginPage handler={this.handleClick} />}
            />
            <Route
              path="/signup"
              render={() => <SignupPage handler={this.handleClick} />}
            />
            <Route path="/family" component={FamilyPage} />
            <Route path="/passwordResetPage/:token" component={ResetPage} />
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
