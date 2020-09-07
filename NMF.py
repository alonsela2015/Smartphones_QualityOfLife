import pandas as pd
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
import numpy as np

df = pd.read_csv('res_SEM.csv')
smart_phones, QOL  = df.iloc[:,:12], df.iloc[:,12:]

aware = smart_phones[['x1','x2','x7','x8','x9']]
unaware = smart_phones[['x4','x3','x5','x6','x12','x10','x11']]



competent = QOL[['y2', 'y12', 'y15',  'y16' , 'y17' , 'y18']]
functioning = QOL[['y3', 'y4','y5','y6','y9','y10','y11','y13','y14', 'y21']]
good_feeling = QOL[['y1', 'y7' , 'y8' , 'y19' , 'y20',  'y22']]

from sklearn.decomposition import NMF


model_3 = NMF(n_components = 3,init='nndsvda')
score_with_random = []
score_without_random = []

nmf_features3 = model_3.fit_transform(unaware)
print(nmf_features3)

#GMM = GaussianMixture(n_components=4)
#pred = GMM.fit_predict(nmf_features3)

from sklearn.cluster import MeanShift
MS = MeanShift()
pred = MS.fit_predict(nmf_features3)


from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = Axes3D(fig)

# to show only 1 out of the clusters (4) of unaware
"""
df_nmf = pd.DataFrame(nmf_features3,columns=['x','y','z'])
print(df_nmf.shape)
df_nmf = df_nmf.loc[df_nmf['y'] < 0.2]
df_nmf = df_nmf.loc[df_nmf['z'] > 0.2]
print(df_nmf.shape)
"""

# with color by prediction
ax.scatter(nmf_features3[:,0],nmf_features3[:,1],nmf_features3[:,2],c=pred)
# without color by prediction
ax.scatter(nmf_features3[:,0],nmf_features3[:,1],nmf_features3[:,2])
#ax.scatter(df_nmf['x'],df_nmf['y'],df_nmf['z'])
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.title('unaware')
plt.show()


"""
data_number = 0
factors_names = ['smart_phones','aware','unaware','QOL','competent','functioning','good_feeling']
for data in [smart_phones,aware,unaware,QOL,competent,functioning,good_feeling]:
    nmf_features3 = model_3.fit_transform(data)
    print(nmf_features3)

    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = Axes3D(fig)

    # with color by prediction
    #ax.scatter(nmf_features3[:,0],nmf_features3[:,1],nmf_features3[:,2],c=pred)
    # without color by prediction
    ax.scatter(nmf_features3[:, 0], nmf_features3[:, 1], nmf_features3[:, 2])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.title(factors_names[data_number])
    plt.show()
    data_number += 1
"""