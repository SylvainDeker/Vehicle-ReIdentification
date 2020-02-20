def getSemantic(imageName):
  return(np.loadtxt(imageName))

def saveSemantic(imageName,features):
  np.savetxt(imageName,features)

def prepareSemanticDataSet(featureExtractor):
  for file in os.listdir("./VeRi_with_plate/image_train/"):
    img = image.load_img(file, target_size=(IMG_HEIGHT, IMG_WIDTH))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = featureExtractor.predict(x)
    saveSemantic('./semanticFolder/'+file,features)

def googleNetScore(img_path,featureExtractor):
  semanticScore = []
  name = []
  img = image.load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  x = preprocess_input(x)
  features = featureExtractor.predict(x)

  for file in os.listdir("./semanticFolder/"):
    semanticScore = semanticScore.append(distance.euclidean(features,getSemantic(file)))
    name = name.append(file)
  newListe = list(zip(semanticScore, name))
  return(newListe)

featureExtractor = load_model("./featureExtractor_model.hdf5")
featureExtractor.load_weights("./featureExtractor_weight.hdf5")
