from flask import json
s=b'{"id":"VexbYQDr2fOpL1oVz2Okx1qZki83","name":"dec","payment_method":0,"phone":"+918989898989"}'

final_dictionary = json.loads(s)
print(final_dictionary)