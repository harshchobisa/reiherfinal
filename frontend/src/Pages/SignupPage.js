import React, { Component } from "react";
import { Container, Form, Button } from "react-bootstrap";
import axios from "axios";

export default class SignupPage extends Component {
  state = {
    email: "",
    password: "",
    role: "",
    submitted: false,
  };

  onSubmit = () => {
    //   weird formatting for payload, should fix this later
    var data = `{\n    "username": "${this.state.email}",\n    "password": "${this.state.password}",\n    "role": "${this.state.role}"\n}`;
    var config = {
      method: "post",
      url: "//localhost:8000/createUser/",
      headers: {
        "Content-Type": "text/plain",
      },
      data: data,
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
        <h1>Signup Page</h1>
        <Form>
          <Form.Group controlId="formBasicEmail">
            <Form.Label>Email address</Form.Label>
            <Form.Control
              type="email"
              placeholder="Enter email"
              value={this.state.email}
              onChange={(e) => this.setState({ email: e.target.value })}
            />
            <Form.Text className="text-muted">
              We'll never share your email with anyone else.
            </Form.Text>
          </Form.Group>

          <Form.Group controlId="formBasicPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              placeholder="Password"
              value={this.state.password}
              onChange={(e) => this.setState({ password: e.target.value })}
            />
          </Form.Group>

          <Form.Group controlId="ControlInput1">
            <Form.Label>Role</Form.Label>
            <Form.Control
              as="select"
              custom
              onChange={(e) => this.setState({ role: e.target.value })}
            >
              <option>mentor</option>
              <option>mentee</option>
            </Form.Control>
          </Form.Group>
          <Button variant="outline-success" type="submit" onClick={this.onSubmit}>
            Submit
          </Button>
          <Button href="#/login" variant="outline-secondary">Already have an account? Sign in here.</Button>{' '}

        </Form>
      </Container>
    );
  }
}
