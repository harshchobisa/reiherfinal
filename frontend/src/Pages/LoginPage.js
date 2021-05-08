import React, { Component } from "react";
import { Container, Form, Button } from "react-bootstrap";

export default class LoginPage extends Component {
  state = {
    email: "",
    password: "",
  };

  onSubmit = () => {
    console.log("email" + this.state.email);
    console.log("pass" + this.state.password);
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
          <Button variant="primary" type="submit" onClick={this.onSubmit}>
            Submit
          </Button>
        </Form>
      </Container>
    );
  }
}
