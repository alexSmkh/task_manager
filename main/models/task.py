from django.db import models

from main.models.tag import Tag
from main.models.user import User


class Task(models.Model):
    class States(models.TextChoices):
        NEW_TASK = 'new'
        IN_DEVELOPMENT = 'in development'
        IN_QA = 'in qa'
        IN_CODE_REVIEW = 'in code review'
        READY_FOR_RELEASE = 'ready for release'
        RELEASED = 'released'
        ARCHIVED = 'archived'

    class Priorities(models.IntegerChoices):
        HIGH = 1, 'high'
        LOW = 2, 'low'

    StateTransitions = {
        States.NEW_TASK: (States.IN_DEVELOPMENT, States.ARCHIVED),
        States.IN_DEVELOPMENT: (States.IN_QA,),
        States.IN_QA: (States.IN_DEVELOPMENT, States.IN_CODE_REVIEW),
        States.IN_CODE_REVIEW: (States.IN_DEVELOPMENT, States.READY_FOR_RELEASE),
        States.RELEASED: (States.ARCHIVED,),
        States.ARCHIVED: (),
    }

    title = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deadline = models.DateTimeField()
    state = models.CharField(max_length=50, choices=States.choices, default=States.NEW_TASK)
    priority = models.PositiveSmallIntegerField(choices=Priorities.choices, default=Priorities.HIGH)
    tags = models.ManyToManyField(Tag, related_name='tasks')
    assigned = models.ForeignKey(
        User,
        related_name='assigned_tasks',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    author = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE)

    class Meta:
        ordering = ['priority']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['deadline']),
            models.Index(fields=['state']),
            models.Index(fields=['priority']),
        ]

    def __str__(self) -> str:
        return self.title

    def to_development(self) -> bool:
        if self.States.IN_DEVELOPMENT in self.StateTransitions[self.state]:
            self.state = self.States.IN_DEVELOPMENT
            self.save()
            return True
        return False

    def to_qa(self) -> bool:
        if self.States.IN_QA in self.StateTransitions[self.state]:
            self.state = self.States.IN_QA
            self.save()
            return True
        return False

    def to_code_review(self) -> bool:
        if self.States.IN_CODE_REVIEW in self.StateTransitions[self.state]:
            self.state = self.States.IN_CODE_REVIEW
            self.save()
            return True
        return False

    def to_ready_for_release(self) -> bool:
        if self.States.READY_FOR_RELEASE in self.StateTransitions[self.state]:
            self.state = self.States.READY_FOR_RELEASE
            self.save()
            return True
        return False

    def to_release(self) -> bool:
        if self.States.RELEASED in self.StateTransitions[self.state]:
            self.state = self.States.RELEASED
            self.save()
            return True
        return False

    def to_archive(self) -> bool:
        if self.States.ARCHIVED in self.StateTransitions[self.state]:
            self.state = self.States.ARCHIVED
            self.save()
            return True
        return False

    def get_possible_transitions(self) -> tuple[States]:
        return self.StateTransitions[self.state]
