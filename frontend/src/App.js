import React from "react"
import { BrowserRouter as Router } from "react-router-dom";
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import reducers from "./reducers";
import thunk from "redux-thunk";
import MainPage from "pages";

const store = createStore(reducers, undefined, applyMiddleware(thunk));

function App() {
  return (
    <div className="App">
      <div>
        <Provider store={store}>
          <Router>
            <MainPage></MainPage>
          </Router>
        </Provider>
      </div>
    </div>
  );
}

export default App;
