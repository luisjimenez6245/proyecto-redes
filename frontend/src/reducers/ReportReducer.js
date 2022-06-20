import Actions from "actions/Report";
import Reducer from "reducers/utils/Reducer";

class Report extends Reducer {
  constructor() {
    super(new Actions());
  }

  reducer = (state, action) => {
    return this.baseReducer(state, action);
  };
}

export default Report;
