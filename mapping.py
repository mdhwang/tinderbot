import folium
from folium.plugins import HeatMap


import plotly.figure_factory as ff

def generateBaseMap(default_location=[37.793331, -122.392776], default_zoom_start=12):
    # Generates Base Folium Map

    base_map = folium.Map(location=default_location, control_scale=True, zoom_start=default_zoom_start)
    return base_map

def plot_user_heatmap(data):
    '''
    Use folium to generate heatmap based on user locations.
    '''
    base_map = generateBaseMap()
    new = data[-data.city.isna()]
    new = new[-new.location.isna()]
    new['lat'] = new.location.apply(lambda x: x[0])
    new['lon'] = new.location.apply(lambda x: x[1])
    new['count'] = 1
    HeatMap(data=new[['lat', 'lon', 'count']].groupby(['lat', 'lon']).sum().reset_index().values.tolist(), radius=8, max_zoom=13).add_to(base_map)
    return base_map
 
def plot_cosine_dist(category,cosine_data):
    fig = ff.create_distplot(np.array([cosine_data.to_list()]), ['cosine'],bin_size=.005)
    mean = cosine_data.mean()
    std = cosine_data.std()
    lines = [mean,mean+std,mean-std,mean+2*std,mean-2*std]
    for each in lines:
        fig.add_shape(
                # Line Vertical
                dict(
                    type="line",
                    x0=each,
                    y0=0,
                    x1=each,
                    y1=50,
                    line=dict(
                        color="Red",
                        width=3
                    )
        ))
    fig.update_layout(title={'text':'Mean Similarity Distribution for {}'.format(category),
                        'xanchor': 'left'},
                        xaxis_title="Cosine Similarity to Average User",
                        yaxis_title="Frequency",)
    fig.show()