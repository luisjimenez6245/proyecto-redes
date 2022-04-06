import MainPage from "pages";
import { Provider } from "react-redux";
import { BrowserRouter as Router } from "react-router-dom";
import { createStore, applyMiddleware } from "redux";
import reducers from "./reducers";
import thunk from "redux-thunk";

const store = createStore(reducers, undefined, applyMiddleware(thunk));

function App() {
  return (
    <div className="App">
      <Provider store={store}>
        <Router>
          <MainPage></MainPage>
        </Router>
      </Provider>
    </div>
  );
}

export default App;
