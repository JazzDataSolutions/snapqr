src/
├── App.tsx                  # Entry point; enrutamiento
├── navigation/              # React Navigation (stack/tabs)
│   └── index.tsx
├── screens/                 # Pantallas principales
│   ├── LoginScreen.tsx
│   ├── ProfileScreen.tsx
│   ├── QRScannerScreen.tsx
│   └── PhotoUploadScreen.tsx
├── components/              # Componentes reutilizables (Buttons, Inputs)
├── infrastructure/
│   ├── api/
│   │   └── axiosClient.ts
│   └── storage/
│       └── s3Client.ts
└── contexts/                # Contexto Auth (proveer token)
