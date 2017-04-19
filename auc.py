import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')



def auc(ground_truth, scores, fig_name="c16_auc.jpg"):
    fpr, tpr, thresholds = metrics.roc_curve(ground_truth, scores, pos_label=1)#computer ROC coordinate
    auc = metrics.auc(fpr, tpr)#computer auc
    plt.title('ROC (AUC=%0.6f)' % (auc))
    plt.grid(True, linestyle='-', color='0.75')
    plt.plot(fpr, tpr)
    plt.savefig(fig_name)
    plt.close()
    return auc