import React,{Component} from 'react'

class Message extends Component{

    constructor(){
        super()
        this.state = {
            message:"Welcome Visitor"
        }
        
    }
    changeState(){
        this.setState({
            message:'Thank you for subcribing'
        })
    }


    render(){
        return (
        <div>
            <h1>{this.state.message}</h1>
            <button onClick={()=> this.changeState()}>Subcribe</button>
        </div>
            
        )
    }
}

export default Message