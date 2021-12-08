from abc import ABC, abstractmethod


class LearningItem(ABC):
    def __init__(self, name) -> None:
        self.name = name

    @abstractmethod
    def estimate_study_time(self):
        raise NotImplementedError


class VideoItem(LearningItem):
    def __init__(self, name, lenght) -> None:
        super().__init__(name)
        self.lenght = lenght

    def estimate_study_time(self):
        return 1.5 * self.lenght


class Quiz(LearningItem):
    def __init__(self, name, questions) -> None:
        super().__init__(name)
        self.questions = questions

    def estimate_study_time(self):
        return 5 * len(self.questions)


class ProgrammingAssigment(LearningItem):
    def __init__(self, name, language) -> None:
        super().__init__(name)
        self.language = language

    def estimate_study_time(self):
        return 120


# тут уже заводим композит
class CompositeLearningItem(LearningItem):
    def __init__(self, name, learning_items=None) -> None:
        super().__init__(name)
        self.learning_items = []
        self.learning_items.extend(learning_items or [])

    def add(self, learning_item):
        self.learning_items.append(learning_item)

    def estimate_study_time(self):
        study_time = sum(
            learning_item.estimate_study_time()
            for learning_item in self.learning_items
        )
        return study_time


"""
# это писалось в начале, потом переместили это в тесты
def main():
    # course = ??()
    # course.add(...)
    video_item_1 = VideoItem(name="Composite Design Pattern", lenght=20)
    video_item_2 = VideoItem(name="Composite Design Pattern v.2", lenght=10)
    lesson_composite = CompositeLearningItem(name="lesson on composite")
    lesson_composite.add(video_item_1)
    lesson_composite.add(video_item_2)

    video_item_3 = VideoItem(name="Adapter Design Pattern", lenght=20)
    quiz = Quiz(name="Adapter Design Patterns Quiz",  questions=["a", "b", "c"])
    lesson_adapter = CompositeLearningItem(name="lesson on adapter", learning_items=[video_item_3, quiz])

    module_design_pattern = CompositeLearningItem(name="Design Patterns", learning_items=[lesson_composite, lesson_adapter])
    module_design_pattern.add(
        ProgrammingAssigment(name="Factory Method Programming Assignment", language="python")
    )


if __name__ == '__main__':
    main()

"""
