import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.style.use('ggplot')

class discovery():
# data is a pandas dataframe	
	def __init__(self, data , timeSeries=[]):
		self.data = data
		self.columns = data.columns

	def sayHello(self):
		print(self.data)

# label is category or number
	def getLabelInfo(self):	
		labels=self.columns
		data=self.data
		labelInfo=pd.DataFrame({'label':labels})
		labelInfo['type']=labelInfo.apply(lambda x:data[x['label']].dtype,axis=1)
		labelInfo['count']=data.shape[0]
		labelInfo['unique']=labelInfo.apply(lambda x:len(data[x['label']].unique()),axis=1)
		labelInfo['null']=labelInfo.apply(lambda x:np.sum(data[x['label']].isnull())/x['count'],axis=1)
		labelInfo['isCategory']=labelInfo['unique']<(labelInfo['count']/2)
		return labelInfo

		