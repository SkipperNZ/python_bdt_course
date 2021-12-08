from lms import VideoItem, CompositeLearningItem, Quiz, ProgrammingAssigment


def test_composite_works():
    video_item_1 = VideoItem(name="Composite Design Pattern", lenght=20)
    video_item_2 = VideoItem(name="Composite Design Pattern v.2", lenght=10)
    lesson_composite = CompositeLearningItem(name="lesson on composite")
    lesson_composite.add(video_item_1)
    lesson_composite.add(video_item_2)
    expeced_composite_study_time = (20 * 1.5 + 10 * 1.5)
    assert expeced_composite_study_time == lesson_composite.estimate_study_time()

    video_item_3 = VideoItem(name="Adapter Design Pattern", lenght=20)
    quiz = Quiz(name="Adapter Design Patterns Quiz",
                questions=["a", "b", "c"])
    lesson_adapter = CompositeLearningItem(
        name="lesson on adapter", learning_items=[video_item_3, quiz])
    expeced_adapter_study_time = (20 * 1.5 + 5 * 3)
    assert expeced_adapter_study_time == lesson_adapter.estimate_study_time()

    module_design_pattern = CompositeLearningItem(
        name="Design Patterns", learning_items=[lesson_composite, lesson_adapter])
    module_design_pattern.add(
        ProgrammingAssigment(
            name="Factory Method Programming Assignment", language="python")
    )
    assert (expeced_composite_study_time + expeced_adapter_study_time +
            120) == module_design_pattern.estimate_study_time()
