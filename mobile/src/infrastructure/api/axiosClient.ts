// mobile/src/infrastructure/api/axiosClient.ts
import axios from "axios";
import Constants from "expo-constants";
import { Platform } from "react-native";

const apiUrl: string = Constants.manifest?.extra?.apiUrl;

// Para Android emulador usa 10.0.2.2 si quieres apuntar al host
const baseURL =
  Platform.OS === "android"
    ? apiUrl.replace("localhost", "10.0.2.2")
    : apiUrl;

export default axios.create({
  baseURL,
  timeout: 5000,
});

