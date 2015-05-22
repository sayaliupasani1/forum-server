# tornado-forum
Forum Server 
### Do Not implement this. It has no security feature. 
This app has been written for personal testing.
An actual forum server will be posted soon.

#### This server provides following features:
* Dummy Forum Posts (Clikcin it doesn't take you anywhere)
* Posts and Auth stored in DB (same DB. Security Vulnerability)
* File server (Upload and Download any file.. again a security vulnerability)

## Dependencies:
* Tornado (>2.0)
* sqlite3

## Working:
#### This app uses sqlite3. Create a database (Very Bad Database)
  
  > sqlite3 test.db
  
* Create Auth table
  
  > CREATE TABLE test.AUTH(
  
  > ID INT PRIMARY KEY,
  
  > USERNAME TEXT,
  
  > PASSWORD TEXT,
  
  > EMAIL TEXT);
  
* Add some user information

  > INSERT INTO AUTH (ID, USERNAME, PASSWORD, EMAIL)

  > VALUES (1, '<username>', '<password>', '<email id>')
  
* Create Forum table

  > CREATE TABLE test.FORUM(
  
  > ID INT PRIMARY KEY,
  
  > USERNAME TEXT,
  
  > POST TEXT,
  
  > POST_TYPE TEXT,
  
  > TIME TEXT);
  
  > .quit
  
#### Run server 
  
  > python forum_server.py --port=8888
  
#### Go to localhost:8888

### Again, This is a very insecure version of a Forum Server and is only meant for private testing. It does not perform any sanity test etc. However, you are welcome to take the idea, improvise and implement your own.
