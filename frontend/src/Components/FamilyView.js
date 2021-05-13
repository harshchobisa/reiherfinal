import React, { Component } from "react";

export default class FamilyView extends Component {
  render() {
    return (
      <div>
        <p>Your family is {JSON.stringify(this.props.family)}</p>
      </div>
    );
  }
}
