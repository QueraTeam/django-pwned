import re

import pytest
import responses
from django.core.exceptions import ValidationError

from django_pwned.api import API_ENDPOINT
from django_pwned.validators import PwnedPasswordValidator


@responses.activate
def test_django_common_passwords():
    responses.add(responses.GET, url=re.compile(r".*"))
    validator = PwnedPasswordValidator()
    with pytest.raises(ValidationError):
        validator.validate("123456")
    with pytest.raises(ValidationError):
        validator.validate("123456789")
    with pytest.raises(ValidationError):
        validator.validate("qwerty")
    with pytest.raises(ValidationError):
        validator.validate("password")
    with pytest.raises(ValidationError):
        validator.validate("qweasdzxc")
    with pytest.raises(ValidationError):
        validator.validate("startfinding")
    with pytest.raises(ValidationError):
        validator.validate("heyhey1")
    # it should not have called requests.get at all
    assert len(responses.calls) == 0


@responses.activate
def test_pwned_api__leaked_password():
    leaked_password = r"haveibeenpwned"
    leaked_password_hash = "667245565F95194F23408B0EA21A0D02C4EEA81D"
    responses.add(
        responses.GET,
        API_ENDPOINT.format(leaked_password_hash[:5]),
        body="\n".join(
            [
                "0BD86C0E684498894064E4AB86B9420CA0E:763",
                "2019C3022C39C4E5FD5A92ECD102E87476D:3",
                "3C56EAB73498B6A58EF5692C4E4937B4466:81",
                "5565F95194F23408B0EA21A0D02C4EEA81D:1",
                "6E9AC9194DA65040917139BA238B3900354:2,103",
                "BB48AB53E4E454BC487CA6400380C05D41A:5",
                "D55A6ED26C1DE9350D40771822316CC4B29:3",
            ]
        ),
    )
    with pytest.raises(ValidationError):
        PwnedPasswordValidator().validate(leaked_password)
    assert len(responses.calls) == 1


@responses.activate
def test_pwned_api__strong_password():
    strong_password = r"SGz=L.%U\;Os$,k]%U2m"
    strong_password_hash = "761E05BF4161AF6CE0DDA796C063B3B5F0F93A4D"
    responses.add(
        responses.GET,
        API_ENDPOINT.format(strong_password_hash[:5]),
        body="\n".join(
            [
                "1C8ED662FF477F5EFB2F43BB5A772877FEF:1",
                "43DF3CB99A3C26781395C72B543E3D9B77A:1",
                "54B2CEEE3E59AACD9CED9BA6A3DAC33CA62:12",
                "6F97235868B9AB0F74702AF7BB5151DB8BE:8",
                "A61E8BD078A4246979AAE41721B795358D5:80",
                "C47A6ED73AD097E959D9417B5E66E22E8F2:5",
                "E82B1DF7CB04693452281037CEAFB29E037:2",
                "FFF5135901E0131D96F2D5B211ACEA61DAE:1",
            ]
        ),
    )
    PwnedPasswordValidator().validate(strong_password)
    assert len(responses.calls) == 1


@responses.activate
def test_pwned_api__count_threshold():
    leaked_password = r"pass-word"
    leaked_password_hash = "43BEF3EAB34187D71D7E1D9CC307C5E7C07665A8"
    responses.add(
        responses.GET,
        API_ENDPOINT.format(leaked_password_hash[:5]),
        body="\n".join(
            [
                "0BD86C0E684498894064E4AB86B9420CA0E:763",
                "3EAB34187D71D7E1D9CC307C5E7C07665A8:3",
                "3C56EAB73498B6A58EF5692C4E4937B4466:81",
                "5565F95194F23408B0EA21A0D02C4EEA81D:1",
                "6E9AC9194DA65040917139BA238B3900354:2,103",
                "BB48AB53E4E454BC487CA6400380C05D41A:5",
                "D55A6ED26C1DE9350D40771822316CC4B29:3",
            ]
        ),
    )
    with pytest.raises(ValidationError):
        PwnedPasswordValidator().validate(leaked_password)
    with pytest.raises(ValidationError):
        PwnedPasswordValidator(count_threshold=2).validate(leaked_password)
    with pytest.raises(ValidationError):
        PwnedPasswordValidator(count_threshold=3).validate(leaked_password)
    PwnedPasswordValidator(count_threshold=4).validate(leaked_password)
    PwnedPasswordValidator(count_threshold=5).validate(leaked_password)
    assert len(responses.calls) == 5


@responses.activate
def test_pwned_api__connection_error():
    strong_password = r"SGz=L.%U\;Os$,k]%U2m"
    PwnedPasswordValidator().validate(strong_password)
    assert len(responses.calls) == 1


@responses.activate
def test_pwned_api__invalid_input():
    binary_password = b"\x23\x25"
    with pytest.raises(TypeError):
        PwnedPasswordValidator().validate(binary_password)  # noqa
    assert len(responses.calls) == 0
