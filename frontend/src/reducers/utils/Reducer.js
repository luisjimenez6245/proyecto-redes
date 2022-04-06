import * as Const from "reducers/utils/Const";

class Reducer
{
  ref;
  initialState = { dataset: [] };

  constructor(ref)
  {
    this.ref = ref;
  }
  
  baseReducer = (state = this.initialState, action) =>
  {
    
    const type = action.type;

    if (type === `${this.ref.id}_${Const.GET_LIST}`) {
      let merge = this.mergeDataset(state.dataset, action.dataset);
      if (merge.changed)
        return Object.assign({}, state, {
          dataset: merge.dataset
        });
    }

    if (type === `${this.ref.id}_${Const.GET_ITEM}` ||
      type === `${this.ref.id}_${Const.POST}` ||
      type === `${this.ref.id}_${Const.PUT}`) {
      let merge = this.mergeDataset(state.dataset, [action.data]);
      if (merge.changed)
        return Object.assign({}, state, {
          dataset: merge.dataset
        });
    }

    if (type === `${this.ref.id}_${Const.DELETE}`) {
      let deleted = this.find(state.dataset, action.id);
      let dataset = state.dataset.splice(0);
      dataset.splice(deleted.pos, 1);
      return Object.assign({}, state, {
        dataset: dataset
      });
    }

    return state;
  }

  isEmpty = (obj) => Object.keys(obj).length === 0;

 

  mergeDataset(original, dataset)
  {
    let result = original.slice(0);
    let changed = false;
   
    return {
      changed: changed,
      dataset: result
    };
  }
}
export default Reducer;