import os

from flashback.debugging import profiled


def dummy_func(left: int, right: int) -> bool:
    return left > right


class TestProfiled:
    def test_profiled(self) -> None:
        output_name = "dummy_func.pstats"
        make_profiled = profiled()
        decorated_func = make_profiled(dummy_func)

        decorated_func(1, 2)

        self.assert_output_valid(output_name)

    def test_profiled_with_name(self) -> None:
        output_name = "output.cprofile"
        make_profiled = profiled(output_name)
        decorated_func = make_profiled(dummy_func)

        decorated_func(1, 2)

        self.assert_output_valid(output_name)

    @staticmethod
    def assert_output_valid(output_name) -> None:
        output_filename = os.path.join(os.getcwd(), output_name)
        try:
            with open(output_filename, "rb") as infile:
                output = infile.read()

                assert output != ""
        finally:
            os.remove(output_filename)
