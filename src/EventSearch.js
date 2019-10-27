import React, { Component } from "react";
import "./App.css";
import TextField from "@material-ui/core/TextField";
import Paper from "@material-ui/core/Paper";
import Button from "@material-ui/core/Button";
import {NavLink, Redirect} from 'react-router-dom';
import Typography from "@material-ui/core/Typography";

export default class EventSearch extends Component {
  constructor(props) {
    super(props);
    this.state = {
      eventCode : "",
      submitted: false
     };
  }
  handleNameChange = evt => {
    this.setState({ eventCode: evt.target.value})
  };

  onSubmitForm = (event) => {
    this.setState({ submitted: true})

  }

  render() {
    if (this.state.submitted){
      return (
        <Redirect to = {"/vote/" + this.state.eventCode}/>
      )
    }
    return (
      <Paper className="find-event">
        <form onSubmit={this.onSubmitForm} className="find-event-field" noValidate autoComplete="off">
          <TextField
            fullWidth
            id="standard-uncontrolled"
            placeholder="It's the thing after vote in the url :)"
            label="What's your special event code?"
            margin="normal"
            onChange = {this.handleNameChange}
          />

          <Button
            variant="contained"
            color="primary"
            className="create-event-submit"
            component = {NavLink}
            to = {"/vote/" + this.state.eventCode}
          >
            Find my Party!
          </Button>
        </form>
      </Paper>
    );
  }
}