import joblib
import pandas as ps
import seaborn as sn
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
df = pd.read_csv(r"C:\Users\admin\OneDrive\Desktop\surveyan\archive\train.txt", sep=";",
                 names=["Description", "Emotion"])
testdf = pd.read_csv(r"C:\Users\admin\OneDrive\Desktop\surveyan\archive\test.txt", sep=";",
                     names=["Description", "Emotion"])
df = pd.concat([df, testdf], ignore_index=True)
df['label_num'] = df['Emotion'].map({
    'joy': 0,
    'love': 1,
    'surprise': 2,
    'sadness': 3,
    'anger': 4,
    'fear': 5
})

X_train, X_test, y_train, y_test = train_test_split(
    df.Description, df.label_num, test_size=0.2)

nlp = spacy.load("en_core_web_sm")


def preprocess(text):
    doc = nlp(text)
    filtered_tokens = []
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        else:
            filtered_tokens.append(token.lemma_)
    return " ".join(filtered_tokens)
# convert it into one sentence without stop words and punctuations(.,-) and also with the base words.


df['processed_text'] = df["Description"].apply(preprocess)

X_train, X_test, y_train, y_test = train_test_split(
    df.processed_text,
    df.label_num,
    test_size=0.2,  # 20% samples will go to test dataset
    random_state=2022,
    stratify=df.label_num
)


# Assuming you already have X_train, y_train, X_test, y_test defined

clfrf = Pipeline([
    # using the ngram_range parameter
    ('vectorizer_tfidf', TfidfVectorizer()),
    ('Random Forest', RandomForestClassifier())
])

# Train the model with X_train and y_train
clfrf.fit(X_train, y_train)

# Save the model to a file
joblib.dump(clfrf, 'random_forest_model.pkl')

# 3. get the predictions for X_test and store it in y_pred
y_predrf = clfrf.predict(X_test)

# 4. print the classfication report
print(classification_report(y_test, y_predrf))

cmrf = confusion_matrix(y_test, y_predrf)

plt.figure(figsize=(8, 5))
sn.heatmap(cmrf, annot=True, fmt='d')
plt.xlabel('Prediction')
plt.ylabel('Truth')

report = classification_report(y_test, y_predrf, output_dict=True)
dfrf = ps.DataFrame(report).transpose()

dict = {0: 'joy', 1: 'love', 2: 'surprise',
        3: 'sadness', 4: 'anger', 5: 'fear'}

X_test_list = X_test.tolist()
y_test_list = y_test.tolist()
y_pred_list = y_predrf.tolist()

# Now, you can use the lists or arrays in the zip function
res = "\n\n".join("{} \nActual:{} ---Predicted:{}".format(x,
                  dict[y], dict[z]) for x, y, z in zip(X_test_list, y_test_list, y_pred_list))
# print(res)

num_lines = res.count('\n') + 1
print(num_lines)
