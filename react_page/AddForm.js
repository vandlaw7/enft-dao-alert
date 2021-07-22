import React, { Component } from 'react';
import { post } from 'axios';

class AddForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      telegram_id: '',
      eth_address: '',
      gov_token: ''
    };

    this.handleFormSubmit = this.handleFormSubmit.bind(this);
    this.handleValueChange = this.handleValueChange.bind(this);
    this.addFormSet = this.addFormSet.bind(this);
  }

  handleFormSubmit(e) {
    e.preventDefault();
    this.addFormSet().then((response) => {
      console.log(response.data);
    });
    alert(`form 제출 성공!`);
  }

  handleValueChange(e) {
    let nextState = {};
    nextState[e.target.name] = e.target.value;
    this.setState(nextState);
  }

  addFormSet() {
    const url = '/test/members';
    const formData = new FormData();
    formData.append('telegram_id', this.state.telegram_id);
    formData.append('eth_address', this.state.eth_address);
    formData.append('gov_token', this.state.gov_token);
    const config = {
      headers: {
        'content-type': 'multipart/form-data'
      }
    };
    return post(url, formData, config);
  }

  render() {
    return (
      <form onSubmit={this.handleFormSubmit}>
        <h1>Add Participant</h1>
        Telegram ID :{' '}
        <input
          type="text"
          name="telegram_id"
          value={this.state.telegram_id}
          onChange={this.handleValueChange}
        />
        <br />
        ETH Address :{' '}
        <input
          type="text"
          name="eth_address"
          value={this.state.eth_address}
          onChange={this.handleValueChange}
        />
        <br />
        Valid Gov. Token :{' '}
        <input
          type="text"
          name="gov_token"
          value={this.state.gov_token}
          onChange={this.handleValueChange}
        />
        <br />
        <button type="submit">register</button>
      </form>
    );
  }
}

export default AddForm;
