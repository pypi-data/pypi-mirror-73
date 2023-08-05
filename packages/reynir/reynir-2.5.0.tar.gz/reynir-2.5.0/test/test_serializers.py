"""

    test_serializers.py

    Tests for JSON serialization of sentences

    Copyright (C) 2020 by Miðeind ehf.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

import json

import pytest


@pytest.fixture(scope="module")
def r():
    """ Provide a module-scoped Greynir instance as a test fixture """
    from reynir import Greynir
    r = Greynir()
    yield r
    # Do teardown here
    r.__class__.cleanup()


def test_serializers(r):
    sents = [
        "Ég fór niðrá bryggjuna með Reyni Vilhjálmssyni í gær.",
        "Það var 17. júní árið 2020.",
        "Við sáum tvo seli og örugglega fleiri en 100 máva.",
        "Klukkan var orðin tólf þegar við fórum heim.",
        "Bíllinn kostaði €30.000 en ég greiddi 25500 USD fyrir hann.",
        "Morguninn eftir vaknaði ég kl. 07:30.",
        "Ég var fyrstur á fætur en Þuríður Hálfdánardóttir var númer 2.",
    ]
    for sent in sents:
        orig = r.parse_single(sent)
        assert orig.tree is not None

        json_str = r.dumps_single(orig, indent=2)
        new = r.loads_single(json_str)

        assert new.tree is not None

        assert orig.tokens == new.tokens
        assert orig.terminals == new.terminals

        assert orig.tree.flat_with_all_variants == orig.tree.flat_with_all_variants
        cls = r.__class__
        assert json.loads(orig.dumps(cls, indent=2)) == json.loads(new.dumps(cls, indent=2))


if __name__ == "__main__":
    # When invoked as a main module, do a verbose test
    from reynir import Greynir
    r = Greynir()
    test_serializers(r)
    r.__class__.cleanup()
