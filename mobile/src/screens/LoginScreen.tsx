// src/screens/LoginScreen.tsx
import React, { useState, useContext } from "react";
import { View, TextInput, Button } from "react-native";
import { AuthContext } from "../contexts/AuthContext";

export default function LoginScreen() {
  const { login } = useContext(AuthContext);
  const [email, setEmail] = useState("");
  const [pass, setPass] = useState("");

  return (
    <View>
      <TextInput placeholder="Email" onChangeText={setEmail} />
      <TextInput
        placeholder="Password"
        secureTextEntry
        onChangeText={setPass}
      />
      <Button
        title="Login"
        onPress={() => login(email, pass)}
      />
    </View>
  );
}

