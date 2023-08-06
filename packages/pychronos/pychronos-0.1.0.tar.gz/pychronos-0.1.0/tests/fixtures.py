from faker import Faker
from faker.providers.lorem.en_US import Provider
import random as rnd
import string
import logging


fake = Faker()


class UniqueObjNameProvider(Provider):
    """ generate uniq word for unique names, labels etc """
    used_words = set()

    def obj_name(self, ext_word_list=None) -> str:

        # 100,000 tries should be enough to get uniq?
        for _ in range(100_000):
            word = super().word(ext_word_list).lower()

            rand_str = ''.join(rnd.choices(string.ascii_uppercase + string.digits, k=6))
            word = f'{word}_{rand_str}'.lower()

            if word in self.used_words:
                continue
            else:
                self.used_words.add(word)
                return word

        logging.critical("Getting new 'word': limit exceeded!")


fake.add_provider(UniqueObjNameProvider)
