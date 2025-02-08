import random
import string

def get_random_code(k=3):
  random_code = ''.join(random.choices(string.ascii_uppercase, k=k))

  return "-"+random_code
