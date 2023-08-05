from collections.abc import Sequence
from matplotlib import pyplot as plt
import seaborn as sns
import matplotlib as mpl
import pandas as pd
import numpy as np

__all__ = ['condition_line_plot', 'condition_violin_plot', 'elapsed_time_scatter_plot_flexible',
           'elapsed_time_scatter_plot', 'paired_plots', 'max_burst_number', "condition_scatter_plot"]
# TODO: This needs to be documented

def condition_line_plot(dataframe, y_vals='all', Neuron='LG', 
                        title='10^-9M CCAP Desheathed \nExperiment 9/5/19'):
    """Return a condition line plot for the dataframe

    :param dataframe:
    :param y_vals:
    :param Neuron:
    :param title:
    :return:
    """
    if y_vals.lower() == 'all': # Default params
        y_vals = ['Burst Duration (sec)', 
                  '# of Spikes', 
                  'Spike Frequency (Hz)', 
                  'Instantaneous Period (sec)', 
                  'Instantaneous Frequency (Hz)', 
                  'Duty Cycle']
        fig, axis = plt.subplots(nrows=2, ncols=3, figsize=(16,8))
        
    else:
        raise NotImplementedError("Non-default behavior is currently not implemented")
        
    if not isinstance(y_vals, Sequence):
        raise TypeError('y_vals must be a sequence (either a list or an array)')
        

    
    if Neuron.lower() != 'all':
        dataframe = dataframe[dataframe['Neuron']==Neuron]
        
    for index, ax in enumerate(axis.ravel()):
        # Make the plot
        g = sns.pointplot(x="Condition", 
                          y=y_vals[index], 
                          hue="Neuron",
                          capsize=.2, 
                          palette="YlGnBu_d", 
                          kind="point", 
                          data=dataframe, 
                          ax=ax)
        
        # Set Title, y-axis, x-axis values
        ax.set_title(title, fontsize=20)
        ax.set_ylabel(y_vals[index], fontsize=16)
        ax.set_xlabel("Condition", fontsize=16)
    
    # Make it look pretty
    mpl.rc('ytick', labelsize=16) 
    mpl.rc('xtick', labelsize=16) 
    plt.tight_layout()
    plt.subplots_adjust(hspace=.6)
    plt.show()
    return fig, ax

def condition_violin_plot(dataframe, y_vals='all', Neuron='all', 
                          title='10^-9M CCAP Desheathed \nExperiment 9/5/19'):

    fig, axis = plt.subplots(ncols=3, nrows=2, figsize=(20,10))

    if y_vals.lower() == 'all': # Default params
            y_vals = ['Burst Duration (sec)', 
                      '# of Spikes', 
                      'Spike Frequency (Hz)', 
                      'Instantaneous Period (sec)', 
                      'Instantaneous Frequency (Hz)', 
                      'Duty Cycle']
            
    else:
        raise NotImplementedError("Non-default behavior is currently not implemented")
        
    if not isinstance(y_vals, Sequence):
        raise TypeError('y_vals must be a sequence (either a list or an array)')
        

    
    if Neuron.lower() != 'all':
        dataframe = dataframe[dataframe['Neuron']==Neuron]
        


    for index, ax in enumerate(axis.ravel()):
            # Make the plot
            g = sns.violinplot(x='Condition', 
                               y=y_vals[index], 
                               data=dataframe, 
                               hue='Neuron', 
                               scale_hue=False, 
                               inner='quartile', 
                               scale='count', 
                               split=False, 
                               ax=ax, 
                               bw='scott',
                               palette='husl')

            # Set Title, y-axis, x-axis values
            ax.set_title(title, fontsize=20)
            ax.set_ylabel(y_vals[index], fontsize=16)
            ax.set_xlabel("Condition", fontsize=16)

    # Make it look pretty
    mpl.rc('ytick', labelsize=16) 
    mpl.rc('xtick', labelsize=16) 
    plt.tight_layout()
    #plt.subplots_adjust(hspace=.6)
    #plt.show()
    return fig, ax

def elapsed_time_scatter_plot(dataframe, y_vals='all', Neuron='LG', 
                              title='9/5/19 Desheathed Experiment'):
    
    if y_vals.lower() == 'all': # Default params
        y_vals = ['Burst Duration (sec)', 
                  '# of Spikes', 
                  'Spike Frequency (Hz)', 
                  'Instantaneous Period (sec)', 
                  'Instantaneous Frequency (Hz)', 
                  'Duty Cycle']
        fig, axis = plt.subplots(nrows=2, ncols=3, figsize=(16,8))
        
    else:
        raise NotImplementedError("Non-default behavior is currently not implemented")
        
    if not isinstance(y_vals, Sequence):
        raise TypeError('y_vals must be a sequence (either a list or an array)')
        
    
    dataframe = dataframe[dataframe['Neuron']==Neuron]    

    pre = dataframe[dataframe['Condition']=='pre']
    exp = dataframe[dataframe['Condition']=='exp']
    post = dataframe[dataframe['Condition']=='post']



    for index, ax in enumerate(axis.ravel()):
        pre_plot = ax.scatter(x=pre['Burst#'], 
                              y=pre[y_vals[index]], 
                              label='Pre Control {} Neuron'.format(Neuron),
                              alpha=.5)
        exp_plot = ax.scatter(x=exp['Burst#'], 
                              y=exp[y_vals[index]], 
                              label='Experiment {} Neuron'.format(Neuron),
                              alpha=.5)
        post_plot = ax.scatter(x=post['Burst#'], 
                               y=post[y_vals[index]], 
                               label='Post Control {} Neuron'.format(Neuron),
                               alpha=.5)

        y_label = ax.set_ylabel(y_vals[index],fontsize=16)
        x_label = ax.set_xlabel('Burst #',fontsize=16)
        ax.set_title(title,fontsize=20)
        
    plt.legend()
    plt.tight_layout()
    return fig, ax

def elapsed_time_scatter_plot_flexible(dataframe, y_vals='all', Neuron='LG', 
                              title='9/5/19 Desheathed Experiment'):
    #sns.set(palette="husl")
    if y_vals.lower() == 'all': # Default params
        y_vals = ['Burst Duration (sec)', 
                  '# of Spikes', 
                  'Spike Frequency (Hz)', 
                  'Instantaneous Period (sec)', 
                  'Instantaneous Frequency (Hz)', 
                  'Duty Cycle']
        fig, axis = plt.subplots(nrows=2, ncols=3, figsize=(16,8))
        
    else:
        raise NotImplementedError("Non-default behavior is currently not implemented")
        
    if not isinstance(y_vals, Sequence):
        raise TypeError('y_vals must be a sequence (either a list or an array)')
        
    
    dataframe = dataframe[dataframe['Neuron']==Neuron]    

    #pre = dataframe[dataframe['Condition']=='pre']
    #exp = dataframe[dataframe['Condition']=='exp']
    #post = dataframe[dataframe['Condition']=='post']


    
    for index, ax in enumerate(axis.ravel()):
        for condition in dataframe['Condition'].unique():
            data = dataframe[dataframe['Condition']==condition]
            plot = ax.scatter(x=data['Burst#'], 
                              y=data[y_vals[index]], 
                              label='{} {} Neuron'.format(condition, Neuron),
                              alpha=.5)

        y_label = ax.set_ylabel(y_vals[index],fontsize=16)
        x_label = ax.set_xlabel('Burst #',fontsize=16)
        ax.set_title(title,fontsize=20)
        
    plt.legend()
    plt.tight_layout()
    return fig, ax

def paired_plots(dataframe, condition='Pre'):

    sns.set(style="ticks", palette="husl")
    data = dataframe[dataframe['Condition']==condition]
    g = sns.PairGrid(data=data, hue="Neuron", height=4, aspect=1)
    g = g.map_diag(plt.hist, histtype="step", linewidth=3)
    g = g.map_offdiag(plt.scatter, alpha=.25)
    g = g.add_legend()

    # There has to be a better way
    # TODO: Fix below
    xlabels,ylabels = [],[]

    for ax in g.axes[-1,:]:
        xlabel = ax.xaxis.get_label_text()
        xlabels.append(xlabel)

    for ax in g.axes[:,0]:
        ylabel = ax.yaxis.get_label_text()
        ylabels.append(ylabel)

    for i in range(len(xlabels)):
        for j in range(len(ylabels)):
            g.axes[j,i].xaxis.set_label_text(xlabels[i], fontsize=16)
            g.axes[j,i].yaxis.set_label_text(ylabels[j], fontsize=16)

    for ax in g.axes.flat:
        # labelleft refers to yticklabels on the left side of each subplot
        ax.tick_params(axis='y', labelleft=True) # method 1
        ax.tick_params(axis='x', labelbottom=True) # method 1

    plt.tight_layout()
    plt.show()
    
def max_burst_number(dataframe):
    # Get Max number of Bursts for each conditon
    x_ = [dataframe[dataframe['Condition']==condition]['Burst#'].max() 
          for condition in dataframe['Condition'].unique()]
    # Put it into a dataframe to use seaborn
    burst_num = dict(zip(dataframe['Condition'].unique(), x_))
    burst_num = pd.DataFrame.from_dict(burst_num, orient='index', columns=['Burst#'])
    burst_num['Condition'] = burst_num.index

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(data=burst_num,x='Condition', y='Burst#',ax=ax)
    ax.set_ylabel('Total LG Bursts', fontsize=16)
    ax.set_xlabel('Condition', fontsize=16)
    title = plt.title('Number of LG Bursts in GMR', fontsize=20)
    return fig, ax


def condition_scatter_plot(dataframe, y_vals='all', Neuron='LG', 
                           title=''):

    fig, axis = plt.subplots(ncols=3, nrows=2, figsize=(20,10))

    if y_vals.lower() == 'all': # Default params
            y_vals = ['Burst Duration (sec)', 
                      '# of Spikes', 
                      'Spike Frequency (Hz)', 
                      'Instantaneous Period (sec)', 
                      'Instantaneous Frequency (Hz)', 
                      'Duty Cycle']
            
    else:
        raise NotImplementedError("Non-default behavior is currently not implemented")
        
        

    
    if Neuron.lower() != 'all':
        dataframe = dataframe[dataframe['Neuron']==Neuron]
        


    for index, ax in enumerate(axis.ravel()):
            # Make the plot
            g = sns.stripplot(x='Condition', 
                              y=y_vals[index], 
                               data=dataframe, 
                               hue='Date', 
                               
                               ax=ax, 
                               palette='viridis', alpha=.25)
            g = sns.pointplot(x='Condition', 
                       y=y_vals[index], 
                       data=dataframe, 
                       hue='Date', 
                       estimator=np.median,
                       ax=ax, 
                       palette='viridis', scale=1.2)

            # Set Title, y-axis, x-axis values
            ax.set_title(title, fontsize=20)
            ax.set_ylabel(y_vals[index], fontsize=16)
            ax.set_xlabel("Condition", fontsize=16)

    # Make it look pretty
    mpl.rc('ytick', labelsize=16) 
    mpl.rc('xtick', labelsize=16) 
    plt.tight_layout()
    #plt.subplots_adjust(hspace=.6)
    #plt.show()
    return fig, ax
