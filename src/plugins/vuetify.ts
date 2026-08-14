import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'auctionLight',
    themes: {
      auctionLight: {
        dark: false,
        colors: {
          // Pure white, per your request — lighter/calmer than the donator app
          background: '#FFFFFF',
          surface: '#FFFFFF',

          // Matches donator app's navbar/sidebar navy exactly
          primary: '#103948',
          secondary: '#103948',
        },
      },
    },
  },
})