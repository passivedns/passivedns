console.log("creating user...")
let user_name = "passive_dns_user"
const users = require('@arangodb/users')
users.save(user_name, "user")

console.log("creating database...")
let db_name = "passive_dns"
db._createDatabase(db_name)
db._useDatabase(db_name)

users.grantDatabase(user_name, db_name, "rw")


console.log("creating collections...")
db._createDocumentCollection("Channel")
db._createDocumentCollection("DomainName")
db._createDocumentCollection("IPAddress")
db._createEdgeCollection("DomainNameResolution")
db._createDocumentCollection("Tag")
db._createEdgeCollection("TagDnIp")
db._createDocumentCollection("Users")
db._createEdgeCollection("UsersChannel")
db._createDocumentCollection("UsersPending")
db._createDocumentCollection("UsersRequest")
db._createEdgeCollection("UsersDn")

console.log("initializing collections...")
stmt = db._createStatement({ "query": "INSERT {\"_key\": \"Admin\", \"role\": \"admin\", \"email\": \"passivedns.dev@gmail.com\", \"hashed_password\": \"$2a$14$JkRM4r/XGZFOeFA39bRtFO32J7qSdrrcOM4R2tkPUYh8q71D1123i\" } INTO Users" })

stmt.execute()

stmt = db._createStatement({"query": "INSERT {\"_key\": \"_default\", \"type\": \"email\", \"infos\": {\"smtp_host\": \"\", \"smtp_port\": \"\", \"sender_email\": \"passivedns.dev@gmail.com\", \"sender_password\": \"\"}} INTO Channel"})

stmt.execute()

stmt = db._createStatement({"query": "INSERT {\"_from\": \"Users/Admin\", \"_to\": \"Channel/_default\", \"username\": \"Admin\", \"channel_name\": \"_default\", \"contact\": \"passivedns.dev@gmail.com\", \"token\": \"token\", \"verified\": true} INTO UsersChannel"})

stmt.execute()


stmt = db._createStatement({ "query": "INSERT {\"_key\": \"sched1\", \"role\": \"scheduler\", \"email\": \"passivedns.dev@gmail.com\", \"hashed_password\": \"$2a$14$WOqjItfk.3CzReAJyW6dpep/Tre2B/v0Hhwlb7wmuGnEchI8MFrbW\" } INTO Users" })

stmt.execute()
