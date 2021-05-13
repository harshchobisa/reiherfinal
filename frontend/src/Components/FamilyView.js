import React, { Component } from "react";
import { JsonToTable } from "react-json-to-table";
import { Container } from "react-bootstrap";

export default class FamilyView extends Component {
  render() {
    return (
      <Container>
        <h3>Here is your family</h3>
        <JsonToTable json={this.props.family} />
      </Container> 
    );
  }
}
