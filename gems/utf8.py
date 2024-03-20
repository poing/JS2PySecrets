#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set et sw=4 fenc=utf-8:
#
# dealing with utf8 issue test_windows

key = "¥ · £ · € · $ · ¢ · ₡ · ₢ · ₣ · ₤ · ₥ · ₦ · ₧ · ₨ · ₩ · ₪ · ₫ · ₭ · ₮ · ₯ · ₹"

def test_with_UTF8():
    key = "¥ · £ · € · $ · ¢ · ₡ · ₢ · ₣ · ₤ · ₥ · ₦ · ₧ · ₨ · ₩ · ₪ · ₫ · ₭ · ₮ · ₯ · ₹"
    expected = "\xa5 \xb7 \xa3 \xb7 \u20ac \xb7 $ \xb7 \xa2 \xb7 \u20a1 \xb7 \u20a2 \xb7 \u20a3 \xb7 \u20a4 \xb7 \u20a5 \xb7 \u20a6 \xb7 \u20a7 \xb7 \u20a8 \xb7 \u20a9 \xb7 \u20aa \xb7 \u20ab \xb7 \u20ad \xb7 \u20ae \xb7 \u20af \xb7 \u20b9"

    assert (
        secrets.hex2str(
            secrets.combine(secrets.share(secrets.str2hex(key), 3, 2))
        )
        == expected
    )

print(key.encode("utf-8", "strict"))    
    