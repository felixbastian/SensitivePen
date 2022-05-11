import numpy as np
def calculateBinaryScores(crp):
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    p = 0
    n = 0

    for item in crp['labels'].unique():
        data = crp[crp['labels'] == item]
        count = data.groupby(['y_pred']).size()

        try:
            yes = count.at['yes']
        except Exception as e:
            yes = 0
        try:
            no = count.at['no']
        except Exception as e:
            no = 0

        # print(f'yes: {yes}, no: {no}')
        if (no > yes):
            pred = 'no'

        else:
            pred = 'yes'

        real = data['y_real'].iloc[0]
        if (real == 'yes'):
            p = p + 1
        else:
            n = n + 1
        # print(f'real: {real}')

        # ratio
        if (pred == 'yes'):
            if (pred == real): tp = tp + 1
            if (pred != real): fp = fp + 1
        if (pred == 'no'):
            if (pred == real): tn = tn + 1
            if (pred != real): fn = fn + 1

    print(f'tp: {tp}')
    print(f'fp: {fp}')
    print(f'tn: {tn}')
    print(f'fn: {fn}')

    sensitivity = tp / (tp + fn)
    specificity = tn / (fp + tn)
    accuracy = (tp + tn) / (tp + tn + fp + fn)

    print(f'sensitivity: {sensitivity}')
    print(f'specificity: {specificity}')
    print(f'accuracy: {accuracy}')

    print()
    print(f'positive: {p}')
    print(f'negative: {n}')


def calculateTriScores(crp):
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    p = 0
    n = 0

    confusion = np.array([[0,0,0],[0,0,0],[0,0,0]])

    for item in crp['labels'].unique():
        data = crp[crp['labels'] == item]
        count = data.groupby(['y_pred']).size()

        #count all numbers of yes, no, mild for a particular subject
        try:
            yes = count.at['yes']
        except Exception as e:
            yes = 0
        try:
            no = count.at['no']
        except Exception as e:
            no = 0
        try:
            mild = count.at['mild']
        except Exception as e:
            mild = 0

        #define yes/no/mild cases

        #define no
        if (no > yes and no > mild):
            pred = 'no'
        #define mild
        elif (mild > no and mild > yes):
            pred = 'mild'
        #define yes
        elif (yes > mild and yes > no):
            pred = 'yes'

        #bias towards predicting as positive cases
        elif (no > yes and no == mild):
            pred = 'mild'
        elif (no < yes and no == mild):
            pred = 'yes'
        elif (yes > no and yes == mild):
            pred = 'yes'
        elif (yes < no and yes == mild):
            pred = 'no'
        elif (no == yes):
            pred = 'mild'

        else:
            pred = 'FALSE'
            print(pred)
            print(yes)
            print(no)
            print(mild)


        real = data['y_real'].iloc[0]

        #create confusion matrix
        #true
        if (real == 'no'):
            col = 0
        elif (real=='mild'):
            col=1
        elif(real =='yes'):
            col=2

        #prediction
        if (pred == 'no'):
            row = 0
        elif (pred=='mild'):
            row=1
        elif(pred =='yes'):
            row=2

        confusion[row, col] = confusion[row, col]+1

    print('Confusion Matrix')
    print(confusion)
    print(f'Nbr. of subjects: {np.sum(confusion)}')
    print(f'Accuracy: {(confusion[0,0]+confusion[1,1]+confusion[2,2])/np.sum(confusion)}')