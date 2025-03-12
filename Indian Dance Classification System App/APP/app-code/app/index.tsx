import React, { useEffect } from "react";
import {
  View,
  Text,
  ImageBackground,
  StyleSheet,
  Image,
  TouchableOpacity,
} from "react-native";
import { StatusBar } from "expo-status-bar";
import { vw } from "react-native-expo-viewport-units";
import { useRouter } from "expo-router";

const Index = () => {
  const router = useRouter();

  return (
    <View style={styles.root}>
      <StatusBar hidden />
      <ImageBackground
        source={require("../assets/images/homepage.png")}
        style={styles.background}
      >
        <View style={styles.header}>
          <Text style={styles.titleText}>Indian Dance</Text>
          <Text style={styles.titleText}>Form Recognition</Text>
          <Text style={styles.titleText1}>भारतीय नृत्यशैली की पहचान</Text>
        </View>
        <View style={styles.imageContainer}>
          <Image source={require("../assets/images/back.png")} style={styles.image} />
        </View>
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            style={styles.button}
            onPress={() => router.push("/pick")}
          >
            <Text style={styles.buttonText}>GET STARTED</Text>
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
  header: {
    alignItems: "center",
    justifyContent: "flex-start",
    marginTop: 30,
  },
  titleText: {
    fontSize: vw(10),
    color: "#6F4E37",
    fontWeight: "700",
  },
  titleText1: {
    fontSize: vw(8),
    color: "#6F4E37",
    fontWeight: "700",
  },
  imageContainer: {
    alignItems: "center",
    justifyContent: "center",
    margin: 50,
  },
  image: {
    resizeMode: "contain",
  },
  buttonContainer: {
    alignItems: "center",
    justifyContent: "center",
    margin: 35,
  },
  button: {
    height: vw(20),
    width: vw(70),
    backgroundColor: "#86AB89",
    justifyContent: "center",
    alignItems: "center",
    borderRadius: 20,
  },
  buttonText: {
    fontSize: 25,
    fontWeight:"700"
  },
});

export default Index;
