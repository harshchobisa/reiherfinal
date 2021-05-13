import React, { Component } from "react";
import { Container, Button } from "react-bootstrap";
import axios from "axios";

export default class AdminPage extends Component {
  state = {
    families: null,
  };
  componentDidMount() {
    var config = {
      method: "post",
      url: "//localhost:8000/getAllFamilies/",
      headers: {
        "Content-Type": "text/plain",
      },
      withCredentials: true,
    };
    axios(config)
      .then(function (response) {
        console.log(response.status);
        console.log(JSON.stringify(response.data));
        this.setState({ families: JSON.stringify(response.data) });
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  onSubmit = () => {
    var config = {
      method: "post",
      url: "//localhost:8000/createFamilies/",
      headers: {
        "Content-Type": "text/plain",
      },
      withCredentials: true,
    };

    axios(config)
      .then(function (response) {
        console.log(response.status);
        console.log(JSON.stringify(response.data));
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  render() {
    return (
      <Container>
        <h1>This is the admin page</h1>
        <p>Here are the families {this.state.families} end</p>
        <Button
          variant="outline-secondary"
          onClick={this.onSubmit}
        >
          Run pairings
        </Button>{" "}
      </Container>
    );
  }
}
