import React, { Component } from "react";
import { Row, Col, Container, Form, Button } from "react-bootstrap";
import axios from "axios";
import { Redirect, NavLink } from "react-router-dom";
import Cookies from "js-cookie";

export default class ResetPage extends Component {
  state = {
    email: "",
    password: "",
  };

  onSubmit = () => {
    console.log(this.props.match.params);
    var data = JSON.stringify({
      email: this.state.email,
      password: this.state.password,
      token: this.props.match.params.token,
    });
    axios({
      method: "post",
      url: "resetPassword/",
      headers: {
        "Content-Type": "text/plain",
        "X-CSRFToken": Cookies.get("XSRF-TOKEN"),
      },
      data: data,
      withCredentials: true,
    })
      .then((response) => {
        console.log(response.status);
        console.log(JSON.stringify(response.data));
        this.props.handler();
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  render() {
    return (
      <Container>
        <h1>Reset Page</h1>
        <Form>
          <Form.Group controlId="formBasicEmail">
            <Form.Label>Email address</Form.Label>
            <Form.Control
              type="email"
              placeholder="Enter email"
              value={this.state.email}
              onChange={(e) => this.setState({ email: e.target.value })}
            />
          </Form.Group>
          <Form.Group controlId="formBasicPassword">
            <Form.Label>New Password</Form.Label>
            <Form.Control
              type="password"
              placeholder="Password"
              value={this.state.password}
              onChange={(e) => this.setState({ password: e.target.value })}
            />
          </Form.Group>
          <Col>
            <Row>
              <NavLink to="/login/" onClick={this.onSubmit}>
                Submit
              </NavLink>
            </Row>
          </Col>
        </Form>
      </Container>
    );
  }
}
