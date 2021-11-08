from cloud.models import VMTag


class VMTagDAO:
    @staticmethod
    def delete_all_records():
        VMTag.objects.all().delete()

    @staticmethod
    def get_or_create_tag(tag_name):
        tag, _ = VMTag.objects.get_or_create(name=tag_name)
        return tag

    @staticmethod
    def get_all_tags_by_accessible_tags(tags):
        return set(VMTag.objects.filter(virtual_machines__tags__name__in=tags).values_list('name', flat=True))
