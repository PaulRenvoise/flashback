# pylint: disable=no-self-use,no-member,protected-access

import os
import pickle

import pytest

from flashback import EncryptedFile

FILE_PATH = "/tmp/secrets.enc"
KEY_PATH = "/tmp/secrets.key"


@pytest.fixture(autouse=True)
def cleanup_test():
    yield

    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)
    if os.path.exists(KEY_PATH):
        os.remove(KEY_PATH)

    if 'ENCRYPTION_KEY' in os.environ:
        del os.environ['ENCRYPTION_KEY']


class TestEncryptedFile:
    def test_init(self):
        encrypted_file = EncryptedFile(
            FILE_PATH,
            KEY_PATH,
        )
        key, init_contents = encrypted_file.init()

        assert key is not None
        assert init_contents is not None
        assert os.path.exists(FILE_PATH)
        assert os.path.exists(KEY_PATH)

    def test_read_and_write(self):
        encrypted_file = EncryptedFile(
            FILE_PATH,
            KEY_PATH,
        )
        _key, _init_contents = encrypted_file.init()
        write_contents = "config"
        encrypted_file.write(write_contents)
        read_contents = encrypted_file.read()

        assert write_contents == read_contents

    def test_read_and_write_with_custom_serializer(self):
        encrypted_file = EncryptedFile(
            FILE_PATH,
            KEY_PATH,
        )
        _key, _init_contents = encrypted_file.init()
        write_contents = {"key": "value"}
        encrypted_file.write(write_contents, serializer=pickle.dumps)
        read_contents = encrypted_file.read(deserializer=pickle.loads)

        assert write_contents == read_contents

    def test_read_and_write_with_no_serializer(self):
        encrypted_file = EncryptedFile(
            FILE_PATH,
            KEY_PATH,
        )
        _key, _init_contents = encrypted_file.init()
        write_contents = "value"
        encrypted_file.write(write_contents, serializer=None)
        read_contents = encrypted_file.read(deserializer=None)

        assert write_contents.encode("utf-8") == read_contents

    def test_read_and_write_with_key_in_env(self):
        encrypted_file = EncryptedFile(
            FILE_PATH,
            KEY_PATH,
        )
        key, _init_contents = encrypted_file.init()
        os.remove(KEY_PATH)
        os.environ["ENCRYPTION_KEY"] = key

        write_contents = "value"
        encrypted_file.write(write_contents)
        read_contents = encrypted_file.read()

        assert write_contents == read_contents

    def test_read_without_key(self):
        encrypted_file = EncryptedFile(
            FILE_PATH,
            KEY_PATH,
        )
        _key, _init_contents = encrypted_file.init()
        os.remove(KEY_PATH)

        with pytest.raises(RuntimeError):
            encrypted_file.read()

    def test_read_without_file(self):
        encrypted_file = EncryptedFile(
            FILE_PATH,
            KEY_PATH,
        )
        _key, _init_contents = encrypted_file.init()
        os.remove(FILE_PATH)

        with pytest.raises(RuntimeError):
            encrypted_file.read()
