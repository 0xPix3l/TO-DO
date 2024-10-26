import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import Signup from './components/Signup';
import TodoList from './components/TodoList';
import Admin from './components/Admin';

function App() {
  const [user, setUser] = useState(null);

  return (
    <Router>
      <div className="App">
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/login" render={() => <Login setUser={setUser} />} />
          <Route path="/signup" component={Signup} />
          <Route path="/todos" render={() => user ? <TodoList user={user} /> : <Redirect to="/login" />} />
          <Route path="/admin" render={() => user && user.username === 'admin' ? <Admin /> : <Redirect to="/" />} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
