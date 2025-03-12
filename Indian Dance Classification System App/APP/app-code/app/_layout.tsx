import { Stack } from "expo-router";
import { ImageProvider } from "./ImageContext";

export default function RootLayout() {
  return (
    <ImageProvider>
      <Stack>
        <Stack.Screen name="index" options={{ headerShown: false }} />
        <Stack.Screen name="pick" options={{ headerShown: false }} />
        <Stack.Screen name="upload" options={{ headerShown: false }} />
      </Stack>
    </ImageProvider>
  );
}
