import pathlib, json

with open('config.json', 'r') as jsonFile:
    config = json.loads(jsonFile.read())

result = open("webserver.cpp","w+")

pages = []

# Writing required variables and seeting up library for result file
result.write(
'#include <Arduino.h>'
+'\n#include <ESP8266WebServer.h>'
+'\n\nconst char* ssid = '
+"\""+ config["SSID"] +"\"" 
+';\nconst char* password = ' 
+"\""+ config["Password"] +"\""
+';\n\nESP8266WebServer server('
+config["Port"] + ');\n\n\n'
)

# Searching for every file in pages folder.
try:
    for path in pathlib.Path('pages').iterdir():
        if path.is_file():
            if path.name.endswith('.html'): # Checking if file is a HTML file.
                currentFile = open(path, "a+") # Opening file
                pageName = currentFile.name.rsplit('\\')[1].rsplit('.')[0] # Getting file name without directory and "/".
                pages.append(pageName) # Adding file name to a list for final declaration.
                result.write("void "+ pageName +"(){\nchar *" + pageName + " = ") # Converting file to a char variable
                try:
                    x = 1
                    currentFile.seek(0)
                    fileLength = sum(1 for line in currentFile)
                    currentFile.seek(0)
                    for line in currentFile: # A loop for every line
                        strippedLine = line.strip() # Clearing empty lines
                        if strippedLine != "": # Checking if the line is empty
                            editedLine = strippedLine.replace("\"","\'")
                            result.write("\"" + editedLine)
                            currentLine = result.tell()
                            result.seek(currentLine)
                            if x == fileLength: # Checking if the line is the last line
                                result.write("\";\n\nserver.send(200, \"text/html\", "+ pageName +");\n}\n\n")
                            else: # If not, it won't add server.send(...).
                                result.write("\"\n")
                            x = x+1
                        else:
                            x = x+1
                            
                finally:
                    currentFile.close()
                    print(pageName + ' page is finished.')
            else:
                print("Skipped non HTML file")
finally:
    print("Proccess ended, Web Server complete.")

# Setup of result file
result.write(
'void setup() {'
+ '\n   Serial.begin('
+ config["BaudRate"] + ');'
+ '\n   delay(10);'
+ '\n   WiFi.begin(ssid,password);'
+ '\n   while(WiFi.status() != WL_CONNECTED){'
+ '\n       Serial.print(\"Connection failed, trying again.\\n\");'
+ '\n       delay(500);'
+ '\n    }'
+ '\n   Serial.println(\"Connected Succesfully.\\n\");'
+ '\n   server.begin();'
+ '\n   Serial.print("Server is live use http://");'
+ '\n   Serial.print(WiFi.localIP());'
+ '\n   Serial.print("/");'
+ '\n\n   server.begin();\n'
)

# Declare every page
for x in pages:
    result.write("   server.on("+ "\"/" + x + "\", " + x +");\n")
result.write("}\n\n\n")

# Loop of result file
result.write("void loop() {"
+ "\n   server.handleClient();"
+ "\n   delay(1000);"
+ "\n}")