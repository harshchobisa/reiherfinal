import React, { Component } from "react";
import { Container, Form, Button } from "react-bootstrap";

export default class SignupPage extends Component {
  state = {
    email: "",
    password: "",
    role: "",
  };

  onSubmit = () => {
    console.log("email " + this.state.email);
    console.log("pass " + this.state.password);
    console.log("role " + this.state.role);
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
              type="text"
              placeholder="Role"
              value={this.state.role}
              onChange={(e) => this.setState({ role: e.target.value })}
            />
          </Form.Group>

          <Form.Group controlId="formBasicCheckbox">
            <Form.Check
              type="checkbox"
              label="I agree to the terms and conditions"
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
