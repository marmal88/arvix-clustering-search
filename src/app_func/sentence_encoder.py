import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util


class SentenceEncoder:
    """Sentence Encoder class"""

    def __init__(self) -> None:
        """Instantiates Sentence Encoder"""
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def encode_sentences(self, df: pd.DataFrame, col="summary") -> np.ndarray:
        """Encodes sentences with embeddings
        Args:
            df (pd.DataFrame): Dataframe from API
            col (str, optional): Identifies the summary column. Defaults to "summary".
        Returns:
            np.ndarray: Encoding
        """
        sentences = df[col].to_list()
        embeddings = self.model.encode(sentences, batch_size=32)

        return embeddings

    def pairwise_cosine_similarity(
        self, embeddings: np.ndarray, titles: pd.Series
    ) -> pd.DataFrame:
        """Cosine Similarity matrix calculation
        Args:
            embeddings (np.ndarray): encoding
            titles (pd.Series): titles
        Returns:
            pd.DataFrame: pairwise summary of cosine data matrix
        """
        cosine_scores = util.cos_sim(embeddings, embeddings)
        title_mapping = dict(zip(range(len(titles)), titles))

        cosine_dataframe = pd.DataFrame(cosine_scores)
        cosine_dataframe = cosine_dataframe.reset_index(drop=True)
        cosine_dataframe = cosine_dataframe.where(
            ~np.tril(np.ones(cosine_dataframe.shape)).astype(np.bool)
        )

        cosine_dataframe = cosine_dataframe.stack().reset_index()
        cosine_dataframe.columns = ["From", "To", "Weights"]
        cosine_dataframe = cosine_dataframe.replace(title_mapping)

        return cosine_dataframe
