Use travis-ci and appveyor to extract info about various python targets

https://travis-ci.org/mdavidsaver/pipsnoop

https://ci.appveyor.com/project/mdavidsaver/pipsnoop

Useful values to distinguish hosts.
Values for Linux checked on python 2.7 and 3.x.
Other targets only 2.7.

<table>
 <tr><th>Name</th>
     <th>Linux/amd64</th>
     <th>Linux/i686</th>
     <td>OS X/amd64</td>
     <td>Windows/amd64</td>
 </tr>
 <tr><td>os.name</td>
     <td>"posix"</td>
     <td>"posix"</td>
     <td>"posix"</td>
     <td>"nt"</td>
 </tr>
 <tr><td>sys.platform()</td>
     <td>"linux2"/"linux"<a href="#sys-plat">[1]</a></td>
     <td>"linux2"/"linux"</td>
     <td>"darwin"</td>
     <td>"win32"</td>
 </tr>
 <tr><td>platform.system()</td>
     <td>"Linux"</td>
     <td>"Linux"</td>
     <td>"Darwin"</td>
     <td>"Windows"</td>
 </tr>
 <tr><td>platform.machine()</td>
     <td>"x86_64"</td>
     <td>"i686"</td>
     <td>"x86_64"</td>
     <td>"AMD64"</td>
 </tr>
 <tr><td></td>
     <td></td>
     <td></td>
     <td></td>
     <td></td>
 </tr>
</table>

<p><a id="sys-plat">[1]</a>Value is "linux2" in python 2.x and "linux" in 3.x</p>
