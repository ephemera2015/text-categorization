import os
import json
from dataset import readDataSet
from text_processing import getVocabulary,preProcessing,tokenize
from algorithm import topicSpecificFeatures,topicsSpecificFeaturesFrequency,topicFrequency,classSpecificBayes

TRAIN_DATA_SET=r'dataset/train'
TEST_DATA_SET=r'dataset/test'
VOCABULARY='vocabulary'
TF='tf'
TOKEN='token'
FEATURES='features'
TOPIC_FEATURES_FREQUENCY='probs'
PARAMS='params'

def createVocabulary():
    if os.path.exists(VOCABULARY):
        with open(VOCABULARY) as f:
            return f.read().split()
    else:
        data_set=readDataSet(TRAIN_DATA_SET)
        preProcessing(data_set)
        vocabulary=getVocabulary(data_set)
        with open(VOCABULARY,'w') as f:
            for v in vocabulary:
                f.write(v+'\n')
        return vocabulary 

def createToken():
    if os.path.exists(TOKEN):
        with open(TOKEN) as f:
            return json.loads(f.read())
    else:
        data_set=readDataSet(TRAIN_DATA_SET)
        preProcessing(data_set)
        tokenize(data_set)
        with open(TOKEN,'w') as f:
            f.write(json.dumps(data_set))
        return data_set
        
def createClassSpecificFeatures():
    if os.path.exists(FEATURES):
        with open(FEATURES) as f:
            return json.loads(f.read())
    else:
        data_set=createToken()
        vocabulary=createVocabulary()
        features=topicSpecificFeatures(data_set,vocabulary,8)
        with open(FEATURES,'w') as f:
            f.write(json.dumps(features))
        return features
    
def createTopicsSpecificFeaturesFrequency():
    if os.path.exists(TOPIC_FEATURES_FREQUENCY):
        with open(TOPIC_FEATURES_FREQUENCY) as f:
            return json.loads(f.read())
    else:
        features=createClassSpecificFeatures()
        vocabulary=createVocabulary()
        data_set=createToken()
        rv=topicsSpecificFeaturesFrequency(features,data_set,vocabulary)
        with open(TOPIC_FEATURES_FREQUENCY,'w') as f:
            f.write(json.dumps(rv))
        return rv

def createBayesParams():
    if os.path.exists(PARAMS):
        with open(PARAMS) as f:
            return json.loads(f.read())
    else:
        data_set=createToken()
        rv=createTopicsSpecificFeaturesFrequency()
        for topic in data_set.keys():
            rv[topic]['.self']=topicFrequency(topic,data_set)
        with open(PARAMS,'w') as f:
            f.write(json.dumps(rv))
    return rv    
    
def test():
    params=createBayesParams()
    test_data_set=readDataSet(TEST_DATA_SET)
    preProcessing(test_data_set)
    tokenize(test_data_set)
    total=0.0
    s=0.0
    for topic in test_data_set.keys():
        cnt=0.0
        for sample in test_data_set[topic].values():
            if (topic==classSpecificBayes(sample,params)):
                cnt+=1
        print(topic,cnt/len(test_data_set[topic]))
        total+=cnt
        s+=len(test_data_set[topic])
    print('total',total/s)
if __name__=='__main__':
    test()
