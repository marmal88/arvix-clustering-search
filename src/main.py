""" main.py is the main page for app.  It provides the text input with button 
    for user to enter query string.  4 plotly components are generated
    1) Network graph show similarity of articles
    2) Word Cloud
    3) Trend of paper published over the years and 
    4) No. of published and non-published papers
"""

import streamlit as st
from streamlit_plotly_events import plotly_events
import time

from app_func.datapipeline import DataPipeline
from app_func.visualisation import Visualisation
from app_func.network_graph import Network


def do_search():
    """this function performs the following action
    1) use DataPipeline to query arXiv and generate the required dataframe
    2) use Visualisation and Network to generate the plotly charts
    """
    with st.spinner("Performing search"):
        start_time = time.time()
        connector = DataPipeline()
        df = connector.query_arxiv(
            st.session_state.search_term, st.session_state.num_searches
        )

    with st.spinner("Calculating paper similarity"):
        df = connector.preprocessing_pipeline(df)
        cosine_df = connector.cosine_similarity_pipeline(
            df,
            num_encodings=st.session_state.num_papers,
            num_links=st.session_state.num_links,
        )
        network = Network()
        st.session_state.network_graph = network.plot_networkgraph(cosine_df)

    with st.spinner("Generating word cloud and other visualizations"):
        wc = Visualisation.generate_word_cloud(df)
        st.session_state.word_cloud = Visualisation.display_word_cloud(wc)
        st.session_state.df = df
        (
            st.session_state.labels,
            st.session_state.network_graph,
        ) = Network().plot_networkgraph(cosine_df)
        wc = Visualisation.generate_word_cloud(df)
        st.session_state.word_cloud = Visualisation.display_word_cloud(wc)
        st.session_state.year_trend = Visualisation.year_published(df)
        st.session_state.published_bar = Visualisation.published_bar(df)

        print("do_search(): [] %s seconds ]" % (time.time() - start_time))


def display_graph():
    """handles the display of network graph"""
    start_time = time.time()
    # st.plotly_chart(st.session_state.network_graph)
    selected_points = plotly_events(st.session_state.network_graph, click_event=True)
    print(selected_points)
    if len(selected_points) != 0:
        idx = selected_points[0]["pointIndex"]
        title = st.session_state.labels[idx]
        df_idx = (st.session_state.df["title"] == title).argmax()
        href = st.session_state.df["id"][df_idx]
        st.markdown(f"Paper url: [{title}]({href})", unsafe_allow_html=True)
    print("display_graph(): [] %s seconds ]" % (time.time() - start_time))


def display_cloud():
    """handles the display of word cloud"""
    start_time = time.time()
    st.plotly_chart(st.session_state.word_cloud)
    print("display_cloud(): [] %s seconds ]" % (time.time() - start_time))


def display_year_trends():
    """handles the display of paper published over years trend"""
    start_time = time.time()
    st.plotly_chart(st.session_state.year_trend, use_container_width=True)
    print("display_year_trends(): [] %s seconds ]" % (time.time() - start_time))


# @st.cache(suppress_st_warning=True)
def display_published_bar():
    """handles the display of published vs non-published paper"""
    start_time = time.time()
    st.plotly_chart(st.session_state.published_bar, use_container_width=True)
    print("display_published_bar(): [] %s seconds ]" % (time.time() - start_time))


load_start_time = time.time()
st.title("ArXiv Clustering Search")
with st.form(key="my_form"):
    st.text_input("Search term", key="search_term")
    submit_button = st.form_submit_button(label="Submit", on_click=do_search)
    with st.expander("Advanced options"):
        results_limit = st.slider(
            label="Search results to return",
            value=50,
            min_value=10,
            max_value=500,
            step=5,
            key="num_searches",
        )
        network_graph_limit = st.slider(
            label="Number of papers for network graph",
            value=50,
            min_value=10,
            max_value=500,
            step=5,
            key="num_papers",
        )
        link_limits = st.slider(
            label="Number of links to show",
            value=50,
            min_value=10,
            max_value=500,
            step=5,
            key="num_links",
        )

if "network_graph" in st.session_state:
    st.subheader(f"Network graph")
    st.caption(
        "The network graph shows the relationships between the papers returned from the search results"
    )
    display_graph()
    st.markdown("""---""")

if "word_cloud" in st.session_state:
    st.subheader(
        f"Wordcloud (Summaries of the first {st.session_state.num_papers} papers)"
    )
    st.caption(
        "The wordcloud shows the related keywords. Users can search using these keywords to generate more relevant search results)"
    )
    display_cloud()
    st.markdown("""---""")

if "year_trend" in st.session_state:
    st.subheader(f"Yearly trends of the number of papers")
    st.caption(
        "From this line plot, we can observe the trends in the number of papers submitted to arXiv for the search term."
    )
    display_year_trends()
    st.markdown("""---""")

if "published_bar" in st.session_state:
    st.subheader(f"Number of published and non-published papers")
    st.caption(
        "From this plot, we can get an idea of how many papers are eventually published."
    )
    display_published_bar()

print("page loading(): [] %s seconds ]" % (time.time() - load_start_time))
