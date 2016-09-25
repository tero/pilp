import { State } from 'jumpsuit'
import _ from 'lodash'
import axios from 'axios'

const temperatureState = State('temperatures', {
  initial: {
    temperatures: [{
        Attributes: []
    }],
    loading: false,
  },

  updateTemperatures: (state, payload) => ({
    loading: true
  }),

  receiveTemperatures: (state, payload) => ({
    temperatures: payload,
    loading: false
  })
})

export default temperatureState

export const getTemperatures = () => {
  axios.get('http://localhost:3000/api/pilp-temperatures/latest')
    .then((response) => {
      console.log(response)
      temperatureState.receiveTemperatures(response.data)
    })
    .catch((err) => {
      temperatureState.receiveTemperatures({})
      console.error(err)
    })
}
