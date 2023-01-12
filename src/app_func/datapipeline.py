import urllib
import pandas as pd
from app_func.sentence_encoder import SentenceEncoder


class DataPipeline:
    """Main data extraction pipeline to deal with data related slicing"""

    def __init__(
        self,
        method_name: str = "query",
        parameters: str = "search_query=all",
    ):
        """Initializes Datapipeline object with Sentence Encoder as well as API keywords
        Args:
            method_name (str, optional): Sets API query to query mode. Defaults to "query".
            parameters (str, optional): Sets API query to search all arXiv. Defaults to "search_query=all".
        """
        self.method_name = method_name
        self.encoder = SentenceEncoder()
        self.parameters = parameters

    def query_arxiv(self, search_term: str, num_results: int) -> pd.DataFrame:
        """Function sends an API call to query arXiv
        Args:
            search_term (str): search term as defined by user
            num_results (int): maximum number of search terms as defined by user
        Returns:
            pd.DataFrame: returns a dataframe with parsed XML data from arXiv
        """
        search_term = search_term.replace(" ", "+")

        query = f"http://export.arxiv.org/api/{self.method_name}?{self.parameters}:{search_term}&start=0&max_results={num_results}"
        dataframe = pd.read_xml(urllib.request.urlopen(query).read())

        return dataframe

    def dropna(self, df: pd.DataFrame) -> pd.DataFrame:
        """Function cleans up dataframe returned by arXiv.
            drops empty column in summary and across dataset and resets index
        Args:
            df (pd.DataFrame): takes in dataframe from arXiv
        Returns:
            pd.DataFrame: cleaned up dataframe
        """
        df = df.dropna(subset=["summary"])
        df = df.dropna(axis=1, how="all")
        df = df.reset_index(drop=True)

        return df

    def preprocessing_pipeline(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocessing pipeline to clean up summary column
        Args:
            df (pd.DataFrame): un preprocessed dataframe from arXiv
        Returns:
            pd.DataFrame: Pre-processed Dataframe
        """
        df = self.dropna(df)

        # drop duplicates based on the summary column
        df = df.drop_duplicates(subset=["summary"])

        # removes newline characters in title/summary
        df["summary"] = df["summary"].replace(
            {"\n": " ", "\\\\textbf{": "", "}": ""}, regex=True
        )
        df["title"] = df["title"].replace(
            {"\n": " ", "\\\\textbf{": "", "}": ""}, regex=True
        )

        return df

    def cosine_similarity_pipeline(
        self,
        df: pd.DataFrame,
        col: str = "summary",
        num_encodings: int = 50,
        num_links: int = 50,
    ) -> pd.DataFrame:
        """Creates a ranking of Cosine Similarity scores
            create embeddings and merging into subset of dataframe
        Args:
            df (pd.DataFrame): Dataframe from arXiv
            col (str, optional): Identifies the summary column. Defaults to "summary".
            num_encodings (int, optional): Slicer to use only first n papers to generate encodigns. Defaults to 50.
            num_links (int, optional): Slicer to keep only top n links. Defaults to 50.
        Returns:
            pd.DataFrame: Cosine Similarity scores with rankings
        """
        df = df.head(num_encodings)
        embeddings = self.encoder.encode_sentences(df, col=col)
        cosine_dataframe = self.encoder.pairwise_cosine_similarity(
            embeddings=embeddings,
            titles=df.title,
        )

        # merge href into cosine similarity dataframe
        href_df = df[["title", "id", "doi"]]

        cosine_dataframe = pd.merge(
            cosine_dataframe, href_df, left_on="From", right_on="title"
        )
        cosine_dataframe.drop(columns="title", inplace=True)
        cosine_dataframe = (
            cosine_dataframe.sort_values("Weights", ascending=False)
            .reset_index(drop=True)
            .iloc[:num_links]
        )

        return cosine_dataframe
