from streamlit_authenticator.utilities.hasher import Hasher

#passwords = ['openai123', 'streamlit456']

#['$2b$12$q.tOsPK/UxMa6AhY8xLL8uJuvacx0ZDoQgWO/E0A14JARwyxaORkW', '$2b$12$se6zbAvvMOrThQZDgjiq0.t3J8IYrSPoAdKykQ7qV5TfGl06lO0ai']

passwords = ['thinkingcode123']
# Hash a list of plaintext passwords
hashed_passwords = Hasher.hash_list(passwords)
print(hashed_passwords)