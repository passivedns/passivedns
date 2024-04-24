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
stmt = db._createStatement({ "query": "INSERT {\"_key\": \"admin\", \"role\": \"admin\", \"email\": \"oquidam@et.esiea.fr\", \"hashed_password\": \"$2a$14$qF7Nu/9lWXUV3dHKPyf9lO8/xySp.tRUEhM8xieaT6.wGU0wHtnym\" } INTO Users" })

stmt.execute()

stmt = db._createStatement({"query": "INSERT {\"_key\": \"_default\", \"type\": \"email\", \"infos\": {\"smtp_host\": \"\", \"smtp_port\": \"\", \"sender_email\": \"\", \"sender_password\": \"\"}} INTO Channel"})

stmt.execute()

stmt = db._createStatement({"query": "INSERT {\"_from\": \"Users/admin\", \"_to\": \"Channel/_default\", \"username\": \"admin\", \"channel_name\": \"_default\", \"contact\": \"oquidam@et.esiea.fr\", \"token\": \"token\", \"verified\": true} INTO UsersChannel"})

stmt.execute()


stmt = db._createStatement({ "query": "INSERT {\"_key\": \"sched1\", \"role\": \"scheduler\", \"email\": \"oquidam@et.esiea.fr\", \"hashed_password\": \"$2a$14$L4oJe1In99Mar767fEPu9Of4ArqodvX7Bu0/JP4EArV4wsZaQ0UE6\" } INTO Users" })

stmt.execute()
