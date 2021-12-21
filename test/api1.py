import pymsteams

# You must create the connectorcard object with the Microsoft Webhook URL
myTeamsMessage = pymsteams.connectorcard("https://teams.microsoft.com/l/channel/19%3aab1b102a7e464ca684b9a8efe2ffd4e6%40thread.tacv2/Allgemein?groupId=4d1a001e-3b32-45cc-8614-def9646b536f&tenantId=c5686dea-4ffd-42a7-891f-c68875cd0b00")
# Add text to the message.
myTeamsMessage.text("this is my text")

# send the message.
myTeamsMessage.send()