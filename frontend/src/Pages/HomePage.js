import React, { Component } from "react";
import { Col, Row, Container } from "react-bootstrap";
import { NavLink } from "react-router-dom";
import axios from "axios";
import FamilyView from "../Components/FamilyView";

export default class HomePage extends Component {
  state = {
    family: [],
  };
  componentDidMount() {
    var config = {
      method: "post",
      url: "//localhost:8000/getFamily/",
      headers: {
        "Content-Type": "text/plain",
      },
      withCredentials: true,
    };
    axios(config)
      .then((response) => {
        this.setState({ family: response.data });
        console.log(response.status);
        console.log(JSON.stringify(response.data));
      })
      .catch(function (error) {
        console.log(error);
      });
  }
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
            <FamilyView family={this.state.family}></FamilyView>
          </Row>
        </Col>
      </Container>
    );
  }
}
