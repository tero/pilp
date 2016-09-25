import { Component } from 'jumpsuit'
import { getCurrentTemperatures, getTemperatureHistory } from 'state/temperatures'

export default Component({
  render () {
    return (
      <div className='temperatures'>
        <button onClick={getCurrentTemperatures}>Fetch</button>
        <button onClick={getTemperatureHistory}>History</button>
        {this.props.temperatures[0].Attributes.map((sensor) =>
            <div>{sensor.Name}: {sensor.Value}</div>
        )}
      </div>
    )
  }
}, (state) => ({
  loading: state.temperatures.loading,
  temperatures: state.temperatures.currentTemperatures,
}))
