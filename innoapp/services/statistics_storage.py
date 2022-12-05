from innoapp.models import Page, Post


class StatisticsStorage:
    pages_count_data = [page.pk for page in Page.objects.all()]
    posts_count_data = [post.pk for post in Post.objects.all()]

    @classmethod
    def get_pages_count_data(cls, pk):
        if pk not in cls.pages_count_data:
            cls.pages_count_data.append(pk)
        return cls.pages_count_data

    @classmethod
    def get_posts_count_data(cls, pk, signal):
        if signal == 'post_save':
            if pk not in cls.posts_count_data:
                cls.posts_count_data.append(pk)
        if signal == 'post_delete':
            if pk in cls.posts_count_data:
                cls.posts_count_data.remove(pk)
        return cls.posts_count_data
