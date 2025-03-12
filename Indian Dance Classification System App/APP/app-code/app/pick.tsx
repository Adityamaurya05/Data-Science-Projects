import React from "react";
import {
  View,
  Text,
  StyleSheet,
  ImageBackground,
  StatusBar,
  TouchableOpacity,
} from "react-native";
import { vw } from "react-native-expo-viewport-units";
import AntDesign from "@expo/vector-icons/AntDesign";
import * as ImagePicker from "expo-image-picker";
import { useImageContext } from "./ImageContext";
import { useRouter } from "expo-router";

const Pick = () => {
  const { setCameraImage, setGalleryImage } = useImageContext();
  const router = useRouter();

  const clickImage = async () => {
    let result = await ImagePicker.launchCameraAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      allowsEditing: false,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      setCameraImage(result.assets[0].uri);
      router.push("/upload");
    }
  };

  const pickImage = async () => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.All,
      allowsEditing: false,
      aspect: [4, 3],
      quality: 1,
    });

    if (!result.canceled) {
      setGalleryImage(result.assets[0].uri);
      router.push("/upload");
    }
  };

  return (
    <View style={styles.root}>
      <StatusBar hidden />
      <ImageBackground
        style={styles.background}
        source={require("../assets/images/camera.png")}
      >
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.button} onPress={clickImage}>
            <AntDesign
              name="camerao"
              size={vw(15)}
              style={styles.icon}
              color="black"
            />
            <Text style={styles.text}>Camera</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.button} onPress={pickImage}>
            <AntDesign
              name="picture"
              size={vw(15)}
              color="black"
              style={styles.icon}
            />
            <Text style={styles.text}>Gallery</Text>
          </TouchableOpacity>
        </View>
      </ImageBackground>
    </View>
  );
};

const styles = StyleSheet.create({
  root: {
    flex: 1,
  },
  background: {
    flex: 1,
    resizeMode: "contain",
  },
  buttonContainer: {
    justifyContent: "center",
    alignItems: "center",
    marginTop: vw(15),
  },
  button: {
    height: vw(20),
    width: vw(80),
    borderRadius: 20,
    backgroundColor: "#EDB257",
    flexDirection: "row",
    alignItems: "center",
  },
  text: {
    fontSize: vw(11),
    marginLeft: vw(6),
    fontWeight: "600",
  },
  icon: {
    marginLeft: vw(7),
  },
});

export default Pick;
