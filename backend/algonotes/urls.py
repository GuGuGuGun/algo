from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AdminChapterViewSet,
    AdminProblemTagViewSet,
    AdminStudyPlanViewSet,
    AdminTopicViewSet,
    ChapterDetailView,
    ChapterListView,
    ExamYearListView,
    HealthView,
    ProblemTagListView,
    StudyPlanListView,
    TopicListView,
)

router = DefaultRouter()
router.register("manage/chapters", AdminChapterViewSet, basename="manage-chapter")
router.register("manage/topics", AdminTopicViewSet, basename="manage-topic")
router.register("manage/tags", AdminProblemTagViewSet, basename="manage-tag")
router.register("manage/study-plans", AdminStudyPlanViewSet, basename="manage-study-plan")

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("chapters/", ChapterListView.as_view(), name="chapter-list"),
    path("chapters/<int:pk>/", ChapterDetailView.as_view(), name="chapter-detail"),
    path("topics/", TopicListView.as_view(), name="topic-list"),
    path("exam-years/", ExamYearListView.as_view(), name="exam-year-list"),
    path("tags/", ProblemTagListView.as_view(), name="tag-list"),
    path("study-plans/", StudyPlanListView.as_view(), name="plan-list"),
    path("", include(router.urls)),
]
