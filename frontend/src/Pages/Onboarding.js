import React, { Component } from "react";
import { Container, Form, Col } from "react-bootstrap";
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
    firstActivity: "dummy",
    secondActivity: "dummy",
    thirdActivity: "dummy",
    fourthActivity: "dummy",
    fifthActivity: "dummy",
  };

  onSubmit = () => {
    var config = {
      method: "post",
      url: "//localhost:8000/createMentor/",
      headers: {
        "Content-Type": "text/plain",
      },
      data: JSON.stringify(this.state),
      withCredentials: true,
      credentials: "same-origin",
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
          <Form.Row>
            <Form.Group as={Col}>
              <Form.Label>First Name</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter your legal first name"
                value={this.state.email}
                onChange={(e) => this.setState({ firstName: e.target.value })}
              />
            </Form.Group>

            <Form.Group as={Col}>
              <Form.Label>Last Name</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter your legal last name"
                value={this.state.email}
                onChange={(e) => this.setState({ lastName: e.target.value })}
              />
            </Form.Group>
          </Form.Row>

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

          <Form.Group controlId="ControlInput1">
            <Form.Label>Gender</Form.Label>
            <Form.Control
              as="select"
              custom
              onChange={(e) => this.setState({ gender: e.target.value })}
            >
              <option>Male</option>
              <option>Female</option>
            </Form.Control>
          </Form.Group>
          <Form.Group controlId="ControlInput1">
            <Form.Label>Major</Form.Label>
            <Form.Control
              as="select"
              custom
              onChange={(e) => this.setState({ major: e.target.value })}
            >
              <option>Computer Science</option>
              <option>Computer Science and Engineering</option>
              <option>Computer Engineering</option>
              <option>Electrical Engineering</option>
              <option>Mechanical Engineering</option>
              <option>Aerospace Engineering</option>
              <option>Bioengineering</option>
              <option>Civil Engineering</option>
              <option>Chemical Engineering</option>
              <option>Materials Engineering</option>
            </Form.Control>
          </Form.Group>
          <Form.Group controlId="ControlInput1">
            <Form.Label>Mentor Type</Form.Label>
            <Form.Control
              as="select"
              custom
              onChange={(e) => this.setState({ mentorType: e.target.value })}
            >
              <option>Academic</option>
              <option>Social</option>
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
