import React, { useState } from "react";
import { View, Button, Image, Text } from "react-native";
import * as ImagePicker from "expo-image-picker";
import { uploadPhoto } from "../../infra/api/photoApi";

export default function PhotoUploadScreen() {
  const [imageUri, setImageUri] = useState<string|undefined>();
  const [detected, setDetected] = useState<number[]>([]);
  const token = "TU_TOKEN"; // obtén de contexto auth

  const pickImage = async () => {
    const res = await ImagePicker.launchCameraAsync({ mediaTypes: ImagePicker.MediaTypeOptions.Images });
    if (!res.cancelled) setImageUri(res.uri);
  };

  const handleUpload = async () => {
    if (!imageUri) return;
    try {
      const { usuarios_detectados } = await uploadPhoto(imageUri, token);
      setDetected(usuarios_detectados);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <View>
      <Button title="Tomar Foto" onPress={pickImage} />
      {imageUri && <Image source={{ uri: imageUri }} style={{ width: 200, height: 200 }} />}
      <Button title="Subir y Procesar" onPress={handleUpload} />
      {detected.length > 0 && (
        <Text>Usuarios detectados: {detected.join(", ")}</Text>
      )}
    </View>
  );
}

