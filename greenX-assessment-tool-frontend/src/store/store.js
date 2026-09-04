// import { configureStore } from "@reduxjs/toolkit";
// import { formReducer } from "./formSlice";
// import { questionAnswerReducer } from "./questionAnswersSlice";
// import { api } from "./api";

// const store = configureStore({
//   reducer: {
//     form: formReducer,
//     questionAnswers: questionAnswerReducer,

//     [api.reducerPath]: api.reducer,
//   },
//   middleware: (getDefaultMiddleware) =>
//     getDefaultMiddleware().concat(api.middleware),
// });

// export default store;

import { configureStore } from "@reduxjs/toolkit";
import { formReducer } from "./formSlice";
import { questionAnswerReducer } from "./questionAnswersSlice";
import { api } from "./api";
import storage from "redux-persist/lib/storage"; // defaults to localStorage for web
import { persistReducer, persistStore } from "redux-persist";
import { combineReducers } from "redux";
import {
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from "redux-persist";

const persistConfig = {
  key: "root",
  storage,
};

const rootReducer = combineReducers({
  form: formReducer,
  questionAnswers: questionAnswerReducer,
  [api.reducerPath]: api.reducer,
});

const persistedReducer = persistReducer(persistConfig, rootReducer);

const store = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }).concat(api.middleware),
});

export const persistor = persistStore(store);
export default store;
