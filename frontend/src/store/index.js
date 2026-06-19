import { configureStore } from '@reduxjs/toolkit'
import dataReducer from './slices/dataSlice'
import analyticsReducer from './slices/analyticsSlice'

const store = configureStore({
  reducer: {
    data: dataReducer,
    analytics: analyticsReducer,
  },
})

export default store
