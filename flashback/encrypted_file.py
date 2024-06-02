from __future__ import annotations

from collections.abc import Callable
import base64
import os
import secrets

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class EncryptedFile:
    """
    Implements a system to encrypt and decrypt the contents of a given file.

    Inspired by:

         - https://github.com/rails/rails/blob/main/activesupport/lib/active_support/encrypted_file.rb

    Examples:
        ```python
        from flashback import EncryptedFile

        encrypted_file = EncryptedFile("secrets.yml.enc", "secrets.key")

        # Inits the encrypted file, and encryption key
        key, init_contents = encrypted_file.init()

        # Reads the contents
        read_contents = encrypted_file.read()

        assert encrypted_file.read() == init_contents

        # Also writes
        passwd = "i{e8m+/1sdf"
        encrypted_file.write(passwd)
        assert encrypted_file.read() == passwd

        # You can pass any serializer (JSON, YAML, pickle, etc.)
        import pickle
        value = ""
        encrypted_file.write(value, serializer=pickle.dumps)
        assert encrypted_file.read(deserializer=pickle.loads) == value
        ```

    Params:
        file_path: the path the file to encrypt
        key_path: the path of the key used to encrypt the file
        env_key_name: the name of the env var from which to fetch the encryption key (default: "ENCRYPTION_KEY")
    """

    DEFAULT_ENV_KEY_NAME = "ENCRYPTION_KEY"

    def __init__(self, file_path: str, key_path: str, env_key_name: str = DEFAULT_ENV_KEY_NAME) -> None:
        self.file_path = os.path.realpath(os.path.expanduser(os.path.abspath(file_path)))
        self.key_path = os.path.realpath(os.path.expanduser(os.path.abspath(key_path)))

        self.env_key_name = env_key_name

        self.key = None

    def init(self) -> tuple[str, str]:
        """
        Initializes the encryption key and encrypted file, and writes them
        to the `key_path` and `file_path` given at init.

        Returns:
            the key and contents
        """
        # Inits the key
        key = secrets.token_hex(16)

        with open(self.key_path, "w", encoding="utf-8") as outfile:
            outfile.write(key)

        os.chmod(self.key_path, 0o600)

        encrypted_key = bytes.fromhex(key)

        # Inits the contents
        contents = ""
        with open(self.file_path, "wb") as outfile:
            outfile.write(self._encrypt(contents.encode("utf-8"), encrypted_key))

        return key, contents

    def read(self, deserializer: Callable[[bytes], str] | None = None) -> str:
        """
        Reads the contents (possibly deserialized with `deserializer`) of the file_path
        given at init, and decrypt them with the encryption key.

        Params:
            deserializer: the deserializer to use on the contents (default: .decode("utf-8"))

        Returns:
            the deserialized contents

        Raises:
            RuntimeError: if the file is not found at file_path
        """
        key = self.get_key()

        if not os.path.exists(self.file_path):
            raise RuntimeError(f"Missing encrypted file in {self.file_path}")

        with open(self.file_path, "rb") as infile:
            contents = self._decrypt(infile.read(), key)

            if deserializer is None:
                return contents.decode("utf-8")

            return deserializer(contents)

    def write(self, contents: str, serializer: Callable[[str], bytes] | None = None) -> None:
        """
        Writes the given `contents` (possibly serialized with `serializer`)
        after encrypting them with the encryption key to the file_path given at init.

        Params:
            contents: the contents to write
            serializer: the serializer to use on the contents (default: .encode("utf-8"))

        Raises:
            RuntimeError: if the file is not found at file_path
        """
        key = self.get_key()

        if serializer is None:
            serialized_contents = contents.encode("utf-8")
        else:
            serialized_contents = serializer(contents)

        # Write on a temp file to avoid corrupting the
        # original file if an error happens
        tmp_path = f"{self.file_path}.tmp"
        with open(tmp_path, "wb") as outfile:
            outfile.write(self._encrypt(serialized_contents, key))

        os.rename(tmp_path, self.file_path)

    def get_key(self) -> bytes:
        """
        Fetches the encryption key.
        First, checks if it has already been read, then checks in the environment,
        and finally, tries to read the file that should contain it.

        Returns:
            the encryption key

        Raises:
            RuntimeError: if the encryption key is not found in the env, and the the file
        """
        if self.key is not None:
            return self.key

        key = os.getenv(self.env_key_name)
        if key is None:
            if not os.path.exists(self.key_path):
                raise RuntimeError(f"Missing encryption key in {self.key_path}")

            with open(self.key_path, encoding="utf-8") as infile:
                key = infile.read().strip()

        self.key = bytes.fromhex(key)

        return self.key

    @staticmethod
    def _encrypt(value: bytes, key: bytes) -> bytes:
        # Constructs an AES-GCM Cipher object with the given key
        # and a randomly generated init_vector
        init_vector = os.urandom(12)
        encryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(init_vector),
        ).encryptor()

        # Unused, but needed
        encryptor.authenticate_additional_data(b"")

        encrypted_value = encryptor.update(value)
        # Gives the tag
        encrypted_value += encryptor.finalize()

        return b"--".join([base64.b64encode(v) for v in [encrypted_value, init_vector, encryptor.tag]])

    @staticmethod
    def _decrypt(obfuscated_value: bytes, key: bytes) -> bytes:
        encrypted_value, init_vector, tag = (base64.b64decode(v) for v in obfuscated_value.split(b"--"))

        # Constructs a Cipher object with the key, init_vector, and the GCM tag
        # used to authenticate the message
        decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(init_vector, tag),
        ).decryptor()

        # We need to authenticate the additional data or the tag will fail to verify
        # and the decryptor will raise InvalidTag when finalizing
        decryptor.authenticate_additional_data(b"")

        decrypted_value = decryptor.update(encrypted_value)
        # Verifies the tag
        decrypted_value += decryptor.finalize()

        return decrypted_value
