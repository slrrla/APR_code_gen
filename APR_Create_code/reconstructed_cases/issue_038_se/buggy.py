# Buggy: using the deprecated IBMQuantumExperience library directly
# This raises a CredentialsError even though the account/token is valid,
# because the old API endpoint requires accepting a license that can't
# be accepted through this deprecated interface anymore.
from IBMQuantumExperience import IBMQuantumExperience

API_TOKEN = 'MY_API_TOKEN'

api = IBMQuantumExperience(API_TOKEN)

# Attempting to check credits via the deprecated API
credits = api.get_my_credits()
print(credits)
