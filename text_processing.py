from copy import deepcopy
__filters__=('?','!',',',':','.',';','-','_','(',')','[',']','{','}','|','\'','"',
'\\','@','#','$','%','^','&','*','+','=','0','1','2','3','4','5','6','7','8','9','>','<','/','~','`','\n',)

def preProcessingText(text):
    rv=[]
    for ch in text:
        if ch in __filters__:
            rv.append(' ')
        else:
            rv.append(ch)
    return ''.join(rv).lower()

def preProcessing(data_set):
    for k,v in data_set.items():
        for kk,vv in v.items():
            v[kk]=preProcessingText(vv)

def getVocabulary(data_set):
    rv=set()
    for c in data_set.values():
        for cc in c.values():
            for ccc in cc.split():
                rv.add(ccc)
    topics=[ a for k in data_set.keys() for a in k.split('.')]
    for x in topics:
        try:
            rv.remove(x)
        except:
            pass
    return rv   


def tokenize(data_set):
    topics=[ a for k in data_set.keys() for a in k.split('.')]
    for k,v in data_set.items():
        for kk,vv in v.items():
            t=vv.split()
            x=set(t)
            tt=dict()
            for y in x :
                if y not in topics:
                    tt[y]=t.count(y)
            v[kk]=tt
               
def test():
    pass

if __name__=='__main__':
    test()

