import Actions from "actions/UserType";
import Reducer from "reducers/utils/Reducer";

class UserType extends Reducer {
  constructor() {
    super(new Actions());
  }

  reducer = (state, action) => {
    return this.baseReducer(state, action);
  };
}

export default UserType;
