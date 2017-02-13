import numpy as np
import scipy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.style.use('ggplot')


class discovery():
    # data is a pandas dataframe
    def __init__(self, data, timeSeries=[]):
        self.data = data
        self.columns = data.columns
        self.labelInfo = self.getLabelInfo()
        self.labelCount = len(self.labelInfo)

    # label is category or number
    def getLabelInfo(self):
        labels = self.columns
        data = self.data
        labelInfo = pd.DataFrame({'label': labels})
        labelInfo['type'] = labelInfo.apply(lambda x: data[x['label']].dtype, axis=1)
        labelInfo['count'] = data.shape[0]
        labelInfo['unique'] = labelInfo.apply(lambda x: len(data[x['label']].unique()), axis=1)
        labelInfo['null'] = labelInfo.apply(lambda x: np.sum(data[x['label']].isnull()) / x['count'], axis=1)
        labelInfo['isNumber'] = labelInfo.apply(lambda x: np.issubdtype(data[x['label']], np.number), axis=1)
        labelInfo['isCategory'] = (labelInfo['unique'] < (labelInfo['count'] / 2)) | ~(labelInfo['isNumber'])
        return labelInfo

    # show null bar
    def getNullData(self):
        nullData = self.labelInfo[['label', 'null']].sort_values(by='null')
        if np.sum(nullData.null) == 0:
            nullData = None
        else:
            nullData = nullData[nullData.null > 0]
            # self.drawBar(nullData, 'null', 'label', 'label', nullData['null'].max(), 'Null Rate', 'nullRateAll')
        return nullData

    # the top pie of all,show number of labels and their types
    def getOverviewPie(self):
        categoryData = self.labelInfo[['label', 'isCategory']]
        categoryCount = categoryData.isCategory.sum()
        x = [categoryCount, self.labelCount - categoryCount]
        label = ['Category', 'Number']
        # self.drawPie(x, label, 'Overview', 'overview', '%1.0f')
        return x, label

    def getAllNumber(self):
        data = self.data[self.labelInfo[~self.labelInfo['isCategory']]['label'].values]
        return data

    def getAllCategory(self):
        data = self.data[self.labelInfo[self.labelInfo['isCategory']]['label'].values]
        return data

    def getLabelCorr(self):
        correlation = {}
        data = self.getAllNumber()
        corr = data.corr()
        labels = data.columns
        for i in labels:
            tmp = corr[i]
            tmp = tmp[(np.fabs(tmp) < 1) & (np.fabs(tmp) > .5)]
            correlation[i] = tmp.index.values
        usefulCorrKey = [{key: correlation[key]} for key in correlation if len(correlation[key]) > 0]
        dataAppend = []
        for i in usefulCorrKey:
            thisKey = list(i.keys())[0]
            for corlabel in i[thisKey]:
                newData = [thisKey, corlabel, corr.loc[thisKey, corlabel]]
                dataAppend.append(newData)
        labelCorr = pd.DataFrame(dataAppend, columns=['label', 'corLabel', 'correlation'])
        return labelCorr.drop_duplicates('correlation')

    def calculateLabelCorrelation(self, correlation):
        data = self.data
        corrDict = {}
        for key in correlation:
            corrDict[key] = []
            for corKey in correlation[key]:
                perason = scipy.stats.pearsonr(data[key], data[corKey])
                corrDict[key].append(perason)
        return corrDict

    # data:pd.dataFrame
    # x:x axis label
    # y:y axis label
    # label:label axis label
    # textLocation:distance from text to bar
    # title:title of picture
    # file:file name of picture
    def drawBar(self, data, x, y, label, textLocation, title, file):
        f, ax = plt.subplots()
        sns.barplot(x=x, y=y, data=data, label=y)
        ax.set_title(title)
        ax.set_xlabel('')
        pictureLength = ax.get_xbound()[1]
        for p in ax.patches:
            width = p.get_width()
            ax.text(width + (pictureLength - textLocation) / 2, p.get_y() + p.get_height() / 2, str(round(width, 2)),
                    ha="center")
        plt.savefig(r'work/picture/' + file + '.png')
        plt.close()

    def drawPie(self, x, label, title, file, autopct):
        plt.pie(x, labels=label, autopct=autopct)
        plt.savefig(r'work/picture/' + file + '.png')
        plt.close()

    def drawOverviewNumber(self, data, title, file):
        columns = data.columns
        dataCount = len(columns)
        row = np.ceil(dataCount / 3.)
        for i in range(dataCount):
            plt.subplot(row, 3, i + 1)
            sns.distplot(data[columns[i]])
        plt.suptitle(title)
        plt.savefig(r'work/picture/' + file + '.png')
        plt.close()

    def drawHist(self, data, file):
        label = data.name
        data = data.dropna()
        sns.distplot(data)
        plt.title(r'{}: $\mu={}$, $\sigma={}$'.format(label, round(data.mean(), 2), round(data.std(), 2)))
        plt.xlabel(r'Number of {}'.format(label))
        plt.ylabel(r'Probability density')
        plt.savefig(r'work/picture/' + file + '.png')
        plt.close()

    def drawLine(self, data, file):
        label = data.name
        data = data.dropna()
        plt.plot(data)
        plt.title(r'{}: $\mu={}$'.format(label, round(data.mean(), 2)))
        plt.xlabel(r'Timeline of {}'.format(label))
        plt.ylabel(r'Number of {}'.format(label))
        plt.savefig(r'work/picture/' + file + '.png')
        plt.close()

    def report(self):
        data = self.data
        numbericData = self.getAllNumber()
        categoricData = self.getAllCategory()
        # show overview info
        overview_label = self.labelInfo
        # draw all types pie
        x, y = self.getOverviewPie()
        self.drawPie(x, y, 'Overview', 'overview', '%3.1f%%')
        # draw all numberic label hist
        self.drawOverviewNumber(numbericData, 'All numberic Labels', 'overview_numberic')
        overview_null = self.getNullData()
        if overview_null is not None and len(overview_null) > 0:
            # draw null bar
            self.drawBar(overview_null, 'null', 'label', 'label', overview_null['null'].max(), 'Null Rate',
                         'nullRateAll')
        overview_corr = self.getLabelCorr()
