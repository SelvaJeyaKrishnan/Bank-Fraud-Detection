import { configureStore } from '@reduxjs/toolkit'

export const store = configureStore({
  reducer: {
    transactions: (state: unknown[] = [], _action) => state,
    customerBehavior: (state: Record<string, unknown> = {}, _action) => state,
    riskAnalysis: (state: Record<string, unknown> = {}, _action) => state,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch