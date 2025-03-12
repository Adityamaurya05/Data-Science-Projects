import React, { createContext, useContext, useState, ReactNode } from "react";

interface ImageContextType {
  cameraImage: string | null;
  setCameraImage: (uri: string | null) => void;
  galleryImage: string | null;
  setGalleryImage: (uri: string | null) => void;
  clearImages: () => void;
}

const ImageContext = createContext<ImageContextType | undefined>(undefined);

export const ImageProvider = ({ children }: { children: ReactNode }) => {
  const [cameraImage, setCameraImage] = useState<string | null>(null);
  const [galleryImage, setGalleryImage] = useState<string | null>(null);

  const clearImages = () => {
    setCameraImage(null);
    setGalleryImage(null);
  };

  return (
    <ImageContext.Provider
      value={{
        cameraImage,
        setCameraImage,
        galleryImage,
        setGalleryImage,
        clearImages,
      }}
    >
      {children}
    </ImageContext.Provider>
  );
};

export const useImageContext = () => {
  const context = useContext(ImageContext);
  if (!context) {
    throw new Error("useImageContext must be used within an ImageProvider");
  }
  return context;
};
