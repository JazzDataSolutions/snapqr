// mobile/app.config.js
import 'dotenv/config';

export default {
  expo: {
    name: "SnapQR",
    slug: "snapqr",
    platforms: ["ios", "android", "web"],
    version: "1.0.0",
    scheme: "snapqr",
    extra: {
      apiUrl: process.env.API_URL || "http://localhost:8000/v1"
    },
    web: {
      build: {
        babel: {
          include: ["react-native-web"]
        }
      }
    }
  }
};

