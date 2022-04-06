import { Route, Switch } from "react-router-dom";
import Login from 'pages/Login'
import Home from 'pages/Home'

function MainPage() {
  return (
    <section className="hero is-fullheight-with-navbar  p-0 m-0">
      <div className="hero-body  p-0 m-0">
        <div className="container is-fluid m-0 p-0">
          <Switch>
            <Route path="/home">
              <Home></Home>
            </Route>
            <Route path="/login" exact>
              <Login></Login>
            </Route>
           
          </Switch>
        </div>
      </div>
    </section>
  );
}
export default MainPage;
