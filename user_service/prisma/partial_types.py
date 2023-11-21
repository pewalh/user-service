from prisma.models import User, ContactDetails

User.create_partial('UserCreate', include={'email', 'username'})
User.create_partial('UserUpdateUsername', include={'email', 'username'})

ContactDetails.create_partial('ContactDetailsData', include={'phoneNumber', 'address'})

