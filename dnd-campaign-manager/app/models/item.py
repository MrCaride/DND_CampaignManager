class Item:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Item {self.name}>"

    def use(self):
        # Logic for using the item
        pass

    def get_info(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }