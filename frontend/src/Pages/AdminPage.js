import React, { Component } from "react";
import { Container, Button } from "react-bootstrap";
import axios from "axios";
import { JsonToTable } from "react-json-to-table";

export default class AdminPage extends Component {
  state = {
    families: [],
    dummy: 0,
  };
  componentDidMount() {
    var config = {
      method: "post",
      url: "//localhost/getAllFamilies/",
      headers: {
        "Content-Type": "text/plain",
      },
      withCredentials: true,
    };
    axios(config)
      .then((response) => {
        this.setState({ families: response.data });
        console.log(response.status);
        console.log(JSON.stringify(response.data));
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  runPairings = () => {
    var config = {
      method: "post",
      url: "//localhost/createFamilies/",
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

    window.location.reload();
  };

  addData = () => {
    var config = {
      method: "post",
      url: "//localhost/populateUsers/",
      headers: {
        "Content-Type": "text/plain",
      },
      data: JSON.stringify({
        num_mentors: 50,
        num_mentees: 150,
      }),
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

    window.location.reload();
  };

  render() {
    return (
      <Container>
        <h1>This is the admin page</h1>
        <Button variant="outline-secondary" onClick={this.runPairings}>
          Run pairings
        </Button>{" "}
        <Button variant="outline-secondary" onClick={this.addData}>
          Create users
        </Button>{" "}
        <p>Here are the families</p>
        {this.state.families.map((family) => (
          <div>
            <b />
            <JsonToTable json={family} />
          </div>
        ))}
      </Container>
    );
  }
}
