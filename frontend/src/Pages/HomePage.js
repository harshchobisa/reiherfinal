import React, { Component } from "react";
import { Col, Row, Container } from "react-bootstrap";
import { NavLink } from "react-router-dom";
import axios from "axios";
import FamilyView from "../Components/FamilyView";
import Cookies from "js-cookie";

export default class HomePage extends Component {
  state = {
    family: [],
    isMentor: true,
    hasCompletedProfile: false,
    hasFamily: false,
  };
  componentDidMount() {
    axios({
      method: "post",
      url: "getFamily/",
      headers: {
        "Content-Type": "text/plain",
        "X-CSRFToken": Cookies.get("XSRF-TOKEN"),
      },
      withCredentials: true,
    })
      .then((response) => {
        this.setState({ family: response.data, hasFamily: true });
      })
      .catch(function (error) {
        console.log(error);
      });

    axios({
      method: "post",
      url: "hasCompletedProfile/",
      headers: {
        "Content-Type": "text/plain",
        "X-CSRFToken": Cookies.get("XSRF-TOKEN"),
      },
      withCredentials: true,
    })
      .then((response) => {
        if (response.data === "True") {
          this.setState({ hasCompletedProfile: true });
        } else {
          this.setState({ hasCompletedProfile: false });
        }
      })
      .catch(function (error) {
        console.log(error);
      });

    axios({
      method: "post",
      url: "isMentor/",
      headers: {
        "Content-Type": "text/plain",
        "X-CSRFToken": Cookies.get("XSRF-TOKEN"),
      },
      withCredentials: true,
    })
      .then((response) => {
        if (response.data === "True") {
          this.setState({ isMentor: true });
        } else {
          this.setState({ isMentor: false });
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  }

  render() {
    function TryProfile(props) {
      const hasCompletedProfile = props.hasCompletedProfile;
      const isMentor = props.isMentor;

      if (hasCompletedProfile) {
        return <p>Your profile is complete.</p>;
      } else {
        if (isMentor) {
          return (
            <NavLink to="/mentor_onboarding/">Complete your profile</NavLink>
          );
        } else {
          return (
            <NavLink to="/mentee_onboarding/">Complete your profile</NavLink>
          );
        }
      }
    }
    function TryFamily(props) {
      const hasFamily = props.hasFamily;
      if (hasFamily) {
        return <FamilyView family={props.family}></FamilyView>;
      }
      return <p>You do not have a family yet.</p>;
    }
    return (
      <Container>
        <h1>Welcome to your MentorSEAS homepage</h1>
        <h3>You are successfully logged in</h3>
        <Col>
          <Row>
            <TryProfile
              hasCompletedProfile={this.state.hasCompletedProfile}
              isMentor={this.state.isMentor}
            ></TryProfile>
          </Row>
          <Row>
            <TryFamily
              hasFamily={this.state.hasFamily}
              family={this.state.family}
            ></TryFamily>
          </Row>
        </Col>
      </Container>
    );
  }
}
