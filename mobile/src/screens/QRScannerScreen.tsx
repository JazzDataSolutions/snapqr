// src/screens/QRScannerScreen.tsx
import React, { useState, useContext } from "react";
import { View, Text } from "react-native";
import { BarCodeScanner } from "expo-barcode-scanner";
import { AuthContext } from "../contexts/AuthContext";

export default function QRScannerScreen() {
  const { token } = useContext(AuthContext);
  const [data, setData] = useState<string>();

  const handleBarCode = ({ data }: { data: string }) => {
    setData(data);
    // aquí parseas el JSON y navegas a ProfileScreen
  };

  return (
    <View style={{ flex: 1 }}>
      <BarCodeScanner
        style={{ flex: 1 }}
        onBarCodeScanned={handleBarCode}
      />
      {data && <Text>QR Data: {data}</Text>}
    </View>
  );
}

