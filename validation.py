import pandas as pd
import os
import openpyxl
from sklearn.metrics import confusion_matrix
import numpy as np
from matplotlib import pyplot as plt

from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.preprocessing import label_binarize

from itertools import cycle
import spacy

def createfolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def split(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


"""
# Validation folder
createfolder("data/validation")

# Hier Alle einlesen
df = pd.read_csv("data/Alle.csv", encoding='utf-8')
df = df[["Date","handle", "Comment"]]
df["Bildung"] = ""
df["Digitalisierung"] = ""
df["SozialeMedien"] = ""
df["SozialeSicherung"] = ""
df["Steuern"] = ""
df["Umwelt"] = ""
df["Haushaltskonsolidierung"] = ""
df["Sonstiges"] = ""

print(df.head)


# hier sample ziehen
df_sample = df.sample(frac=0.04274897, replace=False)
df_sample.to_csv("data/validation/Sample.csv")
df_sample.to_excel("data/validation/Sample.xlsx", encoding="utf-8")
# teile sample in x gleich große dataframes und übergebe die Spalten Tweet/Label_Human
# Spaltenzahl (letzte Spalte ist TweetSpalte)

# anz splits

anz_splits = 160

df_samples = split(df_sample, anz_splits+1)

for x in range(1, anz_splits+1):
    print(x)
    df_1 = pd.DataFrame(df_samples[x])
    df_1 = pd.DataFrame(df_1[["Comment", "Bildung", "Digitalisierung", "SozialeMedien", "SozialeSicherung", "Steuern", "Umwelt", "Haushaltskonsolidierung", "Sonstiges"]])
    df_1["Polar_Human"] = ""
    df_1.to_excel("data/validation/" + str(x) + "split.xlsx", encoding="utf-8")

"""

# RAUSNEHMEN SPÄTER
anz_splits = 150


test_label = pd.DataFrame()

"""
for x in range(anz_splits):
    try:
        sample = pd.read_excel("data/validation/Label/" + str(x) + "split.xlsx")
        test_label = test_label.append(sample, ignore_index=True)
    except:
        print("Der Teildatensatz " + str(x) + " wurde nicht gelabelt")
"""
# ohne sonstiges
test_label = pd.read_excel("data/validation/Label/all.xlsx")

test_label["ID"] = test_label["Unnamed: 0"]

# Bestimme Index des Maximum einer Zeile (Spaltenweise)
test_label['Label_Human'] = test_label[['Bildung', 'Umwelt', 'Digitalisierung', 'SozialeMedien', 'SozialeSicherung', 'Steuern',
                  'Haushaltskonsolidierung', 'Sonstiges']].idxmax(axis=1)

test_label.to_csv(".\\data\\validation\\Label\\split.csv")

test_label_labels = test_label["Polar_Human"].to_numpy()
print(test_label["Polar_Human"].unique())

# test_prediction = df
test_prediction = pd.read_csv(".\\data\\validation\\Prediction\\similarities_list.csv")

# keep if ID test_label ist in ID test_prediction
test_prediction = test_prediction[test_prediction['ID'].isin(test_label["ID"])]
test_prediction = test_prediction.reset_index(drop=True)


# Bestimme Maximum einer Zeile (Spaltenweise)
test_prediction['Label_num'] = test_prediction[['Bildung', 'Umwelt', 'Digitalisierung', 'SozialeMedien', 'SozialeSicherung', 'Steuern',
                  'Haushaltskonsolidierung']].max(axis=1)
# Bestimme Index des Maximum einer Zeile (Spaltenweise)
test_prediction['Label'] = test_prediction[['Bildung', 'Umwelt', 'Digitalisierung', 'SozialeMedien', 'SozialeSicherung', 'Steuern',
                  'Haushaltskonsolidierung']].idxmax(axis=1)

# Lege Schwellwert fest
test_prediction.loc[test_prediction['Label_num'] < 0.5, 'Label'] = "Sonstiges"

mistakes = pd.DataFrame()
i = 0
j = 0
while i < len(test_prediction):
    test_prediction.loc[i, "Polar_Human"] = test_label.loc[i, "Polar_Human"]
    if test_prediction.loc[i, "Polar_num"] != test_prediction.loc[i, "Polar_Human"]:
        mistakes.loc[j, "Tweet"] = test_prediction.loc[i, "Tweet"]
        mistakes.loc[j, "Tweet_Full"] = test_label.loc[i, "Comment"]
        mistakes.loc[j, "Polar_num"] = test_prediction.loc[i, "Polar_num"]
        mistakes.loc[j, "Polar_Human"] = test_prediction.loc[i, "Polar_Human"]
        j=j+1

    i=i+1

mistakes.to_csv(".\\data\\validation\\mistakes2.csv", index=False)

# Wann ist Polarität -1;0;1
test_prediction_label = test_prediction["Polar_num"].to_numpy()

accuracy = accuracy_score(test_label_labels, test_prediction_label)
print('Average accuracy score: {0:0.2f}'.format(
      accuracy))

precision = precision_score(test_label_labels, test_prediction_label, average='macro')
print('Average precision score: {0:0.2f}'.format(
      precision))

recall = recall_score(test_label_labels, test_prediction_label, average='macro')
print('Average recall score: {0:0.2f}'.format(
      recall))

f1 = f1_score(test_label_labels, test_prediction_label, average='macro')
print('Average f1 score: {0:0.2f}'.format(
      f1))


# MultiLabelProblem
test_prediction_bin = label_binarize(test_prediction_label, classes=[-1,0,1])
test_label_bin = label_binarize(test_label_labels, classes=[-1,0,1])

n_classes = 3
# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(test_label_bin[:, i], test_prediction_bin[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

fpr["micro"], tpr["micro"], _ = roc_curve(test_label_bin.ravel(), test_prediction_bin.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

lw = 1

# First aggregate all false positive rates
all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

# Then interpolate all ROC curves at this points
mean_tpr = np.zeros_like(all_fpr)
for i in range(n_classes):
    mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])

# Finally average it and compute AUC
mean_tpr /= n_classes

fpr["macro"] = all_fpr
tpr["macro"] = mean_tpr
roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

# Plot all ROC curves
plt.figure()
plt.plot(fpr["micro"], tpr["micro"],
         label='micro-average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["micro"]),
         color='deeppink', linestyle=':', linewidth=4)

plt.plot(fpr["macro"], tpr["macro"],
         label='macro-average ROC curve (area = {0:0.2f})'
               ''.format(roc_auc["macro"]),
         color='navy', linestyle=':', linewidth=4)

colors = cycle(['aqua', 'darkorange', 'cornflowerblue'])

# anpassen
classe = ["neg","neutral", "pos"]

for i, color in zip(range(n_classes), colors):
    plt.plot(fpr[i], tpr[i], color=color, lw=lw,
             label='ROC curve of class {0} (area = {1:0.2f})'
             ''.format(classe[i], roc_auc[i]))

plt.plot([0, 1], [0, 1], 'k--', lw=lw)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic (multi-label)')
plt.legend(loc="lower right")
plt.savefig(".\\ROC_Curve")
plt.show()


# Repeat for Multi Class Problem (Wie viele Kategorien haben wir gebildet?)
# https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html#sphx-glr-auto-examples-model-selection-plot-roc-py

test_label_labels = test_label["Label_Human"].to_numpy()
categories = set(test_label_labels)
i=0

for cat in categories:
    if i==0:
        test_label_labels = np.where(test_label["Label_Human"] == str(cat), i, test_label["Label_Human"])
        print(str(cat), i)
        i=i+1
    else:
        test_label_labels = np.where(test_label_labels == str(cat), i, test_label_labels)
        print(str(cat), i)
        i=i+1

test_label_labels = test_label_labels.astype(int)

# Transformiere die Spalte Labels (Kategorien) in numerische Werte

test_prediction_labels = test_prediction["Label"].to_numpy()

i=0

for cat in categories:
    if i==0:
        test_prediction_labels = np.where(test_prediction["Label"] == str(cat), i, test_prediction["Label"])
        i=i+1
        print(str(cat), i)
    else:
        test_prediction_labels = np.where(test_prediction_labels == str(cat), i, test_prediction_labels)
        print(str(cat), i)
        i=i+1

test_prediction_labels = test_prediction_labels.astype(int)

# Klassen 0,...,n abspeichern und binarize übergeben
class_num = list(set(test_prediction_labels))

# MultiLabelProblem
test_prediction_bin = label_binarize(test_prediction_labels, classes=class_num)
test_label_bin = label_binarize(test_label_labels, classes=class_num)

n_classes = len(class_num)

# Compute ROC curve and ROC area for each class
fpr = dict()
tpr = dict()
roc_auc = dict()
for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(test_label_bin[:, i], test_prediction_bin[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])

fpr["micro"], tpr["micro"], _ = roc_curve(test_label_bin.ravel(), test_prediction_bin.ravel())
roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])

# First aggregate all false positive rates
all_fpr = np.unique(np.concatenate([fpr[i] for i in range(n_classes)]))

# Then interpolate all ROC curves at this points
mean_tpr = np.zeros_like(all_fpr)
for i in range(n_classes):
    mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])

# Finally average it and compute AUC
mean_tpr /= n_classes

fpr["macro"] = all_fpr
tpr["macro"] = mean_tpr
roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

# Plot all ROC curves
plt.figure()
plt.plot(fpr["micro"], tpr["micro"],
         label='micro-avg. = {0:0.3f}'
               ''.format(roc_auc["micro"]),
         color='deeppink', linestyle=':', linewidth=4)

plt.plot(fpr["macro"], tpr["macro"],
         label='macro-avg. = {0:0.3f}'
               ''.format(roc_auc["macro"]),
         color='navy', linestyle=':', linewidth=4)

colors = cycle(['aqua', 'darkorange', 'cornflowerblue', 'red', 'green', 'yellow', 'black'])
for i, color in zip(range(n_classes), colors):
    plt.plot(fpr[i], tpr[i], color=color, lw=lw,
             label='ROC {}'.format(list(categories)[i]))

plt.plot([0, 1], [0, 1], 'k--', lw=lw)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic (multi-class)')
plt.legend(loc="lower right")
plt.show()
