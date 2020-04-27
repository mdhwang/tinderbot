import pandas as pd
import math
import numpy as np

from nmf_helpers import build_text_vectorizer

from sklearn.metrics.pairwise import cosine_similarity

from clean import stats

import plotly.figure_factory as ff

  
def single_city_query(df):
    query = input("WHAT CITY? : ")
    if query not in df.city.to_list():
        print("CITY NOT FOUND")
    df = df[df.city == query]
    stats(df)
    calc_similarity(df,query)


def calc_similarity(data,query):
    '''
    Take details per user in specified dataset with category equal to value
    Vectorize each
    Compare each to each and calculate mean
    Get distribution of means of all users
    Calculate and label users based on standard deviations away from mean
    Return updated dataframe
    '''
    
    # Vectorize details per user

    reduced = data[-data.filtered_details.isna()].copy()
    contents = reduced.filtered_details
    
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

    reduced['cosine'] = cosine_diff

    def std_classifier(cosine_vals):
        mean = cosine_vals.mean()
        std = cosine_vals.std()
        std_class = []
        for each in cosine_vals:
            diff = abs(each-mean)
            distance = math.ceil(diff / std)
            std_class.append(distance)
        return std_class

    reduced['std_class'] = std_classifier(reduced.cosine)


    # sb.distplot(reduced.cosine)
    # plt.show()

    fig = ff.create_distplot(np.array([reduced.cosine.to_list()]), ['User Cosine Similarity to Mean Profile'],bin_size=.005,show_rug=False)
    mean = reduced.cosine.mean()
    std = reduced.cosine.std()
    deviations = [mean+std,mean-std,mean+2*std,mean-2*std]
    
    fig.add_shape(
                # Line Vertical
                dict(
                    type="line",
                    xref="paper",
                    yref="paper",
                    x0=mean,
                    y0=0,
                    x1=mean,
                    y1=1,
                    line=dict(
                        color="Red",
                        width=3
                    )
        )
    )

    for each in deviations:
        fig.add_shape(
                # Line Vertical
                dict(
                    type="line",
                    xref="paper",
                    yref="paper",
                    x0=each,
                    y0=0,
                    x1=each,
                    y1=1,
                    line=dict(
                        color="Blue",
                        width=3
                    )
        )
    )

    fig.update_layout(title_text='User Similarity to Mean User Distribution for {}'.format(query),
                        title_x=0.5,
                        xaxis_title="Cosine Similarity to Average User",
                        yaxis_title="Frequency",)

    fig.update_layout(
        legend=dict(
            x=0,
            y=1,
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        )
    )
    fig.show()




    return reduced


df = pd.read_csv("data/processed/cleaned_data.csv")
reduced = single_city_query(df)

