import React, { Component } from 'react'

class UserGreeting extends Component {
    constructor(props) {
      super(props)
    
      this.state = {
         isLoggedIn:true
      }
    }
    
  render() {
    return this.state.isLoggedIn && <div>Welcome Zijie</div>
    // return(
    //     this.state.isLoggedIn?
    //     <div>Welcome Zijie</div>:
    //     <div>Welcome Guest</div>
    // )
    // if(this.state.isLoggedIn){
    //     return(
    //         <div>
    //             Welcome Zijie
    //         </div>         
    //     )
    // }else{
    //     return(
    //     <div>Welcome Guest</div>
    //     )    
    //     }
    // }
    // return (
    //     <div>
    //         <div>Welcome Zijie</div>
    //         <div>Welcome Guest</div>
    //     </div>   
    // )
  }
}

export default UserGreeting;
