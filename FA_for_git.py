# Import required libraries
import pandas as pd
from sklearn.datasets import load_iris
from factor_analyzer import FactorAnalyzer
import matplotlib.pyplot as plt
import data_class as dc

df = pd.DataFrame(pd.read_csv('res_SEM.csv'))
df_phone = df.iloc[:,:12]
df_QOL = df.iloc[:,12:]

def FA(observied_variables,name):
    from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
    chi_square_value,p_value=calculate_bartlett_sphericity(observied_variables)
    print("chi_square_value",chi_square_value,"p-value:", p_value)
    from factor_analyzer.factor_analyzer import calculate_kmo
    kmo_all,kmo_model=calculate_kmo(observied_variables)
    print("KMO value",kmo_model)

    # Create factor analysis object and perform factor analysis
    if name == 'phone':
        fa = FactorAnalyzer(n_factors=2)
    if name == 'QOL':
        fa = FactorAnalyzer(n_factors=4)
    fa.fit_transform(observied_variables)
    # Check Eigenvalues
    eigen_values, vectors = fa.get_eigenvalues()
    print(eigen_values)

    """
    # Create scree plot using matplotlib
    plt.scatter(range(1,observied_variables.shape[1]+1),eigen_values)
    plt.plot(range(1,observied_variables.shape[1]+1),eigen_values)
    if name == 'phone':
        plt.title('Scree Plot for phone features',fontsize=24)
    if name == 'QOL':
        plt.title('Scree Plot for QOL features',fontsize=24)
    plt.xlabel('Factors', fontsize=18)
    plt.ylabel('Eigenvalue',fontsize=18)
    plt.grid()
    plt.show()
    """

    loadings = fa.loadings_
    print(pd.DataFrame(loadings,observied_variables.columns))
    #print(pd.DataFrame(fa.get_communalities()))
    return pd.DataFrame(loadings,observied_variables.columns)

    # Get variance of each factors
    print(pd.DataFrame(fa.get_factor_variance(),['SS Loadings','Proportion Var','Cumulative Var']))

print('Phones:')
phone_factors = FA(df_phone,'phone')
print("#############################")
print('QOL:')
QOL_factors = FA(df_QOL,'QOL')

"""
# plotting the factors loadings
plt.scatter(phone_factors.iloc[:,0],phone_factors.iloc[:,1])
plt.show()

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = Axes3D(fig)

ax.scatter(QOL_factors.iloc[:,0],QOL_factors.iloc[:,1],QOL_factors.iloc[:,2])
plt.show()


# loading the factors loading multiple by the people
f0_df = df_phone.copy()
f1_df = df_phone.copy()


for x in range(len(phone_factors.iloc[:,0])):
    f0_df.iloc[:,x] = f0_df.iloc[:,x] * phone_factors.iloc[:,0][x]
f0_df['sum'] = f0_df.sum(axis=1)
print(f0_df)

for x in range(len(phone_factors.iloc[:,1])):
    f1_df.iloc[:,x] = f1_df.iloc[:,x] * phone_factors.iloc[:,1][x]
f1_df['sum'] = f1_df.sum(axis=1)
print(f1_df)

plt.scatter(f0_df['sum'],f1_df['sum'])
plt.show()


Q0_df = df_QOL.copy()
Q1_df = df_QOL.copy()
Q2_df = df_QOL.copy()

for x in range(len(QOL_factors.iloc[:,0])):
    Q0_df.iloc[:, x] = Q0_df.iloc[:, x] * QOL_factors.iloc[:, 0][x]
Q0_df['sum'] = Q0_df.sum(axis=1)
print(Q0_df)

for x in range(len(QOL_factors.iloc[:,1])):
    Q1_df.iloc[:, x] = Q1_df.iloc[:, x] * QOL_factors.iloc[:, 1][x]
Q1_df['sum'] = Q1_df.sum(axis=1)
print(Q1_df)

for x in range(len(QOL_factors.iloc[:,2])):
    Q2_df.iloc[:, x] = Q2_df.iloc[:, x] * QOL_factors.iloc[:, 2][x]
Q2_df['sum'] = Q2_df.sum(axis=1)
print(Q2_df)


fig = plt.figure()
ax2 = Axes3D(fig)
ax2.scatter(Q0_df['sum'],Q1_df['sum'],Q1_df['sum'])
plt.show()

"""
