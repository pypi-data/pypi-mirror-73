def bayes_suspects(df,event,suspects,point,interval='NULL',min='NULL'):
    """Importing what we need"""
    
    import itertools
    from itertools import combinations 
    import scipy
    from sklearn.preprocessing import StandardScaler
    import scipy.stats
    from statsmodels.distributions.empirical_distribution import ECDF
    import pandas as pd
    import numpy as np
    
    """Defining useful functions"""
    def odd_even(num):
        if (num % 2) == 0:
           return 'Even'
        else:
           return 'Odd'
    
    
    """Checking the presence of optimal parameters"""
    if interval == 'NULL':
            interval = 0.05
    else:
            interval = interval
        
    if min == 'NULL':
        min = 10
    else:
        min = min

    """Getting all possible combinations"""
    all_combinations = []
    for r in range(1,len(suspects) + 1):

        combinations_object = itertools.combinations(suspects, r)
        combinations_list = list(combinations_object)
        all_combinations += combinations_list

    all_combinations
    df1 = pd.DataFrame()
    df_final = pd.DataFrame()
    df_final2 = pd.DataFrame()


    """Calculating the combinations joint probabilities"""
    for i in range(len(all_combinations)):
        dfr = df[(df[event]>=(1-interval)*point[event])&(df[event]<=(1+interval)*point[event])]

        df1 = dfr.copy()
        for c in list(all_combinations[i]):
            cut = point[c]
            df1 = df1[(df1[c]<=cut*(1+interval))&(df1[c]>=cut*(1-interval))]

        if len(df1)<=min:
                prob = 0
        else:
            try: 
                prob = scipy.stats.gaussian_kde(df1[c]).integrate_box_1d((1-interval)*point[c],(1+interval)*point[c])
            except np.linalg.LinAlgError as err:
                prob = 0

        final2 = pd.DataFrame(
                        {
                            'name': str(all_combinations[i]),
                            'number_of_variables': len(list(all_combinations[i])),
                            'prob_ba':prob,
                            'number_type':odd_even(len(list(all_combinations[i])))
                        }, index=[0])

        df_final = pd.concat([df_final,final2])

        dfr = df.copy()
        df1 = dfr.copy()
        for c in list(all_combinations[i]):
            cut = point[c]
            df1 = df1[(df1[c]<=cut*(1+interval))&(df1[c]>=cut*(1-interval))]

        if len(df1)<=min:
                prob = 0
        else:
            try: 
                prob = scipy.stats.gaussian_kde(df1[c]).integrate_box_1d((1-interval)*point[c],(1+interval)*point[c])
            except np.linalg.LinAlgError as err:
                prob = 0

        final2 = pd.DataFrame(
                        {
                            'name': str(all_combinations[i]),
                            'number_of_variables': len(list(all_combinations[i])),
                            'prob_b':prob,
                            'number_type':odd_even(len(list(all_combinations[i])))
                        }, index=[0])

        df_final2 = pd.concat([df_final2,final2])

    """Calculating the combinations bayesian probabilities"""
    df_final = pd.merge(df_final,df_final2,how='inner',on=['name','number_of_variables','number_type'])

    df_final['prob_a'] = scipy.stats.gaussian_kde(df[event]).integrate_box_1d((1-interval)*point[event],(1+interval)*point[event])

    df_final['pbayes'] = df_final['prob_a']*df_final['prob_ba']/df_final['prob_b']
    
    df_final = df_final.fillna(0)
    

    """Calculating the intersects"""
    df_final['subtract'] = 0
    
    for r in range(0,len(suspects)):
        name_clean = df_final['name'][r].replace("',)", '') 
        name_clean = name_clean.replace("('", '') 
        name_clean

        frameloop = df_final[df_final['name'].str.contains(name_clean)][df_final['number_of_variables']>1]
        frameloop['pbayes'] = np.where(frameloop['number_type']=='Even',-1*frameloop['pbayes'],frameloop['pbayes'])

        b=0
        for i in range(0,len(frameloop)):
        #i=1
            a=frameloop['pbayes'].iloc[i]/frameloop['number_of_variables'].iloc[i]
            b=b+a
        df_final['subtract'].iloc[r] = b
    
    """Calculating the attribution"""
    df_final['pbayes_attribution'] = df_final['pbayes']+df_final['subtract']
    df_final['pbayes_attribution'] = np.where(df_final['pbayes_attribution']<0,0,df_final['pbayes_attribution'])
    df_final['pbayes_attribution'] = np.where(df_final['number_of_variables']>1,0,df_final['pbayes_attribution'])
    
    del df_final['number_of_variables']
    del df_final['number_type']
    del df_final['subtract']
    
    return df_final
