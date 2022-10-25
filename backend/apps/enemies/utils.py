from apps.enemies.models import Level, UserLevel


def get_opened_user_levels(self, user_id, level_serializer, season_id):
    """
    Принимает на вход self из сериализатора, user_id, сериализатор уровней (иначе circular import)
    Возвращает все уровни юзера по сезону!
    Если мы приходим из вызова всей базы данных, то сюда заходим с каждым сезоном
    """
    all_levels = Level.objects.\
        select_related("enemy_leader__ability", "enemy_leader__faction", "season").\
        prefetch_related(
            "enemies__faction",
            "enemies__color",
            "enemies__move",
            "enemies__passive_ability",
            "related_levels",
            "children",
        ).filter(season_id=season_id).\
        all()
    user_levels = UserLevel.objects.filter(user_id=user_id).values("level__pk", "pk", "finished").all()
    levels = []
    for level in all_levels:
        for user_level in user_levels:
            if level.pk == user_level["level__pk"]:
                levels.append({
                    "level": level_serializer(level, context={"request": self.context.get("request")}).data,
                    "id": user_level["pk"],  # id записи UserLevel, пойдет при прохождении как finished_level
                    "unlocked": True,  # уровень считается открытым, если есть запись в связанной таблице UserLevel
                    "finished": user_level["finished"],  # открытый уровень может быть пройден, а может нет
                })
                break
        # если уровень не нашелся в открытых, значит идем сюда и добавляем его с флажком закрыт (False)
        else:
            levels.append({
                "level": level_serializer(level, context={"request": self.context.get("request")}).data,
                "unlocked": False,
            })
    print(len(levels), "УРОВНИ")
    return levels
