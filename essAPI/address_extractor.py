# This code was made initially during internship 
# It may help to extract address from invoice. The idea behind this is to use words position
# along with words to form cluster such , the closest words form cluster of words. 
# if these words contains indian city name or country(INDIA), or state , then definitely
# it would be the address. The address in an invoice is generally in multi lines where 
# space is sorrounded around it and may be labeled or not.
# The following method worked , but it depends on how close the words are in an invoice 
# some invoice has less distance words or other has more distance in between them. 
# So sometimes unnecessary words may also get extracted along with address words. Example
# 10 am xyz bazar, bengaluru. here 10 am may also get inserted depending upon closeness of words
# later NER(named entity recognition machine learning model is used for this particular task)
import re
class ExtractAddress:
  def __init__(self,loc):
     self.location=loc

  def extractWords(self,pageWords):
     self.words=[]
     for word in pageWords:
       self.words.append({"text": word['text'], "left": word['x0'],"top":word['top'],"right":word['x1']})

  def extractLines(self): 
     self.lines={} 
     self.words.sort(key=lambda x:x['top']) 
     for word in self.words:
       if word['top'] in self.lines:
         self.lines[word['top']].append(word)
       else:
         self.lines[word['top']]=[word] 
     for top in self.lines:
       self.lines[top].sort(key=lambda x:x['left'])

  def getAddress(self):
    groupsDict={}
    groupsDict[1]=[]
    groupsCount=0
    thresholdWidth=10
    thresholdHeight=21
    minDist=None
    selectedGroup=None
    for top in self.lines:
      for wordToInsert in self.lines[top]:
        selectedGroup=1
        minHorizontalDist=10000
        minVerticalDist=10000
        for index in range(1,groupsCount+1):
         if len(groupsDict[index])>0: 
          for word in groupsDict[index]:
             if wordToInsert['left']>word['right']:
                distHorizontal=wordToInsert['left']-word['right']
             else:
                distHorizontal=abs(wordToInsert['left']-word['left'])     
             distVertical=abs(word['top']-wordToInsert['top'])
             if distHorizontal<thresholdWidth and distVertical<thresholdHeight:
                selectedGroup=index 
                minHorizontalDist=distHorizontal
                minVerticalDist=distVertical
        if minVerticalDist<=thresholdHeight and minHorizontalDist<=thresholdWidth:
           groupsDict[selectedGroup].append(wordToInsert)       
        else: 
           groupsCount+=1
           groupsDict[groupsCount]=[wordToInsert]

    address=[]
    for index in range(groupsCount):
       groupedText=''
       for word in groupsDict[index+1]:
          groupedText+=' '+word['text']
       if self.isAddress(groupedText):
          address.append(groupedText)
    return address                    
  def isAddress(self,groupedText):
     commasCount=0
     for c in groupedText:
        if c==',':
          commasCount+=1
     if commasCount<3:
        return False
     words=re.findall(r'\w+',groupedText)
     for word in words:
        if word.lower() in self.location:
          return True
     return False   