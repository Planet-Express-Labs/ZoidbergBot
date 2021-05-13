# confessbot-public

Public branch of confessionbot. Feature request should go in issues. 


# Install

Hosted confessbot is running in a Windows Server 2019 VM. This is the environment we designed for. It should run fine within Ubuntu server, however releases aren't tested very often on that. If you're running on Windows 10, it should run just fine, although you'll probably have some reliablility issues with windows update.


# Planned features. 

- Local logging should transition to Redis or SQL sometime soon. When this transition finishes, you'll be expected to be using one of those two implimentation - text based logging will no longer be supported, and as such must be expected to break. 
- Multiple server support. This should be relatively simple to add, but I haven't had the time to do anything greater then fixing issues when something breaks. This should be added in the coming months, once I have time. 
- 
