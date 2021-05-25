import React, { Component } from "react";
import { Container, Button } from "react-bootstrap";
import { Redirect } from "react-router-dom";
import axios from "axios";
import Cookies from "js-cookie";

export default class LandingPage extends Component {
  state = {
    loggedIn: false,
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
        if (response.data !== "") {
          this.setState({ loggedIn: true });
        }
      })
      .catch(function (error) {
        console.log(error);
      });
    axios({
      method: "get",
      url: "getToken/",
      headers: {
        "Content-Type": "text/plain",
        "X-CSRFToken": Cookies.get("XSRF-TOKEN"),
      },
      withCredentials: true,
    })
      .then((response) => {
        if (response.data !== "") {
          console.log("successfully got token")
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  render() {
    if (this.state.loggedIn) {
      return <Redirect to="/home" />;
    }
    return (
      <Container>
        <h1>Welcome to MentorSEAS!</h1>
        <Button href="#/login" variant="outline-primary">
          Sign In{" "}
        </Button>{" "}
        <Button href="#/signup" variant="outline-secondary">
          Sign Up
        </Button>{" "}
      </Container>
    );
  }
}
