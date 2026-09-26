class MemoryStore:

    memory = {}

    def save_context(self,key,value):
        print(f"[MEMORY SAVE] {key} = {value}")
        MemoryStore.memory[key] = value

    def get_context(self,key):
        value = MemoryStore.memory.get(key)
        print(f"[MEMORY READ] {key} = {value}")
        return value

    def get_all(self):
        return MemoryStore.memory