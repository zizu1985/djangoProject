from haystack import indexes
from .models import Post


# What fields will be indexed and object model for indexing
class PostIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    publish = indexes.DateTimeField(model_attr='publish')

    def get_model(self):
        # What class will be indexed
        return Post

    # indexing range for Post object. We will include all published posts
    def index_queryset(self, using=None):
        return self.get_model().published.all()

