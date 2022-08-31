from src.channels import channels_list_v1, channels_listall_v1
from src.channel import channel_join_v1
from src.error import InputError
from src.other import clear_v1
import pytest

'''def test_channels():
    channel_join_v1(1,1)
    channel_join_v1(1,2)
    assert channels_list_v1(1) == {1,2}

    with pytest.raises(InputError):
        channels_list_v1(2)

def test_all_channels():
    channel_join_v1(1,1)
    channel_join_v1(1,2)
    channel_join_v1(2,3)
    channel_join_v1(3,3)
    assert channels_listall_v1(1) == {1,2,3}'''
