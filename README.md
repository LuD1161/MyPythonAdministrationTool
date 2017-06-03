# MyPythonMalware
Learning Python Interaction With Windows


<strong>Features :</strong>
<ul>
 	<li><strong>2 Way interaction without public IP </strong>( <strong>without global IP</strong> ) : Upto some extent using the '<strong>rtc.php' </strong>file as mediator (need to implement database for commands specific to a particular bot )<strong> </strong></li>
 	<li><strong>Can work on any free webhosting service provider</strong> <strong>, (check the <a style="text-decoration: none;" href="https://digitz.org/blog/free-hosting-2016/" target="_blank" rel="noopener noreferrer">list</a> )</strong></li>
 	<li>PHP script can automatically create folders based on the <strong>unique</strong> '<strong>botId' </strong>created and<strong> </strong>sent by the bot</li>
 	<li><strong>Persistent</strong> ( otherwise what use it is as bot )</li>
 	<li><strong>Send identification details</strong> such as :
<ul>
 	<li>MAC address</li>
 	<li>Locale ( such as en-IN or en-US )</li>
 	<li>Public IP</li>
 	<li>Platform (x86 or x86_64)</li>
 	<li>Architecture</li>
 	<li>Node Name in the network</li>
</ul>
</li>
 	<li><strong>Thread Implementation</strong> for :
<ul>
 	<li>Sending the <strong>loot</strong></li>
 	<li>Keylogger ( so that we don't miss that important key )</li>
 	<li>Receiving Command</li>
</ul>
</li>
  <li><strong>Steal passwords from Google Chrome</strong></li>
  <li><strong>Automatic spreading by copying to USB and creating shortcuts of pre-existing files </strong></li>
 	<li><strong>Sends MD5</strong> hash of the file , before uploading the original file so as to check for any bad upload</li>
 	<li><strong>Retries</strong> until the file is uploaded ( which is checked using the checksum sent earlier )</li>
 	<li><strong>Screenshots : </strong>Takes screenshots based on the URL of the webpage ( this needs to be polished )</li>
 	<li><strong>Search</strong> command on the Bot side to search for the files</li>
 	<li><strong>CMD</strong> commands can be executed by the bot</li>
</ul>
<p>The main file is the <strong>'Client.py' </strong>, which needs to be compiled and run on the user's machine , it has been <strong>tested on my PC</strong> and works out to be fine.</p>

### How spreading works
<p>
First the malware copies itself to the USB.<br>
Then it creates shortcut of each file linking it to the malware's executable.<br>
The shortcut's opening link contains the path to the malware with an extra parameter as the original file.<br>
When the malware executable is run then , first it executes the malware and then restores all the files , in turn opening the file clicked. Thus not making the user suspicious ;) . 
</p>

<header>
<h1 class="title">Disclaimer</h1>
</header>
<div class="post-content box mark-links">

Any actions and or activities related to the material contained within this website is solely your responsibility.The misuse of the information in this website can result in criminal charges brought against the persons in question. The author will not be held responsible in the event any criminal charges be brought against any individuals misusing the information on this website to break the law.

This site may contain links to materials that can be potentially damaging or dangerous.
