import logo from './logo.svg';
import './App.css';
import RefsDemo from './components/RefsDemo';
import FocusInput from './components/FocusInput';
import FRParentInput from './components/FRParentInput';
import PortalDemo from './components/PortalDemo'
import Hero from './components/Hero'
import ErrorBoundary from './components/ErrorBoundary';
import ClickCounter from './components/ClickCounter';
import HoverCounter from './components/HoverCounter';
import ClickCounterTwo from './components/ClickCounterTwo';
import HoverCounterTwo from './components/HoverCounterTwo';
import User from './components/User'
import Counter from './components/Counter';
import { UserProvider } from './components/userContext';
import ComponentC  from './components/ComponentC'

function App() {
  return (
    <div className="App">
      
      {/* <UserProvider value='Zijie'>
      <ComponentC />
      </UserProvider> */}

      {/* <Counter 
      render={(count,incrementCount)=>(
      <ClickCounterTwo count={count} incrementCount={incrementCount} />
      )}
      />
      <Counter 
      render={(count,incrementCount)=>(
      <HoverCounterTwo count={count} incrementCount={incrementCount} />
      )}
      /> */}
      {/* <ClickCounterTwo/>
      <HoverCounterTwo/>
      <User render = {(isLoggedIn)=>isLoggedIn? 'Zijie':'Guest'}/> */}
    
      {/* <ErrorBoundary>
      <Hero heroName="Batman"></Hero>
      </ErrorBoundary>
      <ErrorBoundary>
      <Hero heroName="Superman"></Hero>
      </ErrorBoundary>
      <ErrorBoundary>
      <Hero heroName="Joker"></Hero>
      </ErrorBoundary> */}
      {/* <PortalDemo></PortalDemo> */}
      {/* <FRParentInput /> */}
      {/* <FocusInput/> */}
      {/* <RefsDemo/> */}
    </div>
  );
}

export default App;
