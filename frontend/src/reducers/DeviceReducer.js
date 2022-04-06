import Actions from "actions/Device";
import Reducer from "reducers/utils/Reducer";

class Device extends Reducer {
  constructor() {
    super(new Actions());
  }

  reducer = (state, action) => {
    return this.baseReducer(state, action);
  };
}

export default Device;
