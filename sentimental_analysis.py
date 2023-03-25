from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pickle
import pandas as pd

import nltk
nltk.download('stopwords')

tokenizer = RegexpTokenizer(r"\w+")
en_stopwords = set(stopwords.words('english'))
ps = PorterStemmer()

def applicationDataPreProcessing(X_data):
    #Convert feedback data into lower case
    lower_data = X_data.lower()

    #Convert senetence into words (token)
    tokens = tokenizer.tokenize(lower_data)

    #New token after removing stop words
    new_tokens = [ token for token in tokens if token not in en_stopwords ]

    #Stemming - Converting words into its root format
    stemmed_tokens = [ ps.stem(token) for token in new_tokens ]

    x_clean = " ".join(stemmed_tokens)

    #Vectorization
    cv = CountVectorizer(ngram_range=(1,2))
    xt_vector = cv.transform(x_clean).toarray()

    return x_vector



def modelDataPreprocessing(X_data):
    pre_processed_data = []
    for data in X_data:
        #Convert feedback data into lower case
        lower_data = data.lower()

        #Convert senetence into words (token)
        tokens = tokenizer.tokenize(lower_data)
        
        #New token after removing stop words
        new_tokens = [ token for token in tokens if token not in en_stopwords ]

        #Stemming - Converting words into its root format
        stemmed_tokens = [ ps.stem(token) for token in new_tokens ]

        pre_processed_data.append(" ".join(stemmed_tokens))

    
    return pre_processed_data

csv_data = pd.read_csv("data-set.csv")
data_values = csv_data.values.tolist()
y_train = []
data_list = []
for data in data_values:
    y_train.append(data[0])
    data_list.append(data[1])

X_clean =  modelDataPreprocessing(data_list)

#Vectorization
cv = CountVectorizer(ngram_range=(1,2))
x_vector = cv.fit_transform(X_clean).toarray()

mn = MultinomialNB()
mn.fit(x_vector, y_train)


with open('sentimental-analysis-modal', 'wb') as picklefile:
    pickle.dump(mn,picklefile)
    
#Load the model
#with open('sentimental-analysis-modal', 'rb') as training_model:
#    model = pickle.load(training_model)