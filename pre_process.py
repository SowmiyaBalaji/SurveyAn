# process_file.py
import os
import numpy as np
import pandas as pd
import spacy
from translate import example_tamil


nlp = spacy.load("en_core_web_sm")


def clean(text):
    doc = nlp(text)
    filtered_tokens = []
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        else:
            filtered_tokens.append(token.lemma_)
    return " ".join(filtered_tokens)
# convert it into one sentence without stop words and punctuations(.,-) and also with the base words.


def pre_process_file(file_path):
    # Implement your Python code to process the uploaded file
    # For example, you can read the content of the file, perform sentiment analysis, etc.
    # Return the result or any output from your Python code as a string
    example_tamil()

    df = pd.read_csv(file_path, sep=";", names=["Description", "Emotion"])
    df['processed_text'] = df["Description"].apply(clean)

    print(df.head(5))

    return df
