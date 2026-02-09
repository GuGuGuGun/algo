from django.db.models import Count, Q
from rest_framework import filters, generics, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chapter, ProblemTag, StudyPlan, Topic
from .serializers import (
    AdminChapterSerializer,
    AdminProblemTagSerializer,
    AdminStudyPlanSerializer,
    AdminTopicSerializer,
    ChapterDetailSerializer,
    ChapterListSerializer,
    ProblemTagSerializer,
    StudyPlanSerializer,
    TopicSerializer,
)


class HealthView(APIView):
    def get(self, request):
        return Response({"message": "labelu backend is running"})


class ChapterListView(generics.ListAPIView):
    serializer_class = ChapterListSerializer

    def get_queryset(self):
        queryset = Chapter.objects.annotate(topic_count=Count("topics"))
        difficulty = self.request.query_params.get("difficulty")
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        return queryset


class ChapterDetailView(generics.RetrieveAPIView):
    queryset = Chapter.objects.all().prefetch_related("topics__tags")
    serializer_class = ChapterDetailSerializer


class TopicListView(generics.ListAPIView):
    serializer_class = TopicSerializer

    def get_queryset(self):
        queryset = Topic.objects.select_related("chapter").prefetch_related("tags")
        keyword = self.request.query_params.get("keyword")
        chapter_id = self.request.query_params.get("chapter_id")
        key_exam_only = self.request.query_params.get("key_exam_only")
        year = self.request.query_params.get("year")

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword)
                | Q(knowledge_point__icontains=keyword)
                | Q(note__icontains=keyword)
            )
        if chapter_id:
            queryset = queryset.filter(chapter_id=chapter_id)
        if key_exam_only in {"1", "true", "True"}:
            queryset = queryset.filter(is_key_for_exam=True)
        if year:
            try:
                year_int = int(year)
            except ValueError:
                return queryset.none()
            queryset = queryset.filter(exam_years__contains=[year_int])
        return queryset


class ProblemTagListView(generics.ListAPIView):
    queryset = ProblemTag.objects.all()
    serializer_class = ProblemTagSerializer


class StudyPlanListView(generics.ListAPIView):
    queryset = StudyPlan.objects.all()
    serializer_class = StudyPlanSerializer


class ExamYearListView(APIView):
    def get(self, request):
        counter = {}
        for years in Topic.objects.values_list("exam_years", flat=True):
            for year in years or []:
                counter[year] = counter.get(year, 0) + 1
        data = [
            {"year": year, "topic_count": counter[year]}
            for year in sorted(counter.keys(), reverse=True)
        ]
        return Response(data)


class AdminPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class AdminBaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = AdminPageNumberPagination


class AdminChapterViewSet(AdminBaseViewSet):
    queryset = Chapter.objects.all().order_by("order", "id")
    serializer_class = AdminChapterSerializer
    search_fields = ["title", "summary"]
    ordering_fields = ["id", "order", "difficulty", "estimated_hours", "updated_at"]
    ordering = ["order", "id"]


class AdminTopicViewSet(AdminBaseViewSet):
    queryset = Topic.objects.select_related("chapter").prefetch_related("tags").all().order_by("id")
    serializer_class = AdminTopicSerializer
    search_fields = ["title", "knowledge_point", "note", "exam_tip"]
    ordering_fields = ["id", "title", "chapter_id", "is_key_for_exam", "updated_at"]
    ordering = ["id"]

    def get_queryset(self):
        queryset = super().get_queryset()
        chapter_id = self.request.query_params.get("chapter_id")
        difficulty = self.request.query_params.get("difficulty")
        is_key_for_exam = self.request.query_params.get("is_key_for_exam")
        if chapter_id:
            queryset = queryset.filter(chapter_id=chapter_id)
        if difficulty:
            queryset = queryset.filter(chapter__difficulty=difficulty)
        if is_key_for_exam in {"1", "true", "True"}:
            queryset = queryset.filter(is_key_for_exam=True)
        if is_key_for_exam in {"0", "false", "False"}:
            queryset = queryset.filter(is_key_for_exam=False)
        return queryset


class AdminProblemTagViewSet(AdminBaseViewSet):
    queryset = ProblemTag.objects.prefetch_related("topics").all().order_by("id")
    serializer_class = AdminProblemTagSerializer
    search_fields = ["name"]
    ordering_fields = ["id", "name", "category"]
    ordering = ["id"]


class AdminStudyPlanViewSet(AdminBaseViewSet):
    queryset = StudyPlan.objects.all().order_by("week")
    serializer_class = AdminStudyPlanSerializer
    search_fields = ["target", "focus"]
    ordering_fields = ["id", "week", "recommended_hours"]
    ordering = ["week"]
