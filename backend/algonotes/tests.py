from django.test import TestCase

from .models import Chapter


class ChapterModelTests(TestCase):
    def test_create_chapter(self):
        chapter = Chapter.objects.create(
            title="测试章节",
            summary="测试摘要",
            order=1,
            difficulty="easy",
            estimated_hours=5,
        )
        self.assertEqual(chapter.title, "测试章节")

