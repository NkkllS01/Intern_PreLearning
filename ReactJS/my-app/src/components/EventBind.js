import React, { Component } from 'react'

class EventBind extends Component {

    constructor(props) {
      super(props)
    
      this.state = {
         message:"Hello"
      }
    }
    clickHandler(){
        this.setState({
            message:"GoodBye"
        })
        console.log()
    }
    
  render() {
    return (
      <div>
        <div>{this.state.message }</div>
        {/* <button onClick={this.clickHandler.bind(this)}>Click Button</button> */}
        <button onClick={()=>this.clickHandler()}>Click Button</button>
      </div>
    )
  }
}

export default EventBind
