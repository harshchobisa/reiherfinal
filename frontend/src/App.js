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
import axios from "axios";

import "bootstrap/dist/css/bootstrap.min.css";

class App extends Component {
  state = {
    user: "",
  };

  constructor(props) {
    super(props);
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick = () => {
    window.location.reload();
  };

  componentDidMount() {
    axios({
      method: "post",
      url: "//localhost:8000/getCurrentUser/",
      headers: {
        "Content-Type": "text/plain",
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
      url: "//localhost:8000/logout/",
      headers: {
        "Content-Type": "text/plain",
      },
      withCredentials: true,
    })
      .then((response) => {
        console.log(response.status);
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  render() {
    function TryUsername(props) {
      const user = props.user;

      if (user !== "") {
        return <Navbar.Text>Signed in as: {user} </Navbar.Text>;
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
            {/* <Route path="/login" component={LoginPage} /> */}

            <Route
              path="/login"
              render={() => <LoginPage handler={this.handleClick} />}
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
