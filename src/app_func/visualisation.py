from wordcloud import WordCloud, STOPWORDS
import re
import numpy as np
import pandas as pd
import plotly.express as px
from plotly import graph_objects as go


class Visualisation:
    """Visualization graphs"""

    def published_bar(dataframe: pd.DataFrame) -> go.Figure:
        """Bar chart to show published vs non published
        Args:
            dataframe (pd.DataFrame): Dataframe from API call
        Returns:
            go.Figure: Bar chart figure
        """
        # creating the x and y for plot
        num_notpublished = dataframe["journal_ref"].isnull().sum()
        num_published = dataframe["journal_ref"].notnull().sum()
        x = ["non-published", "published"]
        count = [num_notpublished, num_published]
        num_notpublished_percentage = (
            f"Percentage: {num_notpublished/dataframe.shape[0]*100:2.1f}%"
        )
        num_published_percentage = (
            f"Percentage: {num_published/dataframe.shape[0]*100:2.1f}%"
        )
        percentage = [num_notpublished_percentage, num_published_percentage]

        # execute the plot
        fig = px.bar(
            x=x,
            y=count,
            title="",
            labels=dict(y="Count", x=""),
            color=["non published", "published"],
            text=percentage,
        )
        fig.update_layout(font=dict(size=18))
        # fig.update_layout(autosize=False, width=800, height=800)
        return fig

    def num_words_title(dataframe: pd.DataFrame) -> go.Figure:
        """Number of words in 'Title' histogram
        Args:
            dataframe (pd.DataFrame): dataframe from API call
        Returns:
            go.Figure: Histogram figure
        """
        string_len = []

        for string in dataframe["title"]:
            num_words = len(re.findall(r"\w+", string))
            string_len.append(num_words)

        dataframe["num_words_title"] = string_len

        fig = px.histogram(
            dataframe,
            x="num_words_title",
            nbins=40,
            title="Distribution of the number of words in the title",
        )

        return fig

    def num_words_summary(dataframe: pd.DataFrame) -> go.Figure:
        """Number of words in 'Summary' histogram
        Args:
            dataframe (pd.DataFrame): dataframe from API call
        Returns:
            go.Figure: Histogram figure
        """
        string_len = []

        for string in dataframe["summary"]:
            num_words = len(re.findall(r"\w+", string))
            string_len.append(num_words)

        dataframe["num_words_summary"] = string_len

        fig = px.histogram(
            dataframe,
            x="num_words_summary",
            nbins=40,
            title="Distribution of the number of words in the summary",
        )

        return fig

    def year_published(dataframe: pd.DataFrame) -> go.Figure:
        """Barplot to show year published
        Args:
            dataframe (pd.DataFrame): dataframe from API call
        Returns:
            go.Figure: barplot of year published
        """
        dataframe["year_published"] = dataframe["published"].apply(lambda x: int(x[:4]))

        df_grouped = (
            dataframe.groupby(dataframe["year_published"])["title"]
            .count()
            .rename("Count")
            .to_frame()
        )
        fig = px.bar(
            df_grouped,
            text_auto=".1d",
            x=df_grouped.index,
            y=df_grouped["Count"],
            # markers="x",
            title="",
        )
        fig.update_layout(
            font=dict(size=18),
            xaxis_title="Year",
        )
        return fig

    def generate_word_cloud(dataframe: pd.DataFrame) -> np.ndarray:
        """Word cloud words
        Args:
            dataframe (pd.DataFrame): dataframe from API call
        Returns:
            np.ndarray: numpy array of word cloud words
        """
        text = " ".join(i for i in dataframe["summary"])

        stopwords = set(STOPWORDS)
        wordcloud = WordCloud(
            stopwords=stopwords,
            width=500,
            height=500,
            background_color="#F9F9FA",
            colormap="tab10",
            collocations=False,
            regexp=r"[a-zA-z#&]+",
            max_words=50,
            min_word_length=4,
        ).generate(text)

        wordcloud_image = wordcloud.to_array()

        return wordcloud_image

    def display_word_cloud(wordcloud_image: np.ndarray) -> go.Figure:
        """Displays Word Cloud plot
        Args:
            wordcloud_image (np.ndarray): dataframe from API call
        Returns:
            go.Figure: Wordcloud figure
        """
        fig = go.Figure()
        fig.add_trace(go.Image(z=wordcloud_image))
        fig.update_layout(
            height=800,
            xaxis={"visible": False},
            yaxis={"visible": False},
            margin={"t": 0, "b": 0, "l": 0, "r": 0},
            hovermode=False,
            paper_bgcolor="#F9F9FA",
            plot_bgcolor="#F9F9FA",
            title="",
        )

        return fig
