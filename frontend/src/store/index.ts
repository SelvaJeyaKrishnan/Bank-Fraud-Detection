import { configureStore } from '@reduxjs/toolkit'
import transactionReducer from '../app/redux/transactionSlice'
import behaviorReducer from '../app/redux/behaviorSlice'
import riskReducer from '../app/redux/riskSlice'

export const store = configureStore({
  reducer: {
    transactions: transactionReducer,
    customerBehavior: behaviorReducer,
    riskAnalysis: riskReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
})

export const persistor = persistStore(store)
export type RootState = ReturnType<store.getState>
export type AppDispatch = typeof store.dispatch