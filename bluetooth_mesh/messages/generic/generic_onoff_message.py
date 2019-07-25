from construct import Int8ul, Struct, Switch, Optional, this
from enum import IntEnum
from bluetooth_mesh.messages.util import EnumAdapter, Opcode
from bluetooth_mesh.messages.generics import Delay, TransitionTime


class GenericOpcode(IntEnum):
    ONOFF_GET = 0x8201
    ONOFF_SET = 0x8202
    ONOFF_SET_UNACKNOWLEDGED = 0x8203
    ONOFF_STATUS = 0x8204


GenericOnOffMsg = Struct(
    "onoff" / Int8ul,
    "tid" / Int8ul,
    "transition_time" / Optional(TransitionTime),
    "delay" / Optional(Delay(Int8ul))
)

GenericOnOffStatus = Struct(
    "present_onoff" / Int8ul,
    "target_onoff" / Optional(Int8ul),
    "remaining_time" / Optional(TransitionTime)
)


GenericOnOffMessage = Struct(
    "opcode" / EnumAdapter(Opcode, GenericOpcode),
    "params" / Switch(
        this.opcode,
        {
            GenericOpcode.ONOFF_GET: Struct(),
            GenericOpcode.ONOFF_SET: GenericOnOffMsg,
            GenericOpcode.ONOFF_SET_UNACKNOWLEDGED: GenericOnOffMsg,
            GenericOpcode.ONOFF_STATUS: GenericOnOffStatus,
        },
    )
)