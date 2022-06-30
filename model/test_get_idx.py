import numpy as np

x0 = np.array([np.nan, np.nan, 1,1,2,4,4, np.nan, np.nan])
x1 = np.array([np.nan, np.nan, 1,1,np.nan,4,4, np.nan, np.nan])
x2 = np.array([np.nan, np.nan, 1,1,2,4,4, np.nan, np.nan])
x3 = np.array([np.nan, np.nan, 1,1,2,4,4, np.nan, np.nan, 5,5,2, np.nan, np.nan])
x4 = np.array([np.nan, np.nan, 1,1,2,4,4, np.nan, np.nan,1,2,3])
x5 = np.array([0,0,0,0, np.nan, np.nan, 1,1,2,4,4, np.nan, np.nan])

xs = [x0,x1,x2,x3,x4,x5]


for x in xs:
    idx = np.where(np.diff(np.isnan(x)))[0]
    print(f'x={x} | idx={idx}')


