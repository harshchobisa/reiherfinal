import React, { Component } from "react";
import { Container, Form } from "react-bootstrap";
import axios from "axios";
import { NavLink } from "react-router-dom";

export default class Onboarding extends Component {
  state = {
    firstName: "",
    lastName: "",
    year: "",
    gender: "",
    major: "",
    mentorType: "",
    firstActivity: "",
    secondActivity: "",
    thirdActivity: "",
    fourthActivity: "",
    fifthActivity: "",
  };

  onSubmit = () => {
    var data = JSON.stringify({
      username: this.state.email,
      password: this.state.password,
    });
    var config = {
      method: "post",
      url: "//localhost:8000/createMentor/",
      headers: {
        "Content-Type": "text/plain",
      },
      data: data,
    };

    axios(config)
      .then(function (response) {
        console.log(response.status);
        console.log(JSON.stringify(response.data));
        if (response.status === 200) {
          console.log("redirect");
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  render() {
    return (
      <Container>
        <h1>Onboarding Page</h1>
        <Form>
          <Form.Group>
            <Form.Label>First Name</Form.Label>
            <Form.Control
              type="email"
              placeholder="Enter your legal first name"
              value={this.state.email}
              onChange={(e) => this.setState({ firstName: e.target.value })}
            />
          </Form.Group>
          <Form.Group>
            <Form.Label>Last Name</Form.Label>
            <Form.Control
              type="email"
              placeholder="Enter your legal last name"
              value={this.state.email}
              onChange={(e) => this.setState({ lastName: e.target.value })}
            />
          </Form.Group>
          <Form.Group controlId="ControlInput1">
            <Form.Label>Grad Year</Form.Label>
            <Form.Control
              as="select"
              custom
              onChange={(e) => this.setState({ year: e.target.value })}
            >
              <option>2022</option>
              <option>2023</option>
              <option>2024</option>
            </Form.Control>
          </Form.Group>

          <NavLink to="/home/" onClick={this.onSubmit}>
            Submit
          </NavLink>
        </Form>
      </Container>
    );
  }
}
