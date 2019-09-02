# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 18:22:18 2018

@author: José Pablo
"""

from sklearn.ensemble import RandomForestClassifier as RndFC
from sklearn import metrics as met
import numpy as np
import csv
import os
from createFolder import createFolder

"""
--------------------------------------------------------------------------------------------------
Functions
--------------------------------------------------------------------------------------------------
"""

#A function that eliminates unwanted characters sometimes present in csv files
def cleanLine(line, header = False):
    line = line.replace("'",'')
    line = line.replace("[",'')
    line = line.replace("]",'')
    if header:
        line = line.replace('\ ','')
    else:
        line = line.replace("?",'NaN')
    arr = line.split(',')
    return arr

def PreSel_RF(concept,t_window=['1&0.5', '2&1', '3&1.5'],scr_dir=''):
    for cncpt in concept:
        print(cnpt)
        for twnd in t_window:
            print('--' + fldr[f])
            #The csv file with the features is read and stored in an array
            db_path = scr_dir + cncpt + '//' + twnd + '//PreSelectedFTS_' + twnd + '_' + cncpt + '.csv'
            d_base = []
            r = open(db_path,'r')
            txt = r.read()
            r.close()
            d_base = txt.split('\n')
            #Every feature name is stored in an array
            features = []
            temp = str(base[0])
            feat = celanLine(temp,True)
            for i in range(0,len(feat) - 1):
                features.append(feat[i])
            
            #We train and evaluate adding every feature, starting with the most relevant
            #with the whole data base
            for k in range(0, len(features)):
                x = []
                y = []
                #every string number must be parsed to float
                for i in range(1,len(d_base)):
                    ln = str(d_base[i])
                    q = celanLine(ln)
                    p = []
                    for j in range(0,k+1):
                        if(j < len(q)-1):
                            if (q[j]!=' ')and(q[j]!=''):
                                p.append(float(q[j]))
                            else:
                                if i != len(base)-1:
                                    print('ERROR: ' + str(i+1))
                    if(q[len(features)]!=' ')and(q[len(features)]!=''):
                        y.append(float(q[len(features)]))
                        x.append(p)
                    else:
                        if i != len(d_base)-1:
                            print('ERROR: ' + str(i+1))
                #A numpy array is made with the inputs
                X = np.array([np.array(z) for z in x])
                #A random forest model is trained with the available data
                clsf = RndFC()
                clsf.fit(X,y)
                #An output is gotten from the inputs
                Y = clsf.predict(X)
                
                st = ""
                for i in range(0,k+1):
                    st += features[i] +','
                st += 'Output,Expected' + '\n'
                createFolder(cncpt + '//' + twnd + '//PreSel_RF_outputs')
                print('-----Writing output file ' + str(k+1) + '...')
                #A file with the input features, output and expected output (real value) is written
                w = open(cncpt + '//' + twnd + '//PreSel_RF_outputs//Output' + str(k+1) + '.csv', 'w')
                count = 0
                try:
                    w.write(st)
                    srt = ""
                    for i in range(1, len(base)):
                        count = i
                        ln = str(base[i])
                        q = celanLine(ln)
                        if (q[0]!=' ')and(q[0]!=''):
                            for j in range(0, k+1):
                                w.write(q[j] + ',')
                            w.write(str(Y[i - 1]) + ',' + str(y[i - 1]) + '\n')
                except Exception as e:
                    #In case there's an extra (empty) line at the end
                    if count != len(features)-1:
                        print('------Unexpected error: ' + str(e))
                w.close()      
                print('------...Output file ' + str(k+1) + ' is done')  
            print('----' + fldr[f] + ' finished')

def preSelScores(concept,t_window=['1&0.5', '2&1', '3&1.5',
                binary=True,
                scr_dir=''):
    for cncpt in concept:
        print(cncpt)
        #This will be performed for all the selected time-windows
        for twnd in t_window:
            print('--' + twnd)
            pres = []
            num = []
            path = scr_dir + cncpt + '//' + twnd + '//PreSel_RF_outputs//'
            for i in range(1, len(os.listdir(path)) + 1):
                num.append(i)
                #the database (in a csv file) is opened and stored in 'base'
                r = open(path + '//Output' + str(i) + '.csv','r')
                r_txt = r.read()
                r.close()
                d_base = r_txt.split('\n')
                y_exp = []
                y_prd = []
                for j in range(1,len(base)):
                    ln = str(base[j])
                    q = ln.split(',')
                    if(len(q) > 1)and((q[0]!='')and(q[0]!=' ')):
                        y_prd.append(float(q[-2]))
                        y_exp.append(float(q[-1]))
                
                a_tag = 'binary'
                if binary == False:
                    a_tag = 'macro'
                #accuracy
                acc = 100*met.accuracy_score(y_exp,y_prd)
                #precision
                ppv = 100*met.precision_score(y_exp,y_prd,average=a_tag)
                #f1 score
                fsc = 100*met.f1_score(y_exp,y_prd,average=a_tag)
                #recall
                rec = 100*met.recall_score(y_exp,y_prd,average=a_tag)
                
            #A csv file with the scores is written
            w = open(cncpt + '//' + twnd + '//PreSelectionReport_' + twnd + '_' + cncpt + '.csv', 'w')
            try:
                w.write('Accuracy')
                temp = []
                for arr in pres:
                    w.write(',' + str(arr[0]))
                    temp.append(arr[0])
                w.write('\n')
                mu = np.mean(temp)
                w.write('Avg. Accuracy,' + str(mu) + '\n')
                w.write('Precision')
                temp = []
                for arr in pres:
                    w.write(',' + str(arr[1]))
                    temp.append(arr[1])
                w.write('\n')
                mu = np.mean(temp)
                w.write('Avg. Precision,' + str(mu) + '\n')
                w.write('Recall')
                temp = []
                for arr in pres:
                    w.write(',' + str(arr[2]))
                    temp.append(arr[2])
                w.write('\n')
                mu = np.mean(temp)
                w.write('Avg. Recall,' + str(mu) + '\n')
                w.write('F1Score')
                temp = []
                for arr in pres:
                    w.write(',' + str(arr[3]))
                    temp.append(arr[3])
                w.write('\n')
                mu = np.mean(temp)
                w.write('Avg. F1Score,' + str(mu))
            except Exception as e:
                print('-----An error ocurred: ' + str(e))
            w.close()
            print('---' + twnd + ' done')

"""
--------------------------------------------------------------------------------------------------
End of functions
--------------------------------------------------------------------------------------------------
"""

def main():
    concept = []
    preSel_RF(concept)
    preSelScores(concept)
    print('End of task')

if __name__=="__main__":
    main()
