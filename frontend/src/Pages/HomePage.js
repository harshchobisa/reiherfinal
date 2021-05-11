import React, { Component } from "react";
import { Col, Row, Container } from "react-bootstrap";
import { NavLink } from "react-router-dom";

export default class HomePage extends Component {
  render() {
    return (
      <Container>
        <h1>Welcome to your MentorSEAS homepage</h1>
        <h3>You are successfully logged in</h3>
        <Col>
          <Row>
            <NavLink to="/mentor_onboarding/">Complete your profile</NavLink>
          </Row>
          <Row>
            <NavLink to="/family/">View your family</NavLink>
          </Row>
        </Col>
      </Container>
    );
  }
}
