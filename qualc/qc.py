'''
Author: Yingjie Peng
Date: 2022-04-02 19:16:47
LastEditTime: 2022-04-04 14:45:12
LastEditors: Yingjie Peng
Description: Define by yourself
FilePath: /QC/qualc/qc.py

'''
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from matplotlib import pyplot as plt
import pandas as pd 
import seaborn as sns
from sklearn.svm import OneClassSVM
import numpy as np
from .freesurfer import outlierTable

def create_plot_style():
    plt.style.use('ggplot')
    plt.rcParams['font.size'] = 10
    plt.rcParams['figure.autolayout'] = True
    plt.rcParams['figure.figsize'] = (8, 6)
    # dpi 100
    plt.rcParams['figure.dpi'] = 100
    # ytick.major.size : 5
    plt.rcParams['ytick.major.size'] = 5
    # xtick.major.size : 5
    plt.rcParams['xtick.major.size'] = 5
    # xtick.labelsize : small
    plt.rcParams['xtick.labelsize'] = 'small'
    # ytick.labelsize : small
    plt.rcParams['ytick.labelsize'] = 'small'
    # legend.fontsize : small
    plt.rcParams['legend.fontsize'] = 'small'
    # grid do not display
    plt.rcParams['axes.grid'] = False

# Create a plot style
create_plot_style()


def check_column_threshold(feature,column_name,threshold=0.5,ax=None):
    if ax is None:
        fig,ax = plt.subplots(1,1,figsize=(8,4))
    sns.kdeplot(feature[column_name],shade=True,color='#003460',ax=ax,label='{} distribution'.format(column_name),linewidth=2)
    ax.axvline(threshold,linestyle='--',label='threshold-{}'.format(threshold),lw=2,c='black')
    ax.set_title('{} distribution'.format(column_name))
    ax.set_xlabel(column_name)
    ax.set_ylabel('Density')
    ax.legend()
    fd_threshold_delete_ids = feature[feature[column_name]>threshold]['subject_id'].tolist()
    return fd_threshold_delete_ids,ax


def column_threshold_bar_plot(feature,column_name,threshold=0.5,ax=None):
    if ax is None:
        fig,ax = plt.subplots(1,1,figsize=(8,4))
    # bar plot
    feature.sort_values(column_name).plot.bar(x='subject_id',y=column_name,ax=ax,color='#6e9bc5',label='{} distribution'.format(column_name),linewidth=2)
    ax.axhline(threshold,linestyle='--',label='threshold-{}'.format(threshold),lw=2,c='black')
    ax.set_title('{} distribution'.format(column_name))
    ax.set_xlabel('subject_id')
    ax.set_ylabel('Outlier Density')
    ax.legend()
    fd_threshold_delete_ids = feature[feature[column_name]>threshold]['subject_id'].tolist()
    return fd_threshold_delete_ids,ax

class BaseQC(object):
    def __init__(self,features:pd.DataFrame,target_label=None,drop_columns=[]) -> None:
        # delete features
        self.feature = features.drop(columns=drop_columns)
        self.delete_subject_ids = []
        self.target_label = target_label
        if 'subject_id' not in self.feature.columns:
            raise ValueError('subject_id column not found')
        self.threshold_delete_ids = None 
        self.svm_one_classifier_delete_ids =None
    def check_column_threshold(self,column_name,threshold=0.5,ax=None,plot_type='distribution'):
        """
        check column threshold

        Args:
            column_name (str): column name
            threshold (float): threshold
            ax (matplotlib.axes._subplots.AxesSubplot): ax
            plot_type (str): plot type ('distribution' or 'bar')
        """
        if plot_type == 'distribution':
            self.threshold_delete_ids,ax = check_column_threshold(self.feature,column_name,threshold,ax)
        else:
            self.threshold_delete_ids,ax = column_threshold_bar_plot(self.feature,column_name,threshold,ax)
        self.delete_subject_ids += self.threshold_delete_ids
        return ax
       
    
    def tsne(self,ax=None):
        """
        tsne plot
        Args:
            ax (matplotlib.axes._subplots.AxesSubplot, optional): ax. Defaults to None.
        """
        if ax is None:
            fig,ax = plt.subplots(1,1,figsize=(8,8))
        self.tsne = TSNE(n_components=2,verbose=1,n_iter=1000,learning_rate=500,init='pca',random_state=0)
        features =self.feature.drop(columns=['subject_id'])
        if self.target_label is not None:
            features = features.drop(columns=self.target_label)
        features = StandardScaler().fit_transform(features.values)
        self.embding  = self.tsne.fit_transform(features)
        if self.target_label is not None:
            y = self.feature[self.target_label].values.tolist()
        else:
            y = np.ones(len(self.embding))
        # create color map from target_label
        # scatter plot with color map
        ax.scatter(self.embding[:,0],self.embding[:,1],c=y,alpha=0.8,s=30)

        # write subject id to plot
        for i,c in enumerate(self.feature['subject_id']):
            ax.annotate(c,(self.embding[i,0],self.embding[i,1]))
        ax.legend()
        ax.set_title('TSNE')
        ax.set_xlabel('TSNE1')
        ax.set_ylabel('TSNE2')
        return ax

    def svm_one_classifier(self,ax=None):
        """
        svm one classifier
        """
        features =self.feature.drop(columns=['subject_id'])
        if self.target_label is not None:
            features = self.feature.drop(columns=[self.target_label])
            # y = self.feature[self.target_label].values.tolist()
        #else:
            # y= np.ones(len(self.feature))
        features = StandardScaler().fit_transform(features)
        # fit svm one classifier
        clf = OneClassSVM(gamma='scale',nu=0.1)
        clf.fit(features)
        
        # delete anomaly subject
        
        predy = clf.predict(features)

        self.svm_one_classifier_delete_ids = self.feature[predy==-1]['subject_id'].tolist()
        self.delete_subject_ids += self.svm_one_classifier_delete_ids
    def remove_anomaly_subject(self):
        """
        remove anomaly subject
        """
        return self.feature[~self.feature['subject_id'].isin(list(set(self.delete_subject_ids)))]
         
    def plot_anomaly_subject(self,ax=None):
        """
        plot anomaly subject
        """
        if ax is None:
            fig,ax = plt.subplots(1,1,figsize=(8,8))
        y = np.ones(len(self.feature))
        y[self.feature['subject_id'].isin(self.delete_subject_ids)] =-1

        # create color map from target_label
        cmap = sns.color_palette('Set1',n_colors=len(set(y)))
        for i,c in enumerate(set(y)):
            ax.scatter(self.embding[y==c,0],self.embding[y==c,1],c=cmap[i],label=c)
        # write subject id to plot
        for i,c in enumerate(self.feature['subject_id']):
            ax.annotate(c,(self.embding[i,0],self.embding[i,1]))
        ax.legend()
        ax.set_title('Anomaly subject')
        ax.set_xlabel('TSNE1')
        ax.set_ylabel('TSNE2')
        return ax

class FuncQC(BaseQC):
    def __init__(self, features: pd.DataFrame, target_label=None, drop_columns=[]) -> None:
        super().__init__(features, target_label, drop_columns)
    def check_head_motion(self,column_name='mean-fd',threshold=0.5,ax=None,plot_type='distribution'):

        return self.check_column_threshold(column_name,threshold,ax,plot_type)

class MRIQC(BaseQC):
    def __init__(self, features: pd.DataFrame, target_label=None, drop_columns=[]) -> None:
        super().__init__(features, target_label, drop_columns)


class FreeSurferQC(BaseQC):
    def __init__(self, features: pd.DataFrame,level='prior', target_label=None, drop_columns=[]) -> None:
        """
        initialize FreeSurferQC
        Args:
            features (pd.DataFrame): features
            target_label (str, optional): target_label. Defaults to None.
            drop_columns (list, optional): drop_columns. Defaults to [].
            level (str, optional): level. Defaults to 'prior' or group level.

        """
        super().__init__(features, target_label, drop_columns)
        self.level = level
        if self.level not in ['prior','group']:
            raise ValueError('level must be prior or group')
        if self.level =='group' and self.feature.shape[0]<10:
            raise ValueError('group level must have more than 10 subjects')

    def detect_aseg_stats(self,threshold=10,ax=None,plot_type='distribution'):
        """
        detect aseg stats
        Args:
            threshold (int, optional): threshold. Defaults to 20.
            ax (matplotlib.axes._subplots.AxesSubplot, optional): ax. Defaults to None.
            plot_type (str, optional): plot_type. Defaults to 'distribution' <'bar'>.
        """

        if self.level == 'prior':
            self.detect_aseg_stats_df = self.__prior_aseg_stats__()
        elif self.level == 'group':
            self.detect_aseg_stats_df = self.__group_aseg_stats__()
        if plot_type == 'distribution':
            self.threshold_delete_ids,ax = check_column_threshold(self.detect_aseg_stats_df,'outlier_aseg_stats',threshold,ax)
        else:
            self.threshold_delete_ids,ax = column_threshold_bar_plot(self.detect_aseg_stats_df,'outlier_aseg_stats',threshold,ax)
        self.delete_subject_ids += self.threshold_delete_ids
        return ax 
    
        
    def __prior_aseg_stats__(self):
        """
        prior level
        """
        outlierDict = outlierTable()
        features_norm_df = self.feature['subject_id'].copy().to_frame()

        for key in outlierDict.keys():
            # check <lower >upper with self.features    
            features_norm_df[key] = (self.feature[key]<outlierDict[key]['lower']) | (self.feature[key]>outlierDict[key]['upper'])
        
        features_norm_df['outlier_aseg_stats'] = features_norm_df.sum(axis=1)
        return features_norm_df
    def __group_aseg_stats__(self):
        """
        group level
        """
        df = self.feature.drop(columns=['subject_id'])
        s_df = df.describe().T
        iqr = s_df['75%']-s_df['25%']
        s_df['iqr'] = iqr
        features_norm_df = self.feature['subject_id'].copy().to_frame()
        for key in s_df.index:
            _df = s_df[s_df.index==key]
            features_norm_df[key] = (df[key]<(_df['25%']-1.5*_df['iqr']).values[0]) | (df[key]>(_df['75%']+1.5*_df['iqr']).values[0])
        features_norm_df['outlier_aseg_stats'] = features_norm_df.sum(axis=1)
        return features_norm_df
