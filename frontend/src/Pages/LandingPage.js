import React, { Component } from "react";
import { Container, Button } from "react-bootstrap";
export default class LandingPage extends Component {
    render() {
        return (
            <Container>
                <h1>Welcome to MentorSEAS!</h1>
                <Button href="#/login" variant="outline-primary">Sign In </Button>{' '}
                <Button href="#/signup" variant="outline-secondary">Sign Up</Button>{' '}
            </Container>
        );
    }
}
