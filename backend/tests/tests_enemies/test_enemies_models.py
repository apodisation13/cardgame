import pytest

from apps.enemies.models import Enemy, EnemyLeader, Level, UserLevel


@pytest.mark.django_db
class TestModels:
    def test_level(self):
        children_levels = Level.objects.filter(id__range=(2, 4))
        children_levels_info = [(level.id, level.name) for level in children_levels]
        test_level = Level.objects.get(id=1)
        test_level.related_levels.add(*children_levels)
        assert len(test_level.related_levels.all()) == 3
        assert test_level.get_related_levels() == children_levels_info

    def test_userlevel(self, create_user):
        user = create_user()
        finished_levels_before = user.u_level.filter(finished=True).count()
        level_in_process = UserLevel.objects.filter(user=user.id,
                                                    finished=False).first()
        level_in_process.finished = True
        level_in_process.save()
        finished_levels_after = user.u_level.filter(finished=True).count()
        assert finished_levels_after == finished_levels_before + 1
