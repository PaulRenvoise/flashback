from flashback.formatting import transliterate


class TestTransliterate:
    def test_unicode_only_chars(self):
        origin = "\u2124\U0001d552\U0001d55c\U0001d552\U0001d55b \U0001d526\U0001d52a\U0001d51e \U0001d4e4\U0001d4f7\U0001d4f2\U0001d4ec\U0001d4f8\U0001d4ed\U0001d4ee \U0001d4c8\U0001d4c5\u212f\U0001d4b8\U0001d4be\U0001d4bb\U0001d4be\U0001d4c0\U0001d4b6\U0001d4b8\U0001d4be\U0001d4bf\u212f \U0001d59f\U0001d586 \U0001d631\U0001d62a\U0001d634\U0001d622\U0001d637\U0001d626?!"    # pylint: disable=line-too-long
        target = "Zakaj ima Unicode specifikacije za pisave?!"

        assert transliterate(origin) == target

    def test_ascii_only_chars(self):
        origin = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        target = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

        assert transliterate(origin) == target

    def test_mixed_chars(self):
        origin = "PŘÍLIŠ ŽLUŤOUČKÝ KŮŇ PĚL ĎÁBELSKÉ ÓDY"
        target = "PRILIS ZLUTOUCKY KUN PEL DABELSKE ODY"

        assert transliterate(origin) == target

    def test_mixed_chars_and_keep_case(self):
        origin = "Je vais au ch\u00e2teau de Joséphine"
        target = "je vais au chateau de josephine"

        assert transliterate(origin, keep_case=False) == target
