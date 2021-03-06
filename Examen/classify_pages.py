# -*- coding: utf-8 -*-

import argparse
import logging
import time
import sys
import os

from tqdm import tqdm
import pandas as pd
from PIL import Image, ImageFilter
from sklearn.cluster import KMeans
from sklearn import svm, metrics, neighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

import numpy as np

import matplotlib.pyplot as plt

# Setup logging
logger = logging.getLogger('classify_pages.py')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)

IMG_FEATURE_SIZE = (12, 16)

def extract_features_subresolution(img,img_feature_size = (8, 8)):
    # convert color images to grey level
    gray_img = img.convert('L')
    # find the min dimension to rotate the image if needed
    min_size = min(img.size)
    if img.size[1] == min_size:
        # convert landscape  to portrait
        rotated_img = gray_img.rotate(90, expand=1)
    else:
        rotated_img = gray_img

    # reduce the image to a given size
    reduced_img = rotated_img.resize(
        IMG_FEATURE_SIZE, Image.BOX).filter(ImageFilter.SHARPEN)

    # return the values of the reduced image as features
    return [255 - i for i in reduced_img.getdata()]

def hyperoptize_knn(X_train,Y_train,X_test,Y_test):
    # Create validation set so that train = 60% , validation = 20% and test =  20%
    X_train_hyper, X_valid_hyper, Y_train_hyper, Y_valid_hyper = train_test_split(X_train, Y_train, test_size=0.20, random_state=42)

    for k in [1,2,3,4,5,6,7,8,9,10]:
        logger.info("k={}".format(k))
        clf = neighbors.KNeighborsClassifier(k)
        clf.fit(X_train_hyper,Y_train_hyper)


        for _name,_train_set,_test_set in [('train',X_train_hyper,Y_train_hyper),('valid',X_valid_hyper,Y_valid_hyper),('test',X_test,Y_test)]:

            _predicted = clf.predict(_train_set)
            _accuracy = metrics.accuracy_score(_test_set, _predicted)
            logger.info("{} accuracy : {}".format(_name,_accuracy))



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract features, train a classifier on images and test the classifier')
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--images-list',help='file containing the image path and image class, one per line, comma separated')
    input_group.add_argument('--load-features',help='read features and class from pickle file')
    parser.add_argument('--save-features',help='save features in pickle format')
    parser.add_argument('--limit-samples',type=int, help='limit the number of samples to consider for training')
    classifier_group = parser.add_mutually_exclusive_group(required=False)
    classifier_group.add_argument('--nearest-neighbors',type=int)
    classifier_group.add_argument('--features-only', action='store_true', help='only extract features, do not train classifiers')
    classifier_group.add_argument('--logistic-regression', action='store_true')
    classifier_group.add_argument('--knn', action='store_true')
    curve_group = parser.add_mutually_exclusive_group(required=False)
    curve_group.add_argument('--learning-curve', action='store_true')
    args = parser.parse_args()


    if args.load_features:
        # read features from to_pickle
        df_features = pd.read_pickle(args.load_features+'.pickle')
        if args.limit_samples:
            df_features=df_features.sample(n=args.limit_samples)
        Y = list(df_features['class'])
        X = df_features.drop(columns='class')
        pass
    else:


        # Load the image list from CSV file using pd.read_csv
        # see the doc for the option since there is no header ;
        # specify the column names :  filename , class
        file_list = []
        colnames = ["filename", "class", "name"]
        filename = args.images_list
        file_list = pd.read_csv(args.images_list, header=None, names=colnames)
        print(file_list)
        #logger.info('Loaded {} images in {}'.format(all_df.shape,args.images_list))


        # Extract the feature vector on all the pages found
        # Modify the extract_features from TP_Clustering to extract 8x8 subresolution values
        # white must be 0 and black 255
        data = []
        for i_path in tqdm(file_list.filename):
            if os.path.exists(i_path):
                page_image = Image.open(i_path)
                data.append(extract_features_subresolution(page_image))

        # check that we have data
        if not data:
            logger.error("Could not extract any feature vector or class")
            sys.exit(1)



        # convert to np.array
        X = np.array(data)
        Y = file_list['class']



    # save features
    if args.save_features:
        df_features = pd.DataFrame(X)
        df_features['class'] = Y
        df_features.to_pickle(args.save_features+'.pickle')
        # convert X to dataframe with pd.DataFrame and save to pickle with to_pickle
        logger.info('Saved {} features and class to {}'.format(df_features.shape,args.save_features))


    if args.features_only:
        logger.info('No classifier to train, exit')
        sys.exit()

    # Train classifier
    logger.info("Training Classifier")

    # Use train_test_split to create train/test split
    #X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, train_size=0.2)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)


    logger.info("Train set size is {}".format(X_train.shape))
    logger.info("Test set size is {}".format(X_test.shape))
    #logger.info("Validation set size is {}".format(X_validation.shape))

    if args.nearest_neighbors:
        # create KNN classifier with args.nearest_neighbors as a parameter
        clf = KNeighborsClassifier(args.nearest_neighbors)
        logger.info('Use kNN classifier with k= {}'.format(args.nearest_neighbors))

    elif args.logistic_regression:
        clf = LogisticRegression()
        logger.info('Use logistic regression')

    elif args.knn:
        hyperoptize_knn(X_train, Y_train, X_test, Y_test)

    else:
        logger.error('No classifier specified')
        sys.exit()

    def printaccuracy(sizeTrain,X_train,Y_train):
        X_train, X_none, Y_train, Y_none = train_test_split(X_train,Y_train,train_size=sizeTrain)
        clf.fit(X_train,Y_train)
        predicted = clf.predict(X_test)
        return metrics.accuracy_score(Y_test,predicted),clf.score(X_train, Y_train)

    if args.learning_curve:
        curb_y = []
        curb_y2 = []
        training_size = np.array([0.01, 0.10, 0.20, 0.40, 0.60, 0.80, 0.99])
        curb_x = df_features.shape[0] * np.array(training_size)
        for i in range(0, 7):
            curb_y.append(printaccuracy(training_size[i], X_train, Y_train)[0])
            curb_y2.append(printaccuracy(training_size[i], X_train, Y_train)[1])

        plt.plot(curb_x, curb_y)
        plt.plot(curb_x, curb_y2)
        plt.title("Training curves")
        plt.xlabel("Train set size")
        plt.ylabel("Accuracy")
        plt.show()

    # Do Training@
    t0 = time.time()
    clf.fit(X_train, Y_train)
    logger.info("Training  done in %0.3fs" % (time.time() - t0))

    # Do testing
    logger.info("Testing Classifier")
    t0 = time.time()
    predicted = clf.predict(X_test)

    # Print score produced by metrics.classification_report and metrics.accuracy_score
    print(metrics.classification_report(Y_test, predicted))
    print(metrics.accuracy_score(Y_test, predicted))
    logger.info("Testing  done in %0.3fs" % (time.time() - t0))
