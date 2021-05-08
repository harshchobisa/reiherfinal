import React, { Component } from "react";
import { Container, Form, Button } from "react-bootstrap";
import axios from "axios";
import {NavLink} from 'react-router-dom';

export default class LoginPage extends Component {
  state = {
    email: "",
    password: "",
  };

  onSubmit = () => {
    var data = JSON.stringify({
      username: this.state.email,
      password: this.state.password,
    });
    var config = {
      method: "post",
      url: "//localhost:8000/login/",
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
			console.log("redirect")
		}
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  render() {
    return (
      <Container>
        <h1>Login Page</h1>
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
		  <NavLink to="/home/" onClick = {this.onSubmit}>
			  Submit
		  </NavLink>
          <Button href="#/signup" variant="outline-secondary">
            Don't have an account? Make one here.
          </Button>{" "}
        </Form>
      </Container>
    );
  }
}