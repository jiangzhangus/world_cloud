# pip install -r requirements.txt
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd
import nltk
from wordcloud import WordCloud, STOPWORDS
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# download nltk data
nltk.download('vader_lexicon')


# output format tool
def percentage(part, whole):
    return 100 * float(part) / float(whole)


positive = 0
negative = 0
neutral = 0
polarity = 0
text_list = []
neutral_list = []
negative_list = []
positive_list = []
nrows = 0

with open('yelp_data_part.xlsx', 'rb') as input_file:
    yelp_df = pd.read_excel(input_file)
    yelp_df = yelp_df.head(5)

    for index, row in yelp_df.iterrows():
        # print(index, row['user_id'], row['review_id'], row['useful'], row['cool'], row['funny'], row['text'])
        nrows += 1
        # if nrows > 100:
        #   break

        row_text = row['text']
        text_list.append(row_text)
        analysis = TextBlob(row_text)  #??
        score = SentimentIntensityAnalyzer().polarity_scores(row_text)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        comp = score['compound']
        polarity += analysis.sentiment.polarity  #??

        if neg > pos:
            negative_list.append(row_text)
            negative += 1
        elif pos > neg:
            positive_list.append(row_text)
            positive += 1

        elif pos == neg:
            neutral_list.append(row_text)
            neutral += 1

    pos_percent = percentage(positive, nrows)
    neg_percent = percentage(negative, nrows)
    neu_percent = percentage(neutral, nrows)
    polarity_percent = percentage(polarity, nrows)
    pos_percent = format(pos_percent, '.1f')
    neg_percent = format(neg_percent, '.1f')
    neu_percent = format(neu_percent, '.1f')

text_list_df = pd.DataFrame(text_list)
text_list_df.drop_duplicates(inplace=True)

neutral_list_df = pd.DataFrame(neutral_list)
negative_list_df = pd.DataFrame(negative_list)
positive_list_df = pd.DataFrame(positive_list)
print("total number: ", len(text_list))
print("positive number: ", len(positive_list))
print("negative number: ", len(negative_list))
print("neutral number: ", len(neutral_list))

# Create stopword list:
stopwords = set(STOPWORDS)
stopwords.update(["_x000D_"])

textt = " ".join(review for review in yelp_df.text)
wordcloud = WordCloud(stopwords=stopwords,
                      background_color="white").generate(textt)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
