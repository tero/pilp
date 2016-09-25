import { State } from 'jumpsuit'
import _ from 'lodash'
import axios from 'axios'

const temperatureState = State('temperatures', {
  initial: {
    currentTemperatures: [{
        Attributes: []
    }],
    loading: false,
  },

  updateTemperatures: (state, payload) => ({
    loading: true
  }),

  receiveCurrentTemperatures: (state, payload) => ({
    currentTemperatures: payload,
    loading: false
  }),

  receiveTemperatureHistory: (state, payload) => {
    const history = payload.map((row) => {
      return row.Attributes.map((attribute) => {
        return {[attribute.Name]: attribute.Value}
      })
      .reduce((prev, current) => ({...prev, ...current}))
    })
    console.log(history)
    return {history, loading: false}
  }
})

export default temperatureState

export const getCurrentTemperatures = () => {
  axios.get('http://localhost:3000/api/pilp-temperatures/latest')
    .then((response) => {
      console.log(response)
      temperatureState.receiveCurrentTemperatures(response.data)
    })
    .catch((err) => {
      temperatureState.receiveCurrentTemperatures({})
      console.error(err)
    })
}

export const getTemperatureHistory = () => {
    axios.get('http://localhost:3000/api/pilp-temperatures')
    .then((response) => {
        console.log(response)
        temperatureState.receiveTemperatureHistory(response.data)
    })
    .catch((err) => {
        temperatureState.receiveTemperatureHistory({})
        console.error(err)
    })
}
