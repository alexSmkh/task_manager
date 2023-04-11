from django.db import models

from main.models.tag import Tag


class Task(models.Model):

    class StateChoice(models.TextChoices):
        NEW_TASK = 'new'
        IN_DEVELOPMENT = 'in development'
        IN_QA = 'in qa'
        IN_CODE_REVIEW = 'in code review'
        READY_FOR_RELEASE = 'ready for release'
        RELEASED = 'released'
        ARCHIVED = 'archived'

    class PriorityChoice(models.IntegerChoices):
        HIGH = 1, 'high'
        LOW = 2, 'low'

    StateTransitions = {
        StateChoice.NEW_TASK: (StateChoice.IN_DEVELOPMENT, StateChoice.ARCHIVED),
        StateChoice.IN_DEVELOPMENT: (StateChoice.IN_QA,),
        StateChoice.IN_QA: (StateChoice.IN_DEVELOPMENT, StateChoice.IN_CODE_REVIEW),
        StateChoice.IN_CODE_REVIEW: (StateChoice.IN_DEVELOPMENT, StateChoice.READY_FOR_RELEASE),
        StateChoice.RELEASED: (StateChoice.ARCHIVED,),
        StateChoice.ARCHIVED: (),
    }

    title = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deadline = models.DateTimeField()
    state = models.CharField(max_length=50, choices=StateChoice.choices, default=StateChoice.NEW_TASK)
    priority = models.PositiveSmallIntegerField(choices=PriorityChoice.choices, default=PriorityChoice.HIGH)
    tags = models.ManyToManyField(Tag, related_name='tasks')

    class Meta:
        ordering = ['priority']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['deadline']),
            models.Index(fields=['state']),
            models.Index(fields=['priority']),
        ]

    def __str__(self):
        return f'Task: {self.title}'

    def to_development(self) -> bool:
        if self.StateChoice.IN_DEVELOPMENT in self.StateTransitions[self.state]:
            self.state = self.StateChoice.IN_DEVELOPMENT
            self.save()
            return True
        return False

    def to_qa(self) -> bool:
        if self.StateChoice.IN_QA in self.StateTransitions[self.state]:
            self.state = self.StateChoice.IN_QA
            self.save()
            return True
        return False

    def to_code_review(self) -> bool:
        if self.StateChoice.IN_CODE_REVIEW in self.StateTransitions[self.state]:
            self.state = self.StateChoice.IN_CODE_REVIEW
            self.save()
            return True
        return False

    def to_ready_for_release(self) -> bool:
        if self.StateChoice.READY_FOR_RELEASE in self.StateTransitions[self.state]:
            self.state = self.StateChoice.READY_FOR_RELEASE
            self.save()
            return True
        return False

    def to_release(self) -> bool:
        if self.StateChoice.RELEASED in self.StateTransitions[self.state]:
            self.state = self.StateChoice.RELEASED
            self.save()
            return True
        return False

    def to_archive(self) -> bool:
        if self.StateChoice.ARCHIVED in self.StateTransitions[self.state]:
            self.state = self.StateChoice.ARCHIVED
            self.save()
            return True
        return False

    def get_possible_transitions(self) -> tuple[StateChoice]:
        return self.StateTransitions[self.state]
