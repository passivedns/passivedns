console.log("creating user...")
let user_name = "passive_dns_user"
const users = require('@arangodb/users')
users.save(user_name, "{db_password}")

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
stmt = db._createStatement({ "query": "INSERT {\"_key\": \"{admin_name}\", \"role\": \"admin\", \"email\": \"{admin_email}\", \"hashed_password\": \"{admin_hashed_password}\" } INTO Users" })

stmt.execute()

stmt = db._createStatement({"query": "INSERT {\"_key\": \"_default\", \"type\": \"email\", \"infos\": {\"smtp_host\": \"{smtp_host}\", \"smtp_port\": \"{smtp_port}\", \"sender_email\": \"{sender_email}\", \"sender_password\": \"{sender_password}\"}} INTO Channel"})

stmt.execute()

stmt = db._createStatement({"query": "INSERT {\"_from\": \"Users/{admin_name}\", \"_to\": \"Channel/_default\", \"username\": \"{admin_name}\", \"channel_name\": \"_default\", \"contact\": \"{admin_email}\", \"token\": \"token\", \"verified\": true} INTO UsersChannel"})

stmt.execute()
