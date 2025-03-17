import React, { Component } from 'react'
import { UserConsumer } from './userContext'

class ComponentF extends Component {
  render() {
    return (
      <UserConsumer>
        {
            (s) => {
                return <div>Hello {s} </div>
            }
        }
      </UserConsumer>
    )
  }
} 

export default ComponentF
