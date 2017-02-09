import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.style.use('ggplot')

class discovery():
# data is a pandas dataframe	
	def __init__(self, data , timeSeries=[]):
		self.data = data
		self.columns = data.columns
		self.labelInfo=self.getLabelInfo()

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

# show null bar
	def getNullBar(self):
		nullData=self.labelInfo[['label','null']].sort_values(by='null')
		textLocation=nullData['null'].max()
		f,ax=plt.subplots()
		sns.barplot(x='null',y='label',data=nullData,label='label')
		ax.set_title('Null Rate')
		ax.set_xlabel('')
		pictureLength=ax.get_xbound()[1]
		for p in ax.patches:
		    width=p.get_width()
		    ax.text(width+(pictureLength-textLocation)/2,p.get_y()+p.get_height()/2,str(round(width,2)),ha="center")
		plt.savefig('nullRateAll.png')
		plt.close()
		return nullData			

	