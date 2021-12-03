import typing


test_input = """
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""


class Instruction(typing.TypedDict):
    direction: str
    step: int


class State(typing.TypedDict):
    horizontal: int
    depth: int
    aim: int


def initial_state() -> State:
    return {"horizontal": 0, "depth": 0, "aim": 0}


def parse_input(input: str) -> typing.List[Instruction]:
    lines = input.strip().splitlines()
    return [
        {"direction": split_line[0], "step": int(split_line[1])}
        for line in lines
        if (split_line := line.split(" "))
    ]


def _forward(state: State, step: int) -> State:
    output = state.copy()
    output["horizontal"] += step
    return output


def _up(state: State, step: int) -> State:
    output = state.copy()
    new_depth = output["depth"] - step
    if new_depth < 0:
        new_depth = 0
    output["depth"] = new_depth
    return output


def _down(state: State, step: int) -> State:
    output = state.copy()
    output["depth"] += step
    return output


instruction_handlers = {
    "forward": _forward,
    "up": _up,
    "down": _down,
}


def _apply_instruction(state: State, instruction: Instruction, handlers=instruction_handlers) -> State:
    handler = handlers[instruction["direction"]]
    return handler(state, instruction["step"])


def apply_instructions(
    state: State, instructions: typing.Iterable[Instruction], handlers=instruction_handlers
) -> State:
    for inst in instructions:
        state = _apply_instruction(state, inst, handlers)

    return state


def part1(input):
    parsed_input = parse_input(input)
    state = initial_state()
    updated_state = apply_instructions(state, parsed_input)
    return updated_state["depth"] * updated_state["horizontal"]




def _forward2(state: State, step: int) -> State:
    output = state.copy()
    output["horizontal"] += step
    output["depth"] += state["aim"] * step
    return output


def _up2(state: State, step: int) -> State:
    output = state.copy()
    output["aim"] -= step
    return output


def _down2(state: State, step: int) -> State:
    output = state.copy()
    output["aim"] += step
    return output


instruction_handlers2 = {
    "forward": _forward2,
    "up": _up2,
    "down": _down2,
}


def part2(input):
    parsed_input = parse_input(input)
    state = initial_state()
    updated_state = apply_instructions(state, parsed_input, handlers=instruction_handlers2)
    return updated_state["depth"] * updated_state["horizontal"]


