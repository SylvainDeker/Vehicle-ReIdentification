def getSementic(imageName):
  return(np.loadtxt(imageName))

def saveSementic(imageName,features):
  np.savetxt(imageName,features)

def prepareSementicDataSet(featureExtractor):
  for file in os.listdir("./vehicule/"):
    img = image.load_img(file, target_size=(IMG_HEIGHT, IMG_WIDTH))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = featureExtractor.predict(x)
    saveSementic('./sementicFolder/'+file,features)
	
def googleNetScore(img_path,featureExtractor):
  sementicScore = []
  name = []
  img = image.load_img(img_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis=0)
  x = preprocess_input(x)
  features = featureExtractor.predict(x)

  for file in os.listdir("./sementicFolder/"):
    sementicScore = sementicScore.append(distance.euclidean(features,getSementic(file)))
    name = name.append(file)
  listeTrie = list(zip(sementicScore, name))
  newListe = sorted(listeTrie, key=lambda score: score[0])
  return(newListe)
  
featureExtractor = load_model("./featureExtractor_model.hdf5")
featureExtractor.load_weights("./featureExtractor_weight.hdf5")