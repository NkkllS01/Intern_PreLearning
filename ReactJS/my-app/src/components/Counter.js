import React,{Component} from "react";

class Counter extends Component{

    constructor(props){
        super(props)
        this.state = {
            count:0
        }
    }
    increment(){
        this.setState({
            count:this.state.count+1
        })
        
        console.log(this.state.count)
    }

    render(){
        return(
        <div>
            <div>Counter - {this.state.count}</div>
            <button onClick={() => this.increment()}>Increment</button>
            <button>Decrease</button>
        </div>
        )
    }
}
export default Counter

