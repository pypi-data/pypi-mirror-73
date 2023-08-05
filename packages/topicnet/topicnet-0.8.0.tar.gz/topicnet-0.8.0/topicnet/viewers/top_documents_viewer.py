import numpy as np

from collections import defaultdict
from .base_viewer import BaseViewer


def transform_cluster_objects_list_to_dict(object_clusters):
    """
    Transforms list of object clusters to dict.

    Parameters
    ----------
    object_clusters : list
        ith element of list is cluster of ith object

    Returns
    -------
    clusters : dict
        dict, where key is clusterlabel (int), value is cluster objects (list)

    """
    clusters = defaultdict(list)

    for object_label, cluster_label in enumerate(object_clusters):
        clusters[cluster_label].append(object_label)

    clusters = dict(clusters)

    return clusters


def predict_cluster_by_precomputed_distances(precomputed_distances):
    """
    Predict a cluster for each object with precomputed distances.

    Parameters
    ----------
    precomputed_distances : np.array
        array of shape (n_topics, n_objects) - distances from clusters to objects

    Returns
    -------
    np.array
        array of length X.shape[0], each element is cluster of ith object

    """
    return precomputed_distances.T.argmin(axis=1).ravel()


def compute_cluster_top_objects_by_distance(precomputed_distances,
                                            max_top_number=10,
                                            object_clusters=None):
    """
    Compute the most representative objects for each cluster
    using the precomputed_distances.

    Parameters
    ----------
    precomputed_distances : np.array
        array of shape (n_topics, n_objects) -
        a matrix of pairwise distances: distance from ith cluster centroid to the jth object
    max_top_number : int
        maximum number of top objects of cluster (resulting number can be less than it) 
        (Default value = 10)
    object_clusters : np,array
        array of shape n_objects - precomputed clusters for objects

    Returns
    -------
    clusters_top_objects : list of list of indexes 
        (Default value = None)
    """  # noqa: W291
    # prediction for objects
    if object_clusters is None:
        object_clusters = predict_cluster_by_precomputed_distances(precomputed_distances)
    # transformation from list to dict
    clusters = transform_cluster_objects_list_to_dict(object_clusters)
    n_topics = precomputed_distances.shape[0]

    clusters_top_objects = []
    for cluster_label in range(n_topics):
        # cluster is empty
        if cluster_label not in clusters.keys():
            clusters_top_objects.append([])
            continue
        cluster_objects = np.array(clusters[cluster_label])
        cluster_objects_to_center_distances = (
            precomputed_distances[cluster_label][cluster_objects]
        )
        if max_top_number >= cluster_objects.shape[0]:
            # cluster is too small; grab all objects
            indexes_of_top_objects = np.arange(0, cluster_objects.shape[0])
        else:
            # filter by distance with partition
            indexes_of_top_objects = np.argpartition(
                cluster_objects_to_center_distances,
                kth=max_top_number
            )[:max_top_number]

        distances_of_top_objects = cluster_objects_to_center_distances[indexes_of_top_objects]
        top_objects = cluster_objects[indexes_of_top_objects]

        # sorted partitioned array
        indexes_of_top_objects_sorted_by_distance = np.argsort(distances_of_top_objects)
        sorted_top_objects = top_objects[indexes_of_top_objects_sorted_by_distance]

        clusters_top_objects.append(sorted_top_objects.tolist())

    return clusters_top_objects


def prepare_html_string(
    document,
    num_sentences_in_snippet: int = 4,
    num_words: int = 15,
):
    """
    Prepares basic version of raw html
    representing the document.
    Takes title (document_id) and combines it
    with portion of the document text (first few sentences)
    also makes sure that every line contains same number of words

    Parameters
    ----------
    document : Padas.DataFrame row
        a row that contains columns raw_text
        and index in string form
    distance : float between 0 and 1
        measure of how close found document to the
        initial inquiry
    num_sentences_in_snippet
        how many sentences to use for document snippet
    num_words
        number of document words before the line break in
        the document snippet

    Returns
    -------
    doc_html : str
    """
    doc_title = document.index.values[0]
    get_sentences = (
        document['raw_text'].values[0].split('. ')[:num_sentences_in_snippet])
    doc_snippet = '. '.join(get_sentences).split(' ')
    doc_snippet[-1] += '.'
    doc_snippet = ' '.join([
        word + '<br />' if i % num_words + 1 == num_words
        else word for i, word in enumerate(doc_snippet)
    ])
    doc_html = f'<h3>{doc_title}</h3>{doc_snippet}<br />'
    return doc_html


class TopDocumentsViewer(BaseViewer):
    """ """
    def __init__(self,
                 model,
                 dataset=None,
                 precomputed_distances=None,
                 object_clusters=None,
                 max_top_number=10):
        """
        The class provide information about
        top documents for the model topics
        from some collection.

        Parameters
        ----------
        model : TopicModel
            a class of topic model
        dataset : Dataset
            a class that stores information about the collection
        precomputed_distances :  np.array
            array of shape (n_topics, n_objects) -
            an optional matrix of pairwise distances:
            distance from ith cluster centroid to the jth object
        object_clusters : list of int
            an optional array of topic number labels
            for each document from the collection
            ith element of list is cluster of ith object
        max_top_number : int
            number of top documents to provide for each cluster

        """
        super().__init__(model=model)
        self.precomputed_distances = precomputed_distances
        self.object_clusters = object_clusters
        self._dataset = dataset
        self.max_top_number = max_top_number

    def view(
        self,
        current_num_top_doc=None,
        topic_names=None
    ):

        """
        Returns list of tuples (token,score) for
        each topic in the model.

        Parameters
        ----------
        current_num_top_doc : int
            number of top documents to provide for
            each cluster (Default value = None)
        topic_names : list
            list of topic names to view

        Returns
        -------
        all_cluster_top_titles: dict of dict
            returns dict for each topic of the model dict
            contains document_ids of top documents for that topic
            and their probability of belonging to the topic

        """
        # TODO review how top documents returned
        # make method use topic_names to return top documents only
        # for certain topics
        if current_num_top_doc is None:
            current_num_top_doc = self.max_top_number

        theta = self.model.get_theta(dataset=self._dataset)

        document_ids = theta.columns.values
        if self.precomputed_distances is None:
            precomputed_distances = 1.0 - theta.values
        else:
            precomputed_distances = self.precomputed_distances
        if self.object_clusters is not None:
            num_clusters, num_documents = precomputed_distances.shape
            if len(self.object_clusters) != num_documents:
                raise ValueError('number of topics differ from number of labels')
            if not set(range(num_clusters)) >= set(self.object_clusters):
                raise ValueError('provided clusters are not in 0 to num_clusters - 1 range')

        all_cluster_top_indexes = compute_cluster_top_objects_by_distance(
            precomputed_distances,
            max_top_number=current_num_top_doc,
            object_clusters=self.object_clusters
        )

        all_cluster_top_documents_dict = {
            topic: list(document_ids[cluster_top]) for topic, cluster_top
            in zip(theta.index.values, all_cluster_top_indexes)
        }

        for topic in all_cluster_top_documents_dict:
            all_cluster_top_documents_dict[topic] = {
                doc: theta.loc[topic, doc] for doc in all_cluster_top_documents_dict[topic]
            }

        if topic_names is None:
            return all_cluster_top_documents_dict
        else:
            for topic in topic_names:
                if topic not in all_cluster_top_documents_dict.keys():
                    raise ValueError(f'{topic} incorrect topic name')
            view_topic = {topic: content for topic, content
                          in all_cluster_top_documents_dict.items() if topic in topic_names}
            return view_topic

    def view_from_jupyter(
            self,
            current_num_top_doc: int = None,
            topic_names: list = None,
            display_output: bool = True,
            give_html: bool = False,
    ):
        """
        TopDocumentsViewer method recommended for use
        from jupyter notebooks
        Returns texts of the actual documents.

        Parameters
        ----------
        current_num_top_doc
            number of top documents to provide for
            each cluster (Default value = None)
        topic_names
            list of topic names to view
        display_output
            if provide output at the end of method run
        give_html
            return html string generated by the method

        Returns
        -------
        html_output
            html string of the output
        """
        from IPython.display import display_html
        from topicnet.cooking_machine.pretty_output import make_notebook_pretty

        make_notebook_pretty()
        html_output = []

        doc_list = self.view(current_num_top_doc, topic_names=topic_names)

        for topic_name, topic_docs_dict in doc_list.items():
            topic_docs = list(topic_docs_dict.keys())
            topic_html = ''
            topic_headline = f'<h1><b>Topic name:</b> {topic_name}</h1>'
            topic_html += topic_headline
            for doc_id in topic_docs:
                document = self._dataset.get_source_document(doc_id)
                topic_html += prepare_html_string(document)
            html_output.append(topic_html)
        if display_output:
            display_html('<br />'.join(html_output), raw=True)
        if give_html:
            return html_output
