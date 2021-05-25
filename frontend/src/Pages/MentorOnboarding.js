import React, { Component } from "react";
import { Container, Form, Col } from "react-bootstrap";
import axios from "axios";
import { NavLink } from "react-router-dom";
import Cookies from "js-cookie";

export default class MentorOnboarding extends Component {
  state = {
    firstName: "",
    lastName: "",
    year: "2022",
    gender: "Male",
    major: "Computer Science",
    mentorType: "Academic",
    firstActivity: "Art/Theater",
    secondActivity: "Hiking/Outdoors",
    thirdActivity: "Community Service",
    fourthActivity: "Gym",
    fifthActivity: "Sports",
  };

  onSubmit = () => {
    var config = {
      method: "post",
      url: "createMentor/",
      headers: {
        "Content-Type": "text/plain",
        "X-CSRFToken": Cookies.get("XSRF-TOKEN"),
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
        if (response.status !== 201) {
          alert("API error");
        }
      })
      .catch(function (error) {
        console.log(error);
      });
  };

  render() {
    return (
      <Container>
        <h1>Mentor Onboarding Page</h1>
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
              <option value="">Choose...</option>
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
              <option value="">Choose...</option>
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
              <option value="">Choose...</option>
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
              <option>Undeclared Engineering</option>
            </Form.Control>
          </Form.Group>
          <Form.Group controlId="ControlInput1">
            <Form.Label>Mentor Type</Form.Label>
            <Form.Control
              as="select"
              custom
              onChange={(e) => this.setState({ mentorType: e.target.value })}
            >
              <option value="">Choose...</option>
              <option>Academic</option>
              <option>Social</option>
            </Form.Control>
          </Form.Group>
          <Form.Group controlId="ControlInput1">
            <Form.Label>Activity One</Form.Label>
            <Form.Control
              as="select"
              custom
              onChange={(e) => this.setState({ firstActivity: e.target.value })}
            >
              <option value="">Choose...</option>
              <option>Art/Theater</option>
              <option>Hiking/Outdoors</option>
              <option>Community Service</option>
              <option>Gym</option>
              <option>Sports</option>
              <option>Greek Life</option>
              <option>Video Games</option>
              <option>Watching TV/Movies</option>
              <option>Music</option>
            </Form.Control>
          </Form.Group>
          <Form.Group controlId="ControlInput1">
            <Form.Label>Activity Two</Form.Label>
            <Form.Control
              as="select"
              custom
              onChange={(e) =>
                this.setState({ secondActivity: e.target.value })
              }
            >
              <option value="">Choose...</option>
              <option>Art/Theater</option>
              <option>Hiking/Outdoors</option>
              <option>Community Service</option>
              <option>Gym</option>
              <option>Sports</option>
              <option>Greek Life</option>
              <option>Video Games</option>
              <option>Watching TV/Movies</option>
              <option>Music</option>
            </Form.Control>
          </Form.Group>
          <Form.Group controlId="ControlInput1">
            <Form.Label>Activity Three</Form.Label>
            <Form.Control
              as="select"
              custom
              onChange={(e) => this.setState({ thirdActivity: e.target.value })}
            >
              <option value="">Choose...</option>
              <option>Art/Theater</option>
              <option>Hiking/Outdoors</option>
              <option>Community Service</option>
              <option>Gym</option>
              <option>Sports</option>
              <option>Greek Life</option>
              <option>Video Games</option>
              <option>Watching TV/Movies</option>
              <option>Music</option>
            </Form.Control>
          </Form.Group>
          <Form.Group controlId="ControlInput1">
            <Form.Label>Activity Four</Form.Label>
            <Form.Control
              as="select"
              custom
              onChange={(e) =>
                this.setState({ fourthActivity: e.target.value })
              }
            >
              <option value="">Choose...</option>
              <option>Art/Theater</option>
              <option>Hiking/Outdoors</option>
              <option>Community Service</option>
              <option>Gym</option>
              <option>Sports</option>
              <option>Greek Life</option>
              <option>Video Games</option>
              <option>Watching TV/Movies</option>
              <option>Music</option>
            </Form.Control>
          </Form.Group>
          <Form.Group controlId="ControlInput1">
            <Form.Label>Activity Five</Form.Label>
            <Form.Control
              as="select"
              custom
              onChange={(e) => this.setState({ fifthActivity: e.target.value })}
            >
              <option value="">Choose...</option>
              <option>Art/Theater</option>
              <option>Hiking/Outdoors</option>
              <option>Community Service</option>
              <option>Gym</option>
              <option>Sports</option>
              <option>Greek Life</option>
              <option>Video Games</option>
              <option>Watching TV/Movies</option>
              <option>Music</option>
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
