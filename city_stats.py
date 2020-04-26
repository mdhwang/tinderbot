import pandas as pd

from topics import *
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.metrics.pairwise import cosine_similarity

from clean import stats

def calc_city_stats(df):
    '''
    Take in cleaned and processed data, remove cities with less than 100 data points
    Calculate statistics per city - display top 5
    - % that advertise IG
    - % that advertise SC
    - % that mention Coivd
    - % 

    '''
    reduced = df.groupby('city').filter(lambda x: x["name"].count() > 50)
    citydf = pd.DataFrame(reduced.groupby('city').size(),columns=["DPs"])
    citydf['college'] = reduced.groupby('city').apply(lambda x: round(100*x['college'].count()/x['name'].count(),1))
    citydf['job'] = reduced.groupby('city').apply(lambda x: round(100*x['job'].count()/x['name'].count(),1))
    citydf['anthem'] = reduced.groupby('city').apply(lambda x: round(100*x['anthem'].count()/x['name'].count(),2))
    citydf['age_dist'] = reduced.groupby('city').apply(lambda x: x['age'].to_list())
    for each in topics:
        citydf[each] = reduced.groupby('city').apply(lambda x: round(100*x[each].sum()/x['name'].count(),2))

    return citydf

def top_5(citydf):
    print("---------------------------------------------")
    print("-----------HERE ARE YOUR TOP 5---------------")
    print("-----TOP 5 CITIES WITH HIGHEST COLLEGE %-----")
    print(citydf.college.sort_values(ascending=False).head())
    print("---------------------------------------------")
    print("-------TOP 5 CITIES WITH HIGHEST JOB %-------")
    print(citydf.job.sort_values(ascending=False).head())
    print("------TOP 5 CITIES WITH HIGHEST ANTHEM %-----")
    print(citydf.anthem.sort_values(ascending=False).head())
    print("--------TOP 5 CITIES WITH HIGHEST IG %-------")
    print(citydf.instagram.sort_values(ascending=False).head())
    print("-------TOP 5 CITIES WITH HIGHEST SNAP %------")
    print(citydf.snapchat.sort_values(ascending=False).head())
    print("-------TOP 5 CITIES WITH HIGHEST COVID %-----")
    print(citydf.covid19.sort_values(ascending=False).head())
    print("-------TOP 5 CITIES WITH HIGHEST WEED %-----")
    print(citydf.cannabis.sort_values(ascending=False).head())
    
def single_city_query(df):
    query = input("WHAT CITY? : ")
    if query not in df.city.to_list():
        print("CITY NOT FOUND")
    df = df[df.city == query]
    stats(df)
    sb.distplot(df[-df.age.isna()].age)
    plt.show()
    
df = pd.read_csv("data/processed/cleaned_data.csv")
# new = calc_city_stats(df)
# top_5(new)
single_city_query(df)


def calc_similarity(data,category,value):
    '''
    Take details per user in specified dataset with category equal to value
    Vectorize each
    Compare each to each and calculate mean
    Get distribution of means of all users
    Calculate and label users based on standard deviations away from mean
    Return updated dataframe
    '''

    print("Calculating user similarity on dataset where {} equals {}".format(category,value))
    specified = data[data[category]==value]
    specified = specified[-specified.category.isna()]
    print("Found {} Users".format(len(specified)))
    contents = specified.details
    
    # Vectorize details per user
    vectorizer, vocabulary = build_text_vectorizer(contents,
                             use_tfidf=True,
                             use_stemmer=True,
                             max_features=5000)
    X = vectorizer(contents)
    
    # COMPARE TO THE AVERAGE VECTOR O(n)
    avg = np.mean(X,axis=0)
    cosine_diff = []
    for user in X:
        cosine_diff.append(cosine_similarity(user.reshape(1,-1),avg.reshape(1,-1))[0][0])
    
    # COMPARE EACH TO EACH O(n)^2
    # cosine_diff = []
    # for user in X:
    #     average = []
    #     for other in X:
    #         average.append(cosine_similarity(user.reshape(1, -1),other.reshape(1, -1))[0][0])
    #     cosine_diff.append(np.mean(average))

    data['cosine'] = cosine_diff

    def std_classifier(cosine_vals):
        mean = cosine_vals.mean()
        std = cosine_vals.std()
        std_class = []
        for each in cosine_vals:
            diff = abs(each-mean)
            distance = math.ceil(diff / std)
            std_class.append(distance)
        return std_class

    data['std_class'] = std_classifier(data.cosine)

    return data