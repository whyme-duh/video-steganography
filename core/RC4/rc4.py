from typing import List

class RC4:
    def key_scheduler(self, key: List[bytes]) -> List[bytes]:
        key_length = len(key)
        S = list(range(256))
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % key_length]) % 256
            S[i], S[j] = S[j], S[i]
        return S

    def pseudo_random_gen(self, message: List[int]) -> int:
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + message[i]) % 256
            message[i], message[j] = message[j], message[i]
            K = message[(message[i] + message[j]) % 256]
            yield K

    def __call__(self, key: str, message_ascii_list: List[int], encrypt: bool = True) -> str:
        key_ascii_list = [ord(c) for c in key]
        scheduled_keys = self.key_scheduler(key_ascii_list)
        key_stream = self.pseudo_random_gen(scheduled_keys)
        cipher_text = []
        for char in message_ascii_list:
            integer = char ^ next(key_stream)
            if encrypt:
                cipher_text.append(f'{integer:08b}')
            else:
                cipher_text.append(chr(integer))
        return ''.join(cipher_text)
    
    def encrypt(self, key: str, plaintext: str) -> str:
        plaintext = [ord(c) for c in plaintext]
        return self.__call__(key=key, message_ascii_list=plaintext)

    def decrypt(self,key:str, ciphertext: str) -> str:
        ciphertext = [int(ciphertext[i*8:i*8+8], base=2) for i in range(len(ciphertext)//8)]
        return self.__call__(key=key, message_ascii_list=ciphertext, encrypt=False)

    