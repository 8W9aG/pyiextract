
class Resolver:
    def __init__(self) -> None:
        pass

    def resolve(self, text: str) -> str:
        raise NotImplementedError("Can't use resolve on base Resolver class")

    def name(self) -> str:
        return "base"
