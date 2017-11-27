import math
    
def numberOfSamples(data_set):
    cnt=0
    for topic,samples in data_set.items():
        cnt+=len(data_set[topic])
    return cnt
    
def termFrequency(term,data_set):
    cnt=0.0
    for topic,samples in data_set.items():
        for file_name,token in samples.items():
            if term in token:
                cnt+=1
    return cnt/numberOfSamples(data_set) 
        
def topicFrequency(topic,data_set):
    return len(data_set[topic])/numberOfSamples(data_set)

def termTopicFrequency(topic,term,data_set):
    cnt=0.0
    for file_name,token in data_set[topic].items():
        if term in token:
            cnt+=1
    return cnt/numberOfSamples(data_set) 
    
def informationGain(topic,term,data_set):
    p_t_c=termTopicFrequency(topic,term,data_set)
    p_c=topicFrequency(topic,data_set)
    p_t=termFrequency(term,data_set)
    a=p_t_c*math.log(p_t_c/(p_t*p_c)+1e-100)
    t=(p_c-p_t_c)
    b=t*math.log(t/((1-p_t+1e-6)*(p_c))+1e-100)
    return a+b
        
def findMaxkIGinTopic(topic,vocabulary,data_set,k):
    igs={term:informationGain(topic,term,data_set) for term in vocabulary}
    rv=[]
    for i in range(k):
        k=max(igs,key=igs.get)
        rv.append(k)
        igs.pop(k)
    return rv
    
def topicSpecificFeatures(data_set,vocabulary,k):
    rv=dict()
    for topic in data_set.keys():
        rv[topic]=findMaxkIGinTopic(topic,vocabulary,data_set,k)
    return rv
         
def featureFrequency(feature,document):
    total=0.0
    for k,v in document.items():
        total+=v
    return document[feature]/v
    
def createReferenceClass(data_set,vocabulary):
    rv={v:0 for v in vocabulary}
    for topic,samples in data_set.items():
        for file_name,token in samples.items():
            for k,v in token.items():
                rv[k]+=v
    return {'c0':rv}
    
def topicSpecificFeatureFrequency(feature,topic_samples):
    total=0.0
    fcnt=0.0
    for v in topic_samples.values():
        for vv in v.values():
            total+=vv
        if feature in v:
            fcnt+=v[feature]
    return fcnt/total
    
def topicsSpecificFeaturesFrequency(features,data_set,vocabulary):
    c0=createReferenceClass(data_set,vocabulary)
    rv={}
    for topic,samples in data_set.items():
        t=dict()
        for f in features[topic]:
            a=topicSpecificFeatureFrequency(f,samples)
            b=topicSpecificFeatureFrequency(f,c0)
            t[f]=(a,b)
        rv[topic]=t
    return rv
    
def MBC(x,params):
    z=dict()
    for k in params.keys():
        if k in x.keys():
            z[k]=x[k]
        else:
            if k!='.self':
                z[k]=0
    s=1.0
    t=0.0
    k1=1.0
    k2=1.0
    for k,v in z.items():
        s*=math.factorial(v)
        t+=v
        k1*=params[k][0]**(v)
        k2*=params[k][1]**(v)
    a=(t/s)*k1
    b=(t/s)*k2+1e-300
    return a/b
    
def _classSpecificBayes(x,topic,params):
    return math.log(params['.self'])+math.log(MBC(x,params)+1e-300)
    
def classSpecificBayes(x,params):
    res={t:_classSpecificBayes(x,t,params[t]) for t in params.keys()}
    return max(res,key=res.get)
    
def test():
    pass
    
if __name__=='__main__':
    test()

