// mobile/src/infrastructure/api/axiosClient.ts
import axios from 'axios';
import Constants from 'expo-constants';
import { Platform } from 'react-native';

const { extra } = Constants.manifest || (Constants as any).expoConfig;
let baseURL = extra.apiUrl as string;

// En Android emulador
if (Platform.OS === 'android') {
  baseURL = baseURL.replace('localhost', '10.0.2.2');
}

export default axios.create({
  baseURL,
  timeout: 5000,
});

