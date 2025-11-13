class IDGenerator:
    def __init__(self):
        self.current_id = 0

    def __call__(self) -> int:
        self.current_id += 1
        return self.current_id

unique_id = IDGenerator()

def hard_round(value: float, decimals: int = 2) -> float:
    factor = 10 ** decimals
    return round(value * factor) / factor