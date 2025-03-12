import React, { useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  Image,
  StatusBar,
  ImageBackground,
  TouchableOpacity,
  ActivityIndicator,
} from "react-native";
import { useImageContext } from "./ImageContext";
import { vw } from "react-native-expo-viewport-units";
import Toast from "react-native-toast-message";
import { storage, database } from "../config";
import {
  ref as storageRef,
  uploadBytes,
  getDownloadURL,
} from "firebase/storage";
import {
  ref as databaseRef,
  onValue,
  ref,
  remove as removeDatabase,
} from "firebase/database";
import Feather from "@expo/vector-icons/Feather";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import { useRouter } from "expo-router";

const Upload = () => {
  const { cameraImage, galleryImage, clearImages } = useImageContext();
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState<string | null>(null);

  const imageUri = cameraImage || galleryImage;
  const router = useRouter();

  const formatDate = () => {
    const now = new Date();

    const day = String(now.getDate()).padStart(2, "0");
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const year = now.getFullYear();

    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const seconds = String(now.getSeconds()).padStart(2, "0");

    return `${day}${month}${year}_${hours}${minutes}${seconds}`;
  };

  const handleUpload = async () => {
    if (!imageUri) return;

    setLoading(true);

    try {
      const filename = formatDate() + ".jpg";
      const imageStorageRef = storageRef(storage, `images/${filename}`);

      const response = await fetch(imageUri);
      const blob = await response.blob();
      await uploadBytes(imageStorageRef, blob);

      const downloadURL = await getDownloadURL(imageStorageRef);

      Toast.show({
        type: "success",
        text1: "Image uploaded successfully!",
        position: "bottom",
      });

      const predictionRef = databaseRef(database, "prediction");
      const handleValueChange = (snapshot: any) => {
        const data = snapshot.val();
        if (data) {
          const keys = Object.keys(data);
          const firstKey = keys[0];
          setPrediction(data[firstKey]);

          setLoading(false);

          removeDatabase(ref(database, `prediction/${firstKey}`));
        }
      };
      onValue(predictionRef, handleValueChange);
    } catch (error) {
      console.error("Upload failed:", error);
      setLoading(false);
      Toast.show({
        type: "error",
        text1: "Upload failed. Please try again.",
        position: "bottom",
      });
    }
  };

  const homePageClick = () => {
    clearImages();
    router.push("/");
  };

  return (
    <View style={styles.root}>
      <StatusBar hidden />
      <ImageBackground
        style={styles.background}
        source={require("../assets/images/upload.png")}
      >
        <View style={styles.container}>
          {imageUri ? (
            <View style={styles.imageContainer}>
              <Image source={{ uri: imageUri }} style={styles.image} />
            </View>
          ) : (
            <Text style={styles.noImageText}>No images to display</Text>
          )}

          {loading ? (
            <ActivityIndicator
              size={vw(15)}
              style={{ marginTop: vw(6) }}
              color="#0000ff"
            />
          ) : prediction ? (
            <View style={{ marginTop: vw(6), alignItems: "center" }}>
              <View style={styles.predictionContainer}>
                <Text style={styles.predictionText}>Name of dance form:</Text>
                <View style={styles.predictionContainer}>
                  <Text style={styles.predictionText}>{prediction}</Text>
                </View>
              </View>
              <TouchableOpacity style={styles.button1} onPress={homePageClick}>
                <FontAwesome name="home" size={vw(9)} color="black" />
                <Text style={styles.text1}>Home Page</Text>
              </TouchableOpacity>
            </View>
          ) : (
            <View style={styles.buttonContainer}>
              <TouchableOpacity style={styles.button} onPress={handleUpload}>
                <Feather name="upload" size={vw(10)} color="black" />
                <Text style={styles.text}>UPLOAD</Text>
              </TouchableOpacity>
            </View>
          )}
        </View>
      </ImageBackground>

      <Toast />
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
  container: {
    flex: 1,
    padding: 25,
    justifyContent: "flex-start",
  },
  imageContainer: {
    marginVertical: 4,
  },
  image: {
    width: "100%",
    height: vw(80),
    resizeMode: "cover",
    borderRadius: 40,
  },
  noImageText: {
    fontSize: 16,
    color: "gray",
  },
  predictionContainer: {
    width: "100%",
    justifyContent: "center",
    alignItems: "center",
  },
  predictionText: {
    fontSize: vw(8),
    fontWeight: "bold",
    color: "green",
  },
  buttonContainer: {
    justifyContent: "center",
    alignItems: "center",
    marginTop: vw(10),
  },
  button: {
    height: vw(15),
    width: vw(60),
    justifyContent: "space-evenly",
    alignItems: "center",
    borderRadius: 20,
    borderWidth: 4,
    flexDirection: "row",
  },
  text: {
    fontSize: vw(8),
    fontWeight: "600",
  },
  button1: {
    height: vw(15),
    width: vw(50),
    marginTop: vw(5),
    justifyContent: "space-evenly",
    alignItems: "center",
    borderRadius: 20,
    borderWidth: 4,
    flexDirection: "row",
  },
  text1: {
    fontSize: vw(6),
    fontWeight: "600",
  },
});

export default Upload;
