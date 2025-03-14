import logo from './logo.svg';
import './App.css';
import RefsDemo from './components/RefsDemo';
import FocusInput from './components/FocusInput';
import FRParentInput from './components/FRParentInput';


function App() {
  return (
    <div className="App">
      <FRParentInput />
      {/* <FocusInput/> */}
      {/* <RefsDemo/> */}
    </div>
  );
}

export default App;
