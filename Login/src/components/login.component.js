import React, { Component } from 'react'

export default class Login extends Component {
  render() {
    return (
      <form>
        <h3>Log In - Welcome</h3>

        <div className="mb-3">
          <label>User Name</label>
          <input
            type="username"
            className="form-control"
            placeholder="Enter user name"
          />
        </div>

        <div className="mb-3">
          <label>Password</label>
          <input
            type="password"
            className="form-control"
            placeholder="Enter password"
          />
        </div>

        <div className="d-grid">
          <button type="submit" className="btn btn-primary">
            Log In
          </button>
        </div>
        <br></br>
            <p className="forgot-password text-right">
               New user? <a href="./sign-up">Sign Up</a>
            </p>
      </form>
    )
  }
}
