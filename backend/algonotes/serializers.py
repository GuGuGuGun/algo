from rest_framework import serializers

from .models import Chapter, ProblemTag, StudyPlan, Topic


class TopicSerializer(serializers.ModelSerializer):
    chapter_title = serializers.CharField(source="chapter.title", read_only=True)
    tags = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)

    class Meta:
        model = Topic
        fields = [
            "id",
            "chapter",
            "chapter_title",
            "title",
            "knowledge_point",
            "note",
            "template_code",
            "template_codes",
            "template_modes",
            "practice_links",
            "exam_tip",
            "exam_years",
            "is_key_for_exam",
            "tags",
        ]


class ChapterListSerializer(serializers.ModelSerializer):
    topic_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Chapter
        fields = [
            "id",
            "title",
            "summary",
            "order",
            "difficulty",
            "estimated_hours",
            "topic_count",
        ]


class ChapterDetailSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Chapter
        fields = [
            "id",
            "title",
            "summary",
            "order",
            "difficulty",
            "estimated_hours",
            "topics",
        ]


class ProblemTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemTag
        fields = ["id", "name", "category"]


class StudyPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyPlan
        fields = ["id", "week", "target", "focus", "recommended_hours"]


class AdminChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = [
            "id",
            "title",
            "summary",
            "order",
            "difficulty",
            "estimated_hours",
            "created_at",
            "updated_at",
        ]


class AdminTopicSerializer(serializers.ModelSerializer):
    chapter_title = serializers.CharField(source="chapter.title", read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=ProblemTag.objects.all(), required=False)
    tag_names = serializers.SlugRelatedField(source="tags", slug_field="name", many=True, read_only=True)

    class Meta:
        model = Topic
        fields = [
            "id",
            "chapter",
            "chapter_title",
            "title",
            "knowledge_point",
            "note",
            "template_code",
            "template_codes",
            "template_modes",
            "practice_links",
            "exam_tip",
            "exam_years",
            "is_key_for_exam",
            "tags",
            "tag_names",
            "created_at",
            "updated_at",
        ]

    def validate_template_codes(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("template_codes 必须是对象。")
        for language, code in value.items():
            if not isinstance(language, str) or not isinstance(code, str):
                raise serializers.ValidationError("template_codes 的键和值都必须是字符串。")
        return value

    def validate_template_modes(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("template_modes 必须是对象。")
        for mode, mode_codes in value.items():
            if not isinstance(mode, str) or not isinstance(mode_codes, dict):
                raise serializers.ValidationError("template_modes 的值必须是代码对象。")
            for language, code in mode_codes.items():
                if not isinstance(language, str) or not isinstance(code, str):
                    raise serializers.ValidationError("template_modes 内部代码必须是字符串。")
        return value

    def validate_practice_links(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("practice_links 必须是对象。")
        for platform, items in value.items():
            if platform not in {"leetcode", "nowcoder"}:
                raise serializers.ValidationError("practice_links 平台仅支持 leetcode 或 nowcoder。")
            if not isinstance(items, list):
                raise serializers.ValidationError("practice_links 的平台值必须是列表。")
            for item in items:
                if not isinstance(item, dict):
                    raise serializers.ValidationError("practice_links 列表项必须是对象。")
                title = item.get("title")
                url = item.get("url")
                if not isinstance(title, str) or not isinstance(url, str):
                    raise serializers.ValidationError("practice_links 的 title/url 必须是字符串。")
        return value


class AdminProblemTagSerializer(serializers.ModelSerializer):
    topics = serializers.PrimaryKeyRelatedField(many=True, queryset=Topic.objects.all(), required=False)

    class Meta:
        model = ProblemTag
        fields = ["id", "name", "category", "topics"]


class AdminStudyPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyPlan
        fields = ["id", "week", "target", "focus", "recommended_hours"]
