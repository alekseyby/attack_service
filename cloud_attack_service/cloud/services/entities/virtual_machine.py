class VirtualMachineEntity:
    __slots__ = [
        'vm_id',
        'name',
        'tags'
    ]

    def __init__(self, vm_id, name, tags):
        self.vm_id = vm_id
        self.name = name
        self.tags = tags
