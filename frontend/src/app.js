import { Render, Router, Route, IndexRoute } from 'jumpsuit'
/* state */
import state from 'state/index'
/* screens */
import App from 'screens/index'
import Temperatures from 'screens/temperatures'

Render(state, (
  <Router>
    <Route path='/' component={App}>
      <IndexRoute component={Temperatures} />
    </Route>
  </Router>
))
