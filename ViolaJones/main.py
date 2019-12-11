import sys
import os
import violajones.AdaBoost as AdaBoost
import violajones.Utils as utils
import violajones.IntegralImage as IImg


def testClassifiers(classifiers, facesTestingPath, nonFacesTestingPath):
    print('Loading faces testing data set...')
    facesTesting = utils.load_images(facesTestingPath)
    facesTestingIntegral = list(
        map(IImg.get_integral_image, facesTesting))
    print(str(len(facesTesting)) +
          ' Testing faces data set are loaded!\n')
    print('Loading testing non faces data set...')
    nonFacesTesting = utils.load_images(nonFacesTestingPath)
    nonFacesTestingIntegral = list(
        map(IImg.get_integral_image, nonFacesTesting))
    print(str(len(nonFacesTesting)) +
          ' Testing non faces data set are loaded!\n')

    print('Testing selected classifiers ...')
    correctFacesCount = 0
    correctNonFacesCount = 0
    correctFacesCount = sum(utils.isFaceImgs(
        facesTestingIntegral, classifiers))
    correctNonFacesCount = len(
        nonFacesTesting) - sum(utils.isFaceImgs(nonFacesTestingIntegral, classifiers))
    print('Accuracy:-\nFaces: ' + str(correctFacesCount) + '/' + str(len(facesTesting))
          + '  (' + str((float(correctFacesCount) / len(facesTesting))
                        * 100) + '%)\nNon Faces: '
          + str(correctNonFacesCount) + '/' +
          str(len(nonFacesTesting)) + '  ('
          + str((float(correctNonFacesCount) / len(nonFacesTesting)) * 100) + '%)')


def main():
    #     facesTrainingPath = './DataSet/Training/Faces'
    #     nonFacesTrainingPath = './DataSet/Training/NonFaces'
    classifiersFileName = 'classifiers.pkl'
    facesTrainingPath = './DataSet/Training/Faces'
    nonFacesTrainingPath = './DataSet/Training/NonFaces'
    facesTestingPath = './DataSet/Testing/Faces'
    nonFacesTestingPath = './DataSet/Testing/NonFaces'
    if not os.path.exists(classifiersFileName) or (len(sys.argv) >= 2 and sys.argv[len(sys.argv)-1] == 'relearn'):
        minFeatureHeight = 1
        minFeatureWidth = 1
        maxFeatureHeight = 24
        maxFeatureWidth = 24
        classifiersNum = 4370

        print('Loading faces training data set...')
        facesTraining = utils.load_images(facesTrainingPath)
        facesTrainingIntegral = list(
            map(IImg.get_integral_image, facesTraining))
        print(str(len(facesTraining)) +
              ' Training faces data set are loaded!\n')
        print('Loading non faces training data set...')
        nonFacesTraining = utils.load_images(nonFacesTrainingPath)
        nonFacesTrainingIntegral = list(
            map(IImg.get_integral_image, nonFacesTraining))
        print(str(len(nonFacesTraining)) +
              ' Training non faces data set are loaded!\n')

        classifiers = AdaBoost.adaBoostLearn(facesTrainingIntegral, nonFacesTrainingIntegral,
                                             minFeatureHeight, maxFeatureHeight, minFeatureWidth, maxFeatureWidth, classifiersNum)

        utils.save_classifiers(classifiers, classifiersFileName)

        testClassifiers(classifiers, facesTestingPath, nonFacesTestingPath)

    elif os.path.exists(classifiersFileName):
        classifiers = utils.load_classifiers(classifiersFileName)
        testClassifiers(classifiers, facesTestingPath, nonFacesTestingPath)


main()
