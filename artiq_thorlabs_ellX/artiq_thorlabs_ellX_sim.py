from typing import Union
from artiq_thorlabs_ellX.artiq_thorlabs_ellX_I import ThorlabsELLXInterface
from artiq_thorlabs_ellX.artiq_thorlabs_ellX import (
    ThorlabsELLX,
    COMMAND_WORDS,
    cmd_responses,
    resp_lenghts,
    COMMAND_STATUS
)


class ThorlabsELLXSim(ThorlabsELLX, ThorlabsELLXInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._responses_queue = []

    def _generate_response(self, cmd: COMMAND_WORDS):
        possible_responses = cmd_responses[cmd]
        if type(possible_responses) is COMMAND_WORDS:
            possible_responses = [possible_responses]
        for response_type in possible_responses:
            response_len_hex_bytes = resp_lenghts[response_type]
            self._responses_queue.append('0' * response_len_hex_bytes)

    def _send_cmd(self, cmd: COMMAND_WORDS, data: str = "") -> COMMAND_STATUS:
        full_cmd = f"{self.dev_addr}{cmd.value}{data}"
        self.log(f"Simulate write command: {full_cmd}")
        self._generate_response(cmd)
        return COMMAND_STATUS.OK

    def _read_resp(self, _cmd: Union[COMMAND_WORDS, list[COMMAND_WORDS]]) -> Union[str, COMMAND_STATUS]:
        result = self._responses_queue.pop(0)
        self.log(f"Simulate read response: {result}")
        return result
